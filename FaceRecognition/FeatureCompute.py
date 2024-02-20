import re

import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np

# 文件路径配置
image_folder_path = "D:/Projects/PytorchProject/Image"  # 存放已经收集好的人脸图像的路径
csv_save_folder_path = "D:/Projects/PytorchProject/Csv"  # 存放保存人脸特征的 CSV 文件的路径
shape_predictor_path = "D:/Projects/PytorchProject/Models/shape_predictor_68_face_landmarks.dat"  # 人脸关键点检测模型的路径
face_rec_model_path = "D:/Projects/PytorchProject/Models/dlib_face_recognition_resnet_model_v1.dat"  # Dlib 人脸识别模型路径

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()
# Dlib 人脸预测器
predictor = dlib.shape_predictor(shape_predictor_path)
# Dlib 人脸识别模型, 将会返回 128D 的向量
face_recognition_model = dlib.face_recognition_model_v1(face_rec_model_path)


def extract_landmarks_withSave(img_rd, save_path):
    """
    提取人脸关键点, 并保存到 CSV 文件
    :param img_rd: 当前读入的图像
    :param save_path: csv文件保存路径
    :return: faces: 检测到的人脸列表
    """
    # 将图像从 BGR（蓝绿红）颜色空间转换为 RGB（红绿蓝）颜色空间。openCV读取图片的默认像素排列是BGR, 而dlib是RGB排列
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    faces = detector(img_gray, 1)  # 定位人脸, 返回的是所有人脸信息的列表

    for i, face in enumerate(faces):
        landmarks = np.matrix([[p.x, p.y] for p in predictor(img_rd, face).parts()])  # 提取人脸关键点

        with open(save_path, "a", newline="") as csvFile:  # 采用追加方式打开文件, 如果文件不存在, 创建文件
            writer = csv.writer(csvFile)
            for idx, point in enumerate(landmarks):  # idx: 点的索引, point: 点的坐标
                pos = (point[0, 0], point[0, 1])
                writer.writerow((idx, pos))

    return faces


def compute_face_descriptor(img_rd, shape):
    """
    计算人脸描述符, 提取人脸特征为 128D 向量
    :param img_rd: 当前读入的图像
    :param shape: 人脸关键点
    :return: face_descriptor: 128维的人脸特征向量
    """
    return face_recognition_model.compute_face_descriptor(img_rd, shape)


def getAndSave_128d_features(path_img, csvFolder_path):
    """
    返回 128D 特征, 并保存到 CSV 文件
    :param path_img: 当前读入的图像
    :param csvFolder_path: 保存 CSV 文件的文件夹路径
    :return: face_descriptor: 128维的人脸特征向量
    """
    img_rd = io.imread(path_img)
    if not os.path.exists(csvFolder_path):  # 如果文件夹不存在, 创建文件夹
        os.makedirs(csvFolder_path)

    # 提取文件名中的信息，构造 CSV 文件路径
    _, fileName = os.path.split(path_img)  # 第一个返回值为路径，第二个返回值为文件名
    base, extension = os.path.splitext(fileName)  # 分离文件名和扩展名
    save_path = os.path.join(csvFolder_path, f"{base}_feature.csv")  # 构造 CSV 文件路径

    if not os.path.exists(save_path):  # 如果文件不存在，创建 CSV 文件, 并写入表头
        with open(save_path, "w", newline="") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(["index", "position"])

    # 提取人脸特征并保存到 CSV 文件
    detected_faces = extract_landmarks_withSave(img_rd, save_path)

    print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')

    # 如果检测到人脸，计算人脸描述符
    if detected_faces:
        shape = predictor(img_rd, detected_faces[0])  # 获取的关键点
        face_descriptor = compute_face_descriptor(img_rd, shape)  # 获取128D特征值向量
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor  # 返回128D特征值向量


def return_features_mean(faceImageFolder_path, csv_folder_path):
    """
    计算某个人的人脸图像的平均特征向量
    :param faceImageFolder_path: 这个人的人脸图像的文件夹路径
    :param csv_folder_path: 保存这个人的人脸特征的 CSV 文件的文件夹路径
    :return: features_mean: 128维的人脸特征向量的均值列表
    """
    features_list = []  # 保存某人所有人脸图像的特征向量
    photos_list = os.listdir(faceImageFolder_path)  # 读取该文件夹下的所有人脸图像
    photos_list = sorted(photos_list,
                         key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
    if photos_list:
        for i in range(len(photos_list)):
            # 调用return_128d_features()得到128d特征
            curImagePath = os.path.join(faceImageFolder_path, photos_list[i])
            print("%-40s %-20s" % ("正在读的人脸图像 / image to read:", curImagePath))
            features_128d = getAndSave_128d_features(curImagePath, csv_folder_path)
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                continue
            else:
                features_list.append(features_128d)

    else:
        print("文件夹内图像文件为空 / Warning: No images in " + faceImageFolder_path + '\n')

    # 计算 128D 特征的均值
    # N x 128D -> 1 x 128D
    if features_list:
        features_mean = np.array(features_list).mean(axis=0)
    else:
        features_mean = np.array(0)

    return features_mean


def update_mean_features_csv(csv_folder_path, image_folder_path):
    """
    更新保存全部人脸特征平均值的 CSV 文件
    :param image_folder_path: 图像根目录
    :param csv_folder_path: 存储人脸特征平均值的 CSV 文件的文件夹路径
    :return: None
    """
    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)
    csv_save_path = os.path.join(csv_folder_path, "face_feature_mean.csv")  # 存放平均人脸特征的 CSV 文件路径
    with open(csv_save_path, "w", newline="") as csvFile:  # 程序会新建一个表格文件来保存特征值，方便以后比对
        writer = csv.writer(csvFile)
        name_list = os.listdir(image_folder_path)
        name_list.sort()
        for person_name in name_list:
            print("##### " + person_name + " #####")  # 打印当前处理的人名
            cur_folder_path = os.path.join(image_folder_path, person_name)  # 当前人脸图像文件夹路径
            features_mean = return_features_mean(cur_folder_path, os.path.join(csv_folder_path, person_name))
            writer.writerow([person_name, list(features_mean)])
            print(f"{person_name}的特征均值为{list(features_mean)}\n")


if __name__ == '__main__':
    update_mean_features_csv(csv_save_folder_path, image_folder_path)
    print(f"人脸数据已经存入{os.path.join(csv_save_folder_path, 'face_feature_mean.csv')}")
