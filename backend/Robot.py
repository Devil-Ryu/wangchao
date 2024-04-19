import asyncio
import uiautomator2 as u2
import time
import cv2
import numpy as np
import os
from Utils import compare_region, get_current_device, get_current_device_config

class WangchaoRobot:
    device = None

    config = {
        "device_id": "",
        "protected_mask_region": [],
        "protected_mask_query_time": 60,
        "assemble_detection_region": [],
        "protected_mask_enabled": False,
    }

    # 初始化
    def __init__(self):
        pass

    # 设置设备
    def connectDevice(self, device_id):
        try:
            self.device = u2.connect(device_id)
        except:
            return False
        return True
    
    # 设置配置
    def setConfig(self, config):
        self.config = config

    # 获取设备信息
    def getDeviceInfo(self):
        if self.device is None:
            return {}
        return self.device.info

    # 导航到目标区域
    def navigate_to_target_region(self, region_x, region_y):
        # 检查是否链接设备
        if self.device is None:
            return False
        # 点击目标区域
        self.device.click(0.35, 0.02)  # 点击导航区域

        # 设置X坐标
        self.device.click(0.45, 0.46)  # 点击输入x坐标
        self.device.send_keys(str(region_x))  # 输入x坐标
        self.device(text="确定").click()

        # 设置Y坐标
        self.device.click(0.57, 0.46)  # 点击输入y坐标
        self.device.send_keys(str(region_y))  # 输入y坐标
        self.device(text="确定").click()

        # 点击导航按钮
        self.device.click(0.492, 0.596)  # 点击坐标确定按钮

    # 检测是否有防护罩
    def detect_mask(self):
        # 检查是否链接设备
        if self.device is None:
            return False
        
        # 检测配置是否有region字段
        if len(self.config["protected_mask_region"]) == 0:
            return False
        
        # 定义存储的图片名称
        fileName1 = "detect_mask1"
        fileName2 = "detect_mask2"
        print("config: ", self.config["protected_mask_region"])
        for region in self.config["protected_mask_region"]:
            # 导航到目标区域，并获取目标区域矩阵
            self.navigate_to_target_region(region[0][0], region[0][1])
            time.sleep(2)

            # 查看监听区域变化
            filePath1 = self.get_screenshot(fileName1)
            time.sleep(1)  # 两次操作，间隔1s
            filePath2 = self.get_screenshot(fileName2)

            image1 = cv2.imread(filePath1)
            image2 = cv2.imread(filePath2)
            cropped_image1 = image1[region[1][1]:region[1][1]+region[1][3], region[1][0]:region[1][0]+region[1][2]]
            cropped_image2 = image1[region[1][1]:region[1][1]+region[1][3], region[1][0]:region[1][0]+region[1][2]]
        
            result = compare_region(cropped_image1, cropped_image2)
            print("detect_mask_result:", result)
        return result
    
    # 获取屏幕截图
    def get_screenshot(self, fileName):
        # 检查是否链接设备
        if self.device is None:
            return False
        # 截图并保存
        os.system('adb shell screencap -p /sdcard/{}.jpg'.format(fileName))
        os.system('adb pull /sdcard/{}.jpg ./images/'.format(fileName))
        # 图片路径
        return os.path.join(os.getcwd(),"images", "{}.jpg".format(fileName))

    # 号召检测
    def assemble_detection(self):
        # 检查是否链接设备
        if self.device is None:
            return False


# 运行监测防护罩
async def run_detect_mask():
    while True:
        robot = WangchaoRobot()
        device_name, device_id = get_current_device()
        config, device_name = get_current_device_config()
        robot.connectDevice(device_id)
        robot.setConfig(config)
        robot.detect_mask()
        await asyncio.sleep(config["protected_mask_query_time"])


if __name__ == '__main__':
    device_id = '192.168.2.129:5555'
    robot = WangchaoRobot()
    robot.connectDevice(device_id)
    print(robot.getDeviceInfo())
    # robot.navigate_to_target_region(21, 73)
