SELECT 
    MAX("aaaUser"."FIRST_NAME") AS "User", 
    MAX("workstation"."WORKSTATIONNAME") AS "Machine Name", 
    MAX("workstation"."MANUFACTURER") AS "Manufacturer", 
    MAX("workstation"."MODEL") AS "Model", 
    MAX("workstation"."SERVICETAG") AS "Service Tag", 
    MAX("resource"."ACQUISITIONDATE") AS "Acquisition Date", 
    MAX("memInfo"."TOTALMEMORY") AS "Total Memory", 
    MAX("osInfo"."OSNAME") AS "OS",
    MAX("workstation"."LOGGEDUSER") AS "Last Logged In User"  -- Last logged-in user
FROM "SystemInfo" "workstation"
LEFT JOIN "Resources" "resource" 
    ON "workstation"."WORKSTATIONID" = "resource"."RESOURCEID" 
LEFT JOIN "ResourceState" "state" 
    ON "resource"."RESOURCESTATEID" = "state"."RESOURCESTATEID" 
LEFT JOIN "ResourceOwner" "rOwner" 
    ON "resource"."RESOURCEID" = "rOwner"."RESOURCEID" 
LEFT JOIN "ResourceAssociation" "rToAsset" 
    ON "rOwner"."RESOURCEOWNERID" = "rToAsset"."RESOURCEOWNERID" 
LEFT JOIN "SDUser" "sdUser" 
    ON "rOwner"."USERID" = "sdUser"."USERID" 
LEFT JOIN "AaaUser" "aaaUser" 
    ON "sdUser"."USERID" = "aaaUser"."USER_ID" 
LEFT JOIN "MemoryInfo" "memInfo" 
    ON "workstation"."WORKSTATIONID" = "memInfo"."WORKSTATIONID" 
LEFT JOIN "OsInfo" "osInfo" 
    ON "workstation"."WORKSTATIONID" = "osInfo"."WORKSTATIONID" 
WHERE  
    "state"."DISPLAYSTATE" = N'In Use' 
    AND "aaaUser"."FIRST_NAME" IS NOT NULL 
    AND "memInfo"."TOTALMEMORY" > 4294967296 -- Total memory greater than 4GB (in bytes)
GROUP BY 
    "workstation"."WORKSTATIONID";
