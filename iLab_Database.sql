--USE WAREHOUSE ILABDATA;
--SELECT CURRENT_WAREHOUSE();

CREATE DATABASE ilab_database;
USE DATABASE ilab_database;

--drop DATABASE ilab_database;
Create schema raw;
Use ilab_database.raw;

CREATE STORAGE INTEGRATION ilab_storage_Int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = AZURE
  ENABLED = TRUE
  AZURE_TENANT_ID = 'e8911c26-cf9f-4a9c-878e-527807be8791'
  STORAGE_ALLOWED_LOCATIONS = ('azure://animallogicdata.blob.core.windows.net/data');
  
  

--DROP STORAGE INTEGRATION ilab_storage_Int;
DESC STORAGE INTEGRATION ilab_storage_Int; 
--DESCRIBE INTEGRATION ilab_storage_Int;

CREATE OR REPLACE STAGE stage_ilab2
STORAGE_INTEGRATION = ilab_storage_Int
URL='azure://animallogicdata.blob.core.windows.net/data';

--drop stage stage_ilab2;
list @stage_ilab2;

-- Create a file format for CSV
CREATE OR REPLACE FILE FORMAT file_format_csv 
TYPE = 'CSV' 
FIELD_DELIMITER = ',' 
SKIP_HEADER = 1
NULL_IF = ('\\N', 'NULL', 'NUL', '')
FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-------------------------------------- External Table ---------------------------------
-- create external table for timesheets data.
CREATE OR REPLACE EXTERNAL TABLE raw.timesheets
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'timesheets.*.csv';

-- create external table for versions data.
CREATE OR REPLACE EXTERNAL TABLE raw.versions
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'versions.*.csv';

-- create external table for crew data.
CREATE OR REPLACE EXTERNAL TABLE raw.crew
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'crew.csv';

-- create external table for dept-dept data.
CREATE OR REPLACE EXTERNAL TABLE raw.deptdept
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'dept-dept.csv';

-- create external table for depts data.
CREATE OR REPLACE EXTERNAL TABLE raw.depts
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'depts.csv';

-- create external table for rtypes data.
CREATE OR REPLACE EXTERNAL TABLE raw.rtypes
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'rtypes.csv';

-- create external table for shot-types data.
CREATE OR REPLACE EXTERNAL TABLE raw.shot_types
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'shot-types.csv';

-- create external table for shows data.
CREATE OR REPLACE EXTERNAL TABLE raw.shows
with location = @stage_ilab2 
file_format = file_format_csv
pattern = 'shows.csv';

--Examing external table
select *
from timesheets
limit 5;

--Create Staging, datawarehouse and datamart
Create schema staging;
create schema datawarehouse;
create schema datamart;

-------------------------------------- Staging Table ---------------------------------
-- Create staging tables with correct data type for timesheets
CREATE OR REPLACE TABLE staging.timesheets as
(select 
    value:c1::date as date
    , value:c2::date as week
    , value:c3::date as month
    , value:c4::int as year
    , value:c5::varchar as lpath
    , value:c6::varchar as show
    , value:c7::varchar as jobnumber
    , value:c8::varchar as tasktype
    , value:c9::varchar as dept
    , value:c10::varchar as task
    , value:c11::varchar as scene
    , value:c12::varchar as shot
    , value:c13::varchar as entitytype
    , value:c14::varchar as entity
    , value:c15::varchar as jiraproject
    , value:c16::varchar as jiraissue
    , value:c17::varchar as username
    , value:c18::varchar as zone
    , value:c19::int as entries
    , value:c20::decimal(12,2) as days_logged
    , value:c21::decimal(12,2) as days_signed_off
from raw.timesheets);

select * 
from staging.timesheets
limit 10;

-- create staging tables with correct data type for versions
CREATE OR REPLACE TABLE staging.versions as
(select 
    value:c1::date as date
    , value:c2::date as week
    , value:c3::date as month
    , value:c4::int as year
    , value:c5::varchar as project
    , value:c6::varchar as username
    , value:c7::varchar as atype
    , value:c8::varchar as vtype
    , value:c9::varchar as assettype
    , value:c10::varchar as reviewtype
    , value:c11::varchar as pkgtype
    , value:c12::varchar as scene
    , value:c13::varchar as shot
    , value:c14::varchar as eftype
    , value:c15::varchar as state
    , value:c16::int as count
    , value:c17::int as bytes
    , value:c18::varchar as size
    , value:c19::varchar as intreviewed
    , value:c20::varchar as dirreviewed
from raw.versions);

