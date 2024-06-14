from flask import Flask, request, make_response, send_from_directory,render_template, jsonify
import cv2
import os
from deepface import DeepFace
import numpy as np


# def draw_rectangle(image, dic_list):
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     for dic in dic_list:
#         region = dic['region']
#         x, y, w, h =  region['x'], region['y'], region['w'], region['h']
#         cv2.rectangle(image, pt1 = (x, y), pt2 =(x + w, y + h), color = (255, 0, 0), thickness = min(image.shape[0], image.shape[1]) // 100)
#         text_position = (x, y - 10)  # 根据框的位置调整文本位置
#         # cv2.putText(image, f"Conf: {confidence:.2f}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     return image

## 人脸分析函数
def analyze_face():
    image = request.files['image'].read()
    image = np.asarray(bytearray(image), dtype=np.uint8())
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    result = DeepFace.analyze(image,actions=['emotion', 'age', 'gender', 'race'])
    return jsonify({
        'result': result
    })
