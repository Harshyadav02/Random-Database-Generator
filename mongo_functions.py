from decimal import Decimal                     # class for decimal conversion 
from faker import Faker                         # class for fake data 
from mongo_app import client                    # instance of MongoClient class to use mongodb
import random                                   # to genrate random number 

# making Faker class instance 
fake = Faker()

# function to create a database in MongoDB
def create_database(database) :

    db = client[database]
    return db

 
# Function to create collection in each database 
def create_collection(collection_name, database):
    
    collection = database[collection_name]
    return collection
    
#----------------------------------------------------------------------S

# function to generate fake data for int datatype
def int_fake_data(key, json_data):
    

    # Generate a random integer within the specified range
    random_int = fake.random_int(9)

    if ( 'phone_number' in key or 'contact' in key or 'telephone' in key ):
        json_data[key]  = random_int
        return json_data
    
    elif ('id' in key):
        json_data[key]  = random_int        
        return json_data
    
    elif ('age' in key):
        json_data[key]  = random_int
        return json_data
    
    else:
        json_data[key]  = random_int()
        return json_data
   

# function to generate fake data for long datatype
def long_fake_data(key,json_data):

    

    # Generate a random Long within the specified range
    random_Long = fake.random_int(10)
    if ('phone_number' in key or 'contact' in key or 'telephone' in key) :
        json_data[key]  = random_Long
        return json_data 
    else :
        json_data[key] = random_Long
        return json_data



# function to generate fake data string datatype
def string_fake_data(key, json_data):


    if ('first_name' in key or 'f_name' in key):
        
        json_data[key] = fake.first_name()
        return json_data 
    
    elif ('last_name' in key or 'l_name' in key):
        
        json_data[key] = fake.last_name()
        return json_data
    
    elif ('email' in key or 'mail' in key):
        
        json_data[key] = fake.email()
        
        return json_data
    
    elif ('address' in key):
        
        json_data[key] = fake.address()
        return json_data 
    
    elif ('city' in key):
        
        json_data[key] =  fake.city()
        return json_data 
    
    elif ('country' in key):
        
        json_data[key] = fake.country()
        return json_data  
    
    elif ( 'password' in key ):
        
        json_data[key] =  fake.password()
        return json_data
    
    elif ( 'language' in key ):
        
        json_data[key] = fake.language_name()
        return json_data
    
    elif ('post' in key or 'postal' in key):
        
        json_data[key] =   fake.postalcode()
        return json_data
    
    elif ( 'state' in key ):
        
        json_data[key] =  fake.state()
        return json_data
    
    elif ('color' in key or 'colour' in key):
        
        json_data[key] =  fake.color_name()
        return json_data
    
    elif ( 'name' in key ):
        
        json_data[key] = fake.name()
        return json_data
    
    
    elif ( 'gender' in key.lower() ):
        
       json_data[key] =  fake.random_element(elements=('male', 'female'))
       return json_data        
    else:
    
        
        json_data[key] = fake.text(10)
        return json_data

# function to genrate fake data form array datatype

def array_fake_data(key,json_data) :
    
    json_data[key] = fake.pylist()
    return json_data
        
    
# function to genrate fake data form object datatype
def object_fake_data(key , json_data) :

    json_data[key] = fake.pydict()
    return json_data

# function to generate fake data for decimal data type

def decimal_fake_data(key ,json_data) :
    random_decimal = Decimal(fake.pydecimal(left_digits=13, right_digits=10, positive=True))
    json_data[key] = str(f"{random_decimal}")

# function to generate fake data for Null datatype
def null_fake_data(key,json_data) :

    json_data[key] = 'None'
    return json_data 




# Function to generate fake data based on data type
def generate_fake_data(key, data_type,json_data):
    data_type = data_type.strip().lower()
    

    if 'string' in data_type:
        string_json_data = string_fake_data(key, json_data)
        
        return string_json_data
    
    if 'bool' in data_type or 'boolean' in data_type:
        
        json_data[key] = fake.random_element(elements=(True, False))
        return  json_data
    
    if 'long' in data_type:
        
        long_json_data  =  long_fake_data(key,json_data)
        return long_json_data
    
    if 'int' in data_type or 'numeric' in data_type or 'Int32' in data_type:
        int_json_data = int_fake_data(key,json_data)
        return int_json_data
    
    if 'date' in data_type :
        
        json_data[key] =  f"{str(random.randint(1900, 2023)).zfill(4)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}"  
        return json_data
       
        # zfill() ensure leading zero for months, year , day
    if 'array' in data_type :
        array_data = array_fake_data(key, json_data) 
        return array_data
    
    if 'object' in data_type :
        object_data = object_fake_data(key, json_data)
        return object_data

    if 'decimal' in data_type or 'decimal128' in data_type: 
        decimal_data = decimal_fake_data(key, json_data)
        return decimal_data
    
    if 'Null' in data_type or 'None' in data_type :
        null_data = null_fake_data(key,json_data)
        return null_data


# function which split the key and data type and send it to genrate_fake_data function  

def data_split(key_details_list , json_data):
    #  list to hold the key details for each collections
    key_list = []
    
    #  splitting each keys details 
    for key in key_details_list: 
        key_list.append(key.split(','))   # [['name:string', 'id:int', 'age:int'], ['email:email', 'number:int']]
    
    
    #  list to hold the data and and its data type 
    key_and_data_type = []

    # spliting the key and data type by (:)
    for row in key_list :
        list = []
        for col in row :
        
            list.append(col.split(":")) 
        key_and_data_type.append(list) 
    

    # retriving key and data type and sending to generate_fake_data function 
    for i in range(0, len(key_and_data_type)):
        for j in range(0, len(key_and_data_type[i])):
            key = key_and_data_type[i][j][0]
            data_type = key_and_data_type[i][j][1]
            
            generate_fake_data(key.lower().strip(),data_type.lower(),json_data)
           
        
    # returning a json data which will be stored in the collection as a document        
    return json_data