import cv2

# 测试摄像头是否正常工作
camera = cv2.VideoCapture(0)
# 循环显示摄像头捕获的画面
while True:
    success, img = camera.read()
    cv2.imshow('camera', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break