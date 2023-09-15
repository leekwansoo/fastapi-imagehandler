# Referenced from : https://testdriven.io/blog/fastapi-mongo/ 
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from bson.objectid import ObjectId 

MONGODB_URL = "mongodb+srv://admin:james@cluster0.ujzjm.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(MONGODB_URL)
database = client.image
image_collection = database.get_collection("image_collection")

def image_helper(image) -> dict:
    return {
        "id": str(image["_id"]),
        "filename": image["filename"],
        "filetype": image["filetype"],
        "filesize": image["filesize"],
        "file_path": image["file_path"], 
        "cofile_name": image["cofile_name"], 
        "cofile_path": image["cofile_path"], 
    }
    
# Retrieve all images in the database
async def retrieve_images():
    images = []
    async for image in image_collection.find():
        images.append(image_helper(image))
    return images
 

# Add a new student into to the database
async def add_image(image_data: dict) -> dict:
    image = await image_collection.insert_one(image_data)
    new_image = await image_collection.find_one({"_id": image.inserted_id})
    return image_helper(new_image)


# Retrieve a student with a matching ID
async def retrieve_image(id: str) -> dict:
    image = await image_collection.find_one({"_id": ObjectId(id)})
    if image:
        return image_helper(image)



# Update a student with a matching ID
async def update_image(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    student = await image_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_image = await image_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_image:
            return True
        return False


# Delete a student from the database
async def delete_image(id: str):
    image = await image_collection.find_one({"_id": ObjectId(id)})
    if image:
        await image_collection.delete_one({"_id": ObjectId(id)})
        return True