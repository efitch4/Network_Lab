SELECT DISTINCT
    si.WORKSTATIONNAME AS "Machine Name", 
    MAX(si.LOGGEDUSER) AS "Last Logged In User", 
    FORMAT(DATEADD(SECOND, ah.audittime / 1000, '1970-01-01'), 'MM/dd/yyyy hh:mm:ss tt') AS "Last Contact Time", -- Convert to 12-hour format
    state.DISPLAYSTATE AS "Asset State",
    'Installed' AS "Cylance Install Status"
FROM 
    SystemInfo si
LEFT JOIN lastauditinfo la 
    ON si.WORKSTATIONID = la.workstationid
LEFT JOIN audithistory ah 
    ON la.last_auditid = ah.auditid
LEFT JOIN Resources resource 
    ON si.WORKSTATIONID = resource.RESOURCEID
LEFT JOIN ResourceState state 
    ON resource.RESOURCESTATEID = state.RESOURCESTATEID
LEFT JOIN softwareinfo si_sw 
    ON si.WORKSTATIONID = si_sw.workstationid
LEFT JOIN softwarelist sl 
    ON si_sw.softwareid = sl.softwareid
WHERE 
    si.WORKSTATIONID  IN (
        SELECT si2.workstationid 
        FROM softwareinfo si2
        LEFT JOIN softwarelist sl2 ON si2.softwareid = sl2.softwareid
        WHERE LOWER(sl2.softwarename) = 'Cylance PROTECT with OPTICS'
    )
GROUP BY 
    si.WORKSTATIONNAME, 
    state.DISPLAYSTATE, 
    ah.audittime, 
    sl.softwarename
ORDER BY 
    si.WORKSTATIONNAME;

    