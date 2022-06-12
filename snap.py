from cv2 import VideoCapture, imwrite



cam = VideoCapture(0)

_, dat = cam.read()

imwrite("./angry.png", dat)
