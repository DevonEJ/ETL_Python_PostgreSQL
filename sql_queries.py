# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = (
    """CREATE TABLE songplays
    (songplay_id SERIAL PRIMARY KEY,
    start_time timestamp,
    user_id varchar,
    level varchar,
    song_id varchar,
    artist_id varchar, 
    session_id varchar, 
    location varchar, 
    user_agent varchar);"""
)

user_table_create = (
    """CREATE TABLE users
    (user_id varchar,
    first_name varchar, 
    last_name varchar, 
    gender varchar, 
    level varchar);"""
)

song_table_create = (
    """CREATE TABLE songs 
    (song_id varchar PRIMARY KEY,
    title varchar,
    artist_id varchar,
    year int,
    duration int);"""
)

artist_table_create = (
    """CREATE TABLE artists
    (artist_id varchar,
    name varchar,
    location varchar,
    lattitude decimal,
    longitude decimal);"""
)

time_table_create = (
    """CREATE TABLE time 
    (start_time timestamp,
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday varchar);"""
)

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""")

user_table_insert = ("""INSERT into users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s);""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s);""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, lattitude, longitude) VALUES (%s, %s, %s, %s, %s);""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s);""")

# FIND SONGS

song_select = (""" SELECT s.song_id, a.artist_id FROM songs AS s LEFT OUTER JOIN artists AS a ON a.artist_id =  s.artist_id WHERE s.title =%s AND a.name =%s AND s.duration = %s""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]