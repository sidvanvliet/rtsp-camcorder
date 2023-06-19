from logic import CamCorder

configuration = dict({
    # Authentication
    "auth": {
        "protocol": "rtsp",
        "username": "",
        "password": "",
        "ip": "192.168.178.1",
        "stream": "stream1"
    },

    # Output dir
    "output_dir": "media",

    # Video resolution
    "resolution": {
        "width": 1920,
        "height": 1080,
    },

    # Frames per second
    "fps": 15,

    # Duration in minutes
    "duration": 1,

    # Automatically delete files older than x days, set to 0 to disable
    "delete_older_than": 21
})

recorder = CamCorder(configuration)
recorder.start()
