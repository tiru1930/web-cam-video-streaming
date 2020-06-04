from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from io import StringIO
import io 
import base64
from PIL import Image
import imutils
import cv2
import numpy as np 
from flask_cors import CORS

async_mode = None

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode,cors_allowed_origins="*")
# socketio = SocketIO(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html',async_mode=socketio.async_mode,cors_allowed_origins="*")

@socketio.on('image')
def image(data_image):

    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b).convert('RGB')


    # Process the image frame
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    # frame = imutils.resize(frame, width=1000)
    # frame = cv2.flip(frame, 1)

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (40,40)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2

    cv2.putText(frame,'processed in backend!', 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    
    imgencode = cv2.imencode('.jpg', frame)[1]
   

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)

if __name__ == '__main__':
    socketio.run(app,debug=False,host="0.0.0.0")