from flask import Flask, Response, render_template, request
from slambot.camera import VideoCamera
import time, socket, os, threading

from slambot.actuators.motor import Motor
from slambot.sensors.adc import ADC
from slambot.actuators.servo import Servo
from slambot.sensors.ultrasonic import Ultrasonic
from slambot.actuators.buzzer import Buzzer
from slambot.tracking.infrared import Line_Tracking
from slambot.tracking.line import Follower

from slambot.tests.physical import TestPhy

pi_camera = VideoCamera(flip=False)
app = Flask(__name__)

PWM = Motor()
adc = ADC()
pwm = Servo()
_ultrasonic = Ultrasonic()
_buzzer = Buzzer()


exit_handler = threading.Event()

threads = {}
thread_states = {
    "line_tracking_is_active" : False,
    "line_following_is_active" : False
}

_test = TestPhy()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    return s.getsockname()[0]


def exec_line_tracking():
    # follow black lines
    infrared = Line_Tracking()
    infrared.run_thread(exit_handler)

def exec_line_following():
    #follow yellow line
    follower = Follower()
    follower.run_thread(exit_handler)


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
    args = {
        'Led':_test.test_led,
        'Motor': _test.test_motors,
        'Ultrasonic': _test.test_ultrasonic,
        'Infrared': _test.test_line_tracking,
        'Servo': _test.test_servos,
        'ADC': _test.test_adc,
        'Buzzer': _test.test_buzzer
    }
    arg = request.form['arg']
    print(f"Testing {arg}")

    if arg == "ALL":
        for k,v in args:
            print(f"Testing {arg}")
            v()
 
    elif arg in args:
        args[arg]()
    
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
        'HOME' :  pwm.home,
        
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

@app.route('/line_tracking', methods=['POST'])
def line_tracking():
    arg = request.form['arg']
    if arg == 'START':
        if not thread_states["line_tracking_is_active"]:
            thread_states["line_tracking_is_active"] = True

            threads["line_tracking"] = threading.Thread(target=exec_line_tracking)
            threads['line_tracking'].start()
            threads['line_tracking'].join()
        else:
            print("already active")
            return "Error: service already running"
    elif arg == 'STOP':
        exit_handler.set()
        thread_states['line_tracking_is_active'] = False
    
    else:
        print(f"Error: Argument: {arg} does not exist")
        return f"Error: Argument: {arg} does not exist"
        


@app.route('/line_following', methods=['POST'])
def line_following():
    arg = request.form['arg']
    if arg == 'START':
        if not thread_states["line_following_is_active"]:
            thread_states["line_following_is_active"] = True

            threads["line_following"] = threading.Thread(target=exec_line_following)
            threads['line_following'].start()
            threads['line_following'].join()
        else:
            print("already active")
            return "Error: service already running"
    elif arg == 'STOP':
        exit_handler.set()
        thread_states['line_following_is_active'] = False
    
    else:
        print(f"Error: Argument: {arg} does not exist")
        return f"Error: Argument: {arg} does not exist"
        


if __name__ == '__main__':
    app.run(host=get_local_ip(), debug=False)
