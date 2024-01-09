from flask import Blueprint , request , render_template
from mongo_functions import create_collection   # function to create collection in database
from mongo_functions import create_database     # function to create database in database
from mongo_functions import data_split          # function to split data into key and data type     
from pymongo.errors import  PyMongoError , DuplicateKeyError
from mongo_app import client
db_app = Blueprint('db_app',__name__)


@db_app.route('/collection_creation/' , methods=['POST'])
def collection_creation():
    # retriving database information from html form
    database = request.form["dbName"]
    
    # retriev ing number of collections from html form
    number_of_collections = int(request.form['numTables'])

    return render_template('Mongo/table.html', database=database, number_of_collections=number_of_collections)



@db_app.route('/submit_collection_details/<database>/<int:number_of_collections>/', methods=['POST'])
def table_details(database, number_of_collections=1):
    # list to hold all the messages 
    messages = [] 
    
    try:

        # retrieving data from html form as list
        collection_list = request.form.getlist('tableName')
        key_details_list = request.form.getlist('columnDetails')

        # database creation
        database = create_database(database)
        messages.append("Database Created Successfully")  # messages[0]
        # list to hold the key details for each collection
        
        key_list = []

        # splitting each keys details on the basis of (,)
        for key in key_details_list:
            key_list.append(key.split(','))  # [['name:string', 'id:int', 'age:int'], ['email:email', 'number:int']]

        # creating collections and inserting documnet to each collection 
        for coll in range(len(collection_list)):
           
            # collection creation
            table = create_collection(collection_list[coll], database)
            messages.append(f"Collection {collection_list[coll]} Created Successfully") 

            # N number of time document  will be inserted to collection
            for time in range(5):
                
                # dictionary to store data for each collection
                collection_data = {}

                for key in range(len(key_list)):
                   
                    entry = data_split(key_list[key], {})
                    # store the entry data in the dictionary for the specific collection
                    collection_data[collection_list[key]] = entry
                
                # insert data into the appropriate collection
                table.insert_one(collection_data[collection_list[coll]])
            messages.append(f"Document inserted Successfully")
        
        return render_template('Mongo/output.html', message = messages)
    
    # Handling runtime errors 
    except DuplicateKeyError as keyerror :
        
        return render_template('Mongo/output.html' ,message = messages , error = keyerror)

    except PyMongoError as mongoError :
        
        return render_template('Mongo/output.html' ,message = messages , error = mongoError)

    except Exception as errors:
        
        return render_template('Mongo/output.html' ,message = messages , error = errors)


    finally:
        client.close() 
        pass  


    

