# README
# To start the server in development moder run:
# flask --app app run --host=0.0.0.0

import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import api.CoordinateConverter as Cc

UPLOAD_FOLDER = "/srvgentjkd98p2/K/Projects/2025-03 Project FWO SB Jelle/7.Data/UploadedSessions/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'obj', 'fbx', 'json', 'ttl'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables
referencePosition = 0
errorRadius = 0
dirname = os.path.dirname(__file__)

# The main page to show stuff 
@app.route("/")
def index():
    return render_template('index.html')

# Create a sub selection of the data with given global coordinates
@app.route("/geolocation", methods=['GET', 'POST'])
def geo_location():
    global referencePosition, errorRadius
    if request.method == 'POST':
        data = request.get_json(force = True)
        print("Got a GeoLocation POST request:")
        print(data)
        newPosition = data["position"]
        errorRadius = float(data["errorRadius"])
        type = data["coordinateSystem"]
        referencePosition = Cc.ConvertFromJson(newPosition,type)
        response = "Data succesfully received and converted to: " + str(referencePosition)
        print(response)
        return response
    else:
        print("got a GeoLocation GET request")
        return render_template('geolocation.html', refPos = str(referencePosition), erRad = errorRadius)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a sub selection of the data with given global coordinates
@app.route("/add-session", methods=['GET', 'POST'])
def add_session():
    if request.method == 'POST':
        
        print(request.files)
        
        # check if the post request has a valid session name
        if 'session' not in request.form:
            print('No session name attached')
            return redirect(request.url)
        
        sessionName = request.form.get("session")
        print('Session name:' + sessionName)

        if sessionName == "" or not sessionName:
            print('Invalid session name')
            return redirect(request.url)

        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part in files')
            return redirect(request.url)

        uploaded_files = request.files.getlist("file")
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if len(uploaded_files) == 0:
            print('File array is empty')
            return redirect(request.url)
        else:
            
            savePath = os.path.join(dirname,app.config['UPLOAD_FOLDER'], secure_filename(sessionName))
            try: 
                os.mkdir(savePath) 
            except OSError as error: 
                print("folder already exists: " + str(error))  
            for file in uploaded_files:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(savePath, filename))
            return "<h2>Succes!</h2>"
    else:
        return render_template('add-session.html')
