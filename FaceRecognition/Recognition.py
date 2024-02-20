import ast
import os
import time
import dlib
import numpy as np
import pandas as pd
import cv2


def load_known_features(csv_path):
    """
    从 csv 文件中加载已知人脸特征
    csv 文件中的数据格式为: [name, [feature_1, feature_2, ..., feature_128]]
    :param csv_path:    csv 文件路径
    :return:        已知人脸特征列表
    """
    csv_rd = pd.read_csv(csv_path, header=None)
    features_known_arr = [list(csv_rd.loc[i, :]) for i in range(csv_rd.shape[0])]
    print("数据库中的人脸数据总数为: ", len(features_known_arr))
    return features_known_arr


def calculate_euclidean_distance(feature_1, feature_2):
    """
    计算两个特征之间的欧式距离
    :param feature_1: 特征 1
    :param feature_2: 特征 2
    :return: 两个特征之间的欧式距离
    """
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


def detect_faces(image, detector):
    """
    检测图像中的人脸
    :param image:  每一帧的输入图像
    :param detector:    人脸检测器
    :return: faces: 检测到的人脸列表
    """
    img_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = detector(img_gray, 0)
    return faces


def draw_rectangle_and_text(image, faces, names, positions):
    """
    绘制人脸框和人脸名字
    :param image: 每一帧的输入图像
    :param faces: 检测到的人脸列表
    :param names: 人脸名字列表
    :param positions:   人脸名字位置列表
    :return:    None
    """
    font = cv2.FONT_HERSHEY_COMPLEX
    for i in range(len(faces)):
        cv2.rectangle(image, tuple([faces[i].left(), faces[i].top()]),
                      tuple([faces[i].right(), faces[i].bottom()]), (0, 255, 255), 2)
        cv2.putText(image, names[i], positions[i], font, 0.8, (0, 255, 255), 1, cv2.LINE_AA)


def save_unknown_face(face, save_path):
    """
    存储未知人脸
    :param face: 未知人脸
    :param save_path:   存储路径
    :return:    None
    """
    size = 64
    face = cv2.resize(face, (size, size))
    now_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    save_name = str(now_time) + 'unknown.jpg'
    save_path = os.path.join(save_path, save_name)
    cv2.imwrite(save_path, face)
    print('新存储未知人脸数据到：', save_path)


def main():
    # 文件路径设置
    model_folder_path = "D:\\Projects\\PytorchProject\\Models"
    csv_folder_path = "D:\\Projects\\PytorchProject\\Csv"
    image_folder_path = "D:\\Projects\\PytorchProject\\Image"
    unknownImg_save_folder_path = "D:\\Projects\\PytorchProject\\UnknownImg"

    # 人脸识别模型，提取128D的特征矢量
    face_recognition_model = dlib.face_recognition_model_v1(
        os.path.join(model_folder_path, "dlib_face_recognition_resnet_model_v1.dat"))

    # 处理存放所有人脸特征平均值的 csv 文件
    path_features_known_csv = os.path.join(csv_folder_path, "face_feature_mean.csv")
    features_known_arr = load_known_features(path_features_known_csv)
    # 将str类型的特征数据转为List,[name, [feature_1, feature_2, ..., feature_128]]
    for i in range(len(features_known_arr)):
        features_known_arr[i][1] = ast.literal_eval(features_known_arr[i][1])

    # Dlib 检测器和预测器
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(os.path.join(model_folder_path, "shape_predictor_68_face_landmarks.dat"))

    # 创建 cv2 摄像头对象
    camera = cv2.VideoCapture(0)
    camera.set(3, 480)

    while camera.isOpened():
        key = cv2.waitKey(5)
        # 按下 'q' 键退出
        if key == ord('q'):
            break

        flag, frame_img = camera.read()

        faces = detect_faces(frame_img, detector)
        namelist = ["unknown"] * len(faces)  # 存储人脸名字列表, 初始化为 unknown
        posList = [tuple([face.left(), int(face.bottom() + (face.bottom() - face.top()) / 4)])
                   for face in faces]  # 存储人脸名字位置列表

        if len(faces) != 0:  # 检测到人脸
            features_cap_arr = [
                face_recognition_model.compute_face_descriptor(frame_img, predictor(frame_img, face))
                for face in faces]  # 获取当前摄像头下人脸的特征列表

            for k in range(len(faces)):  # 对于摄像头中的每张人脸
                print("##### camera person", k + 1, "#####")
                # 让当前检测的人脸特征向量(features_cap_arr[k])与目前已知的全部人脸特征向量features_known_arr[::][1]进行比对
                e_distance_list = [calculate_euclidean_distance(features_cap_arr[k], features_known_arr[i][1])
                                   if str(features_known_arr[i][1][0]) != '0.0' else 999999999
                                   for i in range(len(features_known_arr))]

                similar_person_idx = e_distance_list.index(min(e_distance_list))    # 获取最小欧式距离的人脸序号
                print("Minimum e distance with person", similar_person_idx + 1)

                if e_distance_list[similar_person_idx] < 0.4:   # 如果最小距离小于0.4, 则认为是同一个人
                    namelist[k] = features_known_arr[similar_person_idx][0]
                    print("未知人脸")
                    # TODO: 先不存,方便测试
                    # face = faces[k]
                    # save_unknown_face(frame_img[face.top():face.bottom(), face.left():face.right()],
                    #                   unknownImg_save_folder_path)

                print('\n')

            draw_rectangle_and_text(frame_img, faces, namelist, posList)

        print("Faces in camera now:", namelist, "\n")

        cv2.putText(frame_img, "Face Recognition", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame_img, "Visitors: " + str(len(faces)), (20, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1,
                    cv2.LINE_AA)

        cv2.imshow("camera", frame_img)

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
