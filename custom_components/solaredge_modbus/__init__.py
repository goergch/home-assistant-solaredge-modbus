"""The SolarEdge Modbus Integration."""
import asyncio
import logging
import threading
from datetime import timedelta
from typing import Optional

import voluptuous as vol
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

SOLAREDGE_MODBUS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_int
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({cv.slug: SOLAREDGE_MODBUS_SCHEMA})}, extra=vol.ALLOW_EXTRA
)

PLATFORMS = ["sensor"]


async def async_setup(hass, config):
    """Set up the Solaredge modbus component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up a solaredge mobus."""
    host = entry.data[CONF_HOST]
    name = entry.data[CONF_NAME]
    port = entry.data[CONF_PORT]
    scan_interval = entry.data[CONF_SCAN_INTERVAL]

    _LOGGER.debug("Setup %s.%s", DOMAIN, name)

    hub = SolaredgeModbusHub(hass, name, host, port, scan_interval)
    """Register the hub."""
    hass.data[DOMAIN][name] = {
        "hub": hub
    }

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True


async def async_unload_entry(hass, entry):
    """Unload Solaredge mobus entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if not unload_ok:
        return False

    hass.data[DOMAIN].pop(entry.data["name"])
    return True


class SolaredgeModbusHub:
    """Thread safe wrapper class for pymodbus."""

    def __init__(self, hass, name, host, port, scan_interval):
        """Initialize the Modbus hub."""
        self._hass = hass
        self._client = ModbusTcpClient(host=host, port=port)
        self._lock = threading.Lock()
        self._name = name
        self._scan_interval = timedelta(seconds=scan_interval)
        self._unsub_interval_method = None
        self._sensors = []
        self.data = {}

    @callback
    def async_add_solaredge_sensor(self, update_callback):
        """Listen for data updates."""
        # This is the first sensor, set up interval.
        if not self._sensors:
            self.connect()
            self._unsub_interval_method = async_track_time_interval(
                self._hass, self.async_refresh_modbus_data, self._scan_interval
            )

        self._sensors.append(update_callback)

    @callback
    def async_remove_solaredge_sensor(self, update_callback):
        """Remove data update."""
        self._sensors.remove(update_callback)

        if not self._sensors:
            """stop the interval timer upon removal of last sensor"""
            self._unsub_interval_method()
            self._unsub_interval_method = None
            self.close()

    async def async_refresh_modbus_data(self, _now: Optional[int] = None) -> None:
        """Time to update."""
        if not self._sensors:
            return

        update_result = self.read_modbus_data()

        if update_result:
            for update_callback in self._sensors:
                update_callback()

    @property
    def name(self):
        """Return the name of this hub."""
        return self._name

    def close(self):
        """Disconnect client."""
        with self._lock:
            self._client.close()

    def connect(self):
        """Connect client."""
        with self._lock:
            self._client.connect()

    def read_holding_registers(self, unit, address, count):
        """Read holding registers."""
        with self._lock:
            kwargs = {"unit": unit} if unit else {}
            return self._client.read_holding_registers(address, count, **kwargs)

    def calculate_value(self, value, sf):
        return value * 10 ** sf

    def read_modbus_data_stub(self):
        self.data["accurrent"] = 1
        self.data["accurrenta"] = 1
        self.data["accurrentb"] = 1
        self.data["accurrentc"] = 1
        self.data["acvoltageab"] = 1
        self.data["acvoltagebc"] = 1
        self.data["acvoltageca"] = 1
        self.data["acvoltagean"] = 1
        self.data["acvoltagebn"] = 1
        self.data["acvoltagecn"] = 1
        self.data["acpower"] = 1
        self.data["acfreq"] = 1
        self.data["acva"] = 1
        self.data["acvar"] = 1
        self.data["acpf"] = 1
        self.data["acenergy"] = 1
        self.data["dccurrent"] = 1
        self.data["dcvoltage"] = 1
        self.data["dcpower"] = 1
        self.data["tempsink"] = 1
        self.data["status"] = 1
        self.data["statusvendor"] = 1

        #meter1
        self.data["m1acurrent"] = 1
        self.data["m1acurrenta"] = 1
        self.data["m1acurrentb"] = 1
        self.data["m1acurrentc"] = 1
        self.data["m1acvoltageln"] = 1
        self.data["m1acvoltagean"] = 1
        self.data["m1acvoltagebn"] = 1
        self.data["m1acvoltagecn"] = 1
        self.data["m1acvoltagell"] = 1
        self.data["m1acvoltageab"] = 1
        self.data["m1acvoltagebc"] = 1
        self.data["m1acvoltageca"] = 1
        self.data["m1acfreq"] = 1
        self.data["m1acpower"] = 1
        self.data["m1acpowera"] = 1
        self.data["m1acpowerb"] = 1
        self.data["m1acpowerc"] = 1
        self.data["m1acva"] = 1
        self.data["m1acvaa"] = 1
        self.data["m1acvab"] = 1
        self.data["m1acvac"] = 1
        self.data["m1acvar"] = 1
        self.data["m1acvara"] = 1
        self.data["m1acvarb"] = 1
        self.data["m1acvarc"] = 1
        self.data["m1acpf"] = 1
        self.data["m1acpfa"] = 1
        self.data["m1acpfb"] = 1
        self.data["m1acpfc"] = 1
        self.data["m1exported"] = 1
        self.data["m1exporteda"] = 1
        self.data["m1exportedb"] = 1
        self.data["m1exportedc"] = 1
        self.data["m1imported"] = 1
        self.data["m1importeda"] = 1
        self.data["m1importedb"] = 1
        self.data["m1importedc"] = 1
        return True

    def read_modbus_data(self):
        rvInverter = False
        rvMeter1 = False
        inverter_data = self.read_holding_registers(unit=1, address=40071, count=38)
        meter1_data = self.read_holding_registers(unit=1, address=40189, count=53)
        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(inverter_data.registers, byteorder=Endian.Big)
            accurrent = decoder.decode_16bit_uint()
            accurrenta = decoder.decode_16bit_uint()
            accurrentb = decoder.decode_16bit_uint()
            accurrentc = decoder.decode_16bit_uint()
            accurrentsf = decoder.decode_16bit_int()

            accurrent = self.calculate_value(accurrent, accurrentsf)
            accurrenta = self.calculate_value(accurrenta, accurrentsf)
            accurrentb = self.calculate_value(accurrentb, accurrentsf)
            accurrentc = self.calculate_value(accurrentc, accurrentsf)

            self.data["accurrent"] = round(accurrent, abs(accurrentsf))
            self.data["accurrenta"] = round(accurrenta, abs(accurrentsf))
            self.data["accurrentb"] = round(accurrentb, abs(accurrentsf))
            self.data["accurrentc"] = round(accurrentc, abs(accurrentsf))

            acvoltageab = decoder.decode_16bit_uint()
            acvoltagebc = decoder.decode_16bit_uint()
            acvoltageca = decoder.decode_16bit_uint()
            acvoltagean = decoder.decode_16bit_uint()
            acvoltagebn = decoder.decode_16bit_uint()
            acvoltagecn = decoder.decode_16bit_uint()
            acvoltagesf = decoder.decode_16bit_int()

            acvoltageab = self.calculate_value(acvoltageab, acvoltagesf)
            acvoltagebc = self.calculate_value(acvoltagebc, acvoltagesf)
            acvoltageca = self.calculate_value(acvoltageca, acvoltagesf)
            acvoltagean = self.calculate_value(acvoltagean, acvoltagesf)
            acvoltagebn = self.calculate_value(acvoltagebn, acvoltagesf)
            acvoltagecn = self.calculate_value(acvoltagecn, acvoltagesf)

            self.data["acvoltageab"] = round(acvoltageab, abs(acvoltagesf))
            self.data["acvoltagebc"] = round(acvoltagebc, abs(acvoltagesf))
            self.data["acvoltageca"] = round(acvoltageca, abs(acvoltagesf))
            self.data["acvoltagean"] = round(acvoltagean, abs(acvoltagesf))
            self.data["acvoltagebn"] = round(acvoltagebn, abs(acvoltagesf))
            self.data["acvoltagecn"] = round(acvoltagecn, abs(acvoltagesf))

            acpower = decoder.decode_16bit_int()
            acpowersf = decoder.decode_16bit_int()
            acpower = self.calculate_value(acpower, acpowersf)

            self.data["acpower"] = round(acpower, abs(acpowersf))

            acfreq = decoder.decode_16bit_uint()
            acfreqsf = decoder.decode_16bit_int()
            acfreq = self.calculate_value(acfreq, acfreqsf)

            self.data["acfreq"] = round(acfreq, abs(acfreqsf))

            acva = decoder.decode_16bit_int()
            acvasf = decoder.decode_16bit_int()
            acva = self.calculate_value(acva, acvasf)

            self.data["acva"] = round(acva, abs(acvasf))

            acvar = decoder.decode_16bit_int()
            acvarsf = decoder.decode_16bit_int()
            acvar = self.calculate_value(acvar, acvarsf)

            self.data["acvar"] = round(acvar, abs(acvarsf))

            acpf = decoder.decode_16bit_int()
            acpfsf = decoder.decode_16bit_int()
            acpf = self.calculate_value(acpf, acpfsf)

            self.data["acpf"] = round(acpf, abs(acpfsf))

            acenergy = decoder.decode_32bit_uint()
            acenergysf = decoder.decode_16bit_uint()
            acenergy = self.calculate_value(acenergy, acenergysf)

            self.data["acenergy"] = round(acenergy * 0.001, 3)

            dccurrent = decoder.decode_16bit_uint()
            dccurrentsf = decoder.decode_16bit_int()
            dccurrent = self.calculate_value(dccurrent, dccurrentsf)

            self.data["dccurrent"] = round(dccurrent, abs(dccurrentsf))

            dcvoltage = decoder.decode_16bit_uint()
            dcvoltagesf = decoder.decode_16bit_int()
            dcvoltage = self.calculate_value(dcvoltage, dcvoltagesf)

            self.data["dcvoltage"] = round(dcvoltage, abs(dcvoltagesf))

            dcpower = decoder.decode_16bit_int()
            dcpowersf = decoder.decode_16bit_int()
            dcpower = self.calculate_value(dcpower, dcpowersf)

            self.data["dcpower"] = round(dcpower, abs(dcpowersf))

            # skip register
            decoder.skip_bytes(2)

            tempsink = decoder.decode_16bit_int()

            # skip 2 registers
            decoder.skip_bytes(4)

            tempsf = decoder.decode_16bit_int()
            tempsink = self.calculate_value(tempsink, tempsf)

            self.data["tempsink"] = round(tempsink, abs(tempsf))

            status = decoder.decode_16bit_int()
            self.data["status"] = status
            statusvendor = decoder.decode_16bit_int()
            self.data["statusvendor"] = statusvendor

            rvInverter = True
        if not meter1_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(meter1_data.registers, byteorder=Endian.Big)
            m1accurrent =   decoder.decode_16bit_int()
            m1accurrenta =  decoder.decode_16bit_int()
            m1accurrentb =  decoder.decode_16bit_int()
            m1accurrentc =  decoder.decode_16bit_int()
            m1accurrentsf = decoder.decode_16bit_int()
            m1accurrent = self.calculate_value(m1accurrent, m1accurrentsf)
            m1accurrenta = self.calculate_value(m1accurrenta, m1accurrentsf)
            m1accurrentb = self.calculate_value(m1accurrentb, m1accurrentsf)
            m1accurrentc = self.calculate_value(m1accurrentc, m1accurrentsf)
            
            self.data["m1acurrent"] = round(m1accurrent, abs(m1accurrentsf))
            self.data["m1acurrenta"] = round(m1accurrenta, abs(m1accurrentsf))
            self.data["m1acurrentb"] = round(m1accurrentb, abs(m1accurrentsf))
            self.data["m1acurrentc"] = round(m1accurrentc, abs(m1accurrentsf))

            

            m1acvoltageln = decoder.decode_16bit_int()
            m1acvoltagean = decoder.decode_16bit_int()
            m1acvoltagebn = decoder.decode_16bit_int()
            m1acvoltagecn = decoder.decode_16bit_int()
            m1acvoltagell = decoder.decode_16bit_int()
            m1acvoltageab = decoder.decode_16bit_int()
            m1acvoltagebc = decoder.decode_16bit_int()
            m1acvoltageca = decoder.decode_16bit_int()
            m1acvoltagesf = decoder.decode_16bit_int()
                
            
            m1acvoltagell = self.calculate_value(m1acvoltageab, m1acvoltagesf)
            m1acvoltageab = self.calculate_value(m1acvoltageab, m1acvoltagesf)
            m1acvoltagebc = self.calculate_value(m1acvoltagebc, m1acvoltagesf)
            m1acvoltageca = self.calculate_value(m1acvoltageca, m1acvoltagesf)
            m1acvoltageln = self.calculate_value(m1acvoltageab, m1acvoltagesf)
            m1acvoltagean = self.calculate_value(m1acvoltagean, m1acvoltagesf)
            m1acvoltagebn = self.calculate_value(m1acvoltagebn, m1acvoltagesf)
            m1acvoltagecn = self.calculate_value(m1acvoltagecn, m1acvoltagesf)


            self.data["m1acvoltageln"] = round(m1acvoltageln, abs(m1acvoltagesf))
            self.data["m1acvoltagean"] = round(m1acvoltagean, abs(m1acvoltagesf))
            self.data["m1acvoltagebn"] = round(m1acvoltagebn, abs(m1acvoltagesf))
            self.data["m1acvoltagecn"] = round(m1acvoltagecn, abs(m1acvoltagesf))
            self.data["m1acvoltagell"] = round(m1acvoltagell, abs(m1acvoltagesf))
            self.data["m1acvoltageab"] = round(m1acvoltageab, abs(m1acvoltagesf))
            self.data["m1acvoltagebc"] = round(m1acvoltagebc, abs(m1acvoltagesf))
            self.data["m1acvoltageca"] = round(m1acvoltageca, abs(m1acvoltagesf))

            
            m1acfreq = decoder.decode_16bit_int()
            m1acfreqsf = decoder.decode_16bit_int()
            m1acfreq = self.calculate_value(m1acfreq, m1acfreqsf)

            self.data["m1acfreq"] = round(m1acfreq, abs(m1acfreqsf))

            
            m1acpower = decoder.decode_16bit_int()
            m1acpowera = decoder.decode_16bit_int()
            m1acpowerb = decoder.decode_16bit_int()
            m1acpowerc = decoder.decode_16bit_int()
            m1acpowersf = decoder.decode_16bit_int()

            m1acpower = self.calculate_value(m1acpower, m1acpowersf)
            m1acpowera = self.calculate_value(m1acpowera, m1acpowersf)
            m1acpowerb = self.calculate_value(m1acpowerb, m1acpowersf)
            m1acpowerc = self.calculate_value(m1acpowerc, m1acpowersf)
                
            self.data["m1acpower"] = round(m1acpower, abs(m1acpowersf))
            self.data["m1acpowera"] = round(m1acpowera, abs(m1acpowersf))
            self.data["m1acpowerb"] = round(m1acpowerb, abs(m1acpowersf))
            self.data["m1acpowerc"] = round(m1acpowerc, abs(m1acpowersf))

            
            m1acva   = decoder.decode_16bit_int()
            m1acvaa  = decoder.decode_16bit_int()
            m1acvab  = decoder.decode_16bit_int()
            m1acvac  = decoder.decode_16bit_int()
            m1acvasf = decoder.decode_16bit_int()
            
            m1acva  = self.calculate_value(m1acva,  m1acvasf)
            m1acvaa = self.calculate_value(m1acvaa, m1acvasf)
            m1acvab = self.calculate_value(m1acvab, m1acvasf)
            m1acvac = self.calculate_value(m1acvac, m1acvasf)

            self.data["m1acva"]  = round(m1acva,  abs(m1acvasf))
            self.data["m1acvaa"] = round(m1acvaa, abs(m1acvasf))
            self.data["m1acvab"] = round(m1acvab, abs(m1acvasf))
            self.data["m1acvac"] = round(m1acvac, abs(m1acvasf))
            
            m1acvar   = decoder.decode_16bit_int()
            m1acvara  = decoder.decode_16bit_int()
            m1acvarb  = decoder.decode_16bit_int()
            m1acvarc  = decoder.decode_16bit_int()
            m1acvarsf = decoder.decode_16bit_int()
            
            m1acvar  = self.calculate_value(m1acvar,  m1acvarsf)
            m1acvara = self.calculate_value(m1acvara, m1acvarsf)
            m1acvarb = self.calculate_value(m1acvarb, m1acvarsf)
            m1acvarc = self.calculate_value(m1acvarc, m1acvarsf)

            self.data["m1acvar"]  = round(m1acvar,  abs(m1acvarsf))
            self.data["m1acvara"] = round(m1acvara, abs(m1acvarsf))
            self.data["m1acvarb"] = round(m1acvarb, abs(m1acvarsf))
            self.data["m1acvarc"] = round(m1acvarc, abs(m1acvarsf))
            
            m1acpf   = decoder.decode_16bit_int()
            m1acpfa  = decoder.decode_16bit_int()
            m1acpfb  = decoder.decode_16bit_int()
            m1acpfc  = decoder.decode_16bit_int()
            m1acpfsf = decoder.decode_16bit_int()
            
            m1acpf  = self.calculate_value(m1acpf,  m1acpfsf)
            m1acpfa = self.calculate_value(m1acpfa, m1acpfsf)
            m1acpfb = self.calculate_value(m1acpfb, m1acpfsf)
            m1acpfc = self.calculate_value(m1acpfc, m1acpfsf)

            self.data["m1acpf"]  = round(m1acpf,  abs(m1acpfsf))
            self.data["m1acpfa"] = round(m1acpfa, abs(m1acpfsf))
            self.data["m1acpfb"] = round(m1acpfb, abs(m1acpfsf))
            self.data["m1acpfc"] = round(m1acpfc, abs(m1acpfsf))

            
            m1acexported   = decoder.decode_32bit_uint()
            m1acexporteda  = decoder.decode_32bit_uint()
            m1acexportedb  = decoder.decode_32bit_uint()
            m1acexportedc  = decoder.decode_32bit_uint()
            m1acimported   = decoder.decode_32bit_uint()
            m1acimporteda  = decoder.decode_32bit_uint()
            m1acimportedb  = decoder.decode_32bit_uint()
            m1acimportedc  = decoder.decode_32bit_uint()
            m1acenergysf = decoder.decode_16bit_int()
            
            m1acexported  = self.calculate_value(m1acexported,  m1acenergysf)
            m1acexporteda = self.calculate_value(m1acexporteda, m1acenergysf)
            m1acexportedb = self.calculate_value(m1acexportedb, m1acenergysf)
            m1acexportedc = self.calculate_value(m1acexportedc, m1acenergysf)
            m1acimported  = self.calculate_value(m1acimported,  m1acenergysf)
            m1acimporteda = self.calculate_value(m1acimporteda, m1acenergysf)
            m1acimportedb = self.calculate_value(m1acimportedb, m1acenergysf)
            m1acimportedc = self.calculate_value(m1acimportedc, m1acenergysf)

            self.data["m1acexported"]  = round(m1acexported,  abs(m1acenergysf))
            self.data["m1acexporteda"] = round(m1acexporteda, abs(m1acenergysf))
            self.data["m1acexportedb"] = round(m1acexportedb, abs(m1acenergysf))
            self.data["m1acexportedc"] = round(m1acexportedc, abs(m1acenergysf))
            self.data["m1acimported"]  = round(m1acimported,  abs(m1acenergysf))
            self.data["m1acimporteda"] = round(m1acimporteda, abs(m1acenergysf))
            self.data["m1acimportedb"] = round(m1acimportedb, abs(m1acenergysf))
            self.data["m1acimportedc"] = round(m1acimportedc, abs(m1acenergysf))
            rvMeter1 = True
        return rvInverter and rvMeter1