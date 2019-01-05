CREATE TABLE green_taxi
(
    "lpep_pickup_datetime" timestamp without time zone,
    "lpep_dropoff_datetime" timestamp without time zone,
    "Pickup_longitude" double precision,
    "Pickup_latitude" double precision,
    "Dropoff_longitude" double precision,
    "Dropoff_latitude" double precision,
    "Passenger_count" integer,
    "Pickup_area" text,
    "Dropoff_area" text,
    "Dropoff_poi" integer
);

CREATE TABLE poi
(
    "PLACEID" integer,
    "NAME" text,
    "FACILITY_T" integer,
    "FACI_DOM" integer,
    "POI_LONGITUDE" double precision,
    "POI_LATITUDE" double precision
);

CREATE TABLE place_types
(
    "TYPEID" integer,
    "NAME" text
);