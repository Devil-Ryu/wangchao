import json
import cv2
import numpy as np
import os
import uiautomator2 as u2
import time
import re
from datetime import datetime, timedelta
from ocr import find_text_by_ocr
import requests

# 读取json文件并和字典进行合并
def merge_json_to_dict(json_file, dict_obj):
    with open(json_file, 'r') as f:
        json_obj = json.load(f)
    dict_obj.update(json_obj)
    return dict_obj

# 写入字典到json文件
def write_dict_to_json(dict_obj, json_file):
    with open(json_file, 'w') as f:
        json.dump(dict_obj, f)


# 读取json文件并返回字典
def read_json_to_dict(json_file):
    with open(json_file, 'r') as f:
        json_obj = json.load(f)
    return json_obj

def screenshot(filename):
    os.system('adb shell screencap -p /sdcard/{}'.format(filename))
    os.system('adb pull /sdcard/{}'.format(filename))

# 检测防护罩
def compare_region(image1, image2, threshold_min=0.08, threshold_max=0.30):

    image1 = cv2.resize(image1, (400,400))
    image2 = cv2.resize(image2, (400,400))

    # 将图像转换为HSV颜色空间
    hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

    # 设置蓝白色护罩的颜色范围(77,28,147)-(145,151,222)
    # lower_blue = np.array([90, 50, 50])
    # upper_blue = np.array([130, 255, 255])
    lower_blue = np.array([77,28,147])
    upper_blue = np.array([145,151,222])


    # 根据颜色范围创建掩膜
    mask1 = cv2.inRange(hsv1, lower_blue, upper_blue)
    mask2 = cv2.inRange(hsv2, lower_blue, upper_blue)
    cv2.imwrite("./images/detect_mask1_hsv.jpg", mask1)
    cv2.imwrite("./images/detect_mask2_hsv.jpg", mask2)

    diff = cv2.absdiff(mask1, mask2)
    ration = round( np.count_nonzero(diff)/ diff.size, 2)
    print(ration)

    if threshold_min < ration < threshold_max:
        return True, ration
    else:
        return False, ration

# 获取设备列表(从文件中读取设备列表，每一行一个设备，格式为name,filename.json)
def get_device_list():
    device_file = os.path.join(os.getcwd(), 'resources', 'device_list.txt')
    device_list = []
    with open(device_file, 'r') as f:
        for line in f:
            device_name, device_json = line.strip().split(',')
            device_list.append((device_name, device_json))
    return device_list

# 写入设备列表到文件
def write_device_list(device_list):
    device_file = os.path.join(os.getcwd(), 'resources', 'device_list.txt')
    with open(device_file, 'w') as f:
        for device in device_list:
            f.write(f"{device[0]},{device[1]}\n")
    

# 新增设备到设备列表
def add_device_to_list(device_name, device_id):
    device_list = get_device_list()  # 获取设备列表
    for device in device_list:
        if device[0] == device_name:  # 设备已存在
            return False
    device_list.append((device_name, device_id))  # 新增设备到列表
    write_device_list(device_list)  # 写入设备列表到文件
    write_device_config(device_name, {
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
    })
    return True

# 删除设备从设备列表
def delete_device_from_list(device_name):
    device_list = get_device_list()  # 获取设备列表
    for i, device in enumerate(device_list):
        if device[0] == device_name:  # 找到要删除的设备
            del device_list[i]  # 删除设备
            break
    write_device_list(device_list)  # 写入设备列表到文件
    return True

# 切换当前设备，将设备信息写入current_device.txt文件
def switch_current_device(device_name):
    device_list = get_device_list()  # 获取设备列表
    for device in device_list:
        if device[0] == device_name:  # 找到要切换的设备
            with open(os.path.join(os.getcwd(), 'resources', 'current_device.txt'), 'w') as f:
                f.write(f"{device[0]},{device[1]}")  # 写入设备信息到文件
            return True
    return False  # 设备不存在

# 获取设备列表
def get_device_list():
    device_file = os.path.join(os.getcwd(), 'resources', 'device_list.txt')
    device_list = []
    with open(device_file, 'r') as f:
        for line in f:
            device_name, device_json = line.strip().split(',')
            device_list.append((device_name, device_json))
    return device_list


# 获取当前设备
def get_current_device():
    current_device_file = os.path.join(os.getcwd(), 'resources', 'current_device.txt')
    with open(current_device_file, 'r') as f:
        device_name, device_id = f.read().strip().split(',')
    return device_name, device_id

# 读取当前设备配置current_device.txt, 配置内容为device_name, device_id, 根据device_name从device_name.json文件中读取配置, 返回device_config字典和device_id字符串
def get_current_device_config():
    current_device_file = os.path.join(os.getcwd(), 'resources', 'current_device.txt')
    with open(current_device_file, 'r') as f:
        device_name, device_id = f.read().strip().split(',')
    device_config_file = os.path.join(os.getcwd(), 'resources', f"{device_name}.json")
    with open(device_config_file, 'r') as f:
        device_config = json.load(f)
    return device_config, device_name

