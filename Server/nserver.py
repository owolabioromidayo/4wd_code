from flask import Flask, Response, render_template, request
from camera import VideoCamera
import cv2, time, socket, os, threading

from Motor import Motor
from ADC import Adc
from servo import Servo
from Ultrasonic import Ultrasonic
from Buzzer import Buzzer


pi_camera = VideoCamera(flip=False)
app = Flask(__name__)

PWM = Motor()
adc = Adc()
pwm = Servo()
_ultrasonic = Ultrasonic()
_buzzer = Buzzer()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]

@app.route('/')
def index():
    return render_template('index.html') 

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test', methods=['POST'])
def test():
    args = [
        'Led',
        'Motor',
        'Ultrasonic',
        'Infrared',
        'Servo',
        'ADC',
        'Buzzer'
    ]
    arg = request.form['arg']
    print(f"Testing {arg}")

    if arg == "ALL":
        for _arg in args:
            print(f"Testing {arg}")
            os.system(f"python test.py {arg}")
 
    elif arg in args:
        os.system(f"python test.py {arg}")
    
    else:
        print(f"TEST : Argument {arg} does not exist")
    return "Done"

@app.route('/move', methods=['POST'])
def move():
    args = {
        'LEFT'      : PWM.goLeft, 
        'RIGHT'     : PWM.goRight , 
        'FORWARD'   : PWM.goForward, 
        'BACKWARDS' : PWM.goBackwards, 
        'STOP' :  PWM.stop
    }
    arg = request.form['arg']
    print(f"Moving : {arg}")

    if arg in args.keys():
        args[arg]()
    else:
        print(f"MOVE : Argument {arg} does not exist")

    return "Done"


@app.route('/servo', methods=['POST'])
def servo():
    args = {
        'LEFT' :  lambda: pwm.nudgeHoriz(-5), 
        'RIGHT' : lambda: pwm.nudgeHoriz(5), 
        'UP' :    lambda: pwm.nudgeVert(5), 
        'DOWN' :  lambda: pwm.nudgeVert(-5), 
        'HOME' :  pwm.home
    }
    arg = request.form['arg']
    print(f"Moving : {arg}")

    if arg in args.keys():
        args[arg]()
    else:
        print("Argument does not exist")
    return "Done" 


@app.route('/battery_percentage', methods=['GET'])
def battery_percentage():
    adc_power = adc.recvADC(2)*3
    percent_power= int( (adc_power-7)/1.40*100 )
    return f"{percent_power}"


@app.route('/ultrasonic', methods=['GET'])
def ultrasonic():
    return f"{_ultrasonic.get_distance()}"


@app.route('/buzzer', methods=['POST'])
def buzzer():
    arg  = request.form['arg']
    print(f"Buzzing for {arg} seconds.")
    _buzzer.run('1')
    time.sleep(int(arg))
    _buzzer.run('0')

    return "Done"


if __name__ == '__main__':
    app.run(host=get_local_ip(), debug=False)
