SELECT 
    ac.account_id AS "Account ID",
    au.first_name AS "User Name (First Name)",
    CASE 
        WHEN pt.ID IS NULL THEN 'REQUESTER'
        ELSE 'TECHNICIAN'
    END AS "User Type",
    LONGTODATE(lj.opentime) AS "Last Login Time",
    LONGTODATE(lj.closetime) AS "Last Logout Time",
    LONGTODATE(au.CREATEDTIME) AS "Account Created At",
    CASE 
        WHEN lj.session_id IS NULL THEN '-'
        ELSE (
            SELECT user_host 
            FROM aaaaccsession 
            WHERE session_id = lj.session_id
        )
    END AS "IP Address",
    al.NAME AS "Login Name",
    al.DOMAINNAME AS "Domain",
    ot.emailid AS "Email",
    ot.deptname AS "Department",
    repuser.FIRST_NAME AS "Reporting Manager",
    sd.ISVIPUSER AS "VIP User"
FROM 
    aaaaccount ac
INNER JOIN 
    aaalogin al ON ac.login_id = al.login_id
INNER JOIN 
    aaauser au ON al.user_id = au.user_id
INNER JOIN 
    sduser sd ON au.user_id = sd.userid
INNER JOIN 
    portalusers pu ON sd.userid = pu.userid
LEFT JOIN 
    PortalTechnicians pt ON pu.ID = pt.ID
INNER JOIN (
    SELECT 
        acc.account_id AS account_id,
        MAX(acs.opentime) AS opentime,
        MAX(acs.closetime) AS closetime,
        MAX(acs.session_id) AS session_id
    FROM 
        aaaaccount acc
    LEFT JOIN 
        aaaaccsession acs ON acc.account_id = acs.account_id
    GROUP BY 
        acc.account_id
) lj ON ac.account_id = lj.account_id
LEFT JOIN 
    aaauser repuser ON sd.reportingto = repuser.user_id
LEFT JOIN (
    SELECT 
        auu.user_id AS user_id,
        aci.emailid AS emailid,
        dd.deptname AS deptname
    FROM 
        aaauser auu
    INNER JOIN 
        sduser sdd ON auu.user_id = sdd.userid
    LEFT JOIN 
        UserDepartment ud ON sdd.USERID = ud.USERID
    LEFT JOIN 
        DepartmentDefinition dd ON ud.DEPTID = dd.DEPTID
    LEFT JOIN 
        AaaUserContactInfo auci ON auu.user_id = auci.user_id
    LEFT JOIN 
        AaaContactInfo aci ON auci.contactinfo_id = aci.contactinfo_id
) ot ON au.user_id = ot.user_id
WHERE 
    pu.status LIKE 'ACTIVE'
ORDER BY 
    "User Type", 
    "User Name (First Name)";
