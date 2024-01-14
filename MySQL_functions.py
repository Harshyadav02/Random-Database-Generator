from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from faker import Faker
import random
from config import db_config


# Initialize the Faker instance
fake = Faker()


# app = Flask(__name__)

#---------------------------------------------------

#  function for creating a table
def create_table(column_detail, table_name):

    # splitting column_detail by ","   
    column_list = column_detail.split(",")
    
    # list to store the column details after splitting by ":"
    column_detail_list = []
    
    # splitting each column by ":" and storing in column_detail_list
    for column in column_list:
        s = column.split(":")
        column_detail_list.append(s)
    
    # MySQL create table query 
    query = f"create table {table_name} ("
       
    # iterating through the list of column details 
    for column_info in column_detail_list:

        # iterating through the inner list
        for detail in column_info:
            query += f" {detail}"
        if column_info != column_detail_list[-1]:
            query += " , "
    
    # ending part of query
    query += ");"

    # returning the MySQL create table query
    return query

#-----------------------------------------------------

#  function to generate schema and for download that
def generate_schema_sql(db_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Select the database
        cursor.execute(f"USE {db_name}")

        # Get the list of tables in the database
        cursor.execute("SHOW TABLES")
        tables = [table_details[0] for table_details in cursor.fetchall()]

        schema_sql = ''' '''
        for table_name in tables:

            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_query = cursor.fetchone()[1]

            schema_sql += f"\n\n-- Table: {table_name}\n"
            schema_sql += f"{create_query}\n;"

    except mysql.connector.Error as err:
        return f"Error: {err}"

    finally:
        cursor.close()
        connection.close()

    return schema_sql

#----------------------------------------------------------------------------------------------------------
# function to generate fake data for int datatype
def int_fake_data(column_name):

    if ( 'phone_number' in column_name or 'contact' in column_name or 'telephone' in column_name ):
        return fake.random_number(9)
    
    elif ('id' in column_name):
        return fake.random_number()
    
    elif ('age' in column_name):
        return fake.random_number(3)
    
    else:
        return fake.random_int()
    
#----------------------------------------------------------------------------------------------------------

# function to generate fake data for bigint datatype
def bigint_fake_data(column_name):

    if ('phone_number' in column_name or 'contact' in column_name or 'telephone' in column_name) :
        return fake.random_number(10) 
    else :
        return fake.random_int()


# function to generate fake data for for varchar and char datatype
def varchar_char_fake_data(column_name, data_type):

    if 'varchar' in data_type:
        max_length = int(data_type.replace('varchar', '').strip('()'))

    elif 'char' in data_type:
        try:
            max_length = int(data_type.replace('char', '').strip('()'))
        except:
            max_length = 1



    if ('first_name' in column_name or 'f_name' in column_name):
        fake_fname = fake.first_name()
        if len(fake_fname) > max_length:
            fake_fname = fake_fname[:max_length]
        return fake_fname
    
    elif ('last_name' in column_name or 'l_name' in column_name):
        fake_lname = fake.last_name()
        if len(fake_lname) > max_length:
            fake_lname = fake_lname[:max_length]
        return fake_lname
    
    elif ('email' in column_name or 'mail' in column_name):
        fake_email = fake.email()
        if len(fake_email) > max_length:
            fake_email = fake_email[:max_length]
        return fake_email
    
    elif ('address' in column_name):
        fake_add = fake.address()
        if len(fake_add) > max_length:
            fake_add = fake_add[:max_length]
        return fake_add
    
    elif ('city' in column_name):
        fake_city = fake.city()
        if len(fake_city) > max_length:
            fake_city = fake_city[:max_length]
        return fake_city
    
    elif ('country' in column_name):
        fake_country = fake.country()
        if len(fake_country) > max_length:
            fake_country = fake_country[:max_length]
        return fake_country
    
    elif ('phone_number' in column_name or 'contact'  in column_name):
        return f"{fake.random_number(10)}"
    
    elif ( 'password' in column_name ):
        fake_pass = fake.password()
        if len(fake_pass) > max_length:
            fake_pass = fake_pass[:max_length]
        return fake_pass
    
    elif ( 'language' in column_name ):
        fake_lang = fake.language_name()
        if len(fake_lang) > max_length:
            fake_lang = fake_lang[:max_length]
        return fake_lang
    
    elif ('post' in column_name or 'postal' in column_name):
        fake_postal = fake.postalcode()
        if len(fake_postal) > max_length:
            fake_postal = fake_postal[:max_length]
        return fake_postal
    
    elif ( 'state' in column_name ):
        fake_state = fake.state()
        if len(fake_state) > max_length:
            fake_state = fake_state[:max_length]
        return fake_state
    
    elif ('color' in column_name or 'colour' in column_name):
        fake_color = fake.color_name()
        if len(fake_color) > max_length:
            fake_color = fake_color[:max_length]
        return fake_color
    
    elif ( 'name' in column_name ):
        fake_name = fake.name()
        if len(fake_name) > max_length:
            fake_name = fake_name[:max_length]
        return fake_name
    
    elif ( 'id' in column_name ):
        fake_id = f"{fake.random_number()}"
        if len(fake_id) > max_length:
            fake_id = fake_id[:max_length]
        return fake_id
    
    elif ( 'gender' in column_name.lower() ):
        if max_length > 5:
            return fake.random_element(elements=('male', 'female'))
        else:
            return fake.random_element(elements=('M', 'F'))
        
    else:
    
        if max_length <= 6:
            fake_txt = fake.word()[:max_length]
        elif max_length > 6:
                fake_txt = fake.text(max_length)
        return fake_txt
#----------------------------------------------------------------------------------------------------------

# Function to generate fake data based on data type
def generate_fake_data(column_name, data_type):
    data_type = data_type.strip().lower()
    column_name = column_name.strip().lower()


    if 'varcahr' in data_type or 'char' in data_type:
        return varchar_char_fake_data(column_name, data_type)

    if 'bool' in data_type or 'boolean' in data_type:
        return fake.random_number(2)
    
    if 'bigint' in data_type:
        return bigint_fake_data(column_name)

    if 'int' in data_type:
        return int_fake_data(column_name)

    if 'date' in data_type :
        return f"{str(random.randint(1900, 2023)).zfill(4)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}"  
        # zfill() ensure leading zero for months, year , day

#----------------------------------------------------------------------------------------------------------


# to handle foreign keys.
def finding_foreign_key(column_detail_list):

    column_detail_list = column_detail_list.split(',')

    temp_fk = [column for column in column_detail_list if 'foreign' in column.lower() ]

    temp_detail = []
    f_k_details = ''

    for details in temp_fk:

        f_k_details = details
        f_k_details = f_k_details.replace( '(' , "")
        f_k_details = f_k_details.replace( ')' , "")
        f_k_details = f_k_details.split()
        temp_detail.append(f_k_details)

    foreign_key = [ [], [], [] ]    # columns name which are foreign key, table name has primary key, column name which are primary key   


    for foreign_key_detail in temp_detail:
        foreign_key[0].append(foreign_key_detail[2].strip())
        foreign_key[1].append(foreign_key_detail[4].strip())
        foreign_key[2].append(foreign_key_detail[5].strip())

    return foreign_key
#---------------------------------------------------------------------------


# function to generate insert query for generated table.
def generagte_insert_query(table_name, col_details,db_name):
    
    # Extract foreign key details.
    foreign_key = finding_foreign_key(col_details)
    print(foreign_key)

    # Split col_details by ","
    column_list =  col_details.split(",")
    column_list = [table_details for table_details in column_list if 'foreign' not in table_details.lower()]
   
    column_details_list = []
    
    for column in column_list:
        s = column.split(":")
        column_details_list.append(s)
    
    
    columns_info = [ ]
    for col_info in column_details_list:

        if (len(col_info) > 2) and (col_info[2].lower().strip() == 'primary key' or col_info[2].lower().strip() == 'unique' ):
            columns_info.append([col_info[0].strip(),  col_info[1].strip(),  col_info[2].strip() ])
        else:
            columns_info.append([col_info[0].strip()  , col_info[1].strip() ])
    print(columns_info)

    
    # Generate fake data for each column and print as comma-separated values
    fake_data = []
    for col_info in columns_info:                 # [['name', 'char(23)', 'primary key'], [' dob', 'date'], [' id', 'int'], [' city', 'varchar()']]
        

        if col_info[0].strip() in foreign_key[0]:
            print('foreign key')

            index = foreign_key[0].index(col_info[0].strip())


            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()



                cursor.execute(f"USE {db_name}")
                cursor.execute(f"select {foreign_key[2][index]} from {foreign_key[1][index]}")
                all_fk_value = cursor.fetchall()
                
                all_data = [ data[0] for data in all_fk_value ]
                # print(all_data)

                fake_data.append(fake.random_element(elements=all_data))

            except mysql.connector.Error as err:
                print(err)
                pass

            finally:
                cursor.close()
                connection.close()
        

        elif (len(col_info) > 2) and (col_info[2].lower() == 'primary key' or col_info[2].lower() == 'unique' ):
            
            print("primary key")
            
            column_name = col_info[0]
            data_type = col_info[1]

            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                cursor.execute(f"USE {db_name}")
                cursor.execute(f"select {column_name} from {table_name}")
                result = cursor.fetchall()


                # finding all values from table of primary key.
                all_value = [ value[0] for value in result ]
                # print(all_value)


                real_data = generate_fake_data(column_name, data_type)

                
                while(True):
                    if real_data not in all_value:
                        fake_data.append(real_data)
                        # print(real_data)
                        break
                    else:
                        print('find duplicate: ', real_data)
                        real_data = generate_fake_data(column_name, data_type)

            except mysql.connector.Error as err:
                print(err)
                pass

            finally:
                cursor.close()
                connection.close()

        else:
            print('normal')
            column_name = col_info[0]
            data_type = col_info[1]
            fake_data.append(generate_fake_data(column_name, data_type))
    



    # Print the generated fake data as comma-separated values
    if len(fake_data)==1:
        if type(fake_data[0]) == str:
            insert_query = f"insert into {table_name} values ('{fake_data[0]}') ;"
            print(insert_query)
            return insert_query
        else:
            insert_query = f"insert into {table_name} values ({fake_data[0]}) ;"
            print(insert_query)
            return insert_query
    else:
        fake_data = tuple(fake_data)
        insert_query = f"insert into {table_name} values {fake_data} ;"
        print(insert_query)
        return insert_query
