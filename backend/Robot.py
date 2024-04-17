import uiautomator2 as u2
import time
import cv2
import numpy as np
import os
from Utils import compare_region

class WangchaoRobot:
    device = None
    config = {
        "device_id": "192.168.45.193:5555",
        "protected_mask_region": [[[220, 100], [400, 300, 500, 600]], [[100, 200], [300, 400, 500, 600]]],
        "protected_query_time": 60,
        "assemble_detection_region": [],
    }

    # 初始化
    def __init__(self):
        pass

    # 设置设备
    def connectDevice(self, device_id):
        self.device = u2.connect(device_id)

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

        # 定义存储的图片名称
        fileName1 = os.path.join(os.getcwd(),"images", "screenshot1.jpg")
        fileName2 =  os.path.join(os.getcwd(),"images", "screenshot2.jpg")
        for region in self.config["protected_mask_region"]:
            # 导航到目标区域，并获取目标区域矩阵
            self.navigate_to_target_region(region[0][0], region[0][1])

            # 查看监听区域变化
            self.device.screenshot(fileName1, "opencv")
            time.sleep(1)  # 两次操作，间隔1s
            self.device.screenshot(fileName2, "opencv")

            image1 = cv2.imread(fileName1)
            image2 = cv2.imread(fileName2)
            cropped_image1 = image1[region[1][1]:region[1][3], region[0][0]:region[1][2]]
            cropped_image2 = image2[region[1][1]:region[1][3], region[0][0]:region[1][2]]
        
        result = compare_region(cropped_image1, cropped_image2)
        print(result)
        return result


    # 号召检测
    def assemble_detection(self):
        # 检查是否链接设备
        if self.device is None:
            return False


if __name__ == '__main__':
    device_id = '192.168.2.129:5555'
    robot = WangchaoRobot()
    robot.connectDevice(device_id)
    print(robot.getDeviceInfo())
    # robot.navigate_to_target_region(21, 73)
