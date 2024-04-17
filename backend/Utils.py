import json
import cv2
import numpy as np
import os

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
    cv2.imwrite("mask1.jpg", mask1)
    cv2.imwrite("mask2.jpg", mask2)

    # cv2.imwrite("test1ccc.jpg", mask)
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
    return device_config, device_id