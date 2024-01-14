from pymongo import MongoClient                 # class to intract to mongodb 


#  Mysql configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root'
}


#  MongoDb configuration 
client = MongoClient("mongodb://127.0.0.1:27017")
