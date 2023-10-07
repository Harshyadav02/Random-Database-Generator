from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
from faker import Faker
import random


# Initialize the Faker instance
fake = Faker()

# Define your MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '9644'
}

app = Flask(__name__)



#  function for creating a table
def create_table(column_detail, table_name):

    # splitting value by ","   
    str1 = column_detail.split(",")
    

    str2 = []
    
    # splitting value by ":" and storing in str2
    for i in str1:
        s = i.split(":")
        str2.append(s)
    
    # query 
    query = f"create table {table_name} ("
       
    # traversing into list  
    for i in str2:

        #  traversing inner list
        for j in i:
            query += f" {j}"
        if i != str2[-1]:
            query += " , "
    
    # ending part of query
    query += ");"

    # returning the query
    return query



#  function to generate schema and for download that
def generate_schema_sql(db_name):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Select the database
        cursor.execute(f"USE {db_name}")

        # Get the list of tables in the database
        cursor.execute("SHOW TABLES")
        tables = [x[0] for x in cursor.fetchall()]


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



# Function to generate fake data based on data type
def generate_fake_data(column_name, data_type):
    data_type = data_type.strip().lower()
    column_name = column_name.strip().lower()

    # max_length = int


    if 'varchar' in data_type:
        max_length = int(data_type.replace('varchar', '').strip('()'))

    elif 'char' in data_type:
        try:
            max_length = int(data_type.replace('char', '').strip('()'))
        except:
            max_length = 1


    if 'bool' in data_type or 'boolean' in data_type:
        return fake.random_number(2)
    

    if 'bigint' in data_type and ('phone_number' in column_name or 'contact' in column_name or 'telephone' in column_name) :
        return fake.random_number(10) 
    if 'bigint' in data_type:
        return fake.random_int()


    if 'int' in data_type:
        if 'int' in data_type and ('phone_number' in column_name or 'contact' in column_name or 'telephone' in column_name):
            return fake.random_number(9)
        if 'int' in data_type and 'id' in column_name:
            return fake.random_number()
        if 'int' in data_type and 'age' in column_name:
            return fake.random_number(3)
        if 'int' in data_type:
            return fake.random_int()




    if 'varcahr' in data_type or 'char' in data_type:

        if ('varchar' in data_type or 'char' in data_type) and  ('first_name' in column_name or 'f_name' in column_name):
            fake_fname = fake.first_name()

            if len(fake_fname) > max_length:
                fake_fname = fake_fname[:max_length]
            return fake_fname

        if ('varchar' in data_type or 'char' in data_type) and  ('last_name' in column_name or 'l_name' in column_name):
            fake_lname = fake.last_name()

            if len(fake_lname) > max_length:
                fake_lname = fake_lname[:max_length]
            return fake_lname

        if ('varchar' in data_type or 'char' in data_type) and ('email' in column_name or 'mail' in column_name):
            fake_email = fake.email()

            if len(fake_email) > max_length:
                fake_email = fake_email[:max_length]
            return fake_email

        if ('varchar' in data_type or 'char' in data_type) and  'address' in column_name:
            fake_add = fake.address()

            if len(fake_add) > max_length:
                fake_add = fake_add[:max_length]
            return fake_add

        if ('varchar' in data_type or 'char' in data_type) and 'city' in column_name:
            fake_city = fake.city()

            if len(fake_city) > max_length:
                fake_city = fake_city[:max_length]
            return fake_city


        if ('varchar' in data_type or 'char' in data_type) and  'country' in column_name:
            fake_country = fake.country()

            if len(fake_country) > max_length:
                fake_country = fake_country[:max_length]
            return fake_country

        if ('varchar' in data_type or 'char' in data_type) and ('phone_number' in column_name or 'contact'  in column_name):
            return f"{fake.random_number(10)}"

        if ('varchar' in data_type or 'char' in data_type) and  'password' in column_name:
            fake_pass = fake.password()

            if len(fake_pass) > max_length:
                fake_pass = fake_pass[:max_length]
            return fake_pass

        if ('varchar' in data_type or 'char' in data_type) and  'language' in column_name:
            fake_lang = fake.language_name()

            if len(fake_lang) > max_length:
                fake_lang = fake_lang[:max_length]
            return fake_lang

        if ('varchar' in data_type or 'char' in data_type) and ('post' in column_name or 'postal' in column_name):
            fake_postal = fake.postalcode()

            if len(fake_postal) > max_length:
                fake_postal = fake_postal[:max_length]
            return fake_postal


        if ('varchar' in data_type or 'char' in data_type) and 'state' in column_name:
            fake_state = fake.state()

            if len(fake_state) > max_length:
                fake_state = fake_state[:max_length]
            return fake_state

        if ('varchar' in data_type or 'char' in data_type) and ('color' in column_name or 'colour' in column_name):
            fake_color = fake.color_name()

            if len(fake_color) > max_length:
                fake_color = fake_color[:max_length]
            return fake_color

        if ('varchar' in data_type or 'char' in data_type) and 'name' in column_name:
            fake_name = fake.name()

            if len(fake_name) > max_length:
                fake_name = fake_name[:max_length]
            return fake_name



        if ('varchar' in data_type or 'char' in data_type) and  'id' in column_name:
            fake_id = f"{fake.random_number()}"

            if len(fake_id) > max_length:
                fake_id = fake_id[:max_length]
            return fake_id

        if ('varchar' in data_type or 'char' in data_type) and  'gender' in column_name.lower():
            if max_length > 5:
                return fake.random_element(elements=('male', 'female'))
            else:
                return fake.random_element(elements=('M', 'F'))

        if ('varchar' in data_type or 'char' in data_type):
                if max_length <= 6:
                    fake_txt = fake.word()[:max_length]

                elif max_length > 6:
                    fake_txt = fake.text(max_length)

                return fake_txt 




    if 'date' in data_type and ('dob' in column_name.lower() or 'date' in column_name.lower() or 'birth' in column_name.lower()):
        print()
        return f"{str(random.randint(1900, 2023)).zfill(4)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}"   # Ensure leading zero for months, year , day

    elif 'date' in data_type :
        return f"{str(random.randint(1900, 2023)).zfill(4)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}"   # Ensure leading zero for months, year , day



