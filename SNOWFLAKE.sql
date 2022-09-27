-- create a database
CREATE DATABASE animal_logic;

-- switch to the databsse
USE DATABASE animal_logic;

-- Create a storage integration called animal_logic with:
CREATE STORAGE INTEGRATION animal_logic
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = AZURE
  ENABLED = TRUE
  AZURE_TENANT_ID = 'e8911c26-cf9f-4a9c-878e-527807be8791'
  STORAGE_ALLOWED_LOCATIONS = ('azure://utsbdeleah.blob.core.windows.net/animal-logic-sample');

-- Create a Stage called animal_logic 
CREATE OR REPLACE STAGE animal_logic
STORAGE_INTEGRATION = animal_logic
URL='azure://utsbdeleah.blob.core.windows.net/animal-logic-sample';

list @animal_logic;

-- Create an external table called productivity
CREATE OR REPLACE EXTERNAL TABLE EX_PRODUCTIVITY_TABLE(
  date DATE AS (value:c1::DATE),
  dept VARCHAR AS (value:c2::VARCHAR),
  productivity FLOAT AS (value:c3::FLOAT),
  project VARCHAR AS (value:c4::VARCHAR)
)
WITH LOCATION = @animal_logic
FILE_FORMAT = (TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 1)
PATTERN = 'productivity.csv';


CREATE OR REPLACE TABLE FINAL_PRODUCTIVITY_TABLE AS
SELECT
    DATE,
    DEPT,
    PROJECT,
    PRODUCTIVITY
FROM EX_PRODUCTIVITY_TABLE;

SELECT * FROM FINAL_PRODUCTIVITY_TABLE;

-- average day peruser
-- average day per shot
-- average version per user
-- average day per shot

-- avg per shot: representation of pre-work - how many versions we work on until the final work - quantity
-- average days per user: workload

-- 2019 -2022


