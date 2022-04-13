import os
import logging
import socketserver
from threading import Condition
from http import server
from flask import Flask, render_template, request, session, redirect, url_for, flash
import picamera 

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

# Defining Path of Assets Folder
UPLOAD_FOLDER = './flask_app/assets/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# Creating Application Object Using Flask
app = Flask(__name__, static_url_path='/assets', static_folder='./flask_app/assets', template_folder='./flask_app')

# Configuring the Assets Path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to Set Cache-Configuration to 'no-cache' in our case
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

# Routing default to 'index.html'
@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/camera.html')
def camera():
    return render_template('camera.html')

@app.route('/capture.html')
def capture():
    return render_template('capture.html')

@app.route('/camera_shoot', methods=['POST', 'GET'])
def camera_shoot():


    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        #camera.rotation = 90
        camera.start_recording(output, format='mjpeg')


@app.route('/capture', methods=['POST', 'GET'])
def capture():

    with picamera.PiCamera() as camera:
        camera.resolution=(640,480)
        camera.framerate=24
        camera.capture('./flask_app/assets/images/image.jpg')





























if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True, port=80)
    app.run(host='0.0.0.0', port=8080)

