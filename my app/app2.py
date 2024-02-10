
import cv2
import os
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator,img_to_array,load_img
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input, decode_predictions

model = load_model('new_predict.h5')

UPLOAD_FOLDER = './my app/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def prediction(path):
    ref = {0: 'Ants', 1: 'Bees', 2: 'Beetle', 3: 'Caterpillar', 4: 'Earthworms', 5: 'Earwig', 6: 'Grasshopper',
           7: 'Moth', 8: 'Slug', 9: 'Snail', 10: 'Wasp', 11: 'Weevil'}
    
    img = load_img(path,target_size=(128,128))
    img = img_to_array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img,axis=0)
    pred = np.argmax(model.predict(img))
    return ref[pred]

@app.route('/')
def home():
    return render_template('Pest_Detect.html')

@app.route('/prediction',methods=['POST'])
def predict():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        pred = prediction(UPLOAD_FOLDER+'/'+filename)
        return render_template('Pest_Detect.html',org_img_name=filename,prediction=pred)


if __name__ == '__main__':
    app.run(debug=True)