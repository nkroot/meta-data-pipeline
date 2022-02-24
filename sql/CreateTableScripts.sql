/*Creating a development schema*/
CREATE SCHEMA IF NOT EXISTS dev;

/*Creating a staging schema*/
CREATE SCHEMA IF NOT EXISTS staging;

--DROP TABLE IF EXISTS staging.stg_weather_detail_info;
CREATE TABLE IF NOT EXISTS staging.stg_weather_detail_info 
(
	weather_dtl_id 		INT  GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
	latitude			NUMERIC,
	longitude			NUMERIC,
	location            VARCHAR(500),
	timezone            VARCHAR(100),
	timezone_offset		INT,
	unixtimestamp		INT,
	date_time			TIMESTAMP,
	sunrise				TIMESTAMP,
	sunset				TIMESTAMP,
	temperature			NUMERIC(18,2),
	temp_feels_like		NUMERIC(18,2),
	atm_pressure_hpa	INT,
	humidity_percent	INT,
	dew_point			NUMERIC(18,2),
	uv_index			NUMERIC(18,2),
	clouds_percent		INT,
	visibility_meters	INT,
	wind_speed			NUMERIC(18,2),
	wind_deg			INT,
	wind_gust			NUMERIC(18,2),
	condition_id		INT,
	weather_group       VARCHAR(1000),
	description         VARCHAR(5000),
	rain_volume_mm		NUMERIC(18,2),
	snow_volume_mm		NUMERIC(18,2),
	is_active           BIT NOT NULL DEFAULT cast(1 as bit),
	created_at			TIMESTAMP default current_timestamp,
	CONSTRAINT PK_stg_weather_detail_info_weather_dtl_id PRIMARY KEY(weather_dtl_id)
);

--DROP TABLE IF EXISTS dev.agg_max_temp_location;
CREATE TABLE IF NOT EXISTS dev.agg_max_temp_location 
(
	max_temp_loc_id 	INT  GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
	latitude			NUMERIC,
	longitude			NUMERIC,
	location            VARCHAR(500),
	date_of_reading		DATE,
	temperature			NUMERIC(18,2),
	is_active           BIT NOT NULL DEFAULT cast(1 as bit),
	created_at			TIMESTAMP default current_timestamp,
	CONSTRAINT PK_agg_max_temp_location_max_temp_loc_id PRIMARY KEY(max_temp_loc_id)
);

--DROP TABLE IF EXISTS dev.agg_weather_details;
CREATE TABLE IF NOT EXISTS dev.agg_weather_details 
(
	agg_weather_dtl_id 	INT  GENERATED ALWAYS AS IDENTITY(START WITH 1 INCREMENT BY 1),
	date_of_reading		DATE,
	avg_temperature		NUMERIC(18,2),
	min_temperature		NUMERIC(18,2),
	min_temp_latitude	NUMERIC,
	min_temp_longitude	NUMERIC,
	max_temp_latitude	NUMERIC,
	max_temp_longitude	NUMERIC,
	is_active           BIT NOT NULL DEFAULT cast(1 as bit),
	created_at			TIMESTAMP default current_timestamp,
	CONSTRAINT PK_agg_weather_details_agg_weather_dtl_id PRIMARY KEY(agg_weather_dtl_id)
);