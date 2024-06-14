from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import cv2
import os
from deepface import DeepFace
import numpy as np



def verify():
    # 获取上传的文件
    image1 = request.files['image1'].read()
    image1 = np.asarray(bytearray(image1), dtype=np.uint8())
    image1 = cv2.imdecode(image1, cv2.IMREAD_COLOR)
    
    image2 = request.files['image2'].read()
    image2 = np.asarray(bytearray(image2), dtype=np.uint8())
    image2 = cv2.imdecode(image2, cv2.IMREAD_COLOR)

    # 验证两张图像是否属于同一个人
    result = DeepFace.verify(img1_path=image1, img2_path=image2)
    # 根据验证结果设置结果文本
    verification_result = "YES" if result['verified'] else "NO"
    
    return jsonify({
        'result': verification_result,
        'distance': round(result['distance'], 3)
    })
