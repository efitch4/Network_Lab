SELECT 
    MAX("aaaUser"."FIRST_NAME") AS "User Name", 
    SystemInfo.WORKSTATIONNAME AS "Asset Name", 
    ah.comments AS "Notes", 
    state.DISPLAYSTATE AS "Asset State", 
    

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
    ON SystemInfo.WORKSTATIONID = NetworkInfo.WORKSTATIONID  
LEFT JOIN ResourceOwner rOwner  
    ON resource.RESOURCEID = rOwner.RESOURCEID
LEFT JOIN "SDUser" "sdUser" 
    ON "rOwner"."USERID" = "sdUser"."USERID" 
LEFT JOIN "AaaUser" "aaaUser" 
    ON "sdUser"."USERID" = "aaaUser"."USER_ID"

-- GROUP BY required due to MAX()
GROUP BY 
    SystemInfo.WORKSTATIONNAME, 
    ah.comments, 
    state.DISPLAYSTATE, 
    SystemInfo.SERVICETAG 

ORDER BY "User Name";  
