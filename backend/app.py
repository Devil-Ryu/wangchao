import asyncio
import time
from fastapi import FastAPI, File, Response, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from Robot import WangchaoRobot, run_detect_mask
from Utils import add_device_to_list, get_device_list, switch_current_device, delete_device_from_list, get_current_device, get_current_device_status, get_current_device_config, update_protected_mask_region, update_global_config_by_name


class TaskManager:
    def __init__(self):
        self.tasks = {}
    
    def add_task(self, task_id, task):
        self.tasks[task_id] = task
    
    def get_task(self, task_id):
        return self.tasks.get(task_id)
    
    def remove_task(self, task_id):
        self.tasks.pop(task_id, None)

task_manager = TaskManager()
app = FastAPI()

origins = [
    "*",
    ""
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


class ProtectParams(BaseModel):
    index: int
    protected_mask_region: list
    protected_mask_query_time: int


@app.get("/items/{item_id}")
async def read_item(item_id: Union[int, str]):
    return {"item_id": item_id}

# 获取当前设备状态
@app.get("/devices/status")
async def device_status():
    device = get_current_device_status()
    if device is not None:
        return {"status_code": 200, "message": "", "data": device}
    else:
        return {"status_code": 400, "message": "当前没有设备", "data": {}}

# 获取当前设备
@app.get("/devices/current")
async def current_device():
    device = {}
    current_device = get_current_device()
    status = get_current_device_status()
    config, device_name = get_current_device_config()
    if current_device:
        device["device_name"] = current_device[0]
        device["device_id"] = current_device[1]
        device["device_status"] = status
        device["protected_mask_enabled"] = config.get("protected_mask_enabled", False)
    else:
        device["device_name"] = ""
        device["device_id"] = ""
        device["device_status"] = status
        device["protected_mask_enabled"] = False
    return {"status_code": 200, "message": "", "data": device}


# 获取当前设备配置
@app.get("/devices/config")
async def current_device_config():
    config, device_name = get_current_device_config()
    return {"status_code": 200, "message": "", "data": config}

# 保存设备保护罩配置
@app.post("/update/protect_config")
async def update_protect_config(item: ProtectParams):
    # 获取设备配置
    update_protected_mask_region(item.index, item.protected_mask_region)
    update_global_config_by_name("protected_mask_query_time", item.protected_mask_query_time)
    return {"status_code": 200, "message": "", "data": []}


# 更新配置
@app.get("/update/config")
async def update_config(key: str, value: str):
    # 获取设备配置
    update_global_config_by_name(key, value)
    return {"status_code": 200, "message": "", "data": []}

# 添加设备
@app.post("/devices/add")
async def add_device(device: Device):
    print(device.device_name, device.device_id)
    result = add_device_to_list(device.device_name, device.device_id)
    status_code = 200 if result else 400
    msg = "设备添加成功" if result else "设备名称已存在"
    return {"status_code": status_code, "message": msg, "data": []}

# 删除设备
@app.delete("/devices/delete")
async def delete_device(device_name: str):
    result = delete_device_from_list(device_name)
    status_code = 200 if result else 400
    msg = "设备删除成功" if result else "设备不存在"
    return {"status_code": status_code, "message": msg, "data": []}

# 获取设备列表
@app.get("/devices/list")
async def get_devices():
    result = []
    device_list = get_device_list()
    for device in device_list:
        result.append({"device_name": device[0], "device_id": device[1]})
    return {"status_code": 200, "message": "", "data": result}

# 切换设备
@app.get("/devices/switch")
async def switch_device(device_name: str):
    # 切换设备
    result = switch_current_device(device_name)
    status_code = 200 if result else 400
    msg = "设备切换成功" if result else "设备不存在"
    return {"status_code": status_code, "message": msg, "data": []}

# 返回图片
@app.get("/images/{image_name}")
async def get_image(image_name: str):
    # 检查图片名称是否在白名单内
    if image_name not in ["target.jpg", "current.jpg"]:
        return ""
    try:
        with open(f"./images/{image_name}", "rb") as f:
            image_data = f.read()
    except FileNotFoundError:
        return ""
    return Response(content=image_data, media_type="image/jpeg")


# 导航到目标区域
@app.get("/devices/navigate")
async def navigate_to_target(target_x: int, target_y: int):
    robot = WangchaoRobot()
    device_name, device_id = get_current_device()
    robot.connectDevice(device_id)
    robot.navigate_to_target_region(target_x, target_y)
    time.sleep(1)
    imagePath = robot.get_screenshot('target')
    return {"status_code": 200, "message": "", "data": imagePath}

task = None
# 启动保护罩监听
@app.get("/functions/start_protect")
async def start_protect():
    task = asyncio.create_task(run_detect_mask())
    task_manager.add_task("protect_task", task)
    return {"status_code": 200, "message": "任务:[" +task.get_name() + "]启动成功", "data": []}

# 停止保护罩监听
@app.get("/functions/stop_protect")
async def stop_protect(task_id: str):
    task = task_manager.get_task(task_id)
    try:
        task.cancel()
        await task
    except asyncio.CancelledError:
        return {"status_code": 200, "message": "任务:[" +task_id + "]已经取消", "data": []}
    except Exception as e:
        return {"status_code": 400, "message": str(e), "data": []}

async def test_task():
    for i in range(10):
        print("task running")
        await asyncio.sleep(1)