import psycopg2, psycopg2.extras

db_settings = {
    "host": "localhost",
    "database": "RideShareApp",
    "user": "postgres",
    "password": "Alfred45"}
conn = psycopg2.connect(**db_settings)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

try:
    cur.execute(
        "create table address \
        (address_id SERIAL, \
        address_name varchar (20) not null, \
        address_number varchar(20) not null, \
        address_city varchar (20) not null,  \
        address_zip varchar(9) not null, \
        state varchar(20) not null, \
        primary key (address_id)) " 
    )

    cur.execute(
        "create table rider \
        (rider_id SERIAL,\
        rider_first_name varchar (20) not null,\
        rider_last_name varchar (20) not null,\
        address_id INT,\
        rider_username varchar (20),\
        rider_password varchar (20),\
        primary key(rider_id),\
        foreign key (address_id) references address))"
    )

    cur.execute(
        "create table driver\
        (driver_id SERIAL,\
        driver_first_name varchar (20) not null,\
        driver_last_name varchar (20) not null,\
        address_id INT,\
        driver_username varchar (20),\
        driver_password varchar(20),\
        primary key(driver_id),\
        foreign key (address_id) references address))"
    )

    cur.execute(
        "create table rider_credit_card \
        rider_card_number varchar(20), \
        rider_id INT, \
        address_id INT, \
        primary key (rider_card_number), \
        foreign key (rider_id) references rider))"
    )

    cur.execute (
        "create table driver_credit_card \
        (driver_card_number varchar(20), \
        driver_id INT, \
        driver_address_id INT, \
        primary key (driver_card_number), \
        foreign key (driver_id) references driver)"
    )

    cur.execute (
        "create table ride_information \
        (ride_id SERIAL, \
        rider_id SERIAl, \
        driver_id SERIAL, \
        rating INT CONSTRAINT rating CHECK (rating BETWEEN 1 AND 5), \
        primary key (ride_id), \
        foreign key (rider_id) references rider, \
        foreign key (driver_id) references driver)"

    )

    conn.commit()

except Exception as e:
    print (e)
    conn.rollback()

