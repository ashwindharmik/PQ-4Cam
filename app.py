import cv2
from flask import Flask, Response, render_template

app = Flask(__name__)

# Define the video capture objects for each camera
# cap1 = cv2.VideoCapture(0)
# cap2 = cv2.VideoCapture(0)
# cap3 = cv2.VideoCapture(0)
# cap4 = cv2.VideoCapture(0)
# 
# # Set the resolution for all cameras
# cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap3.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap3.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# cap4.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap4.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def concat_vh(list_2d):
    # return final image
    return cv2.vconcat([cv2.hconcat(list_h) 
                        for list_h in list_2d])
    

@app.route('/')
def index():
    return render_template('index.html')



def get_frame():
    
    cap1 = cv2.VideoCapture("1.mp4")
    cap2 = cv2.VideoCapture("2.mp4")
    cap3 = cv2.VideoCapture("3.mp4")
    cap4 = cv2.VideoCapture("4.mp4")
    # cap1 = cv2.VideoCapture(0)
    # cap2 = cv2.VideoCapture(0)
    # cap3 = cv2.VideoCapture(0)
    # cap4 = cv2.VideoCapture(0)
    
    while True:
        # Capture frames from each camera
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()
        
        if not ret1 or not ret2 or not ret3 or not ret4:
            break

        # Resize the frames to the same size and merge them horizontally
        frame1 = cv2.resize(frame1, (320, 240))
        frame2 = cv2.resize(frame2, (320, 240))
        frame3 = cv2.resize(frame3, (320, 240))
        frame4 = cv2.resize(frame4, (320, 240))
        
        # Combine frames into one image
        # combined_frame = cv2.hconcat([frame1, frame2, frame3, frame4])
        combined_frame = concat_vh([[frame1, frame2],
                                    [frame3, frame4]])

        # Convert the combined frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', combined_frame)

        # Yield the JPEG data as bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        
    # Release the video capture resources
    cap1.release()
    cap2.release()
    cap3.release()
    cap4.release()
    
    
@app.route('/video_feed')
def video_feed():
    # return the response generated along with the specific media
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
