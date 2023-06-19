import os
import shutil
import cv2
import time
from datetime import datetime
import os


class CamCorder:
    configuration = {}

    def __init__(self, config):
        print('CamCorder initializing...')
        self.configuration = config

    def start(self):
        print('Started recording...')

        # Create CV2 stream
        cap = cv2.VideoCapture(
            '{protocol}://{username}:{password}@{ip}/{stream}'.format(**self.configuration['auth']))

        cap.set(3, self.configuration['resolution']['width'])
        cap.set(4, self.configuration['resolution']['height'])

        # Create video writer (H264)
        fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
        dated_subfolder = time.strftime('%Y-%m-%d', time.localtime())

        if not os.path.exists(os.sep.join([self.configuration['output_dir'], dated_subfolder])):
            os.makedirs(os.sep.join(
                [self.configuration['output_dir'], dated_subfolder]))

        output = cv2.VideoWriter(os.sep.join([self.configuration['output_dir'], dated_subfolder, time.strftime('%H-%M-%S', time.localtime()) + '.avi']), fourcc, self.configuration['fps'],
                                 (self.configuration['resolution']['width'], self.configuration['resolution']['height']))

        # Recording loop
        start_time = time.time()
        capture_duration = self.configuration['duration']
        i = 1

        while cap.isOpened():
            e1 = cv2.getTickCount()
            ret, frame = cap.read()

            duration = time.time() - start_time
            minutes = int(duration / 60)

            # write text to the frame
            cv2.imshow("RTSP Camcorder by github.com/sidvanvliet", frame)

            # Write frame to video writer
            if round(minutes) < capture_duration:
                output.write(frame)

            # Flush video writer and reinitialize
            elif round(minutes) == capture_duration:
                print("Recorded {file} (length: {duration} minute)".format(
                    file=os.sep.join(
                        [self.configuration['output_dir'], dated_subfolder, time.strftime('%H-%M-%S', time.localtime()) + '.avi']),
                    duration=self.configuration['duration'])
                )

                # Lets use the while loop to also check for any old folders to delete, if enabled
                days_to_keep = self.configuration['delete_older_than']

                if days_to_keep > 0:
                    for subdir in os.listdir(self.configuration['output_dir']):
                        subdir_path = os.path.join(
                            self.configuration['output_dir'], subdir)
                        if os.path.isdir(subdir_path):
                            try:
                                subdir_date = datetime.strptime(
                                    subdir, '%Y-%m-%d')
                            except ValueError:
                                print(
                                    f"Skipping {subdir_path}: invalid date format")
                                continue
                            if (datetime.now() - subdir_date).days > days_to_keep:
                                print(f"Deleting {subdir_path}")
                                shutil.rmtree(subdir_path)

                output.release()
                i += 1
                capture_duration += 1

                # Reinitialize video writer (flush)
                # Create video writer (H264)
                dated_subfolder = time.strftime('%Y-%m-%d', time.localtime())

                if not os.path.exists(os.sep.join([self.configuration['output_dir'], dated_subfolder])):
                    os.makedirs(os.sep.join(
                        [self.configuration['output_dir'], dated_subfolder]))

                # TODO: merge this with line 34
                output = cv2.VideoWriter(os.sep.join([self.configuration['output_dir'], dated_subfolder, time.strftime('%H-%M-%S', time.localtime()) + '.avi']), fourcc, self.configuration['fps'],
                                         (self.configuration['resolution']['width'], self.configuration['resolution']['height']))

        else:
            # Something went wrong, the stream being down being the most likely cause
            print("Unable to open {stream}".format(
                stream=self.configuration['auth']['ip']))

        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        output.release()

        # Final goodbye 🫡
        print('Script finished.')
