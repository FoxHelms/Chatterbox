import psycopg2
import os

try:
    # Establish connection
    conn = psycopg2.connect(
        host="localhost",
	port=5432,
        database="postgres",
        user="postgres",
    )
    
    # Create a cursor object
    cur = conn.cursor()
    
    # Execute a query
    cur.execute("SELECT version();")
    
    # Fetch results
    db_version = cur.fetchone()
    print(f"PostgreSQL database version: {db_version}")
    
    # Close cursor and connection
    # cur.close()
    # conn.close()

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")

create_table_sql = """
	CREATE TABLE IF NOT EXISTS test_memes (
		id SERIAL PRIMARY KEY,
		name TEXT UNIQUE NOT NULL,
		image_path TEXT UNIQUE NOT NULL, 
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	"""


# write_image_sql = f'INSERT INTO memes (, image_path) VALUES ({}, {});'

cur.execute('DROP TABLE memes')
cur.execute(create_table_sql)

for img in test_imgs:
	temp_subdir = f'{test_subdir}/{img}'
	write_sql = f"INSERT INTO test_memes (name, image_path) VALUES ( '{img}' , '{temp_subdir}' );"
	cur.execute(write_sql)


conn.commit()

cur.close()
conn.close()
