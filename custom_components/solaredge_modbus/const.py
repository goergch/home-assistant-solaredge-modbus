DOMAIN = "solaredge_modbus"
DEFAULT_NAME = "solaredge"
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_PORT = 1502
CONF_SOLAREDGE_HUB = "solaredge_hub"
ATTR_STATUS_DESCRIPTION = "status_description"
ATTR_MANUFACTURER = "Solaredge"

SENSOR_TYPES = {
    "AC_Current": ["AC Current", "accurrent", "A", "mdi:current-ac"],
    "AC_CurrentA": ["AC Current A", "accurrenta", "A", "mdi:current-ac"],
    "AC_CurrentB": ["AC Current B", "accurrentb", "A", "mdi:current-ac"],
    "AC_CurrentC": ["AC Current C", "accurrentc", "A", "mdi:current-ac"],
    "AC_VoltageAB": ["AC Voltage AB", "acvoltageab", "V", None],
    "AC_VoltageBC": ["AC Voltage BC", "acvoltagebc", "V", None],
    "AC_VoltageCA": ["AC Voltage CA", "acvoltageca", "V", None],
    "AC_VoltageAN": ["AC Voltage AN", "acvoltagean", "V", None],
    "AC_VoltageBN": ["AC Voltage BN", "acvoltagebn", "V", None],
    "AC_VoltageCN": ["AC Voltage CN", "acvoltagecn", "V", None],
    "AC_Power": ["AC Power", "acpower", "W", "mdi:solar-power"],
    "AC_Frequency": ["AC Frequency", "acfreq", "Hz", None],
    "AC_VA": ["AC VA", "acva", "VA", None],
    "AC_VAR": ["AC VAR", "acvar", "VAR", None],
    "AC_PF": ["AC PF", "acpf", "%", None],
    "AC_Energy_KWH": ["AC Energy KWH", "acenergy", "kWh", "mdi:solar-power"],
    "DC_Current": ["DC Current", "dccurrent", "A", "mdi:current-dc"],
    "DC_Voltage": ["DC Voltage", "dcvoltage", "V", None],
    "DC_Power": ["DC Power", "dcpower", "W", "mdi:solar-power"],
    "Temp_Sink": ["Temp Sink", "tempsink", "°C", None],
    "Status": ["Status", "status", None, None],
    "Status_Vendor": ["Status Vendor", "statusvendor", None, None],

    
    "M1_AC_Current":  ["Meter 1 AC Current",   "m1accurrent",  "A", "mdi:current-ac"],
    "M1_AC_CurrentA": ["Meter 1 AC Current A", "m1accurrenta", "A", "mdi:current-ac"],
    "M1_AC_CurrentB": ["Meter 1 AC Current B", "m1accurrentb", "A", "mdi:current-ac"],
    "M1_AC_CurrentC": ["Meter 1 AC Current C", "m1accurrentc", "A", "mdi:current-ac"],
    "M1_AC_VoltageLL": ["Meter 1 AC Voltage LL", "m1acvoltagell", "V", None],
    "M1_AC_VoltageAB": ["Meter 1 AC Voltage AB", "m1acvoltageab", "V", None],
    "M1_AC_VoltageBC": ["Meter 1 AC Voltage BC", "m1acvoltagebc", "V", None],
    "M1_AC_VoltageCA": ["Meter 1 AC Voltage CA", "m1acvoltageca", "V", None],
    "M1_AC_VoltageLN": ["Meter 1 AC Voltage LN", "m1acvoltageln", "V", None],
    "M1_AC_VoltageAN": ["Meter 1 AC Voltage AN", "m1acvoltagean", "V", None],
    "M1_AC_VoltageBN": ["Meter 1 AC Voltage BN", "m1acvoltagebn", "V", None],
    "M1_AC_VoltageCN": ["Meter 1 AC Voltage CN", "m1acvoltagecn", "V", None],
    "M1_AC_Frequency": ["Meter 1 AC Frequency", "m1acfreq", "Hz", None],
    "M1_AC_Power":  ["Meter 1 AC Power",   "m1acpower",  "W", "mdi:flash"],
    "M1_AC_PowerA": ["Meter 1 AC Power A", "m1acpowera", "W", "mdi:flash"],
    "M1_AC_PowerB": ["Meter 1 AC Power B", "m1acpowerb", "W", "mdi:flash"],
    "M1_AC_PowerC": ["Meter 1 AC Power C", "m1acpowerc", "W", "mdi:flash"],
    "M1_AC_VA":  ["Meter 1 AC Apparent Power",   "m1acva",  "VA", "mdi:flash"],
    "M1_AC_VAA": ["Meter 1 AC Apparent Power A", "m1acvaa", "VA", "mdi:flash"],
    "M1_AC_VAB": ["Meter 1 AC Apparent Power B", "m1acvab", "VA", "mdi:flash"],
    "M1_AC_VAC": ["Meter 1 AC Apparent Power C", "m1acvac", "VA", "mdi:flash"],
    "M1_AC_VAR":  ["Meter 1 AC Reactive Power",   "m1acvar",  "VAR", "mdi:flash"],
    "M1_AC_VARA": ["Meter 1 AC Reactive Power A", "m1acvara", "VAR", "mdi:flash"],
    "M1_AC_VARB": ["Meter 1 AC Reactive Power B", "m1acvarb", "VAR", "mdi:flash"],
    "M1_AC_VARC": ["Meter 1 AC Reactive Power C", "m1acvarc", "VAR", "mdi:flash"],
    "M1_AC_PF":  ["Meter 1 AC Power Factor",   "m1acpf",  "%", "mdi:flash"],
    "M1_AC_PFA": ["Meter 1 AC Power Factor A", "m1acpfa", "%", "mdi:flash"],
    "M1_AC_PFB": ["Meter 1 AC Power Factor B", "m1acpfb", "%", "mdi:flash"],
    "M1_AC_PFC": ["Meter 1 AC Power Factor C", "m1acpfc", "%", "mdi:flash"],
    "M1_AC_PF":  ["Meter 1 AC Power Factor",   "m1acpf",  "%", "mdi:flash"],
    "M1_AC_PFA": ["Meter 1 AC Power Factor A", "m1acpfa", "%", "mdi:flash"],
    "M1_AC_PFB": ["Meter 1 AC Power Factor B", "m1acpfb", "%", "mdi:flash"],
    "M1_AC_PFC": ["Meter 1 AC Power Factor C", "m1acpfc", "%", "mdi:flash"],
    "M1_AC_EXPORTED":  ["Meter 1 Exported Real Energy",   "m1acexported",  "kWh", "mdi:arrow-expand-all"],
    "M1_AC_EXPORTEDA": ["Meter 1 Exported Real Energy A", "m1acexporteda", "kWh", "mdi:arrow-expand-all"],
    "M1_AC_EXPORTEDB": ["Meter 1 Exported Real Energy B", "m1acexportedb", "kWh", "mdi:arrow-expand-all"],
    "M1_AC_EXPORTEDC": ["Meter 1 Exported Real Energy C", "m1acexportedc", "kWh", "mdi:arrow-expand-all"],
    "M1_AC_IMPORTED":  ["Meter 1 Imported Real Energy",   "m1acimported",  "kWh", "mdi:arrow-collapse-all"],
    "M1_AC_IMPORTEDA": ["Meter 1 Imported Real Energy A", "m1acimporteda", "kWh", "mdi:arrow-collapse-all"],
    "M1_AC_IMPORTEDB": ["Meter 1 Imported Real Energy B", "m1acimportedb", "kWh", "mdi:arrow-collapse-all"],
    "M1_AC_IMPORTEDC": ["Meter 1 Imported Real Energy C", "m1acimportedc", "kWh", "mdi:arrow-collapse-all"]
}

DEVICE_STATUSSES = {
    1: "Off",
    2: "Sleeping (auto-shutdown) – Night mode",
    3: "Grid Monitoring/wake-up",
    4: "Inverter is ON and producing power",
    5: "Production (curtailed)",
    6: "Shutting down",
    7: "Fault",
    8: "Maintenance/setup"
}
