SELECT 
    state.DISPLAYSTATE AS "Asset State",
    workstation.WORKSTATIONNAME AS "Machine Name", 
    workstation.LOGGEDUSER AS "Last Logged In User",
    LONGTODATE(MAX(ah.audittime)) AS "Last Scanned On"  -- Fetching the last scan time
FROM 
    SystemInfo workstation
LEFT JOIN 
    Resources resource ON workstation.WORKSTATIONID = resource.RESOURCEID
LEFT JOIN 
    ResourceState state ON resource.RESOURCESTATEID = state.RESOURCESTATEID
LEFT JOIN 
    lastauditinfo la ON workstation.WORKSTATIONID = la.workstationid
LEFT JOIN 
    audithistory ah ON la.last_auditid = ah.auditid
GROUP BY 
    state.DISPLAYSTATE, workstation.WORKSTATIONNAME, workstation.LOGGEDUSER;


