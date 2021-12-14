from flask import Flask, Response, render_template
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2, time, socket

app = Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


def generate_img():
    try:
        camera = PiCamera()
        rawCapture = PiRGBArray(camera)
        time.sleep(0.1)
        camera.capture(rawCapture, format="bgr")
        image = rawCapture.array
        camera.close()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
    except Exception as e:
        print("Error: No Image")
        return
    

@app.route('/get_img')
def get_img():
    return Response(generate_img(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(host=get_local_ip(), port=8000, debug=True)
