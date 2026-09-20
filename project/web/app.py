from fastapi import FastAPI
from starlette.responses import FileResponse
import bus

app = FastAPI()
bus.start()

@app.get("/")
def index():
    return FileResponse('index.html')

@app.get("/state")
def state():
    return bus.last_values