# 写入设备配置到文件
def write_device_config(device_name, device_config):
    device_config_file = os.path.join(os.getcwd(), 'resources', f"{device_name}.json")
    with open(device_config_file, 'w') as f:
        json.dump(device_config, f)

# 更新配置文件中protected_mask_region的值，如果没有该字段则创建字段，默认为[], 如果有字段, 则将传入的protected_mask_region值按照index更新到列表中, 考虑列表为空的情况
def update_protected_mask_region(index, protected_mask_region):
    device_config, device_name = get_current_device_config()  # 获取当前设备配置
    if 'protected_mask_region' not in device_config:  # 如果没有protected_mask_region字段则创建字段
        device_config['protected_mask_region'] = []
    if index >= len(device_config['protected_mask_region']):  # 如果index大于protected_mask_region列表长度, 则新增元素
        device_config['protected_mask_region'].append(protected_mask_region)
    else:  # 如果index小于protected_mask_region列表长度, 则更新元素
        device_config['protected_mask_region'][index] = protected_mask_region

    write_device_config(device_name, device_config)  # 写入设备配置到文件

# 更新配置文件中的全局参数，根据参数名称直接替换，如果没有该字段则创建字段
def update_global_config_by_name(config_name, config_value):
    device_config, device_name = get_current_device_config()  # 获取当前设备配置
    if config_name not in device_config:  # 如果没有该字段则创建字段
        device_config[config_name] = ""
    device_config[config_name] = config_value  # 更新配置
    write_device_config(device_name, device_config)  # 写入设备配置到文件

# 获取当前设备连接状态
def get_current_device_status():
    current_device_file = os.path.join(os.getcwd(), 'resources', 'current_device.txt')
    with open(current_device_file, 'r') as f:
        device_name, device_id = f.read().strip().split(',')
        print("device_id", device_id)
        try:
            d = u2.connect(device_id)
            print("device_info", d.info)
            return True
        except:
            return False

# 采用opencv的模板匹配算法，在gather_detection_region区域中查找gather_image的位置，返回坐标(x,y)(限定区域)
def detect_gather_image(detect_image, sample_image, ration=0.4, threshold=0.9, visualize=False):

     # 将图片和模板都等比缩小
    detect_image = cv2.resize(detect_image, (0,0), fx=ration, fy=ration)
    sample_image = cv2.resize(sample_image, (0,0), fx=ration, fy=ration)

    found = None
    for scale in np.linspace(0.5, 1.5, 15)[::-1]:
        resized = cv2.resize(sample_image, (0,0), fx=scale, fy=scale)

        alpha_channel = resized[:,:,3]
        _, mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)

        resized = resized[:,:,:3]

        result = cv2.matchTemplate(detect_image, resized, cv2.TM_CCORR_NORMED, mask=mask)
        # 将result中inf的元素替换为0
        result[np.where(np.isinf(result))] = 0
        (_, max_val, _, max_loc) = cv2.minMaxLoc(result)

        if found is None or max_val > found[0]:
            found = (max_val, max_loc, scale)

    print("found: ", found)
    (max_val, max_loc, scale) = found
    top_left = (int(max_loc[0] ), int(max_loc[1] ))
    bottom_right = (int((max_loc[0] + sample_image.shape[1]*scale)), int((max_loc[1] + sample_image.shape[0] * scale)))

    # 打印素材中心点位置的百分比坐标
    center_x = (top_left[0] + bottom_right[0]) / 2
    center_y = (top_left[1] + bottom_right[1]) / 2
    center_x_percent = center_x / detect_image.shape[1]
    center_y_percent = center_y / detect_image.shape[0]
    print(f"center_x_percent: {center_x_percent}, center_y_percent: {center_y_percent}")

    if max_val > threshold:
        if visualize:
            # 在图像上标记出找到的位置
            cv2.rectangle(detect_image, top_left, bottom_right, (0, 255, 0), 1)
            cv2.putText(detect_image, "{:.2f}".format(max_val), (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            # 显示结果
            # 设置窗口大小
            cv2.imshow('Result', detect_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return center_x_percent, center_y_percent
    else:
        print("not found")
        return None

# 从截图中获取集结剩余时间
def get_gather_time_left(filePath):
    result = find_text_by_ocr(filePath, "集结时间")
    if result is not None:
        match = re.search(r'\d+:\d+', result)
        if match is None:
            return None
        gather_time_left = match.group()
        # 从字符串中读取时间，并转化为秒
        time_obj = datetime.strptime(gather_time_left, '%M:%S')
        # 使用timedelta计算时间对象的总秒数
        total_seconds = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second).total_seconds()
        return total_seconds
    else:
        return None

# 微信通知
def wechat_notify(token, receiver, message, isRoom=False):
    url = "http://192.168.2.29:3001/webhook/msg/v2?token={}".format(token)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "to": receiver,
        "isRoom": isRoom,
        "data": {"content": message}
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        resData = response.json()
        print((response.status_code, resData))
        return response.status_code, resData
    except Exception as e:
        print((response.status_code, e.args))
        return 500, e.args
    


def test():
#    check_gather_notification()
   pass




if __name__ == '__main__':
    status_code, resData = wechat_notify("", "Hypocrite", "测试消息\n第二行")    
    print(status_code, resData)