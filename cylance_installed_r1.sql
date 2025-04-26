SELECT 
    SystemInfo.WORKSTATIONNAME AS "Workstation", 
    MAX(SystemInfo.LOGGEDUSER) AS "Last Logged In User",
    FORMAT(DATEADD(SECOND, ah.audittime / 1000, '1970-01-01'), 'MM/dd/yyyy hh:mm:ss tt') AS "Last Audit Time",  -- Last scan time
    'Installed' AS "Installed Cylance Status",  -- Indicating Cylance PROTECT with OPTICS is installed
    state.DISPLAYSTATE AS "Asset State",
    CASE 
        WHEN LOWER(sl.softwarename) = 'Cylance PROTECT with OPTICS' THEN 'Installed'
        ELSE 'Not Installed'
    END AS "Cylance Install Status"
FROM 
    SystemInfo
LEFT JOIN 
    softwareinfo si ON SystemInfo.WORKSTATIONID = si.workstationid
LEFT JOIN 
    softwarelist sl ON si.softwareid = sl.softwareid
LEFT JOIN 
    lastauditinfo la ON SystemInfo.WORKSTATIONID = la.workstationid
LEFT JOIN 
    audithistory ah ON la.last_auditid = ah.auditid
WHERE 
    SystemInfo.WORKSTATIONID IN (
        SELECT si.workstationid 
        FROM softwareinfo si
        LEFT JOIN softwarelist sl ON si.softwareid = sl.softwareid
        WHERE LOWER(sl.softwarename) = 'Cylance PROTECT with OPTICS'
    )
GROUP BY 
    SystemInfo.WORKSTATIONNAME

    