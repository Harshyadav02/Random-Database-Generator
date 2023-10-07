
from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from faker import Faker
import random
from all_functions import create_table                      # def create_table(column_detail, table_name)
from all_functions import generate_fake_data                # def generate_fake_data(column_name, data_type):
from all_functions import generagte_insert_query            # def generate_schema_sql(db_name)
from all_functions import generate_schema_sql

# Initialize the Faker instance
fake = Faker()

# Define your MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9644'
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

    # print(table_name_list)
    # print(column_details_list)

    messages = []

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")


    # Iterate through the provided table names and column details
    num = 1
    for table_name, column_details in zip(table_name_list, column_details_list):
        create_query = create_table(column_details, table_name)
        print(create_query)
        


        try:

            cursor.execute(f"SHOW TABLES LIKE '{table_name}' ")
            existing_table = cursor.fetchone()

            # print(existing_table)

            if existing_table:
                existing_table = existing_table[0]
                messages.append( (f'Table {num}', table_name, 'Table already exists.') )
                num += 1
                # print(existing_table)
                # print(messages)
            else:
                
                # Execute the create table query
                cursor.execute(create_query)
                connection.commit()
                messages.append( (f'Table {num}', table_name, 'Table created successfully') )
                num += 1

                try:
                    for i in range(100):
                        insert_query = generagte_insert_query(table_name, column_details, db_name)
                        cursor.execute(insert_query)
                        # print(insert_query)
                        connection.commit()

                except mysql.connector.Error as err:
                    messages.append( (f'Table Name : ', f'{table_name} insertion error', err) )


        except mysql.connector.Error as err:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            messages.append( (f'Table {num}', f'{table_name} creation error', err) )
            num += 1
    
    cursor.close()
    connection.close()

    total = 0
    for i in messages:
        if i[2]=='Table created successfully' or i[2]=='Table already exists.':
            total += 1

    return render_template('output.html', messages=messages, total= total, num_tables=num_tables, db_name=db_name )



#  to download the schema file
@app.route("/download_schema/<db_name>", methods=['GET','POST'])
def download_schema(db_name):

    if request.method == 'POST':

        schema_sql = generate_schema_sql(db_name)

        # print(schema_sql)

        # Save the SQL to a file
        file_path = f"{db_name}_schema.sql"
        with open(file_path, 'w') as file:
            file.write(schema_sql)

        # Provide the file for download
        return send_file(file_path, as_attachment=True) # If set to True, the file will be sent as an attachment


if __name__ == '__main__':
    app.run(debug=True)
