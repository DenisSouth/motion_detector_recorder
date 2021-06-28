import cv2
import os
import datetime


class VidRec:
    def __init__(self, height, width, fps=20, codec='mp4v'):
        self.fourcc = cv2.VideoWriter_fourcc(*codec)  # XVID
        self.width = width
        self.height = height
        self.fps = fps
        self.videoWriter = None
        self.file_path = None

    def start(self, file_path):
        self.file_path = file_path
        self.videoWriter = cv2.VideoWriter(self.file_path, self.fourcc, self.fps, (self.width, self.height))

    def stop(self):
        self.videoWriter.release()

    def add_frame(self, my_frame):
        self.videoWriter.write(my_frame)


directory = "record/"
if not os.path.exists(directory):
    os.makedirs(directory)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = cap.read()
h, w = frame.shape[:2]

video = VidRec(height=h, width=w)

is_recording = False

while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)

        k = cv2.waitKey(30) & 0xff

        if is_recording:
            print("==ADD==")
            video.add_frame(frame)

        if k == 27:  # press 'esc' to quit
            break

        elif k == 113:  # press 'q' to record
            if not is_recording:
                print("==START==")
                is_recording = True
                path = directory + 'video_' + str(datetime.datetime.now().strftime("%H_%M_%S")) + '.mp4'
                video.start(file_path=path)

        elif k == 119:  # press 'w' to stop recording
            if is_recording:
                print("==STOP==")
                is_recording = False
                video.stop()

cap.release()
cv2.destroyAllWindows()
