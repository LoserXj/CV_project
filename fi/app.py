
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
from deepface import DeepFace
import pandas as pd

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'static/uploads/'
#########
#路径
#########
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform DeepFace find
        try:
            dfs = DeepFace.find(img_path=filepath, db_path=UPLOAD_FOLDER)

            # Converting DataFrame to HTML
            results = [df.to_html(classes='data', header="true") for df in dfs]
            return render_template('result.html', tables=results)
        except Exception as e:
            return str(e)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
