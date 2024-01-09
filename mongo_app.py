from flask import Flask, render_template        
from pymongo import MongoClient                 # class to intract to mongodb 

# database connection for MongoDB 
client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000")


def create_app():
    app = Flask(__name__)

    @app.route("/") 
    def index():
        return render_template("Mongo/index.html")

    # Move the import statement here
    from mongo_views import db_app
    app.register_blueprint(db_app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
