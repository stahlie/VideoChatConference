import cv2
import zmq
import base64
import numpy as np,time
import pyshine as ps
# www.pyshine.com
context = zmq.Context()
client_socket = context.socket(zmq.SUB)
client_socket.connect("tcp://10.0.0.110:5555")
client_socket.setsockopt_string(zmq.SUBSCRIBE,optval='')
fps=0
st=0
frames_to_count=20
cnt=0
while True:
    if cnt == frames_to_count:
        try:

            fps = round(frames_to_count/(time.time()-st))
            st = time.time()
            cnt=0
        except:
            pass
    cnt+=1
    frame = client_socket.recv()
    img = base64.b64decode(frame)
    npimg = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    text  =  'FPS: '+str(fps)
    source = ps.putBText(source,text,text_offset_x=20,text_offset_y=30,background_RGB=(10,20,222))
    time.sleep(0.01)
    cv2.imshow("client image", source)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
cv2.destroyAllWindows()
