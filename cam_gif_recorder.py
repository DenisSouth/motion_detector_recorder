import cv2
import os
import datetime
import imageio

directory = "record/"
fps = 5

class GifRec:
    def __init__(self):
        self.frames = []
        self.file_path = None

    def start(self, file_path):
        self.file_path = file_path

    def stop(self):
        with imageio.get_writer(self.file_path, mode="I") as writer:
            for idx, frame_ in enumerate(self.frames):
                print("Adding frame to GIF file: ", idx + 1)
                writer.append_data(frame_)

    def add_frame(self, my_frame):
        self.frames.append(my_frame)


if not os.path.exists(directory):
    os.makedirs(directory)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, fps)

gif = GifRec()

is_recording = False
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)

        k = cv2.waitKey(30) & 0xff

        if is_recording:
            print("==ADD==")
            gif.add_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if k == 27:  # press 'esc' to quit
            break

        elif k == 113:  # press 'q' to record
            if not is_recording:
                print("==START==")
                is_recording = True
                path = directory + 'video_' + str(datetime.datetime.now().strftime("%H_%M_%S")) + '.gif'
                gif.start(file_path=path)

        elif k == 119:  # press 'w' to stop recording
            if is_recording:
                print("==STOP==")
                is_recording = False
                gif.stop()

cap.release()
cv2.destroyAllWindows()