-- Create staging tables with correct data type for crew
CREATE OR REPLACE TABLE staging.crew as
(select 
    value:c1::varchar as username
    , value:c2::varchar as type
from raw.crew);

-- create staging tables with correct data type for deptdept
CREATE OR REPLACE TABLE staging.deptdept as
(select 
    value:c1::varchar as dept
    , value:c2::varchar as department
from raw.deptdept);

-- create staging tables with correct data type for depts
CREATE OR REPLACE TABLE staging.depts as
(select 
    value:c1::varchar as department
    , value:c2::varchar as name
from raw.depts);

-- create staging tables with correct data type for rtypes
CREATE OR REPLACE TABLE staging.rtypes as
(select 
    value:c1::varchar as rtype
    , value:c2::varchar as dept
    , value:c3::varchar as type
from raw.rtypes);

-- create staging tables with correct data type for shot_types
CREATE OR REPLACE TABLE staging.shot_types as
(select 
    value:c1::varchar as Shot_Type
from raw.shot_types);

-- create staging tables with correct data type for shows
CREATE OR REPLACE TABLE staging.shows as
(select 
    value:c1::varchar as shortname
    , value:c2::varchar as title
    , value:c3::varchar as end
    , value:c4::varchar as refweek
from raw.shows);

-------------------------------------- data warehouse ---------------------------------
--Data Cleaning and transforming, create data warehouse
-- CREATE datawarehouse.versions_mod with enriched data 
CREATE OR REPLACE TABLE datawarehouse.versions_mod as
SELECT v.*
    , r.type as review_type
    , dn.department as department_name
    , c.type as crew_type
    , case when dirreviewed = 'yes' then 'Director Reviewed'
           when intreviewed = 'yes' then 'Internal Reviewed'
           else 'Surplus Reviewed'
           end as review_Category
FROM staging.versions as v
left join staging.rtypes as r
    on v.reviewtype = r.rtype --# 1. add dept and type based on reviewtype
left join staging.deptdept as d
    on r.dept = d.dept --# 2. add department
left join staging.depts as dn
    on d.department = dn.department --# 3. add department full name
left join staging.crew as c
    on v.username = c.username --# 4. add employee type
;

-- SELECT count(*)
-- FROM staging.versions;

-- SELECT count(*)
-- FROM datawarehouse.versions_mod;

-- CREATE datawarehouse.timesheets_mod with enriched data 
CREATE OR REPLACE TABLE datawarehouse.timesheets_mod as
SELECT t.*
    , c.type as crew_type
    , dn.department as department_name
FROM staging.timesheets as t
left join staging.crew as c
    on t.username = c.username --# 1. add employee type
left join staging.deptdept as d
    on t.dept = d.dept --# 2. add department
left join staging.depts as dn
    on d.department = dn.department --# 3. add department full name
;


-- SELECT TOP 1000 *
-- FROM staging.timesheets;

-- SELECT TOP 1000 *
-- FROM datawarehouse.timesheets_mod;


CREATE OR REPLACE TABLE datawarehouse.WorkDays_Department AS
SELECT *
FROM
    (
        SELECT DISTINCT DATE, WEEK, MONTH
        FROM datawarehouse.timesheets_mod
    ) AS bd
    CROSS JOIN
    (
        SELECT DISTINCT DEPARTMENT_NAME
        FROM datawarehouse.timesheets_mod
        WHERE DEPARTMENT_NAME IS NOT NULL
    ) AS dp
WHERE DEPARTMENT_NAME NOT IN ('prod', 'art', 'supervision', 'edit', 'di')
;

CREATE OR REPLACE TABLE datawarehouse.T_V_Date_Bridge AS
SELECT COALESCE(T_DATE, first_value(T_DATE) OVER (PARTITION BY T_DATE_GROUP ORDER BY DATE)) AS T_DATE
    , V_DATE
FROM
    (
        SELECT COALESCE(t.DATE, v.DATE) AS Date
            , t.DATE AS T_DATE
            , COUNT(t.DATE) OVER (ORDER BY COALESCE(t.DATE, v.DATE)) AS T_DATE_GROUP
            , v.DATE AS V_DATE
        FROM 
            (
                SELECT DISTINCT DATE FROM datawarehouse.timesheets_mod
            ) AS t
            FULL OUTER JOIN
            (
                SELECT DISTINCT DATE FROM datawarehouse.versions_mod
            ) AS v
            ON t.DATE = v.DATE
    )
