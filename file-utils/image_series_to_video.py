'''
Images to Video Convertor
Author: Fraser Love, me@fraser.love
Created: 2021-07-06
Latest Release: v1.0.3, 2023-08-10
Python: v3.10.12
Dependencies: opencv-python

Converts multiple images into on video with a desired length and framerate.

Usage:  Update the below variables to produce the desired video output. Note that if a duration other than 0 is used then
        the framerate variable will be overridden.
'''

import cv2, os, functools, time


# Numerically sorts filenames
def image_sort_name(x, y):
    x = int(x.split(".")[0])
    y = int(y.split(".")[0])
    return x - y


# Sort filenames by their last edited datetime stamp
def image_sort_datetime(x, y):
    x = os.path.getmtime(x)
    y = os.path.getmtime(y)
    return x - y


class Convertor:
    def __init__(self, input_dir, input_ext, output, framerate=60, sort_type='numeric', duration=0):
        self.images = []
        self.start_time = None
        self.video = None
        self.image_dir = input_dir  # Directory where images are located.
        self.image_ext = input_ext  # File extension of the images.
        self.output = output + '.mp4'  # Name of the output video.
        self.framerate = framerate  # Framerate will be overridden if a desired duration is not 0.
        self.sort_type = sort_type  # Type of image name sorting (alphabetic, numeric, datetime).
        self.duration = duration  # Duration of video in seconds, adjusts framerate accordingly.

    def get_images(self):
        # Get the images from input directory
        try:
            for file in os.listdir(self.image_dir):
                if file.endswith(self.image_ext):
                    self.images.append(file)
        except:
            print('Error, no directory called {} found'.format(self.image_dir))
            exit(0);

    def sort(self):
        # Sort the files found in the directory
        if self.sort_type == "numeric":
            if self.images[0].split(".")[0].isnumeric():
                self.images = sorted(self.images, key=functools.cmp_to_key(image_sort_name))
            else:
                print("Error, failed to sort numerically, switching to alphabetic sort")
                self.images.sort()

        elif self.sort_type == "datetime":
            self.images = [self.image_dir + "/" + image for image in self.images]
            self.images = sorted(self.images, key=functools.cmp_to_key(image_sort_datetime))
            self.images = ["".join(im.split(self.image_dir + "/")[1:]) for im in self.images]

        elif self.sort_type == "alphabetic":
            self.images.sort()

    def find_duration(self):
        # Change framerate to fit the duration in seconds if a duration has been specified.
        if self.duration != 0:
            self.framerate = int(len(self.images) / int(self.duration))
            print("Framerate adjusted to {} for {}s duration".format(self.framerate, self.duration))

    def video_setup(self):
        # Determine the width and height from the first image
        image_path = os.path.join(self.image_dir, self.images[0])
        frame = cv2.imread(image_path)
        height, width, channels = frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec to create mp4 videos
        self.video = cv2.VideoWriter(self.output, fourcc, self.framerate, (width, height))

    def write_to_video(self):
        for n, image in enumerate(self.images):
            image_path = os.path.join(self.image_dir, image)
            frame = cv2.imread(image_path)
            self.video.write(frame)

            completion = n * 100 / len(self.images)
            if completion % 5 == 0:
                print('{} ({:.0f}% complete)'.format(self.output, completion))

        self.video.release()
        cv2.destroyAllWindows()

    def convert(self):
        self.start_time = time.time()
        self.get_images()
        self.sort()
        self.find_duration()
        self.video_setup()
        self.write_to_video()
        dt = time.time() - self.start_time
        print("Completed conversion of {}, took {:.0f}s".format(self.output, dt))


if __name__ == "__main__":
    convertor = Convertor('./images', 'jpg', 'output')
    convertor.convert()