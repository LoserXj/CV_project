from flask import Flask, request, make_response, send_from_directory
import cv2
import os
from deepface import DeepFace
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def draw_rectangle(image, dic_list):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    for dic in dic_list:
        x, y, w, h, confidence = dic["facial_area"]['x'], dic["facial_area"]['y'], dic["facial_area"]['w'], dic["facial_area"]['h'], dic["confidence"]
        cv2.rectangle(image, pt1 = (x, y), pt2 =(x + w, y + h), color = (255, 0, 0), thickness = min(image.shape[0], image.shape[1]) // 100)
        text_position = (x, y - 10)  # 根据框的位置调整文本位置
        # cv2.putText(image, f"Conf: {confidence:.2f}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# 人脸检测函数
def detect_faces(image):
    # 使用OpenCV加载图像
    result = DeepFace.extract_faces(
        img_path = image,
        enforce_detection = False
    )
    return draw_rectangle(image, result)


@app.route('/')
def index():
    # 发送index.html文件给客户端浏览器
    return send_from_directory('static', 'index.html')


@app.route('/extract_faces', methods=['POST'])
def upload():
    image = request.files['image'].read()
    image_array = np.asarray(bytearray(image), dtype=np.uint8())
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # 检测人脸并绘制矩形框
    detected_image_rgb = detect_faces(frame)
    # detected_image_rgb = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
    # resized_image = cv2.resize(detected_image_rgb, (400, int(detected_image_rgb.shape[0] * 400 / detected_image_rgb.shape[1])), interpolation=cv2.INTER_AREA)
    # 将处理后的图像转换为内存文件对象，以便发送
    _, buffer = cv2.imencode('.jpg', detected_image_rgb)
    # 使用make_response创建响应
    response = make_response(buffer.tobytes())
    # 设置MIME类型
    response.mimetype = 'image/jpeg'
    # 设置Content-Disposition头部，以提供下载文件的名称
    response.headers.set('Content-Disposition', 'attachment', filename='image_with_faces.jpg')
    return response

if __name__ == '__main__':
    app.run(debug=True)