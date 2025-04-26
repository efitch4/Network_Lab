SELECT 
    state.DISPLAYSTATE AS "Asset State",
    workstation.WORKSTATIONNAME AS "Machine Name", 
    workstation.LOGGEDUSER AS "Last Logged In User",
    LONGTODATE(MAX(ah.audittime)) AS "Last Scanned On",  -- Fetching the last scan time
    LONGTODATE(MAX(LASTSUCCESSAUDIT.audittime)) AS "Last Success Scan Date",
    LONGTODATE(MAX(audithistory.audittime)) AS "Last Scan Date"
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
LEFT JOIN 
    audithistory LASTSUCCESSAUDIT ON la.last_success_auditid = LASTSUCCESSAUDIT.auditid
LEFT JOIN 
    audithistory ON la.last_auditid = audithistory.auditid
GROUP BY 
    state.DISPLAYSTATE, 
    workstation.WORKSTATIONNAME, 
    workstation.LOGGEDUSER;

