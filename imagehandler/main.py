import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["ImageHandler"])
async def read_root():
    return {"message": "Welcome to this Image Handler app!"}

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)