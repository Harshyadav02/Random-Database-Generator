import json
from flask import Blueprint, jsonify , request , render_template ,send_file
from MongoDB_functions import create_collection   # function to create collection in database
from MongoDB_functions import create_database     # function to create database in database
from MongoDB_functions import data_split          # function to split data into key and data type     
from pymongo.errors import  PyMongoError , DuplicateKeyError
from config import client 
from MongoDB_functions import generate_schema_mongo

# blueprint 
mongo_db = Blueprint('mongo_db',__name__)


@mongo_db.route('/collection_creation/' , methods=['POST'])
def collection_creation():
    # retriving database information from html form
    database = request.form["dbName"]
    print("This is database " ,database)
    # retriev ing number of collections from html form
    number_of_collections = int(request.form['numTables'])

    return render_template('Mongo/table.html', database=database, number_of_collections=number_of_collections)



@mongo_db.route('/submit_collection_details/<mongo_database>/<int:number_of_collections>/', methods=['POST'])
def table_details(mongo_database, number_of_collections):
    # list to hold all the messages 
    messages = []
    errors = [] 
    
    try:

        # retrieving data from html form as list
        collection_list = request.form.getlist('tableName')
        key_details_list = request.form.getlist('columnDetails')

        # database creation
        database = create_database(mongo_database)
        print("Table route database " ,database)
        print("Table route mongo_database " ,mongo_database)

        messages.append("Database Created Successfully")  # messages[0]
        # list to hold the key details for each collection
        
        key_list = []

        # splitting each keys details on the basis of (,)
        for key in key_details_list:
            key_list.append(key.split(','))  # [['name:string', 'id:int', 'age:int'], ['email:email', 'number:int']]

        # creating collections and inserting documnet to each collection 
        for coll in range(len(collection_list)):
            data_type_error = False
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

        return render_template('Mongo/output.html', messages = messages , db = mongo_database)
    
    # Handling runtime errors 
    except DuplicateKeyError as keyerror :
        
        return render_template('Mongo/output.html' ,message = messages , error = keyerror)

    except PyMongoError as mongoError :
        
        return render_template('Mongo/output.html' ,message = messages , error = mongoError)

    except Exception as errors:
        return render_template('Mongo/output.html' ,message = messages , error = errors)


    finally:
        # client.close() 
        pass  

@mongo_db.route('/download_schema/<db_name>/' , methods=['GET', 'POST'])
def download_schema(db_name):
    try:
        db = client[db_name]

        if request.method == 'POST':
            schema_result = generate_schema_mongo(db)

            # Save the schema to a file
            file_path = f"{db_name}_schema.json"
            with open(file_path, 'w') as file:
                json.dump(schema_result,file ,indent=2, default=str)

            # Provide the file for download
            return send_file(file_path, as_attachment=True)

        return "Send a POST request to download the schema."

    except Exception as e:
        return jsonify({"error": f"Error connecting to MongoDB: {e}"}), 500
