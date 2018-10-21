from pymongo import MongoClient
from bson.objectid import ObjectId

def connectDB(coll = "NASA"):
    try:
        #Create the auth client in mlab
        client = MongoClient('mongodb://Master:asJGa876@ds227119.mlab.com:27119/desafioestagio')
        #Select the database we want to use
        db = client.desafioestagio
        #Return the desired collection
        coll = 'NASA'

    except:
        print ("Error trying to connect to database")


#Receive a document and insert in the database
def dbinsert(DocumentoInserir):
    try:
        collection = connectDB('NASA')
        #Insert the document and print the id
        doc_id = collection.insert_one(DocumentoInserir).inserted_id
        print(doc_id)
    except:
        print("Error trying to write to database")

def dbretrieve():
    try:
        collection = connectDB('NASA')

        lista_de_posts = []
        for post in collection.find().sort("dataPost", -1).limit(10):
            lista_de_posts.append(post)
        return lista_de_posts
    except:
        print("Error when retrieving from database")

def dbretrievepost(_postId):
    try:
        collection = connectDB('NASA')
        post = collection.find_one({"_id": ObjectId(_postId)})
        return post
    except:
        print("error when retrieving the post")

def removepost(_postId):
    try:
        collection = connectDB('NASA')
        collection.remove({"_id": ObjectId(_postId)})
    except:
        print("error when deleting post")

def updatepost(_postId):
    try:
        collection = connectDB('NASA')
        collection.update_one({"_id": ObjectId(_postId)})
    except:
        print("error to update post")

def dbretrievecategoria(_categoria="batata"):
    try:
        collection = connectDB('NASA')
        listadeposts = []
        for post in collection.find({"categoriaPost": {"$regex": _categoria}}):
            listadeposts.append(post)
        return listadeposts
    except:
        print("error retrieving categorie")

def dbinsertusuario(usuarioainserir):
    try:
        collection = connectDB('users')
        #Insere o documento na collection e retorna o id
        print(usuarioainserir)
        doc_id = collection.insert_one(usuarioainserir).inserted_id
        print(doc_id)
    except:
        print("error writing to database")

def dbretrieveusuario(usuario):
    try:
        collection = connectDB('users')
        user = collection.find_one({"username": usuario })
        return user
    except:
        print("error retrieving user from database")

def dbretrieveusers():
    try:
        collection = connectDB('users')

        lista_de_users = []
        for user in collection.find().sort("username", 1):
            lista_de_users.append(user)
        return lista_de_users
    except:
        print("Error when retrieving from database")

def removeuser(_userId):
    try:
        collection = connectDB('users')
        collection.remove({"_id": ObjectId(_userId)})
    except:
        print("error when deleting user")

def dblogaction(loginformation):
    try:
        collection = connectDB('logs')
        collection.insert_one(loginformation)
    except Exception as e:
        print(e)
        print("error when registering log")