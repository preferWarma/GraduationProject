# coding=utf-8
import sys
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import face_recognition

# 加载已知人脸图像
known_image = face_recognition.load_image_file("Image/img.png")

# 提取已知人脸的编码
known_face_encoding = face_recognition.face_encodings(known_image)[0]

# 初始化摄像头
video_capture = cv2.VideoCapture(0)


def cv2AddChineseText(frame, name, position, fill):
    font = ImageFont.truetype('simsun.ttc', 30)
    img_pil = Image.fromarray(frame)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, name, font=font, fill=fill)
    return np.array((img_pil))


while True:
    # 读取摄像头中的图像
    ret, frame = video_capture.read()

    # 将图像转换为RGB格式
    rgb_frame = frame[:, :, ::-1]

    # 检测图像中的人脸
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, model="large")

    # 在图像中标记人脸位置
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # 判断检测到的人脸是否和已知人脸匹配
        matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=0.38)

        # 如果匹配，则标记人脸为已知人脸
        name = "unknown"
        if True in matches:
            name = "know"

        # 在图像中标记人脸位置和姓名
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
        frame = cv2AddChineseText(frame, name, (left, top - 38), (0, 0, 255))

    # 显示图像
    cv2.imshow('Video', frame)

    # 按下q键退出程序
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头
video_capture.release()

# 关闭所有窗口
cv2.destroyAllWindows()
