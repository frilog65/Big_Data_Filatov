create database if not exists project;
use project;
create external table if not exists aparts (
    id int,
    price int,
    metro int,
    address string,
    district string,
    rooms int,
    total_area int,
    live_area int,
    kitchen_area int,
    current_floor int,
    max_floor int,
    build_year int,
    housing_type string,
    meter_cost int,
    bath string,
    repair string,
    window_type string,
    ceiling float,
    description string
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/project.db/aparts';


create external table if not exists districts (
    id int,
    name string,
    total int,
    street int,
    kills int,
    harm int,
    theft int,
    robbery int,
    brigandage int,
    cameras int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/project.db/districts';

create external table if not exists places (
    id int,
    address string,
    places_total int
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/project.db/places';
