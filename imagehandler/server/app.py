from fastapi import FastAPI, Body, File, UploadFile
from .routes.image import router as ImageRouter
from .routes.process import router as ProcessRouter
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import List, Optional, Set
import cv2
import os
import shutil

from .database import (
    add_image,
    delete_image,
    retrieve_image,
    retrieve_images,
    update_image,
)
from .models.image import (
    ErrorResponseModel,
    ResponseModel,
    ImageSchema,
    UpdateImageModel,
)


app = FastAPI()

app.include_router(ImageRouter, tags=["IMAGE"], prefix="/image")
app.include_router(ProcessRouter, tags=["PROCESS"], prefix="/process")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

