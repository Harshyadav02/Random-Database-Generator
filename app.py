from flask import Flask, render_template, request, redirect, url_for, send_file
import psycopg2
from faker import Faker
import random
import time
from all_functions import create_table                      # def create_table(column_detail, table_name)
from all_functions import generate_fake_data                # def generate_fake_data(column_name, data_type):
from all_functions import generagte_insert_query            # def generate_schema_sql(db_name)
# from all_functions import generate_schema_sql

# Initialize the Faker instance
fake = Faker()

# Define your MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'root',
    'dbname': 'postgres',
    'port': 5432
}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# this function will be triggered by index.html
@app.route('/create_tables/', methods=['POST'])
def create_tables():
    global db_name 
    db_name  = request.form['dbName']
    num_tables = int(request.form['numTables'])
    return render_template('table.html', db_name=db_name, num_tables=num_tables)



@app.route('/submit_table_details/<db_name>/<int:num_tables>/', methods=['POST'])
def table_details(db_name, num_tables):

    table_name_list = request.form.getlist('tableName')
    column_details_list = request.form.getlist('columnDetails')

    messages = []

    connection = psycopg2.connect(**db_config)
    # Set autocommit mode to True
    connection.autocommit = True
    cursor = connection.cursor()

    # Check if the database already exists
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()

    # Create database if not exists
    if not exists:
        cursor.execute(f"CREATE DATABASE {db_name}")
    
    # Close the cursor and connection to commit the database creation outside of the transaction
    cursor.close()
    connection.close()

     # Reset autocommit mode to False
    # connection.autocommit = False

    # Reconnect to the newly created database
    connection = psycopg2.connect(
        database=db_name,
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )

    cursor = connection.cursor()

    # Iterate through the provided table names and column details
    num = 1
    for table_name, column_details in zip(table_name_list, column_details_list):
        create_query = create_table(column_details, table_name)
        
        try:

            cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_name LIKE '{table_name}' ")
            existing_table = cursor.fetchone()

            if existing_table:
                existing_table = existing_table[0]
                messages.append( (f'Table {num}', table_name, 'Table already exists.') )
                num += 1

            else:
                
                # Execute the create table query
                cursor.execute(create_query)
                connection.commit()
                messages.append( (f'Table {num}', table_name, 'Table created successfully') )
                num += 1

                try:
                    for entry in range(5):
                        insert_query = generagte_insert_query(table_name, column_details, db_name)
                        cursor.execute(insert_query)
                        connection.commit()

                except psycopg2.Error as err:
                    messages.append( (f'Table Name : ', f'{table_name} insertion error', err) )


        except psycopg2.Error as err:
            # Rollback the transaction on exception
            connection.rollback()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            messages.append( (f'Table {num}', f'{table_name} creation error', err) )
            num += 1
    
    time.sleep(2)
    cursor.close()
    connection.close()

    total = 0
    for message in messages:
        if message[2]=='Table created successfully' or message[2]=='Table already exists.':
            total += 1

    return render_template('output.html', messages=messages, total= total, num_tables=num_tables, db_name=db_name )


if __name__ == '__main__':
    app.run(debug=True)

# # lokesh@notebook:~$ psql
# psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  role "lokesh" does not exist