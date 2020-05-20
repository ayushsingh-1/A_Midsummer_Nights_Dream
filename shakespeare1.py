from pymongo import MongoClient
import re
import pprint
import cProfile

client=MongoClient()
db=client.learning_mongo
shakespeare=db.shakespeare

#Preprocessing: Readlines as array, Strip White spaces
with open("characters.txt") as charfile:
    characters=charfile.readlines()
    characters=[x.strip() for x in characters]
    # Test:
    # print("Characters: ",characters) 

with open("A_Midsummer_Nights_Dream.txt") as files:
    lines=files.readlines()
    lines=[x.strip() for x in lines]
    # Test:
    # print("Lines: ",lines)

#Drop Collection
def deleteShakespeare():
    shakespeare.drop()
    print("Shakespeare Collection has been dropped!")

#Creating all lines in the MongoDB: Inserting LineNumber, Speaker Name and the Line itself
def createLines():
    count=0
    speaker=""
    for line in lines:
        count=count+1
        # print("Count :",count)
        # print("Speaker :",speaker)
        # print("Line :",line)
        if line in characters:
            speaker=line
            continue
        elif speaker=="":
            continue
        else:
            print("\n")
            print("Count :",count)
            print("Speaker :",speaker)
            print("Line :",line)
            pipeline={"lineNumber": count, "speaker": speaker, "line": line}
            shakespeare.insert_one(pipeline)
    print("Creating Lines....Done!")


#Find all characters, Convert to propercase and update lines in the shakespeare collection
def updateLines():
    for character in characters:
        characterName=character.lower().capitalize()
        print("\n\n\nUppercase name of Character: ",characterName,"\n\n\n")
        for record in shakespeare.find({"line":{"$regex":characterName}}):
            # Test:
            printLine=shakespeare.find_one({"_id":record["_id"]},{"_id":0,"line":1})
            print("\nLine being replaced: ",printLine)

            newLine=record["line"].replace(characterName,character)
            shakespeare.update_one({"_id":record["_id"]},{"$set":{"line":newLine}})
            
            # Test:
            print("Character being replaced: ",characterName)
            printLine=shakespeare.find_one({"_id":record["_id"]},{"_id":0,"line":1})
            print("New Line: ",printLine)
            
#Delete all stage directions and the lines that start with them.
def deleteLines():
    stringMatch="^Enter|^Exit|^Exeunt|^Act|^ACT|^SCENE|^Scene" 

    # Print Method 1: Takes more time probably since there are twice the number of mongo commands and a for loop.
    for record in shakespeare.find({"line":{"$regex":stringMatch}}):
        i=shakespeare.find_one({"_id":record["_id"]},{"_id":0, "line":1})
        print("Line being removed: ",i) 

    # Print Method 2: One Mongo command and one for loop.
    #deletes=shakespeare.find({"line":{"$regex":stringMatch}},{"_id":0, "line":1}) 
    # Deletes will now have multiple documents, so to print each one, do a for loop
    #for i in deletes:
    #    print("Line being deleted: ",i)
    
    shakespeare.delete_many({"line":{"$regex":stringMatch}})

#Sort by line number and display
def displayLines():
    display=shakespeare.find({},{"_id":0,"lineNumber":1,"line":1}).sort([("lineNumber",1)])
    #Display will now have multiple documents, so to print each one, do a for loop
    for i in display:
        print(i)

#Another ending to execute could have been:
# Main function
# if __name__ == "__main__":
#     deleteShakespeare()
#     createLines()
#     updateLines()
#     deleteLines()
#     displayLines()

#Envelope function
def CRUD():
    deleteShakespeare()
    createLines()
    updateLines()
    deleteLines()
    displayLines()

# Main function
if __name__ == "__main__":
    cProfile.run("CRUD()")
    #Gives us execution time info for each function

