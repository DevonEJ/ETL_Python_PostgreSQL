
# Sparkify Database Overview

## Introduction & Purpose
<p>
    
    
    The purpose of the sparkify database is to allow the Sparkify company to analyse the songs that its users are listening to using its streaming application. 

    As such, the database contains a number of fact and dimension tables housing data on the songs users are listening to, as well as information about those users (e.g. are they paid or free users?), and about the songs and artists that they have listened to in the app.
    
    Please see the 'Example Queries' section for further detail on the expected and intended use of the database.
    
   
</p>

---

## Databases
### Database: sparkifydb

<p>
    
    * The code base within this project creates tables within a Postgresql database named 'sparkifydb'
    
    * The database has been created using a 'star schema' with fact and dimension tables, to allow analysis of user's 'song plays' on the app
    
    * Two collections of JSON log files are the data sources for the database: 'song data' and 'log_data'

</p>

---

## Tables & Schemas

<br>

### Fact Table: songplays

<p>
    
    * Comprised of event data from the log_data JSON files, where the 'page' is equal to 'NextSong' - indicating that the user is playing songs via the app - other values for 'page' are excluded from the table
    
    * Table is created by combining the log_data file with the artist_id and song_id columns from the songs and artists tables
    
Table Schema;
    
<code>songplay_id SERIAL PRIMARY KEY,
        start_time timestamp,
        user_id varchar, 
        level varchar,
        song_id varchar,
        artist_id varchar, 
        session_id varchar, 
        location varchar, 
        user_agent varchar</code>
    
</p>


### Dimension Table: users

<p>
    
    * Comprised of data from the log_data JSON files

Table schema;
    
<code>user_id varchar,
first_name varchar, 
last_name varchar, 
gender varchar, 
level varchar
</code>
    
</p>

### Dimension Table: songs 

<p>
    
    * Comprised of data from the song_data JSON files
    
Table schema;
    
<code>song_id varchar PRIMARY KEY,
    title varchar,
    artist_id varchar,
    year int,
    duration int
    
</code>    
    
</p>

### Dimension Table: Artists

<p>
    
    * Comprised of data from the song_data JSON files
    
Table schema;
    
    
<code>artist_id varchar,
    name varchar,
    location varchar,
    lattitude decimal,
    longitude decimal
    
</code>    
    
</p>

### Dimension Table: time

<p>
    
    * Comprised of data from the log_data JSON files
    
    * The table features the timestamp of each song play broken down into individual units of time in columns
    
Table schema;
     
    
<code>start_time timestamp,
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday varchar
    
</code>    
    
</p>


---

## Operation Instructions
### Connecting to the Database
<p>
    
    *   Database connections can be made using a connection object
    
Example;
<br>
<code>conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=##### password=#####")</code>
</p>

### Creating & Populating Tables
<p>
    
    * To populate the tables, you must first execute the create_tables.py file at the terminal
    
Example command;
    <code>python create_tables.py</code>
    
<br>
    
    * Next, you should run the etl.py file to populate the tables with data

Example command;
    <code>python etl.py</code>

    
</p>

### Running Queries

<p>
    
    * To run queries, first create a 'cursor' object using your connection object previously created
    
    * SQl queries can be placed within parentheses, and executed using the cursor object
    
    * Queries must then be 'committed' to actually run against the database
    
    * Be sure to close the database connection once you have finished executing queries

Example;
<br>
    <code>cur = conn.cursor()</code>
    <br>
    <code>cur.execute("""SELECT * FROM sparkifydb.songs;""")</code>
    <br>
    <code>conn.commit()</code>
    <br>
    <code>conn.close()</code>
</p>


---

## Example Query

<p>
    
    * Example; View female, non-paying users
    
<code>SELECT * FROM songplays AS sp INNER JOIN users AS u ON sp.user_id = u.user_id WHERE u.level = 'free' AND u.gender = 'F' LIMIT 10;
</code>

Result:

<code>songplay_id	start_time	user_id	level	song_id	artist_id	session_id	location	user_agent	user_id_1	first_name	last_name	gender	level_1
22	2018-11-29 01:09:23.796000	50	free	None	None	1011	New Haven-Milford, CT	"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"	50	Ava	Robinson	F	free</code>
    
    
</p>


---