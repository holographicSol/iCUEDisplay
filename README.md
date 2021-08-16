
--------------------------------------------------------------------------------------------------------------------------------------------
      iCUEDisplay

Converts a Corsair K95 Platinum into a HUD.

There may be further feature updates in the future.

Google Drive Early Releases: https://drive.google.com/drive/folders/1xHeI_X5vnpKqQ3vkBz6hw97RnqaPwWNl?usp=sharing

--------------------------------------------------------------------------------------------------------------------------------------------
![DEMO IMAGE](/image/icue_demo_image_0.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE OVERVIEW

[BASIC UTILIZATION:
CPU Utilization Monitor
DRAM Utilization Monitor
VRAM Utilization Monitor]

[DISK UTILIZATION:
Disk Read Monitor (Disks Mounted With Letter A:\ - Z:\)
Disk Write Monitor (Disks Mounted With Letter A:\ - Z:\)
Disk Mount Monitor (Disks Mounted With Letter A:\ - Z:\)]

[NETWORK TRAFFIC:
Network Sent Bytes to Terabytes (Overkill)
Network Received Bytes To Terrabytes (Overkill)]

[NETWORKING:
Internet Connection Status (Online, Offline, Intermittent)
Network Shares (Remote IPC, Remote Admin, Default share(s), User Defined Shares)]

[EVENT NOTIFICATION & EVENT RESPONSE (Advanced Users)]

[SETTINGS:
A Backlight When Needed and automatic backlight
Automatic Startup
Start Minimized]

[OTHER FEATURES (Backend):
Threads running designed for keyboard are stopped if keyboard removed while threads designed for mouse continue and vis versa. Threads will
be restarted automatically when device plugged back in]

--------------------------------------------------------------------------------------------------------------------------------------------
      BASIC UTILIZATION
[CPU UTILIZATION: Utilization is displayed in stages of 25% on Numpad 1, 4, 7, NumLock.]

[DRAM UTILIZATION: Utilization is displayed in stages of 25% on Numpad 2, 5, 8, ForwardSlash.]

[VRAM UTILIZATION: Utilization is displayed in stages of 25% on Numpad 3, 6, 9, Asterisk.]

[CPU TEMPERATURE]

[VRAM TEMPERATURE]

![DEMO IMAGE](/image/icue_demo_image_1.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      DISKS UTILIZATION
[Displays information accross the alpha keys about disks mounted with a letter. Alpha keys are reserved for this feature]

[DISKS MOUNTED: Displayed in Blue when disk letter is mounted]

[DISK READS: Displayed in Yellow by default]

[Disk Writes: Displayed in Red by default]

![DEMO IMAGE](/image/icue_demo_image_2.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      NETWORKING TRAFFIC
[ADAPTER SELECTION: Choose which network adapter to monitor sent/received bytes]

[BYTES SENT: Displayed on keys F1-F10. F1-F9 Displayes number of bytes/KB/MB/GB/TB sent while F10 displays unit/ten/hundred/thousand+]

[BYTES RECEIVED: Displayed on keys 1-0. 1-9 Displayes number of bytes/KB/MB/GB/TB sent while 0 displays unit/ten/hundred/thousand+]

![DEMO IMAGE](/image/icue_demo_image_3.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      NETWORKING
[INTERNET CONNECTION STATUS (KEYBOARD): ESC Key]

[INTERNET CONNECTION STATUS (MOUSE): Choose which LED (Tested with Scimitar Elite)]

[NETWORK SHARE (Remote IPC): Dipslayed on PRINTSCREEN key when shared]

[NETWORK SHARE (Remote Admin): Displayed on SCROLLLOCK key when shared]

[NETWORK SHARE (Default Share): Displayed on PAUSEBREAK key when shared]

[NETWORK SHARE (NON-DEFAULT): Displayed on HOME key when shared]

![DEMO IMAGE](/image/icue_demo_image_4.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      EVENT NOTIFICATION & EVENT RESPONSE
[Enables slightly advanced users to create small programs that simply write True to any event_notification_gx.dat file in the /data directory
to receive an event notification (blinking G key) for any possible reason and if requested execute code for event response]

[EVENT NOTIFICATION: A G key will begin blinking until user short or long presses the G key]

[EVENT NOTIFICATION & EVENT RESPONSE: Short pressing the Blinking G key will remove the notification and execute code/start file while a long
press (0.75 seconds +) will remove the notification and not run the directed code/file]

[EVENT RESPONSE: Requires event notification to be enabled and is also designed to only run code/file once per notification event]

![DEMO IMAGE](/image/icue_demo_image_5.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      SETTINGS
[AUTOMATIC BACKLIGHT: User may set a time for the backlight to turn on and off and may optionally enable the backlight manually]

![DEMO IMAGE](/image/icue_demo_image_6.png)

--------------------------------------------------------------------------------------------------------------------------------------------
      BUG REPORTS & FEATURE REQUESTS
[Bug reports & Feature requests may be submitted to holographic.sol@gmail.com and will gratefully accepted and reviewed]

--------------------------------------------------------------------------------------------------------------------------------------------
      REQUIREMENTS
[PYTHON: Written in Python 3.9]

[OS: Windows 10]

[Run as Admin]

[Resolution: 1920x1080 or higher is recommended]

--------------------------------------------------------------------------------------------------------------------------------------------
      DEVELOPERS
[IF running iCUEDisplay.py then for certain media playback functionality you may need to modify a module as follows:]
[1. Open __init__.py in site-packages\winrt]
[2. Replace line 'winrt.init_apartment()' with 'pythoncom.CoInitialize()']
