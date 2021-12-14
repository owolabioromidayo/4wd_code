from flask import Flask, Response, render_template
import picamera, io

app = Flask(__name__)


im_width = 1280 
im_height = 720
camera = picamera.PiCamera(resolution=(im_width, im_height), framerate = 60 )
stream = io.BytesIO()


@app.route('/')
def index():
    return render_template('index.html')




def generate_img():
    for _ in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
        try:
            stream.seek(0)
            image = cv2.imdecode(np.frombuffer(stream.read(), np.uint8), 1)

            stream.seek(0)
            stream.truncate()

            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        except Exception as e:
            print("Error: No Image")
            return
        



@app.route('/get_img')
def get_img():
    return Response(generate_img(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)