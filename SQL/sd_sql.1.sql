-- Step 1: Selecting Technician Name and Work Order Information
SELECT 
	au.FIRST_NAME AS 'Technicican',
	
	-- Step 2: Subquery for Total Number of Calls Created
	(SELECT COUNT(wo4.WORKORDERID)
	from workorder wo4
	LEFT JOIN WorkorderStates wos4 ON wos4.WORKORDERID = wo4.WORKORDERID
	WHERE wo4.CREATEDTIME >= <from_thismonth>
	AND wo4.CREATEDTIME <= >to_thismonth>
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
	AND wos3.CREATEDTIME >=<from_thismonth>
	AND wo3.CREATEDTIME <=<to_thismonth>
	AND wos3.OWNERID = wos0.OWNERID
	) AS 'No . of Calls Closed Within SLA',
	
	-- Step 5: Subquery for calls Closed Exceeding SLA
	(SELECT COUNT(wo3.WORKORDERID)
	FROM Workorderwo3
	LEFT JOIN WorkOrderStates wos3 ON wo3.WORKORDERID = wos3.WORKORDERID
	LEFT JOIN StatusDefinition std3 ON wos3.STATUSID = std3.STATUSID
	WHERE std3.STATUSNAME = 'Closed'
	AND wos3.ISOVERDUE = '1'
	AND wo3.CREATEDTIME >= <from_thismonth>
	AND wo3.CREATEDTIME <= <to_thismonth>
	AND wos3.OWNERID = wos0.OWNDERID
   ) AS 'No. of Call Closed Exceeding SLA',
   
  -- Step 6: Percentage of Calls Closed Within SLA
	CASE
		WHEN (SELECT COUNT(wo.WORKORDERID)
			  FROM WorkOrder wo
			  LEFT JOIN WorkorderStates wos ON wo.WORKORDERID = wos.WORKORDERID
			  LEFT JOIN StatusDefinition std ON wos.STATUSID = std.STATUSID
			  WHERE std.STATUSNAME = 'Closed'
			  AND wo.CREATEDTIME >= <from_thismonth>
			  AND wo.CREATEDTIME <= <to_thismonth>
			  AND wos.OWNERID = wos0.OWNDERID
			  ) > 0
		THEN (SELECT COUNT(wo.workorderid)
			  FROM workorder wo4
			  LEFT JOIN WorkOrderStates wos4 ON wos4.WORKORDERID = wo4.WORKORDERID
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
			 AND wo4CREATEDTIME <= <to_thismonth>
			 AND wos4.OWNERID = wos0.OWNERID
			 AND wos4.STATUSID = std.STATUSID
			 AND std.STATUSNAME = 'Closed'
			 )
	    ELSE 0
	END AS '% of Calls Created and Completed Within SLA',