# to handle foreign keys.
def finding_foreign_key(column_detail_list):

    column_detail_list = column_detail_list.split(',')

    temp_fk = [x for x in column_detail_list if 'foreign' in x.lower() ]

    temp_detail = []
    f_k_details = ''

    for i in temp_fk:

        f_k_details = i
        f_k_details = f_k_details.replace( '(' , "")
        f_k_details = f_k_details.replace( ')' , "")
        f_k_details = f_k_details.split()
        temp_detail.append(f_k_details)

    print(temp_detail)

    foreign_key = [ [], [], [] ]    # columns name which are foreign key, table name has primary key, column name which are primary key   


    for i in temp_detail:
        foreign_key[0].append(i[2].strip())
        foreign_key[1].append(i[4].strip())
        foreign_key[2].append(i[5].strip())

    return foreign_key


def generagte_insert_query(table_name, col_details,db_name):
    
    foreign_key = finding_foreign_key(col_details)

    str1 =  col_details.split(",")
    str1 = [x for x in str1 if 'foreign' not in x.lower()]
   
    str2 = []
    for i in str1:
        s = i.split(":")
        str2.append(s)
    print(str2)
    
    
    columns_info = [ ]
    for i in str2:

        if (len(i) > 2) and (i[2].lower().strip() == 'primary key' or i[2].lower().strip() == 'unique' ):
            columns_info.append([i[0].lower().strip(),  i[1].lower().strip(),  i[2].lower().strip() ])
        else:
            columns_info.append([i[0].lower().strip()  , i[1].lower().strip() ])


    
    # Generate fake data for each column and print as comma-separated values
    fake_data = []
    for i in columns_info:                 # [['name', 'char(23)', 'primary key'], [' dob', 'date'], [' id', 'int'], [' city', 'varchar()']]
        

        if i[0].lower().strip() in foreign_key[0]:
            print('fk')

            index = foreign_key[0].index(i[0].lower().strip())


            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()



                cursor.execute(f"USE {db_name}")
                cursor.execute(f"select {foreign_key[2][index]} from {foreign_key[1][index]}")
                all_fk_value = cursor.fetchall()
                
                all_data = [ x[0] for x in all_fk_value ]
                fake_data.append(fake.random_element(elements=all_data))

            except mysql.connector.Error as err:
                print(err)
                pass

            finally:
                cursor.close()
                connection.close()
        

        elif (len(i) > 2) and (i[2].lower() == 'primary key' or i[2].lower() == 'unique' ):
            
            print("hii pk")
            
            column_name = i[0]
            data_type = i[1]

            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                cursor.execute(f"USE {db_name}")
                cursor.execute(f"select {column_name} from {table_name}")
                result = cursor.fetchall()


                # finding all values from table of primary key.
                all_value = [ x[0] for x in result ]


                real_data = generate_fake_data(column_name, data_type)
                print(real_data)
                
                while(True):
                    if real_data not in all_value:
                        fake_data.append(real_data)
                        break
                    else:
                        print('find duplicate: ', real_data)
                        real_data = generate_fake_data(column_name, data_type)

            except:
                pass

            finally:
                cursor.close()
                connection.close()

        else:
            print('normal')
            column_name = i[0]
            data_type = i[1]
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

