from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ImageSchema(BaseModel):
    
    filename: str = Field(...)
    filetype: str = Field(...)
    filesize: int = Field(..., gt=0)
    file_path: str = Field(...)
    cofile_name: str = Field(...) 
    cofile_path: str = Field(...)   
    class Config:
        schema_extra = {
            "example": {
                "filename": "Photo1.jpg",
                "filetype": "image/jpg",
                "filesize": 56872012,
                "file_path": "static/images/Photo1.jpg",
                "cofile_name": "Photo2.jpg",
                "cofile_path": "static/images/Photo1.jpg",
            }
        }

class UpdateImageModel(BaseModel):
    filename: Optional[str]
    filetype: Optional[str]
    filesize: Optional[str]
    file_path: Optional[str]
    cofile_name: Optional[str] 
    cofile_path: Optional[str]
    class Config:
        schema_extra = {
            "example": {
                "filename": "Photo1.jpg",
                "filetype": "image/jpg",
                "filesize": 56872012,
                "file_path": "static/images/Photo1.jpg",
                "cofile_name": "Photo2.jpg",
                "cofile_path": "static/images/Photo1.jpg",
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}