/*
=========================================

Purpose of this script :
    Configure Change Data Capture (CDC)
    for the database and WeatherData table.

! Running the script more than once will raise an error !
=========================================
*/

-- Enable Change Data Capture (CDC) at the database level
EXEC sys.sp_cdc_enable_db;

-- Enable Change Data Capture (CDC) for the WeatherData table
EXEC sys.sp_cdc_enable_table 
    @source_schema = N'dbo',
    @source_name = N'WeatherData',
    @role_name = NULL;
