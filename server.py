import cv2,imutils
import zmq
import base64,time
import queue,threading
# www.pyshine.com
context = zmq.Context()
server_socket = context.socket(zmq.PUB)
server_socket.bind("tcp://10.0.0.110:5555")
camera = True
if camera == True:
	vid = cv2.VideoCapture(0)
else:
	vid = cv2.VideoCapture('videos/sample-mp4-file.mp4')

def pyshine_video_queue(vid):
	
	frame = [0]
	q = queue.Queue(maxsize=10)
	def getAudio():
		while (vid.isOpened()):
			try:
				img, frame = vid.read()
				frame = imutils.resize(frame,width=640)
				q.put(frame)
			except:
				pass
			
	thread = threading.Thread(target=getAudio, args=())
	thread.start()
	return q

q = pyshine_video_queue(vid)

while True:
	frame = q.get()
	encoded, buffer = cv2.imencode('.jpg', frame,[cv2.IMWRITE_JPEG_QUALITY,80])
	data = base64.b64encode(buffer)
	print(server_socket.send(data))
	cv2.imshow("server image", frame)
	key = cv2.waitKey(1) & 0xFF
	time.sleep(0.01)
	if key  == ord('q'):
		break

vid.release()
cv2.destroyAllWindows()