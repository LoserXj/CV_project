from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import cv2
import os
from deepface import DeepFace
import numpy as np
import base64

def draw_source_rectangle(image, df):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    x, y, w, h = df.iloc[0]['source_x'], df.iloc[0]['source_y'], df.iloc[0]['source_w'], df.iloc[0]['source_h']
    cv2.rectangle(image, pt1 = (x, y), pt2 =(x + w, y + h), color = (255, 0, 0), thickness = min(image.shape[0], image.shape[1]) // 100)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def draw_target_rectangle(image, df):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    x, y, w, h = df.iloc[0]['target_x'], df.iloc[0]['target_y'], df.iloc[0]['target_w'], df.iloc[0]['target_h']
    cv2.rectangle(image, pt1 = (x, y), pt2 =(x + w, y + h), color = (255, 0, 0), thickness = min(image.shape[0], image.shape[1]) // 100)
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def find():
    image = request.files['image'].read()
    image_array = np.asarray(bytearray(image), dtype=np.uint8())
    original_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    dfs = DeepFace.find(img_path = original_image, db_path = "./my_db")
    original_image = draw_source_rectangle(original_image, dfs[0])
    file_path = dfs[0].iloc[0]['identity']
    db_img = cv2.imread(file_path)
    db_img = draw_target_rectangle(db_img, dfs[0])
    _, buffer = cv2.imencode('.jpg', original_image)
    byte_data = buffer.tobytes()
    # 将字节数据编码为base64字符串
    encoded_original_image = base64.b64encode(byte_data).decode('utf-8')
    _, buffer = cv2.imencode('.jpg', db_img)
    byte_data = buffer.tobytes()
    # 将字节数据编码为base64字符串
    encoded_db_image = base64.b64encode(byte_data).decode('utf-8')    
    # 构建返回的数据结构
    response_data = {
        'original_image': encoded_original_image,
        'db_image': encoded_db_image,
        'distance': round(dfs[0].iloc[0]['distance'], 3)
    }
    return jsonify(response_data)

