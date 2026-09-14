from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "JitsHub API is running"}