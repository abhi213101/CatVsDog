from flask import Flask, render_template, request, flash, redirect
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename

Model = load_model("./CatVsDog.h")

#init flask app

UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('homePage.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img = cv2.imread(path,cv2.IMREAD_COLOR)
            img = cv2.resize(img, (100,100))
            os.remove(path)
            img = np.array(img)
            img = img.reshape((1,100,100,3))
            img = img/255
            out = Model.predict(img)
            if(out[0][0] < out[0][1]):
                return render_template("result.html", percentage=str(out[0][1]*100)[:5] + "%", src="https://www.pngitem.com/pimgs/m/79-794322_shenandoah-valley-animal-services-dog-icon-icon-dog.png", animal="DOG")

            else:
                return render_template("result.html", percentage=str(out[0][0]*100)[:5] + "%", src="https://www.vippng.com/png/detail/365-3650931_shenandoah-valley-animal-services-cat-icon-smiley.png", animal="CAT")
        
        else:
            return 'Incorrect File Format'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
