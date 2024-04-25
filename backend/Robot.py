import asyncio
import uiautomator2 as u2
import time
import cv2
import numpy as np
import os
from Utils import compare_region, get_current_device, get_current_device_config, detect_gather_image, get_gather_time_left, wechat_notify




class WangchaoRobot:
    device = None

    config = {
        "device_id": "",
        "protected_mask_region": [],  # 防护罩区域
        "protected_mask_query_time": 60,  # 防护罩查询间隔
        "gather_detection_region": [],  # 集结图标区域
        "gather_notification_deadline": 180,  # 集结通知截止时间
        "gather_notification_interval": 15,  # 集结通知间隔
        "gather_notification_enabled": False,  # 集结通知是否开启
        "gather_notification_token": "",  # 集结通知token
        "gather_notification_receiver": "",  # 集结通知接收者
        "gather_notification_isGroup": False,  # 集结通知是否为群聊
        "gather_detection_interval": 60,  # 集结检测间隔
        "gather_detection_enabled": False,  # 集结检测是否开启
        "protected_mask_enabled": False,  # 防护罩检测是否开启
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

        # 防止有弹窗
        time.sleep(1)
        self.device.click(0.43, 0.024)  # 点击收藏按钮
        time.sleep(1)
        self.device.click(0.868, 0.117)  # 点击收藏面板关闭按钮

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
            cropped_image1 = image1[region[1][1]:region[1][1] +
                                    region[1][3], region[1][0]:region[1][0]+region[1][2]]
            cropped_image2 = image1[region[1][1]:region[1][1] +
                                    region[1][3], region[1][0]:region[1][0]+region[1][2]]

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
        return os.path.join(os.getcwd(), "images", "{}.jpg".format(fileName))

    # 号召检测
    def gather_detection(self):
        # 检查是否链接设备
        if self.device is None:
            return False
        # 读取集结图标
        gather_ico = cv2.imread(
            "./images/gather_ico.png", cv2.IMREAD_UNCHANGED)

        filePath = self.get_screenshot("detect_gather")
        gather_image = cv2.imread(filePath)
        result = detect_gather_image(
            gather_image, gather_ico, ration=0.5, threshold=0.94)
        if result is not None:
            # 点击集结按钮
            self.device.click(result[0], result[1])  # 点击坐标确定按钮
            time.sleep(1)
            filePath = self.get_screenshot("gather_panel")
            self.device.click(0.868, 0.117)  # 点击关闭按钮
            return filePath
        else:
            return None



# 运行监测防护罩
async def run_detect_mask(queue):
    while True:
        print("测防护罩1: 当前队列元素:", queue.qsize())
        await queue.get()
        print("开始检测防护罩")
        print("测防护罩2:当前队列元素:", queue.qsize())
        start = time.time()
        robot = WangchaoRobot()
        device_name, device_id = get_current_device()
        config, device_name = get_current_device_config()
        robot.connectDevice(device_id)
        robot.setConfig(config)
        robot.detect_mask()
        end = time.time()
        print("detect_mask_time:", end-start)
        await queue.put(1)
        await asyncio.sleep(config["protected_mask_query_time"])

# 运行号召检测
async def run_gather_detection(queue):
    while True:
        print("检测集结1: 当前队列元素:", queue.qsize())
        await queue.get()
        print("开始检测集结")
        print("检测集结2: 当前队列元素:", queue.qsize())
        start = time.time()
        robot = WangchaoRobot()
        device_name, device_id = get_current_device()
        config, device_name = get_current_device_config()
        robot.connectDevice(device_id)
        robot.setConfig(config)
        filePath = robot.gather_detection()
        if filePath is not None:
            print("发现集结")
            time_left = get_gather_time_left(filePath)
            print("集结剩余时间:", time_left)
            if time_left == None:
                print("未知集结时间")
                await queue.put(1)
                await asyncio.sleep(config["gather_detection_interval"])
            else:
                end = time.time()
                deal_time = int(end - start)
                print("deal_time: ", deal_time)
                if time_left > int(config["gather_notification_deadline"]):
                    print("config:  ", config)
                    # 发送微信通知
                    if config["gather_notification_enabled"]:
                        wechat_notify(config["gather_notification_token"], config["gather_notification_receiver"], "通知: 集结时间还剩{}秒".format(time_left), isRoom=config["gather_notification_isGroup"])
                    print("通知: 集结时间还剩{}秒".format(time_left))
                    await queue.put(1)
                    await asyncio.sleep(config["gather_notification_interval"])
                else:
                    # 开启防护罩，并通知
                    # 发送微信通知
                    if config["gather_notification_enabled"]:
                        wechat_notify(config["gather_notification_token"], config["gather_notification_receiver"], "通知: 集结时间还剩{}秒, 开启防护罩".format(time_left), isRoom=config["gather_notification_isGroup"])
                    print("通知: 集结时间还剩{}秒, 开启防护罩".format(time_left))
                    await queue.put(1)
                    await asyncio.sleep(config["gather_detection_interval"])
        else:
            print("未发现集结")
            await queue.put(1)
            await asyncio.sleep(config["gather_detection_interval"])


if __name__ == '__main__':
    device_id = '192.168.2.129:5555'
    robot = WangchaoRobot()
    robot.connectDevice(device_id)
    print(robot.getDeviceInfo())
    # robot.gather_detection()
    asyncio.run(run_gather_detection())
