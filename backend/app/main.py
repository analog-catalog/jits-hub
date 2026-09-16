from fastapi import FastAPI

from app.routers import classes, users, bookings


app = FastAPI()


app.include_router(classes.router)
app.include_router(users.router)
app.include_router(bookings.router)


@app.get("/")
def root():
    return {"message": "JitsHub API is running"}