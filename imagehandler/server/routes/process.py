# Routes File
from fastapi import APIRouter, Body, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional, Set

from ..database import (
    add_image,
    delete_image,
    retrieve_image,
    retrieve_images,
    update_image,
)
from ..models.image import (
    ErrorResponseModel,
    ResponseModel,
    ImageSchema,
    UpdateImageModel,
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")
router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory = "imagehandler/templates")

@router.get("/", response_description="List all images")

async def retrieve_images_all():
    
    images = await retrieve_images()
    return ResponseModel(images, "All Images listed successfully.")

@router.get(
    "/imagelist/{id}", response_description="Get a single image"
)
async def show_image(id: str):
    image = await retrieve_image(id)
    return ResponseModel(image, "Image listed successfully.")
   
@router.post("/", response_description="Image data added into the database")
async def add_Image_data(image: ImageSchema = Body(...)):
    image = jsonable_encoder(image)
    new_image = await add_image(image)
    return ResponseModel(new_image, "Image added successfully.")

@router.delete("delete/{id}", response_description="Delete an image")
async def deleteimage(id: str):
    delete_result = await delete_image(id)
    return ResponseModel(delete_result, "Image Deleted successfully.")

@router.put("update/{id}", response_description="Update a image")
async def update_student(id: str, image: UpdateImageModel = Body(...)):
    
    student = {k: v for k, v in image.dict().items() if v is not None}
    update_result = update_image(id, student)
    if update_result == 1:
        return(update_result, "update succeed")
    else:   
        return(update_result, "updating failed")


@router.post("/uploadfiles/", response_description="Image uploaded and data added into the database")
async def create_upload_files(files: List[UploadFile] = File(...)):
    file_names = []
    file_paths = []
    images =[]
    for file in files:
        file_name = file.filename
        file_names.append(file_name)
        file_path = f"static/images/" + file_name
        file_paths.append(file_path)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
           
    i = 0
    for file in files:
        if i == 0:
            cofile_name = file_names[1] 
            cofile_path = file_paths[1]
        else:
            cofile_name = file_names[0] 
            cofile_path = file_paths[0]
        image = {
            "filename": file.filename,
            "filetype": "image/jpeg",
            "filesize": 201645,
            "file_path": file_path,
            "cofile_name": cofile_name,
            "cofile_path": cofile_path,
            }
             
        image = jsonable_encoder(image)
        new_image = await add_image(image)
        images.append(new_image)
        
        i =+ 1
    print(images)   
    return ResponseModel(images, "Images added successfully.")   
        
    
@router.get("/upload")
async def main(request: Request):
    return templates.TemplateResponse('form.html', {"request": request})
    