;

CREATE OR REPLACE TABLE datawarehouse.full_calendar AS
WITH DATES_CTE (date) AS (
    SELECT MIN(T_DATE) FROM datawarehouse.t_v_date_bridge
    UNION ALL
    SELECT DATEADD(day, 1, date)
    FROM DATES_CTE
    WHERE date < (SELECT MAX(T_DATE) FROM datawarehouse.t_v_date_bridge)
)

SELECT DATE, DEPARTMENT_NAME
FROM DATES_CTE
    CROSS JOIN
    (SELECT DISTINCT DEPARTMENT_NAME FROM datawarehouse.WorkDays_Department)
;

-------------------------------------- data mart ---------------------------------
CREATE OR REPLACE TABLE datamart.hours AS
WITH Productive AS (
    SELECT DATE
        , DEPARTMENT_NAME
        , CASE WHEN TASK IN ('td', 'prod', 'supervision', 'meeting', 'training', 'di', NULL) THEN 'Overheads' ELSE 'Productive' END AS ProdOver
        , SUM(DAYS_LOGGED)*8 AS HOURS_LOGGED
    FROM datawarehouse.timesheets_mod
    WHERE DEPARTMENT_NAME IS NOT NULL
    GROUP BY DATE, DEPARTMENT_NAME, ProdOver
), Artists AS (
    SELECT DATE
        , DEPARTMENT_NAME
        , COUNT(DISTINCT(USERNAME)) AS ARTISTS
    FROM datawarehouse.timesheets_mod
    WHERE DEPARTMENT_NAME IS NOT NULL
    GROUP BY DATE, DEPARTMENT_NAME
), ProdPivot AS (
    SELECT p.DATE
        , p.DEPARTMENT_NAME
        , a.ARTISTS
        , SUM(CASE WHEN p.ProdOver = 'Productive' THEN p.HOURS_LOGGED ELSE 0 END) AS Productive_Hours
        , SUM(CASE WHEN p.ProdOver = 'Overheads' THEN p.HOURS_LOGGED ELSE 0 END) AS Overhead_Hours
        , SUM(p.HOURS_LOGGED) AS Total_Hours
    FROM
        Productive AS p,
        Artists AS a
    WHERE p.DATE = a.DATE
        AND p.DEPARTMENT_NAME = a.DEPARTMENT_NAME
    GROUP BY p.DATE, p.DEPARTMENT_NAME, ARTISTS
)

SELECT wdd.DATE
    , wdd.DEPARTMENT_NAME
    , CASE WHEN p.ARTISTS IS NULL THEN 0 ELSE p.ARTISTS END AS ARTISTS
    , CASE WHEN p.PRODUCTIVE_HOURS IS NULL THEN 0 ELSE p.PRODUCTIVE_HOURS END AS PRODUCTIVE_HOURS
    , CASE WHEN p.OVERHEAD_HOURS IS NULL THEN 0 ELSE p.OVERHEAD_HOURS END AS OVERHEAD_HOURS
    , CASE WHEN p.TOTAL_HOURS IS NULL THEN 0 ELSE p.TOTAL_HOURS END AS TOTAL_HOURS
FROM
    datawarehouse.WorkDays_Department AS wdd
    LEFT JOIN
    ProdPivot AS p
    ON p.DATE = wdd.date AND p.DEPARTMENT_NAME = wdd.DEPARTMENT_NAME
;

CREATE OR REPLACE TABLE datamart.file_prod AS
SELECT DATE
    , DEPARTMENT_NAME
    , SUM(BYTES) AS TotalFileSize
FROM datawarehouse.versions_mod
WHERE DEPARTMENT_NAME IS NOT NULL
    AND DEPARTMENT_NAME <> 'di'
    AND ASSETTYPE <> 'Other'
GROUP BY DATE, DEPARTMENT_NAME
ORDER BY DATE, DEPARTMENT_NAME
;

