import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):
    """ 
    Reads a song data JSON file in given filepath into a dataframe, and inserts relevant data into
    songs and artists database tables.
    
    cur -- Postgres database connection cursor object
    filepath -- absolute path of the relevant file
    
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # insert song record
    song_data = song_data = tuple(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist())
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = tuple(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist())
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Reads a log data JSON file in given filepath into a dataframe, filters for the 
    'NextSong' action, and inserts relevant attributes into time, users and songplays 
    database tables.
    
    cur -- Postgres database connection cursor object
    filepath -- absolute path of the relevant file
    
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df['ts'] = pd.to_datetime(df['ts'], unit='ms') 
    
    # insert time data records
    time_data = ([df['ts'], 
              df['ts'].dt.hour, 
              df['ts'].dt.day, 
              df['ts'].dt.weekofyear, 
              df['ts'].dt.month,
              df['ts'].dt.year, 
              df['ts'].dt.weekday])
    column_labels = (['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday'])
    time_dict = dict((k,v) for (k,v) in zip(column_labels, time_data))
    time_df = pd.DataFrame.from_dict(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts,unit='ms'),row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Locates and iterates over files located in the given filepath, applying a specified function.
    
    cur -- Postgres database connection cursor object
    conn -- Postgres database connection object
    filepath -- Filepath of files to be iterated over
    func -- user specified function to be applied to each file
    
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Connects to sparkifydb database, creates cursor object, and passes this to the process_data
    function, called within, before closing database connection.
    
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()