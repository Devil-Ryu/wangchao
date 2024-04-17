from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from Utils import add_device_to_list, get_device_list, switch_current_device, delete_device_from_list, get_current_device


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Device(BaseModel):
    device_id: str
    device_name: str


@app.get("/items/{item_id}")
async def read_item(item_id: Union[int, str]):
    return {"item_id": item_id}

@app.get("/deviceinfo")
async def get_device_info():
    return {"device_id": "1234567890", "device_name": "MyDevice"}

# 获取当前设备
@app.get("/devices/current")
async def current_device():
    device = {}
    current_device = get_current_device()
    if current_device:
        device["device_name"] = current_device[0]
        device["device_id"] = current_device[1]
    else:
        device["device_name"] = ""
        device["device_id"] = ""
    return {"status_code": 200, "message":"", "data":device}


# 添加设备
@app.post("/devices/add")
async def add_device(device: Device):
    print(device.device_name, device.device_id)
    result = add_device_to_list(device.device_name, device.device_id)
    status_code = 200 if result else 400
    msg = "设备添加成功" if result else "设备名称已存在"
    return {"status_code": status_code, "message":msg, "data":[]}

# 删除设备
@app.delete("/devices/delete")
async def delete_device(device_name: str):  
    result = delete_device_from_list(device_name)
    status_code = 200 if result else 400
    msg = "设备删除成功" if result else "设备不存在"
    return {"status_code": status_code, "message":msg, "data":[]}

# 获取设备列表
@app.get("/devices/list")
async def get_devices():
    result = []
    device_list = get_device_list()
    for device in device_list:
        result.append({"device_name": device[0], "device_id": device[1]})
    return {"status_code": 200, "message":"", "data":result}

# 切换设备
@app.get("/devices/switch")
async def switch_device(device_name: str):
    # 切换设备
    result = switch_current_device(device_name)
    status_code = 200 if result else 400
    msg = "设备切换成功" if result else "设备不存在"
    return {"status_code": status_code, "message":msg, "data":[]}