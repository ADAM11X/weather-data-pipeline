/*
=========================================

Purpose of this script :
    Track all the changes made to the DATABASE

=========================================
*/
-- Verify that WeatherData is registered as a CDC source table
SELECT *
FROM   cdc.change_tables
WHERE  source_object_id = OBJECT_ID('dbo.WeatherData');

-- Declare variables to define the LSN interval
DECLARE @from_lsn AS BINARY (10);

DECLARE @to_lsn AS BINARY (10);

-- Create the watermark table if it does not already exist
IF OBJECT_ID('cdc.pipeline_watermark', 'U') IS NULL
    BEGIN
        CREATE TABLE cdc.pipeline_watermark (
            last_lsn BINARY (10)
        );
        -- Initialize the starting LSN with the minimum LSN available for WeatherData
        SET @from_lsn = sys.fn_cdc_get_min_lsn('dbo_WeatherData');
        -- Store the initial LSN in the watermark table
        INSERT  INTO cdc.pipeline_watermark (last_lsn)
        VALUES                             (@from_lsn);
    END
ELSE
    BEGIN
        PRINT 'CDC.pipeline_watermark IS ALREADY CREATED';
        -- Retrieve the last processed LSN from the watermark table
        SELECT @from_lsn = last_lsn
        FROM   cdc.pipeline_watermark;
    END

-- Retrieve the maximum available LSN to define the end of the current interval
SET @to_lsn = sys.fn_cdc_get_max_lsn();

-- Retrieve all changes between the last processed LSN and the current maximum LSN
SELECT 
       CASE __$operation 
            WHEN 2 THEN 'INSERTED' 
            WHEN 1 THEN 'DELETED' 
            WHEN 4 THEN 'UPDATED' 
       END AS operation,
       ID AS id,
       city_name,
       country_code,
       timestamp,
       temperature,
       feels_like,
       humidity,
       wind_speed,
       weather_description
FROM   cdc.fn_cdc_get_all_changes_dbo_WeatherData(@from_lsn, @to_lsn, 'all');

-- Update the watermark with the latest processed LSN
UPDATE cdc.pipeline_watermark
SET    last_lsn = @to_lsn;