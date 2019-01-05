CREATE TABLE green_taxi
(
    "VendorID" integer,
    "lpep_pickup_datetime" timestamp without time zone,
    "lpep_dropoff_datetime" timestamp without time zone,
    "Store_and_fwd_flag" character(1) COLLATE pg_catalog."default",
    "RateCodeID" integer,
    "Pickup_longitude" double precision,
    "Pickup_latitude" double precision,
    "Dropoff_longitude" double precision,
    "Dropoff_latitude" double precision,
    "Passenger_count" integer,
    "Trip_distance" double precision,
    "Fare amount" double precision,
    "Extra" double precision,
    "MTA_tax" double precision,
    "Tip_amount" double precision,
    "Tolls_amount" double precision,
    "Ehail_fee" double precision,
    improvement_surcharge double precision,
    "Total_amount" double precision,
    "Payment_type" integer,
    "Trip_type" integer,
    "Pickup_area" text,
    "Dropoff_area" text,
    "Dropoff_poi" text
);