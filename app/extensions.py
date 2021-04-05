from flask_pymongo import PyMongo
from pymongo import MongoClient
# Setup MongoDB here
mongo = MongoClient("mongodb+srv://shivang:Dewang123@cluster0.kme6n.mongodb.net/webhook?retryWrites=true&w=majority")

db = mongo.webhook
