SELECT 
    SystemInfo.WORKSTATIONNAME AS "Machine Name", 
    SystemInfo.LOGGEDUSER AS "Last Logged In User", 
    DATEADD(SECOND, ah.audittime / 1000, '1970-01-01') AS "Last Audit Time", -- Convert to human-readable time
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
WHERE 
    SystemInfo.WORKSTATIONID IN (
        SELECT si.workstationid 
        FROM softwareinfo si
        LEFT JOIN softwarelist sl ON si.softwareid = sl.softwareid
        WHERE LOWER(sl.softwarename) = 'cylance protect with optics'
    )
ORDER BY 
    SystemInfo.WORKSTATIONNAME;



