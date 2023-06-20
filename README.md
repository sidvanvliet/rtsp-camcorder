<img src="https://i.imgur.com/0HyWl6w.png" alt="RTSP Camcorder logo">

# RTSP-Camcorder

## Overview
An adaptable Python script designed to effortlessly capture and store RTSP streams. This versatile tool empowers users to record CCTV feeds onto a (personal) server, providing an alternative to costly subscriptions and eliminating concerns over the storage of sensitive footage in third-party cloud platforms.

## Deployment Recommendation

To ensure the highest possible uptime and smooth operation of the application, I highly recommend using PM2 for deployment and management. PM2 is a process manager for Node.js applications that offers advanced features for process monitoring, automatic restarts, and load balancing.

### PM2 benefits

- **Process Monitoring:** PM2 provides real-time monitoring of the application, allowing you to track resource usage, performance metrics, and logs. This helps in identifying and addressing any issues promptly.

- **Automatic Restarts:** In the event of a crash or unexpected termination, PM2 can automatically restart the application, ensuring minimal downtime and uninterrupted service.

- **Load Balancing:** PM2 offers load balancing capabilities, allowing you to scale the application horizontally across multiple instances. This helps distribute the processing load and improves overall system performance.

### Deploy RTSP-Camcorder using PM2

1. Install PM2 globally on your server by running: `npm install pm2 -g`

2. Clone the project repository: `git clone https://github.com/sidvanvliet/rtsp-camcorder.git`

3. Navigate to the project directory: `cd rtsp-camcorder`

4. Install project dependencies: `pip install -r requirements.txt`

5. Start the application using PM2: `pm2 start main.py --name rtsp-camcorder`

6. Monitor the application's status and logs: `pm2 monit`

For more advanced configuration options and customization, please refer to the [PM2 documentation](https://pm2.io/docs/runtime/overview/).

By using PM2 for deployment, you can ensure the reliability and continuous operation of the RTSP-Camcorder, enabling you to capture and process video feeds with the highest possible uptime.
