from flask import Flask, render_template, Response
import redis

redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page
    """

    return render_template('index.html')

def gen():
    """Video streaming generator function
    """
    
    while True:
        frame = redis_server.get('camera1')
        # print(frame)
        # if frame:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # else:
            # continue

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag
    """

    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
