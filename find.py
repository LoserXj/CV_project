from flask import Flask, request, jsonify, render_template
from deepface import DeepFace

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find', methods=['POST'])
def find():
    try:
        target_image = request.files['target_image']
        database_image = request.files['database_image']

        target_image_path = f"./uploads/{target_image.filename}"
        database_image_path = f"./uploads/{database_image.filename}"

        target_image.save(target_image_path)
        database_image.save(database_image_path)

        result = DeepFace.find(img_path=target_image_path, db_path=database_image_path, model_name='VGG-Face')

        return jsonify(result)
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
   app.run(debug=True)

