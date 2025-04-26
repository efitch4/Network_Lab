SELECT 
    SystemInfo.WORKSTATIONNAME AS "Machine Name", 
    SystemInfo.LOGGEDUSER AS "Last Logged In User", 
    FORMAT(DATEADD(SECOND, ah.audittime / 1000, '1970-01-01'), 'MM/dd/yyyy hh:mm:ss tt') AS "Last Audit Time", -- Convert to 12-hour format
    ah.comments AS "Comments", -- Include comments column from audithistory
    state.DISPLAYSTATE AS "Asset State", 
    SystemInfo.MANUFACTURER AS "Manufacturer", 
    SystemInfo.MODEL AS "Model", 
    SystemInfo.SERVICETAG AS "Service Tag",
    osInfo.OSNAME AS "Operating System",
    memInfo.TOTALMEMORY AS "Total Memory"
FROM 
    SystemInfo
LEFT JOIN lastauditinfo la 
    ON SystemInfo.WORKSTATIONID = la.workstationid
LEFT JOIN audithistory ah 
    ON la.last_auditid = ah.auditid
LEFT JOIN Resources resource 
    ON SystemInfo.WORKSTATIONID = resource.RESOURCEID
LEFT JOIN ResourceState state 
    ON resource.RESOURCESTATEID = state.RESOURCESTATEID
LEFT JOIN MemoryInfo memInfo 
    ON SystemInfo.WORKSTATIONID = memInfo.WORKSTATIONID
LEFT JOIN OsInfo osInfo 
    ON SystemInfo.WORKSTATIONID = osInfo.WORKSTATIONID
ORDER BY 
    SystemInfo.WORKSTATIONNAME;

