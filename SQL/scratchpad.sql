SELECT DISTINCT 
    si.WORKSTATIONNAME AS "Machine Name",
    MAX(aaaUser.FIRST_NAME) AS "Assigned User",
    MAX(si.LOGGEDUSER) AS "Last Logged In User",
    FORMAT(DATEADD(SECOND, ah.audittime / 1000, '1970-01-01'), 'MM/dd/yyyy hh:mm:ss tt') AS "Last Audit Time",
    state.DISPLAYSTATE AS "Asset State",
    MAX(resource.ACQUISITIONDATE) AS "Acquisition Date",
    MAX(memInfo.TOTALMEMORY / 1024 / 1024) AS "Total Memory (MB)",
    MAX(osInfo.OSNAME) AS "Operating System",
    CASE
        WHEN LOWER(sl.softwarename) = 'sentinel agent' THEN 'Installed'
        ELSE 'Not Installed'
    END AS "SentinelOne Status"
    CASE
        WHEN LOWER(sl.softwarename) = 'forcepoint one endpoint' THEN 'Installed'
        ELSE 'Not Installed'
    END AS "Forcepoint Status"
FROM
    Systeminfo si 
LEFT JOIN lastauditinfo la
    ON si.WORKSTATIONID = la.workstationid