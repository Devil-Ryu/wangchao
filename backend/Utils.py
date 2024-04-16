import json
import cv2
import numpy as np

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