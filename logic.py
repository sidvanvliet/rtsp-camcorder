import os
import shutil
import cv2
import time
from datetime import datetime


class CamCorder:
    configuration = {}

    # Constructor
    def __init__(self, config):
        print('CamCorder initializing...')
        self.configuration = config

    # Start application
    def start(self):
        print('Started recording...')
        cap = self.create_cv2_stream()
        output = self.create_video_writer()

        start_time = time.time()
        capture_duration = self.configuration['duration']

        # Recording loop
        while cap.isOpened():
            ret, frame = cap.read()

            duration = time.time() - start_time
            minutes = int(duration / 60)

            # Open OpenCV window
            cv2.imshow("RTSP Camcorder by github.com/sidvanvliet", frame)

            # Split video into chunks of self.configuration['duration'] minutes
            if round(minutes) < capture_duration:
                self.write_frame(output, frame)

            elif round(minutes) == capture_duration:
                output.release()

                # When enabled, clean up old directories
                if self.configuration['automatic_deletion'] == True:
                    self.delete_old_folders()

                capture_duration += 1
                output = self.create_video_writer()

        # Release resources
        self.release_resources(cap, output)

        # Final goodbye 🫡
        print('Script finished.')

    # Generate OpenCV stream
    def create_cv2_stream(self):
        cap = cv2.VideoCapture(
            '{protocol}://{username}:{password}@{ip}/{stream}'.format(**self.configuration['auth']))

        # Set resolution
        cap.set(3, self.configuration['resolution']['width'])
        cap.set(4, self.configuration['resolution']['height'])

        return cap

    # Generate video writer (using H.264 codec)
    def create_video_writer(self):
        fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')

        dated_subfolder = time.strftime('%Y-%m-%d', time.localtime())
        output_directory = self.configuration['output_directory']

        # Ensure the output directory exists, creating it if it doesn't
        if not os.path.exists(os.path.join(output_directory, dated_subfolder)):
            os.makedirs(os.path.join(output_directory, dated_subfolder))

        output_path = os.path.join(output_directory, dated_subfolder, time.strftime(
            '%H-%M-%S', time.localtime()) + '.avi')

        output = cv2.VideoWriter(output_path, fourcc, self.configuration['fps'],
                                 (self.configuration['resolution']['width'], self.configuration['resolution']['height']))

        return output

    # Ouput each frame onto the video
    def write_frame(self, output, frame):
        output.write(frame)

    # (Optional) Automates the deletion of old directories
    def delete_old_folders(self):
        days_to_keep = self.configuration['delete_older_than']
        output_directory = self.configuration['output_directory']

        if days_to_keep > 0:
            for subdir in os.listdir(output_directory):
                subdir_path = os.path.join(output_directory, subdir)
                if os.path.isdir(subdir_path):
                    try:
                        subdir_date = datetime.strptime(subdir, '%Y-%m-%d')
                    except ValueError:
                        print(f"Skipping {subdir_path}: invalid date format")
                        continue

                    if (datetime.now() - subdir_date).days > days_to_keep:
                        print(f"Deleting {subdir_path}")
                        shutil.rmtree(subdir_path)

    # Release resources
    def release_resources(self, cap, output):
        cap.release()
        cv2.destroyAllWindows()
        output.release()