--Calculate Weekly outcome (Count of Verions), by Department, using weighting 
CREATE OR REPLACE TABLE datamart.Review_Product as
with agg_data as (
select DATE,
       Department_Name,
       sum(count) AS count_of_version, 
       sum(case when review_Category = 'Director Reviewed' then count*1
           when review_Category = 'Internal Reviewed' then count*0.75
           else count*0.01
           end) as weighted_output
from datawarehouse.versions_mod
group by 1, 2
)
select DATE,
       Department_Name,
       count_of_version,
       weighted_output
from agg_data
where Department_Name is not null
;

CREATE OR REPLACE TABLE datamart.DEPARTMENT_WAITTIMES AS 
WITH HANDOVER_TEST AS (
SELECT DATE
    , DEPARTMENT_NAME
    , SCENE
    , SHOT
    , CASE WHEN 
        LAG(DEPARTMENT_NAME, 1) 
        OVER (
            PARTITION BY SCENE, SHOT 
            ORDER BY DATE
        ) <> DEPARTMENT_NAME 
        THEN 'HANDOVER' END AS HANDOVER_TEST
    , DATEDIFF(DAY, LAG(DATE, 1) OVER (PARTITION BY SCENE, SHOT ORDER BY DATE), DATE) AS DATETEST
FROM datawarehouse.versions_mod 
WHERE SCENE IS NOT NULL
    AND DEPARTMENT_NAME IS NOT NULL
    AND DEPARTMENT_NAME IN ('light', 'fx', 'anim', 'layout', 'charfx', 'assets')
ORDER BY SCENE, SHOT, DATE
)

SELECT DATE, DEPARTMENT_NAME, AVG(DATETEST) AS AVG_WAITTIME
FROM HANDOVER_TEST 
WHERE HANDOVER_TEST IS NOT NULL
GROUP BY DATE, DEPARTMENT_NAME
;

SET window_size = 25;

