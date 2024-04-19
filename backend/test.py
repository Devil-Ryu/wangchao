import asyncio
import time
import os
from Robot import WangchaoRobot
from Utils import add_device_to_list, get_device_list, switch_current_device, delete_device_from_list, get_current_device, get_current_device_status, get_current_device_config, update_protected_mask_region, update_global_config_by_name


async def task_to_execute():
    # 模拟一个长时间运行的任务
    while True:
        print("Task is running...")
        await asyncio.sleep(1)

async def start_task():
    # 启动任务
    task = asyncio.create_task(task_to_execute())
    print("Task started.")
    return task

async def stop_task(task):
    # 停止任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Task stopped.")

async def main():
    # 启动任务
    task = await start_task()
    print("dddd")
    
    # 模拟一段时间后停止任务
    await asyncio.sleep(2)
    
    # 停止任务
    d = await stop_task(task)
    print("eeee")

asyncio.run(main())
# robot = WangchaoRobot()
# device_name, device_id = get_current_device()
# config, device_name = get_current_device_config()
# robot.connectDevice(device_id)
# robot.setConfig(config)
# print(robot.config)
# # robot.get_screenshot("detect_mask1")
# robot.detect_mask()