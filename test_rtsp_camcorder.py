import pytest
import os
import time
from datetime import datetime, timedelta
from logic import CamCorder
import random
import cv2


#######################
###     Fixtures    ###
#######################

@pytest.fixture
def config():
    return dict({
        "auth": {
            "protocol": "rtsp",
            "username": "root",
            "password": "toor",
            "ip": "192.168.178.24",
            "stream": "stream1"
        },
        "resolution": {
            "width": 1920,
            "height": 1080,
        },
        "fps": 15,
        "duration": 1,
        "output_directory": "__media_test__{0}".format(str(random.randint(10000, 16000))),
        "automatic_deletion": True,
        "delete_older_than": 7
    })


@pytest.fixture
def recorder(config):
    return CamCorder(config)


#######################
###      Tests      ###
#######################

# Test create_cv2_stream method
def test_create_cv2_stream(recorder):
    cap = recorder.create_cv2_stream()

    assert cap is not None
    assert type(cap) == cv2.VideoCapture


# Test create_video_writer method
def test_create_video_writer(recorder):
    output = recorder.create_video_writer()

    assert output is not None
    assert type(output) == cv2.VideoWriter


# Test automatic directory deletion functionality/logic
def test_automatic_directory_deletion(recorder):
    output_dir = recorder.configuration['output_directory']

    if os.path.exists(output_dir):
        os.rmdir(output_dir)

    os.makedirs(output_dir)

    today = datetime.now()
    delete_older_than = timedelta(
        days=recorder.configuration['delete_older_than'])

    # Create three old directories
    for x in range(3):
        old_date = today - delete_older_than - timedelta(days=x + 1)
        old_directory = os.path.join(
            output_dir, old_date.strftime('%Y-%m-%d'))

        os.makedirs(old_directory)

    # Create two recent directories
    for x in range(2):
        recent_date = today - timedelta(days=x)
        recent_directory = os.path.join(
            output_dir, recent_date.strftime('%Y-%m-%d'))
        os.makedirs(recent_directory)

    # Perform automatic directory deletion
    recorder.delete_old_folders()

    # Assertions
    for x in range(3):
        old_date = today - delete_older_than - timedelta(days=x + 1)
        old_directory = os.path.join(
            output_dir, old_date.strftime('%Y-%m-%d'))

        # Assert that old directories have been deleted
        assert not os.path.exists(old_directory)

    # Check if recent directories still exist
    for x in range(2):
        recent_date = today - timedelta(days=x)
        recent_directory = os.path.join(
            output_dir, recent_date.strftime('%Y-%m-%d'))

        # Assert that newer directories have not been touched
        assert os.path.exists(recent_directory)
