SELECT 
    SystemInfo.WORKSTATIONNAME AS "Machine Name", 
    SystemInfo.LOGGEDUSER AS "Last Logged In User", 
    FORMAT(DATEADD(SECOND, ah.audittime / 1000, '1970-01-01'), 'MM/dd/yyyy hh:mm:ss tt') AS "Last Audit Time", 
    ah.comments AS "Comments", 
    state.DISPLAYSTATE AS "Asset State", 
    SystemInfo.MANUFACTURER AS "Manufacturer", 
    SystemInfo.MODEL AS "Model", 
    SystemInfo.SERVICETAG AS "Service Tag",
    NetworkInfo.IPADDRESS AS "IP Address"  -- Add the IP Address from NetworkInfo

FROM SystemInfo
LEFT JOIN lastauditinfo la 
    ON SystemInfo.WORKSTATIONID = la.workstationid
LEFT JOIN audithistory ah 
    ON la.last_auditid = ah.auditid
LEFT JOIN Resources resource 
    ON SystemInfo.WORKSTATIONID = resource.RESOURCEID
LEFT JOIN ResourceState state 
    ON resource.RESOURCESTATEID = state.RESOURCESTATEID
LEFT JOIN NetworkInfo 
    ON SystemInfo.WORKSTATIONID = NetworkInfo.WORKSTATIONID  -- Join NetworkInfo to get the IP

ORDER BY SystemInfo.WORKSTATIONNAME;
