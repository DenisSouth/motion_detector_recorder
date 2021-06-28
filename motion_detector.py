import numpy as np
import cv2
import os
import datetime

# directory for records
directory = "record/"

# number of frames in line with detected movement
length_thresh = 5

# percent of changed pixels per bitmap
bmp_thresh = 0.005

# width of frame for analysing
target_frame_width = 500


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    h_, w_ = image.shape[:2]
    if width is None and height is None:
        return image

    if width is None:
        r = height / float(h_)
        dim = (int(w_ * r), height)

    else:
        r = width / float(w_)
        dim = (width, int(h_ * r))

    return cv2.resize(image, dim, interpolation=inter)


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


if not os.path.exists(directory):
    os.makedirs(directory)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

_, frame_orig = cap.read()
frame_grey = cv2.cvtColor(frame_orig, cv2.COLOR_BGR2GRAY)
frame_grey = image_resize(frame_grey, width=target_frame_width)
frame_grey = cv2.GaussianBlur(frame_grey, (5, 5), 0)
frame_temp = frame_grey

frame_length = frame_grey.shape[0] * frame_grey.shape[1]
frame_counter = 0


h, w = frame_orig.shape[:2]
video = VidRec(height=h, width=w)

is_recording = False

while True:
    ret, frame = cap.read()
    if ret:
        ret, frame = cap.read()
        frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_grey = image_resize(frame_grey, width=target_frame_width)
        frame_grey = cv2.GaussianBlur(frame_grey, (5, 5), 0)
        frame_delta = cv2.absdiff(frame_grey, frame_temp)
        frame_start = frame_grey

        # compare last and current frame
        frame_delta = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        # count percent of moved pixels
        delta_percent = (np.count_nonzero(frame_delta) + 1) / (frame_length + 1)

        frame_counter = max(0, frame_counter + (1 if delta_percent > bmp_thresh else -5))

        if frame_counter > length_thresh:
            if not is_recording:
                print("==START==")
                is_recording = True
                path = directory + 'video_' + str(datetime.datetime.now().strftime("%H_%M_%S")) + '.mp4'
                video.start(file_path=path)
            else:
                print(f"{frame_counter} ==ADD==")
                video.add_frame(frame)

        elif frame_counter == 0:
            if is_recording:
                print(f"==STOP== {video.file_path}")
                is_recording = False
                video.stop()

        cv2.imshow('delta', frame_delta)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

cap.release()
cv2.destroyAllWindows()
