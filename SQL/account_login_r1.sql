SELECT 
    ac.account_id AS "Account ID",
    au.first_name AS "User Name (First Name)",
    LONGTODATE(lj.opentime) AS "Last Login Time",
    al.NAME AS "Login Name",
    ot.emailid AS "Email"
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
INNER JOIN (
    SELECT 
        acc.account_id AS account_id,
        MAX(acs.opentime) AS opentime
    FROM 
        aaaaccount acc
    LEFT JOIN 
        aaaaccsession acs ON acc.account_id = acs.account_id
    GROUP BY 
        acc.account_id
) lj ON ac.account_id = lj.account_id
LEFT JOIN (
    SELECT 
        auu.user_id AS user_id,
        aci.emailid AS emailid
    FROM 
        aaauser auu
    LEFT JOIN 
        AaaUserContactInfo auci ON auu.user_id = auci.user_id
    LEFT JOIN 
        AaaContactInfo aci ON auci.contactinfo_id = aci.contactinfo_id
) ot ON au.user_id = ot.user_id
WHERE 
    pu.status LIKE 'ACTIVE'
ORDER BY 
    "User Name (First Name)";
