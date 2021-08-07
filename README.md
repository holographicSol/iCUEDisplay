
--------------------------------------------------------------------------------------------------------------------------------------------
      iCUEDisplay

Converts a Corsair K95 Platinum into a HUD.

Project in early development and UI does not necessarliy reflect the final products image. Currently the UI is purely logic and has minimun
aesthetic design.
Features being refined and added daily. Existing features may be more complex in coming updates.

Google Drive Early Releases: https://drive.google.com/drive/folders/1xHeI_X5vnpKqQ3vkBz6hw97RnqaPwWNl?usp=sharing

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE OVERVIEW

[FEATURE 0:
CPU Utilization Monitor
DRAM Utilization Monitor
VRAM Utilization Monitor]

[FEATURE 1:
Disk Read Monitor (Disks Mounted With Letter A:\ - Z:\)
Disk Write Monitor (Disks Mounted With Letter A:\ - Z:\)
Disk Mount Monitor (Disks Mounted With Letter A:\ - Z:\)]

[FEATURE 2:
Network Sent Bytes to Terabytes (Overkill)
Network Received Bytes To Terrabytes (Overkill)]

[FEATURE 3:
Internet Connection Status (Online, Offline, Intermittent)]

[FEATURE 4:
Network Shares (Remote IPC, Remote Admin, Default share(s), User Defined Shares)]

[FEATURE 5:
Event Notifiaction & Event Response (Advanced Users)]

[FEATURE 6:
A Backlight When Needed and automatic backlight]

[OTHER FEATURES (Backend):
Threads running designed for keyboard are stopped if keyboard removed while threads designed for mouse continue and vis versa. Threads will
be restarted automatically when device plugged back in]

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 0 CPU DRAM & VRAM UTILIZATION
[CPU UTILIZATION: Utilization is displayed in stages of 25% on Numpad 1, 4, 7, NumLock.]

[DRAM UTILIZATION: Utilization is displayed in stages of 25% on Numpad 2, 5, 8, ForwardSlash.]

[VRAM UTILIZATION: Utilization is displayed in stages of 25% on Numpad 3, 6, 9, Asterisk.]

[CPU TEMPERATURE: Keypad Minus, Yellow, Amber, Red]

[DRAM TEMPERATURE: Keypad Plus, Yellow, Amber, Red]

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 1 DISKS UTILIZATION
[Displays information accross the alpha keys about disks mounted with a letter. Alpha keys are reserved for this feature]

[DISKS MOUNTED: Displayed in Blue when disk letter is mounted]

[DISK READS: Displayed in Yellow by default]

[Disk Writes: Displayed in Red by default]

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 2 NETWORKING SENT/RECEIVED BYTES
[ADAPTER SELECTION: Choose which network adapter to monitor sent/received bytes]

[BYTES SENT: Displayed on keys F1-F10. F1-F9 Displayes number of bytes/KB/MB/GB/TB sent while F10 displays unit/ten/hundred/thousand+]

[BYTES RECEIVED: Displayed on keys 1-0. 1-9 Displayes number of bytes/KB/MB/GB/TB sent while 0 displays unit/ten/hundred/thousand+]


--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 3 INTERNET CONNECTION STATUS
[KEYBOARD: ESC Key]

[MOUSE: Choose which LED (Tested with Scimitar Elite)]

[ONLINE: Green]

[INTERMITTENT: Amber]

[OFFLINE: Red]



--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 4 NETWORK SHARES
[Remote IPC: Dipslayed on PRINTSCREEN key when shared]

[Remote Admin: Displayed on SCROLLLOCK key when shared]

[Default Share: Displayed on PAUSEBREAK key when shared]

[NON-DEFAULT: Displayed on HOME key when shared]

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 5 EVENT NOTIFICATION & EVENT RESPONSE
[Enables slightly advanced users to create small programs that simply write True to any event_notification_gx.dat file in the /data directory
to receive an event notification (blinking G key) for any possible reason and if requested execute code for event response]

[EVENT NOTIFICATION: A G key will begin blinking until user short or long presses the G key]

[EVENT NOTIFICATION & EVENT RESPONSE: Short pressing the Blinking G key will remove the notification and execute code/start file while a long
press (0.75 seconds +) will remove the notification and not run the directed code/file]

[EVENT RESPONSE: Requires event notification to be enabled and is also designed to only run code/file once per notification event]

--------------------------------------------------------------------------------------------------------------------------------------------
      FEATURE 6 BACKLIGHT AND AUTOMATIC BACKLIGHT
[AUTOMATIC BACKLIGHT: User may set a time for the backlight to turn on and off and may optionally enable the backlight manually]

--------------------------------------------------------------------------------------------------------------------------------------------
      BUG REPORTS & FEATURE REQUESTS
[Bug reports & Feature requests may be submitted to holographic.sol@gmail.com and will gratefully accepted and reviewed]

--------------------------------------------------------------------------------------------------------------------------------------------
      REQUIREMENTS
[PYTHON: Written in Python 3.9]

[OS: Windows 10]

[NOTES 0: Right click OpenHardwareMonitor.dll in /py/bin/ select Properties, General Tab, Click Unblock and apply (skip if running exe/py as Admin)]

[NOTES 1: Then Run exe/.py as Admin]

--------------------------------------------------------------------------------------------------------------------------------------------

