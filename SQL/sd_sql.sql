-- Step 1: Selecting Technician Name and Work Order Information 
SELECT 
    au.FIRST_NAME AS 'Technician',

    -- Step 2: Subquery for Total Number of Calls Created
    (SELECT COUNT(wo4.WORKORDERID)
     FROM workorder wo4
     LEFT JOIN WorkOrderStates wos4 ON wos4.WORKORDERID = wo4.WORKORDERID
     WHERE wo4.CREATEDTIME >= <from_thismonth>
     AND wo4.CREATEDTIME <= <to_thismonth>
     AND wos4.OWNERID = wos0.OWNERID
    ) AS 'Total Number of Calls Created',

    -- Step 3: Subquery for Total Closed Calls
    (SELECT COUNT(wo.WORKORDERID)
     FROM WorkOrder wo
     LEFT JOIN WorkOrderStates wos ON wo.WORKORDERID = wos.WORKORDERID
     LEFT JOIN StatusDefinition std ON wos.STATUSID = std.STATUSID
     WHERE std.STATUSNAME = 'Closed'
     AND wo.CREATEDTIME >= <from_thismonth>
     AND wo.CREATEDTIME <= <to_thismonth>
     AND wos.OWNERID = wos0.OWNERID
    ) AS 'Total Closed Calls',

    -- Step 4: Subquery for Calls Closed Within SLA
    (SELECT COUNT(wo3.WORKORDERID)
     FROM WorkOrder wo3
     LEFT JOIN WorkOrderStates wos3 ON wo3.WORKORDERID = wos3.WORKORDERID
     LEFT JOIN StatusDefinition std3 ON wos3.STATUSID = std3.STATUSID
     WHERE std3.STATUSNAME = 'Closed'
     AND wos3.ISOVERDUE = '0'
     AND wo3.CREATEDTIME >= <from_thismonth>
     AND wo3.CREATEDTIME <= <to_thismonth>
     AND wos3.OWNERID = wos0.OWNERID
    ) AS 'No. of Calls Closed Within SLA',

    -- Step 5: Subquery for Calls Closed Exceeding SLA
    (SELECT COUNT(wo3.WORKORDERID)
     FROM WorkOrder wo3
     LEFT JOIN WorkOrderStates wos3 ON wo3.WORKORDERID = wos3.WORKORDERID
     LEFT JOIN StatusDefinition std3 ON wos3.STATUSID = std3.STATUSID
     WHERE std3.STATUSNAME = 'Closed'
     AND wos3.ISOVERDUE = '1'
     AND wo3.CREATEDTIME >= <from_thismonth>
     AND wo3.CREATEDTIME <= <to_thismonth>
     AND wos3.OWNERID = wos0.OWNERID
    ) AS 'No. of Calls Closed Exceeding SLA',

    -- Step 6: Percentage of Calls Closed Within SLA
    CASE 
        WHEN (SELECT COUNT(wo.WORKORDERID)
              FROM WorkOrder wo
              LEFT JOIN WorkOrderStates wos ON wo.WORKORDERID = wos.WORKORDERID
              LEFT JOIN StatusDefinition std ON wos.STATUSID = std.STATUSID
              WHERE std.STATUSNAME = 'Closed'
              AND wo.CREATEDTIME >= <from_thismonth>
              AND wo.CREATEDTIME <= <to_thismonth>
              AND wos.OWNERID = wos0.OWNERID
             ) > 0 
        THEN (SELECT COUNT(wo.workorderid)
              FROM WorkOrder wo
              LEFT JOIN WorkOrderStates wos ON wo.WORKORDERID = wos.WORKORDERID
              LEFT JOIN StatusDefinition std ON wos.STATUSID = std.STATUSID
              WHERE std.STATUSNAME = 'Closed'
              AND wo.CREATEDTIME >= <from_thismonth>
              AND wo.CREATEDTIME <= <to_thismonth>
              AND wos.OWNERID = wos0.OWNERID
              AND wos.ISOVERDUE = '0'
             ) * 100 / 
             (SELECT COUNT(wo4.workorderid)
              FROM workorder wo4
              LEFT JOIN WorkOrderStates wos4 ON wos4.WORKORDERID = wo4.WORKORDERID
              WHERE wo4.CREATEDTIME >= <from_thismonth>
              AND wo4.CREATEDTIME <= <to_thismonth>
              AND wos4.OWNERID = wos0.OWNERID
              AND wos4.STATUSID = std.STATUSID
              AND std.STATUSNAME = 'Closed'
             )
        ELSE 0 
    END AS '% of Calls Created & Completed Within SLA',

    -- Step 7: Percentage of Calls Closed Exceeding SLA
    CASE 
        WHEN (SELECT COUNT(wo.WORKORDERID)
              FROM WorkOrder wo
              LEFT JOIN WorkOrderStates wos ON wo.WORKORDERID = wos.WORKORDERID
              LEFT JOIN StatusDefinition std ON wos.STATUSID = std.STATUSID
              WHERE std.STATUSNAME = 'Closed'
              AND wo.CREATEDTIME >= <from_thismonth>
              AND wo.CREATEDTIME <= <to_thismonth>
              AND wos.OWNERID = wos0.OWNERID
             ) > 0 
        THEN (SELECT COUNT(wo3.WORKORDERID)
              FROM WorkOrder wo3
              LEFT JOIN WorkOrderStates wos3 ON wo3.WORKORDERID = wos3.WORKORDERID
              LEFT JOIN StatusDefinition std3 ON wos3.STATUSID = std3.STATUSID
              WHERE std3.STATUSNAME = 'Closed'
              AND wos3.ISOVERDUE = '1'
              AND wo3.CREATEDTIME >= <from_thismonth>
              AND wo3.CREATEDTIME <= <to_thismonth>
              AND wos3.OWNERID = wos0.OWNERID
             ) * 100 /
             (SELECT COUNT(wo4.WORKORDERID)
              FROM WorkOrder wo4
              LEFT JOIN WorkOrderStates wos4 ON wo4.WORKORDERID = wos4.WORKORDERID
              WHERE wo4.CREATEDTIME >= <from_thismonth>
              AND wo4.CREATEDTIME <= <to_thismonth>
              AND wos4.OWNERID = wos0.OWNERID
              AND wos4.STATUSID = 3
             )
        ELSE 0 
    END AS '% of Calls Created & Completed Exceeding SLA'

-- Main FROM clause, joining WorkOrder with WorkOrderStates and AaaUser for technician information
FROM WorkOrder wo2
LEFT JOIN WorkOrderStates wos0 ON wos0.workorderid = wo2.workorderid
LEFT JOIN AaaUser au ON au.user_id = wos0.ownerid

-- WHERE clause for filtering time period and ensuring owner and technician name exist
WHERE wos0.OWNERID IS NOT NULL
AND wo2.CREATEDTIME >= <from_thismonth>
AND wo2.CREATEDTIME <= <to_thismonth>
AND au.FIRST_NAME IS NOT NULL

-- GROUP BY clause to group results by technician and owner ID
GROUP BY au.first_name, wos0.OWNERID; 
