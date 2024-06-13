from flask import Flask, request, make_response, send_from_directory
import cv2
import os
# from deepface import DeepFace
import numpy as np

veri = Flask(__name__)
veri.config['UPLOAD_FOLDER'] = 'uploads/'

# 确保上传文件夹存在
os.makedirs(veri.config['UPLOAD_FOLDER'], exist_ok=True)

# verify function
def verify(image1_p,image2_p):
    # # 使用OpenCV加载图像
    # result = DeepFace.extract_faces(
    #     img_path = image,
    #     enforce_detection = False
    # )
    # return draw_rectangle(image, result)
    img1=cv2.imread(image1_p)
    img2 = cv2.imread(image2_p)



@veri.route('/')
def index():
    # 发送index.html文件给客户端浏览器
    return send_from_directory('verify', 'index_veri.html')


@veri.route('/verify_faces', methods=['POST'])
def upload():
    image = request.files['image'].read()
    image_array = np.asarray(bytearray(image), dtype=np.uint8())
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # 检测人脸并绘制矩形框
    # detected_image_rgb = detect_faces(frame)
    # detected_image_rgb = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
    # resized_image = cv2.resize(detected_image_rgb, (400, int(detected_image_rgb.shape[0] * 400 / detected_image_rgb.shape[1])), interpolation=cv2.INTER_AREA)
    # 将处理后的图像转换为内存文件对象，以便发送

    # _, buffer = cv2.imencode('.jpg', detected_image_rgb)
    image_path='/Users/apple/Desktop/024-06-11 05.40.40'
    image = cv2.imread(image_path)
    _, buffer = cv2.imencode('.jpg', image)
    # 使用make_response创建响应
    response = make_response(buffer.tobytes())
    # 设置MIME类型
    response.mimetype = 'image/jpeg'
    # 设置Content-Disposition头部，以提供下载文件的名称
    response.headers.set('Content-Disposition', 'attachment', filename='image_with_faces.jpg')
    return response

if __name__ == '__main__':
    veri.run(debug=True)










#
#
#
#
#
#
#
#
# from flask import Flask, request, render_template, redirect, url_for
# import cv2
# import os
# # from deepface import DeepFace
# import numpy as np
#
# veri = Flask(__name__)
# veri.config['UPLOAD_FOLDER'] = 'uploads/'
#
# # 确保上传文件夹存在
# os.makedirs(veri.config['UPLOAD_FOLDER'], exist_ok=True)
#
# def save_image(file, filename):
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(filepath)
#     return filepath
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/verify', methods=['POST'])
# def verify():
#     # 获取上传的文件
#     image1 = request.files['image1']
#     image2 = request.files['image2']
#
#     # 保存图像
#     path1 = save_image(image1, 'image1.jpg')
#     path2 = save_image(image2, 'image2.jpg')
#
#     # 验证两张图像是否属于同一个人
#     result = DeepFace.verify(img1_path=path1, img2_path=path2)
#
#     # 根据验证结果设置结果文本
#     verification_result = "YES" if result["verified"] else "NO"
#
#     return render_template('result.html', image1_url=url_for('uploaded_file', filename='image1.jpg'),
#                            image2_url=url_for('uploaded_file', filename='image2.jpg'),
#                            result=verification_result)
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# if __name__ == '__main__':
#     app.run(debug=True)
