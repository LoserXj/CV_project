from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import cv2
import os
from deepface import DeepFace
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def save_image(file, filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    # 获取上传的文件
    image1 = request.files['image1']
    image2 = request.files['image2']

    # 保存图像
    path1 = save_image(image1, 'image1.jpg')
    path2 = save_image(image2, 'image2.jpg')

    # 验证两张图像是否属于同一个人
    result = DeepFace.verify(img1_path=path1, img2_path=path2)
    # 根据验证结果设置结果文本
    verification_result = "YES" if result[0] else "NO"

    # return render_template('result.html', image1_url=url_for('uploaded_file', filename='image1.jpg'),
    #                        image2_url=url_for('uploaded_file', filename='image2.jpg'),
    #                        result=verification_result)
    return jsonify({
        'image1_url': url_for('uploaded_file', filename='image1.jpg'),
        'image2_url': url_for('uploaded_file', filename='image2.jpg'),
        'result': verification_result
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
