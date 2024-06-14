from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify, make_response
import cv2
import os
from deepface import DeepFace
import numpy as np

from extract_faces import extract_faces
from verify import verify
from animegan2.test import animate

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def jump_to_start():
    return send_from_directory('static/start', 'start.html')

@app.route('/verify')
def jump_to_verify():
    return send_from_directory('static/verify', 'verify.html')

@app.route('/extract_faces')
def jump_to_extract_faces():
    return send_from_directory('static/extract_faces', 'extract_faces.html')

@app.route('/animate')
def jump_to_animate():
    return send_from_directory('static/animate', 'animate.html')

@app.route('/extract_faces', methods=['POST'])
def function_extract_faces():
    return extract_faces()

@app.route('/verify', methods=['POST'])
def function_verify():
    return verify()

@app.route('/animate', methods=['POST'])
def function_animate():
    return animate()

if __name__ == '__main__':
    app.run(debug=True)