CREATE OR REPLACE VIEW datamart.v_Data_Export AS
WITH Joint AS (
SELECT h.DATE
    , h.DEPARTMENT_NAME
    , h.PRODUCTIVE_HOURS
    , h.OVERHEAD_HOURS
    , h.TOTAL_HOURS
    , h.ARTISTS
    , CASE WHEN SUM(afp.TOTALFILESIZE) IS NULL THEN 0 ELSE SUM(afp.TOTALFILESIZE) END AS TOTALFILESIZE
    , CASE WHEN SUM(rp.COUNT_OF_VERSION) IS NULL THEN 0 ELSE SUM(rp.COUNT_OF_VERSION) END AS VERSION_COUNT
    , CASE WHEN SUM(rp.WEIGHTED_OUTPUT) IS NULL THEN 0 ELSE SUM(rp.WEIGHTED_OUTPUT) END AS WEIGHTED_OUTPUT
    , CASE WHEN SUM(wt.AVG_WAITTIME) IS NULL THEN 0 ELSE SUM(wt.AVG_WAITTIME) END AS AVG_WAITTIME
FROM datamart.HOURS AS h
    FULL OUTER JOIN
    datawarehouse.t_v_date_bridge AS br
    ON h.date = br.t_date
    FULL OUTER JOIN
    datamart.file_prod AS afp
    ON afp.date = br.v_date AND afp.DEPARTMENT_NAME = h.DEPARTMENT_NAME
    FULL OUTER JOIN
    datamart.REVIEW_PRODUCT AS rp
    ON rp.date = br.v_date AND rp.DEPARTMENT_NAME = afp.DEPARTMENT_NAME
    FULL OUTER JOIN
    datamart.DEPARTMENT_WAITTIMES AS wt
    ON wt.date = br.v_date AND wt.DEPARTMENT_NAME = afp.DEPARTMENT_NAME
GROUP BY h.DATE, h.DEPARTMENT_NAME, h.PRODUCTIVE_HOURS, h.OVERHEAD_HOURS, h.TOTAL_HOURS, h.ARTISTS
ORDER BY h.DATE, h.DEPARTMENT_NAME
), Prod AS (
SELECT DATE
    , DEPARTMENT_NAME
    , PRODUCTIVE_HOURS
    , OVERHEAD_HOURS
    , TOTAL_HOURS
    , CASE WHEN PRODUCTIVE_HOURS = 0 THEN 1 ELSE OVERHEAD_HOURS / PRODUCTIVE_HOURS END AS OVERHEADS_PER_PRODUCTIVE
    , ARTISTS
    , CASE WHEN TOTAL_HOURS = 0 THEN 0 ELSE TOTALFILESIZE / TOTAL_HOURS END AS FILESIZE_PRODUCTIVITY
    , CASE WHEN TOTAL_HOURS = 0 THEN 0 ELSE VERSION_COUNT / TOTAL_HOURS END AS COUNT_PRODUCTIVITY
    , CASE WHEN TOTAL_HOURS = 0 THEN 0 ELSE WEIGHTED_OUTPUT / TOTAL_HOURS END AS REVIEW_PRODUCTIVITY
    , AVG_WAITTIME
FROM Joint
), AVERAGED AS (
SELECT DATE
    , DEPARTMENT_NAME
    , AVG(PRODUCTIVE_HOURS) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS PRODUCTIVE_HOURS
    , AVG(OVERHEAD_HOURS) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS OVERHEAD_HOURS
    , AVG(TOTAL_HOURS) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS TOTAL_HOURS
    , AVG(OVERHEADS_PER_PRODUCTIVE) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS OVERHEADS_PER_PRODUCTIVE
    , AVG(ARTISTS) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS ARTISTS
    , AVG(FILESIZE_PRODUCTIVITY) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS FILESIZE_PRODUCTIVITY
    , AVG(COUNT_PRODUCTIVITY) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS COUNT_PRODUCTIVITY
    , AVG(REVIEW_PRODUCTIVITY) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS REVIEW_PRODUCTIVITY
    , AVG(AVG_WAITTIME) OVER (PARTITION BY DEPARTMENT_NAME ORDER BY DATE ROWS BETWEEN $window_size PRECEDING AND CURRENT ROW) AS AVG_WAITTIME
FROM Prod
WHERE DATE IS NOT NULL
), Full_Calendar AS (
SELECT c.DATE
    , c.DEPARTMENT_NAME
    , v.PRODUCTIVE_HOURS
    , v.OVERHEAD_HOURS
    , v.TOTAL_HOURS
    , v.OVERHEADS_PER_PRODUCTIVE
    , v.ARTISTS
    , REPLACE(v.FILESIZE_PRODUCTIVITY, ',', '') AS FILESIZE_PRODUCTIVITY
    , v.COUNT_PRODUCTIVITY
    , v.REVIEW_PRODUCTIVITY
    , v.AVG_WAITTIME
    , COUNT(v.DATE) OVER (PARTITION BY c.DEPARTMENT_NAME ORDER BY c.DATE) AS Val_Group
FROM datawarehouse.full_calendar AS c
    LEFT JOIN
    AVERAGED AS v
    ON c.DATE = v.DATE AND c.DEPARTMENT_NAME = v.DEPARTMENT_NAME
)

SELECT DATE
    , DEPARTMENT_NAME
    , COALESCE(PRODUCTIVE_HOURS, FIRST_VALUE(PRODUCTIVE_HOURS) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS PRODUCTIVE_HOURS
    , COALESCE(OVERHEAD_HOURS, FIRST_VALUE(OVERHEAD_HOURS) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS OVERHEAD_HOURS
    , COALESCE(TOTAL_HOURS, FIRST_VALUE(TOTAL_HOURS) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS TOTAL_HOURS
    , COALESCE(OVERHEADS_PER_PRODUCTIVE, FIRST_VALUE(OVERHEADS_PER_PRODUCTIVE) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS OVERHEADS_PER_PRODUCTIVE
    , COALESCE(ARTISTS, FIRST_VALUE(ARTISTS) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS ARTISTS
    , COALESCE(FILESIZE_PRODUCTIVITY, FIRST_VALUE(FILESIZE_PRODUCTIVITY) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS FILESIZE_PRODUCTIVITY
    , COALESCE(COUNT_PRODUCTIVITY, FIRST_VALUE(COUNT_PRODUCTIVITY) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS COUNT_PRODUCTIVITY
    , COALESCE(REVIEW_PRODUCTIVITY, FIRST_VALUE(REVIEW_PRODUCTIVITY) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS REVIEW_PRODUCTIVITY
    , COALESCE(AVG_WAITTIME, FIRST_VALUE(AVG_WAITTIME) OVER (PARTITION BY DEPARTMENT_NAME, Val_Group ORDER BY DATE)) AS AVG_WAITTIME
FROM Full_Calendar
;

SELECT * FROM datamart.v_data_export LIMIT 100;
