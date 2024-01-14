from flask import Flask, render_template
from faker import Faker
from MongoDB_views import mongo_db
from MySQL_views import mysql_db


# Initialize the Faker instance
fake = Faker()


# Initialize the Flask instance
app = Flask(__name__)

app.register_blueprint(mongo_db)
app.register_blueprint(mysql_db)

# Starting route for the project 
@app.route('/' , methods = ['GET' , 'POST'])
def db_choice() :

    return render_template('index.html')

# route for MySQL database 
@app.route('/mysql/' )
def mysql_route() :

    return render_template('Mysql/index.html')

# route for MongoDB database
@app.route('/monogodb/' )
def mongo_route() :

    return render_template('Mongo/index.html')


if __name__ == '__main__':
    
    
    app.run(debug=True)
