# Starting necessary service and connecting to the DB.


import psycopg

def get_db_connection():
    connection = psycopg.connect(
        host="localhost",
        dbname="serviceops",
        user="postgres",
        password="1A2l3a4e$",
        port=5433
    )

    # Return the connection to the route that requested it.
    return connection