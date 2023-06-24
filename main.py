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

    # Video resolution
    "resolution": {
        "width": 1920,
        "height": 1080,
    },

    # Frames per second
    "fps": 15,

    # Duration in minutes before a new video gets created
    "duration": 1,

    # Output directory
    "output_directory": "media",

    # When enabled, the script will also automate the deletion of old directories
    "automatic_deletion": False,

    # Automatically delete files older than x days
    "delete_older_than": 21
})

recorder = CamCorder(configuration)
recorder.start()
