from fastapi import FastAPI
from typing import Union

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: Union[int, str]):
    return {"item_id": item_id}

@app.get("/deviceinfo")
async def get_device_info():
    return {"device_id": "1234567890", "device_name": "MyDevice"}