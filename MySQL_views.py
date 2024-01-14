from flask import  render_template, request, send_file ,Blueprint
import mysql.connector
from MySQL_functions import create_table                      # def create_table(column_detail, table_name)
from MySQL_functions import generate_fake_data                # def generate_fake_data(column_name, data_type):
from MySQL_functions import generagte_insert_query            # def generate_schema_sql(db_name)
from MySQL_functions import generate_schema_sql
from config import db_config


mysql_db = Blueprint('mysql_db', __name__)


# this function will be triggered by index.html
@mysql_db.route('/create_tables/', methods=['POST'])
def create_tables():
    global db_name 
    db_name  = request.form['dbName']
    num_tables = int(request.form['numTables'])
    return render_template('Mysql/table.html', db_name=db_name, num_tables=num_tables)



@mysql_db.route('/submit_table_details/<db_name>/<int:num_tables>/', methods=['POST'])
def table_details(db_name, num_tables):

    table_name_list = request.form.getlist('tableName')
    column_details_list = request.form.getlist('columnDetails')

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
        
        try:

            cursor.execute(f"SHOW TABLES LIKE '{table_name}' ")
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

                except mysql.connector.Error as err:
                    messages.append( (f'Table Name : ', f'{table_name} insertion error', err) )


        except mysql.connector.Error as err:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
            messages.append( (f'Table {num}', f'{table_name} creation error', err) )
            num += 1
    
    cursor.close()
    connection.close()

    total = 0
    for message in messages:
        if message[2]=='Table created successfully' or message[2]=='Table already exists.':
            total += 1

    return render_template('Mysql/output.html', messages=messages, total= total, num_tables=num_tables, db_name=db_name )



#  to download the schema file
@mysql_db.route("/download_schema/<db_name>", methods=['GET','POST'])
def download_schema(db_name):

    if request.method == 'POST':

        schema_sql = generate_schema_sql(db_name)

        # Save the SQL to a file
        file_path = f"{db_name}_schema.sql"
        with open(file_path, 'w') as file:
            file.write(schema_sql)

        # Provide the file for download
        return send_file(file_path, as_attachment=True) # If set to True, the file will be sent as an attachment
