SELECT 
    MAX("aaaUser"."FIRST_NAME") AS "User",
    MAX("resource"."RESOURCENAME") AS "Asset Name",
    MAX("productType"."COMPONENTTYPENAME") AS "Product Type",
    MAX("product"."COMPONENTNAME") AS "Product"
FROM 
    "Resources" "resource"
LEFT JOIN 
    "ComponentDefinition" "product" 
    ON "resource"."COMPONENTID" = "product"."COMPONENTID"
LEFT JOIN 
    "ComponentType" "productType" 
    ON "product"."COMPONENTTYPEID" = "productType"."COMPONENTTYPEID"
LEFT JOIN 
    "ResourceState" "state" 
    ON "resource"."RESOURCESTATEID" = "state"."RESOURCESTATEID"
LEFT JOIN 
    "ResourceOwner" "rOwner" 
    ON "resource"."RESOURCEID" = "rOwner"."RESOURCEID"
LEFT JOIN 
    "ResourceAssociation" "rToAsset" 
    ON "rOwner"."RESOURCEOWNERID" = "rToAsset"."RESOURCEOWNERID"
LEFT JOIN 
    "SDUser" "sdUser" 
    ON "rOwner"."USERID" = "sdUser"."USERID"
LEFT JOIN 
    "AaaUser" "aaaUser" 
    ON "sdUser"."USERID" = "aaaUser"."USER_ID"
WHERE  
    "state"."DISPLAYSTATE" = N'In Use'
    AND (
        "productType"."COMPONENTTYPENAME" IN (
            N'Smart Phone',
            N'Cell Phone'
            )
    )
GROUP BY 
    "resource"."RESOURCEID"