# SECURITY-CAMERA

## Overview
Send images when motion is detected by web camera and sends images to Slack channel.

## Directory Structure
```
.
├── LICENSE
├── README.md
├── requirements.txt
├── security_camera.py
├── settings.py
├── (.env)
└── .env.sample
```

## Requirement
I recommend Python 3.6 or higher. 

## Usage
1. First of all, you need to make Slack bot, so create it from the following link: https://YOUR-CHANNEL-NAME.slack.com/apps  
Then, search for "Bots" and proceed to "Add Configuration".  
User name can be anything, but here it is "security-camera".  

2. Click "Add bot integration" to get API Token, and add it to the .env file.  
Please decide the icon etc. freely and save settings.

3. Next, you need to get Slack channel ID.  
There are several ways, but you can access the web version of Slack, select the channel that this bot will post in your workspace, and get alphanumeric characters of about nine letters from the URL, so copy and paste it to .env file.

4. This completes the setting of the Bot, but of course please run the following command to align Python libraries:
    ```
    pip3 install -r requirements.txt
    ```

5. When you can start up:
    ```
    python3 security_camera.py
    ```
    Let's first take a picture of the landscape by pressing space. If this application detects more than a certain amount of error with the landscape, a notification will be sent to Slack.

6. If you get an opencv error at runtime here, you may be cured by manually re-installing `opencv-python` and `opencv-contrib-python`.


## Licence
[MIT License](https://github.com/nazboost/image-collector/blob/master/LICENSE)

## Author
[Nazna](https://github.com/nazboost)
