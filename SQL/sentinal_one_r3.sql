SELECT 
    SystemInfo.WORKSTATIONNAME AS "Workstation", 
    state.DISPLAYSTATE AS "Asset State",
    MAX(SystemInfo.LOGGEDUSER) AS "Last Logged In User",
    LONGTODATE(MAX(ah.audittime)) AS "Last Scanned On",  -- Last scan time
    'Not Installed' AS "SentinelOne Status",             -- Indicating Sentinel Agent is not installed
    'Not Installed' AS "FORCEPOINT ONE ENDPOINT Status",  -- Indicating Force Point is not installed
    'Installed' AS "Installed Cylance Status"  -- Indicating Cylance PROTECT with OPTICS is installed
FROM 
    SystemInfo
LEFT JOIN 
    softwareinfo si ON SystemInfo.WORKSTATIONID = si.workstationid
LEFT JOIN 
    softwarelist sl ON si.softwareid = sl.softwareid
LEFT JOIN 
    Resources resource ON SystemInfo.WORKSTATIONID = resource.RESOURCEID
LEFT JOIN 
    ResourceState state ON resource.RESOURCESTATEID = state.RESOURCESTATEID
LEFT JOIN 
    lastauditinfo la ON SystemInfo.WORKSTATIONID = la.workstationid
LEFT JOIN 
    audithistory ah ON la.last_auditid = ah.auditid
WHERE 
    SystemInfo.WORKSTATIONID NOT IN (
        SELECT si.workstationid 
        FROM softwareinfo si
        LEFT JOIN softwarelist sl ON si.softwareid = sl.softwareid
        WHERE LOWER(sl.softwarename) = 'sentinel agent'
    )
    AND SystemInfo.WORKSTATIONID NOT IN (
        SELECT si.workstationid 
        FROM softwareinfo si
        LEFT JOIN softwarelist sl ON si.softwareid = sl.softwareid
        WHERE LOWER(sl.softwarename) = 'forcepoint one endpoint'
    )
    AND SystemInfo.WORKSTATIONID IN (
        SELECT si.workstationid 
        FROM softwareinfo si
        LEFT JOIN softwarelist sl ON si.softwareid = sl.softwareid
        WHERE LOWER(sl.softwarename) = 'Cylance PROTECT with OPTICS'
    )
GROUP BY 
    SystemInfo.WORKSTATIONNAME, state.DISPLAYSTATE, SystemInfo.LOGGEDUSER;



