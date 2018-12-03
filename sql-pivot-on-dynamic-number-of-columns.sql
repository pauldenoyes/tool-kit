--Need the sales by month per product
--     > From an uncommon model
--     > That seems to have duplicated lines, in that case take the max. value
--     > That will have to be updated every month... until we can make the resultset columns "dynamic"

------------------------------------------------
--Step 1/ set our example datas
------------------------------------------------
DECLARE @uncommonModel TABLE(
monthOfYear INT,
Product1Name VARCHAR(15),
SalesCount1 INT,
Product2Name VARCHAR(15),
SalesCount2 INT,
Product3Name VARCHAR(15),
SalesCount3 INT)

INSERT INTO @uncommonModel
SELECT 1, 'car', NULL, 'train', 75, 'plane', 50
UNION ALL -- Union all is to keep duplicates (simple union would have removed duplicates)
SELECT 2, 'car', 25, 'train', 50, 'plane', NULL
UNION ALL
SELECT 3, 'car', 50, 'train', NULL, 'plane', 100
UNION ALL
SELECT 4, 'car', NULL, 'train', 100, 'plane', NULL
UNION ALL
SELECT 5, 'car', 100, 'train', 75, 'plane', 25
UNION ALL
SELECT 5, 'car', 100, 'train', 75, 'plane', 25
UNION ALL
SELECT 6, 'car', 100, 'train', NULL, 'plane', NULL
UNION ALL
SELECT 6, 'car', NULL, 'train', 50, 'plane', NULL

SELECT * FROM @uncommonModel

------------------------------------------------
--Step 2/ Reshape datas and pivot to get the specified resultset
------------------------------------------------
;WITH moreCommonModel AS (
SELECT monthOfYear, Product1Name AS ProductName, SalesCount1 AS SalesCount FROM @uncommonModel
UNION ALL
SELECT monthOfYear, Product2Name AS ProductName, SalesCount2 AS SalesCount FROM @uncommonModel
UNION ALL
SELECT monthOfYear, Product3Name AS ProductName, SalesCount3 AS SalesCount FROM @uncommonModel
)

SELECT ProductName,
	   [1] AS '1', [2] AS '2', [3] AS '3', [4] AS '4', [5] AS '5', [6] AS '6'
FROM (
SELECT * FROM moreCommonModel
) AS P
PIVOT (
MAX(SalesCount)
FOR monthOfYear IN ([1], [2], [3], [4], [5], [6])
) AS PVT

------------------------------------------------
--Step 3/ Make those columns dynamically taken (don't want to update the query every monthes)
------------------------------------------------
DECLARE @monthOfYear NVARCHAR(63)
SELECT @monthOfYear = COALESCE(@monthOfYear + ', ', '') + '[' + CONVERT(VARCHAR, monthOfYear) + ']'
FROM (SELECT DISTINCT monthOfYear FROM @uncommonModel) DistinctMonthesTable --> This removes duplicates in our "dynamic" columns extraction


DECLARE @getSalesByMonthByProduct VARCHAR(MAX)
SET @getSalesByMonthByProduct = N'
------------------------------------------------------------------------------------------
--      This is just same declaration of tables we did before, else we would need       --
--      to create true tables (not temp) then delete them, don''t want to do that       --
------------------------------------------------------------------------------------------
DECLARE @uncommonModel TABLE(
monthOfYear INT,
Product1Name VARCHAR(15),
SalesCount1 INT,
Product2Name VARCHAR(15),
SalesCount2 INT,
Product3Name VARCHAR(15),
SalesCount3 INT)

INSERT INTO @uncommonModel
SELECT 1, ''car'', NULL, ''train'', 75, ''plane'', 50
UNION ALL -- Union all is to keep duplicates (simple union would have removed duplicates)
SELECT 2, ''car'', 25, ''train'', 50, ''plane'', NULL
UNION ALL
SELECT 3, ''car'', 50, ''train'', NULL, ''plane'', 100
UNION ALL
SELECT 4, ''car'', NULL, ''train'', 100, ''plane'', NULL
UNION ALL
SELECT 5, ''car'', 100, ''train'', 75, ''plane'', 25
UNION ALL
SELECT 5, ''car'', 100, ''train'', 75, ''plane'', 25
UNION ALL
SELECT 6, ''car'', 100, ''train'', NULL, ''plane'', NULL
UNION ALL
SELECT 6, ''car'', NULL, ''train'', 50, ''plane'', NULL
;WITH moreCommonModel AS (
SELECT monthOfYear, Product1Name AS ProductName, SalesCount1 AS SalesCount FROM @uncommonModel
UNION ALL
SELECT monthOfYear, Product2Name AS ProductName, SalesCount2 AS SalesCount FROM @uncommonModel
UNION ALL
SELECT monthOfYear, Product3Name AS ProductName, SalesCount3 AS SalesCount FROM @uncommonModel
)
------------------------------------------------------------------------------------------
--      The same query as above, with DYNAMICALLY grabbed columns names (monthes)       --
--                  THAT is the INTERESTING PART I wanted to point out                  --
--    Any part of the query can be made dynamic, following this very same principle     --
------------------------------------------------------------------------------------------
SELECT ProductName, ' + @monthOfYear + '
FROM (
SELECT * FROM moreCommonModel
) AS P
PIVOT (
MAX(SalesCount)
FOR monthOfYear IN (' + @monthOfYear + ')
) AS PVT'

EXEC (@getSalesByMonthByProduct)
