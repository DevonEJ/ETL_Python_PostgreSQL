import psycopg2
from sql_queries import create_table_queries, drop_table_queries, drop_database, database_create


def create_database():
    """
    Connects to Postgres default database, deletes any existing named sparkifydb database if it exists,
    and then creates a new, empty sparkifydb database.
    
    Closes connection to default database, and creates new connection to sparkifydb created.
    
    Returns:
    cur -- postgres cursor object for sparkifydb
    conn -- postgres connection object for sparkifydb
    
    """
    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    cur.execute(drop_database)
    cur.execute(database_create)

    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Executes and commits a list of SQL queries to drop tables from the sparkifydb Postgres database.
    
    cur -- Postgres cursor object
    conn -- Postgres connection object
    
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Executes and commits a list of SQL queries to create tables in the sparkifydb Postgres database.
    
    cur -- Postgres cursor object
    conn -- Postgres connection object
    
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Creates a Postgres database named sparkifydb, drops tables from the database if they exist
    and then creates tables, before closing the database connection.
    
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()