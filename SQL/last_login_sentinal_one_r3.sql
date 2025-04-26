SELECT 
    SystemInfo.WORKSTATIONNAME AS "Machine Name", 
    SystemInfo.LOGGEDUSER AS "Last Logged In User", 
    DATEADD(SECOND, ah.audittime / 1000, '1970-01-01') AS "Last Audit Time", -- Convert to human-readable time
    state.DISPLAYSTATE AS "Asset State",
    'Not Installed' AS "SentinelOne Status"
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
WHERE 
    SystemInfo.WORKSTATIONID NOT IN (
        SELECT si.workstationid 
        FROM softwareinfo si
        LEFT JOIN softwarelist sl ON si.softwareid = sl.softwareid
        WHERE LOWER(sl.softwarename) = 'sentinel agent'
    )
ORDER BY 
    SystemInfo.WORKSTATIONNAME;


--    SystemInfo.WORKSTATIONID NOT IN ( This will check if not installed)