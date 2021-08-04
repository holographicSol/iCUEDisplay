"""
Written by Benjamin Jack Cullen aka Holographic_Sol
"""
import os
import sys
import time
import GPUtil
import psutil
import pythoncom
import unicodedata
import win32con
import win32api
import win32process
import win32com.client
import datetime
import subprocess
import distutils.dir_util
from cuesdk import CueSdk
from cuesdk import CueSdk, CorsairEventId
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QCursor, QFont, QPixmap
from PyQt5.QtCore import Qt, QThread, QSize, QPoint, QCoreApplication, QTimer, QEvent, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QDesktopWidget, QLineEdit, QComboBox, QFileDialog

info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0

sdk = ''

print('-- [CueSdk] searching for CueSDK in: bin\\CUESDK.x64_2017.dll')
if os.path.exists('.\\bin\\CUESDK.x64_2017.dll'):
    print('-- [CueSDK]: found')
    sdk = CueSdk(os.path.join(os.getcwd(), 'bin\\CUESDK.x64_2017.dll'))
elif not os.path.exists('.\\bin\\CUESDK.x64_2017.dll'):
    print('-- [CueSDK]: missing from iCUEDisplay bin directory')


def entry_sequence_0():
    print('-- [entry_sequence_0]: plugged in')
    connected = sdk.connect()
    sdk.request_control()
    if connected:
        device = sdk.get_devices()
        print('device:', device)
        i = 0
        for _ in device:
            led_position = sdk.get_led_positions_by_device_index(i)
            led_position_str = str(led_position).split('), ')
            for _ in led_position_str:
                var = _.split()
                var_1 = var[1].replace('>:', '')
                itm = [{int(var_1): (90, 90, 90)}]
                sdk.set_led_colors_buffer_by_device_index(i, itm[0])
                sdk.set_led_colors_flush_buffer()
            i += 1


entry_sequence_0()


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())


def initialize_scaling_dpi():
    print('-- [initialize_scaling_dpi]: initializing:')
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    print('-- [initialize_scaling_dpi]: QT_AUTO_SCREEN_SCALE_FACTOR = 1')
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        print('-- [initialize_scaling_dpi]: AA_EnableHighDpiScaling: True')
    elif not hasattr(Qt, 'AA_EnableHighDpiScaling'):
        print('-- [initialize_scaling_dpi]: AA_EnableHighDpiScaling: False')
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        print('-- [initialize_scaling_dpi]: AA_UseHighDpiPixmaps: True')
    elif not hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        print('-- [initialize_scaling_dpi]: AA_UseHighDpiPixmaps: False')


def initialize_priority():
    priority_classes = [win32process.IDLE_PRIORITY_CLASS,
                        win32process.BELOW_NORMAL_PRIORITY_CLASS,
                        win32process.NORMAL_PRIORITY_CLASS,
                        win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                        win32process.HIGH_PRIORITY_CLASS,
                        win32process.REALTIME_PRIORITY_CLASS]
    pid = win32api.GetCurrentProcessId()
    print('-- [initialize_priority] pid:', pid)
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priority_classes[4])
    print('-- [initialize_priority]: settings win32process priority class:', priority_classes[4])

ui_feature_page = 0
backlight_time_0 = ''
backlight_time_1 = ''
hdd_bytes_type_w = ''
hdd_bytes_type_r = ''
hdd_bytes_str = ''

bool_event_notification_g1 = False
bool_event_notification_g2 = False
bool_event_notification_g3 = False
bool_event_notification_g4 = False
bool_event_notification_g5 = False
bool_event_notification_g6 = False

bool_allow_g1_short = False
bool_allow_g2_short = False
bool_allow_g3_short = False
bool_allow_g4_short = False
bool_allow_g5_short = False
bool_allow_g6_short = False

bool_switch_event_notification_g1 = False
bool_switch_event_notification_g2 = False
bool_switch_event_notification_g3 = False
bool_switch_event_notification_g4 = False
bool_switch_event_notification_g5 = False
bool_switch_event_notification_g6 = False

bool_switch_event_notification_run_g1 = False
bool_switch_event_notification_run_g2 = False
bool_switch_event_notification_run_g3 = False
bool_switch_event_notification_run_g4 = False
bool_switch_event_notification_run_g5 = False
bool_switch_event_notification_run_g6 = False

str_event_notification_run_path_g1 = ''
str_event_notification_run_path_g2 = ''
str_event_notification_run_path_g3 = ''
str_event_notification_run_path_g4 = ''
str_event_notification_run_path_g5 = ''
str_event_notification_run_path_g6 = ''

bool_switch_display_disk_mount = True
bool_switch_backlight = False
bool_switch_show_discrete = True
bool_switch_startup_exclusive_control = False
bool_switch_startup_autorun = False
bool_switch_backlight_auto = False
bool_switch_startup_minimized = False
bool_switch_startup_net_con = False
bool_switch_startup_net_con_ms = False
bool_switch_startup_net_con_kb = False
bool_switch_startup_hdd_read_write = False
bool_switch_startup_cpu_util = False
bool_switch_startup_dram_util = False
bool_switch_startup_vram_util = False
bool_switch_startup_net_traffic = False
bool_switch_startup_net_share_mon = False

bool_backend_enum_kb = True
bool_backend_enum_ms = True
bool_backend_install = False
bool_backend_allow_display = False
bool_backend_icue_connected = False
bool_backend_icue_connected_previous = None
bool_backend_config_read_complete = False
bool_backend_valid_network_adapter_name = False

thread_compile_devices = []
thread_disk_rw = []
thread_cpu_util = []
thread_dram_util = []
thread_vram_util = []
thread_net_traffic = []
thread_net_connection = []
thread_net_share = []
thread_sdk_event_handler = []
thread_sdk_event_handler_read_file_events = []
thread_g1_notify = []
thread_g2_notify = []
thread_g3_notify = []
thread_g4_notify = []
thread_g5_notify = []
thread_g6_notify = []
thread_backlight_auto = []

event_filter_self = []

devices_kb = []
devices_ms = []
devices_kb_selected = 0
devices_ms_selected = 0
devices_kb_name = []
devices_ms_name = []
devices_previous = []
devices_gpu_selected = int()
devices_network_adapter_name = ""

corsairled_id_num_cpu = [116,113, 109, 103]
corsairled_id_num_dram = [117,114, 110, 104]
corsairled_id_num_vram = [118,115, 111, 105]
corsairled_id_num_hddreadwrite = [38, 55, 53, 40, 28, 41, 42, 43, 33, 44, 45, 46, 57, 56, 34, 35, 26, 29, 39, 30, 32, 54, 27, 52, 31, 51]
corsairled_id_num_netrcv = [14, 15, 16, 17, 18, 19, 20, 21, 22]
corsairled_id_num_netsnt = [2, 3, 4, 5, 6, 7, 8, 9, 10]
corsairled_id_num_netrcv_utype = 23
corsairled_id_num_netsnt_utype = 11
corsairled_id_num_netcon_ms = int()
corsairled_id_num_netcon_kb = int()
corsairled_id_num_netshare = [74, 75, 76, 78]
corsairled_id_num_kb_complete = []
corsairled_id_num_ms_complete = []

corsairled_id_name_cpu = ['CorsairLedId.K_Keypad1',
                          'CorsairLedId.K_Keypad4',
                          'CorsairLedId.K_Keypad7',
                          'CorsairLedId.K_NumLock']

corsairled_id_name_dram = ['CorsairLedId.K_Keypad2',
                           'CorsairLedId.K_Keypad5',
                           'CorsairLedId.K_Keypad8',
                           'CorsairLedId.K_KeypadSlash']

corsairled_id_name_vram = ['CorsairLedId.K_Keypad3',
                           'CorsairLedId.K_Keypad6',
                           'CorsairLedId.K_Keypad9',
                           'CorsairLedId.K_KeypadAsterisk']

corsairled_id_name_hddreadwrite = ['CorsairLedId.K_A', 'CorsairLedId.K_B', 'CorsairLedId.K_C', 'CorsairLedId.K_D',
                                   'CorsairLedId.K_E', 'CorsairLedId.K_F', 'CorsairLedId.K_G', 'CorsairLedId.K_H',
                                   'CorsairLedId.K_I', 'CorsairLedId.K_J', 'CorsairLedId.K_K', 'CorsairLedId.K_L',
                                   'CorsairLedId.K_M', 'CorsairLedId.K_N', 'CorsairLedId.K_O', 'CorsairLedId.K_P',
                                   'CorsairLedId.K_Q', 'CorsairLedId.K_R', 'CorsairLedId.K_S', 'CorsairLedId.K_T',
                                   'CorsairLedId.K_U', 'CorsairLedId.K_V', 'CorsairLedId.K_W', 'CorsairLedId.K_X',
                                   'CorsairLedId.K_Y', 'CorsairLedId.K_Z']

corsairled_id_name_netrcv = ['CorsairLedId.K_1', 'CorsairLedId.K_2', 'CorsairLedId.K_3',
                             'CorsairLedId.K_4', 'CorsairLedId.K_5', 'CorsairLedId.K_6',
                             'CorsairLedId.K_7', 'CorsairLedId.K_8', 'CorsairLedId.K_9']

corsairled_id_name_netsnt = ['CorsairLedId.K_F1', 'CorsairLedId.K_F2', 'CorsairLedId.K_F3',
                             'CorsairLedId.K_F4', 'CorsairLedId.K_F5', 'CorsairLedId.K_F6',
                             'CorsairLedId.K_F7', 'CorsairLedId.K_F8', 'CorsairLedId.K_F9']

corsairled_id_name_netsnt_utype = 'CorsairLedId.K_F10'
corsairled_id_name_netrcv_utype = 'CorsairLedId.K_0'
corsairled_id_name_netshare = ['CorsairLedId.K_PrintScreen', 'CorsairLedId.K_ScrollLock', 'CorsairLedId.K_PauseBreak', 'CorsairLedId.K_Home']

alpha_str = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z']
# for _ in alpha_str:
#     corsairled_id_num_hddreadwrite.append('pending')

sdk_color_backlight_on = [15, 15, 20]
sdk_color_backlight = (0, 0, 0)
sdk_color_cpu_on = [255, 255, 255]
sdk_color_dram_on = [255, 255, 255]
sdk_color_vram_on = [255, 255, 255]
sdk_color_hddwrite_on = [255, 255, 255]
sdk_color_hddread_on = [255, 255, 255]

sdk_color_net_traffic_bytes = [255, 7, 0]
sdk_color_net_traffic_kb = [73, 255, 0]
sdk_color_net_traffic_mb = [0, 0, 255]
sdk_color_net_traffic_gb = [0, 255, 255]
sdk_color_net_traffic_tb = [255, 255, 255]
sdk_color_netshare_on = [165, 255, 0]

sdk_color_net_traffic_utype_0 = [255, 7, 0]
sdk_color_net_traffic_utype_1 = [0, 0, 255]
sdk_color_net_traffic_utype_2 = [0, 255, 255]
sdk_color_net_traffic_utype_3 = [255, 255, 255]

sdk_color_g1_event_notification = [255, 255, 255]
sdk_color_g2_event_notification = [255, 255, 255]
sdk_color_g3_event_notification = [255, 255, 255]
sdk_color_g4_event_notification = [255, 255, 255]
sdk_color_g5_event_notification = [255, 255, 255]
sdk_color_g6_event_notification = [255, 255, 255]

timing_cpu_util = 1.0
timing_dram_util = 1.0
timing_vram_util = 1.0
timing_hdd_util = 0.0
timing_net_traffic_util = 0.0

config_data = ['sdk_color_cpu_on: 255,255,0',
               'timing_cpu_util: 0.1',
               'cpu_startup: true',
               'sdk_color_dram_on: 255,255,0',
               'timing_dram_util: 2.0',
               'dram_startup: true',
               'sdk_color_vram_on: 255,255,0',
               'timing_vram_util: 2.0',
               'vram_startup: true',
               'devices_gpu_selected: 0',
               'sdk_color_hddwrite_on: 255,0,0',
               'sdk_color_hddread_on: 255,255,0',
               'timing_hdd_util: 0.0',
               'hdd_startup: true',
               'exclusive_access: true',
               'start_minimized: false',
               'run_startup: false',
               'timing_net_traffic_util: 0.0',
               'network_adapter_startup: false',
               'devices_network_adapter_name: ',
               'bool_switch_startup_net_con_ms: true',
               'bool_switch_startup_net_con_kb: true',
               'corsairled_id_num_netcon_ms: 0',
               'bool_switch_startup_net_con: true',
               'netshare_startup: true',
               'sdk_color_netshare_on: 255,15,100',
               'bool_switch_backlight: false',
               'sdk_color_backlight_on: 63,63,63',
               'bool_switch_backlight_auto: false',
               'bool_switch_event_notification_g1: false',
               'bool_switch_event_notification_g2: false',
               'bool_switch_event_notification_g3: false',
               'bool_switch_event_notification_g4: false',
               'bool_switch_event_notification_g5: false',
               'bool_switch_event_notification_g6: false',
               'bool_switch_event_notification_run_g1: false',
               'bool_switch_event_notification_run_g2: false',
               'bool_switch_event_notification_run_g3: false',
               'bool_switch_event_notification_run_g4: false',
               'bool_switch_event_notification_run_g5: false',
               'bool_switch_event_notification_run_g6: false',
               'str_event_notification_run_path_g1: ',
               'str_event_notification_run_path_g2: ',
               'str_event_notification_run_path_g3: ',
               'str_event_notification_run_path_g4: ',
               'str_event_notification_run_path_g5: ',
               'str_event_notification_run_path_g6: ']


def create_new():
    global bool_backend_install
    print('-- [create_new]: started')
    config_line_missing = []
    config_line_file = []
    count_missing = 0

    if not os.path.exists('./config.dat'):
        print('-- [create_new]: creating configuration file')
        open('./config.dat', 'w').close()
        with open('./config.dat', 'a') as fo:
            for _ in config_data:
                fo.writelines(_+'\n')
        fo.close()

    elif os.path.exists('./config.dat'):
        print('-- checking configuration file')
        print('-- checking', len(config_data), ' configuration items')

        with open('./config.dat', 'r') as fo:
            i = 0
            for line in fo:
                line = line.strip()
                line_var = line.split(':')
                config_line_file.append(line_var[0])
                i += 1
        fo.close()

        print('-- configuration file items:', len(config_line_file))

        for _ in config_data:
            config_line_var = _.split(':')
            config_line_var = config_line_var[0]
            if config_line_var not in config_line_file:
                print('-- item', config_line_var, 'not in configuration file or data incorrect in configuration file')
                config_line_missing.append(_)
                count_missing += 1
            else:
                print('-- correct:', config_line_var)
        print('-- missing items:', count_missing)
        for _ in config_line_missing:
            print('-- attempting to update configuration file:', _)
            with open('./config.dat', 'a') as fo:
                fo.writelines(_+'\n')
        fo.close()

    if not os.path.exists('./iCUEDisplay.vbs') or not os.path.exists('./iCUEDisplay.bat'):
        cwd = os.getcwd()
        print('-- [create_new] current working directory:', cwd)
        path_for_in_bat = os.path.join('"' + cwd + '\\iCUEDisplay.exe"')
        path_to_bat = cwd + '\\iCUEDisplay.bat'
        print('-- [create_new] creating batch file:', path_to_bat)
        path_for_in_vbs = 'WshShell.Run chr(34) & "' + path_to_bat + '" & Chr(34), 0'
        print('-- [creating new] creating vbs file: ./iCUEDisplay.vbs')
        open('./iCUEDisplay.bat', 'w').close()
        open('./iCUEDisplay.vbs', 'w').close()
        with open('./iCUEDisplay.bat', 'a') as fo:
            fo.writelines(path_for_in_bat)
        fo.close()
        with open('./iCUEDisplay.vbs', 'a') as fo:
            fo.writelines('Set WshShell = CreateObject("WScript.Shell")\n')
            fo.writelines(path_for_in_vbs + '\n')
            fo.writelines('Set WshShell = Nothing\n')
        fo.close()
        try:
            path = os.path.join(cwd + '\\iCUEDisplay.lnk')
            target = cwd + '\\iCUEDisplay.vbs'
            icon = cwd + './icon.ico'
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = cwd
            shortcut.IconLocation = icon
            shortcut.save()
        except Exception as e:
            print('-- [create_new] Error:', e)
        time.sleep(1)
        print('-- [create_new]: checking existence of created files')
        if os.path.exists('./iCUEDisplay.exe') and os.path.exists(path_to_bat) and os.path.exists('./iCUEDisplay.vbs'):
            print('-- [create_new]: files exist')
            if os.path.exists('./iCUEDisplay.lnk'):
                print('-- [create_new]: starting program')
                os.startfile(cwd+'./iCUEDisplay.lnk')
                time.sleep(2)
                bool_backend_install = True

    distutils.dir_util.mkpath('./data/')
    if not os.path.exists('./data/event_notification_g1.dat'):
        open('./data/event_notification_g1.dat', 'w').close()
    if not os.path.exists('./data/event_notification_g2.dat'):
        open('./data/event_notification_g2.dat', 'w').close()
    if not os.path.exists('./data/event_notification_g3.dat'):
        open('./data/event_notification_g3.dat', 'w').close()
    if not os.path.exists('./data/event_notification_g4.dat'):
        open('./data/event_notification_g4.dat', 'w').close()
    if not os.path.exists('./data/event_notification_g5.dat'):
        open('./data/event_notification_g5.dat', 'w').close()
    if not os.path.exists('./data/event_notification_g6.dat'):
        open('./data/event_notification_g6.dat', 'w').close()
    time.sleep(2)


class ObjEveFilter(QObject):

    def eventFilter(self, obj, event):
        global event_filter_self
        obj_eve = obj, event

        # Uncomment This Line To See All Object Events
        # print('-- ObjEveFilter(QObject).eventFilter(self, obj, event):', obj_eve)

        """There is no Qt Layout for Qt objects and with everything made, I am trying to break the program.
        Re-scaling will need to occur when windows scaling is changed. The following code is a temporary solution &
        should not compensate permanently for Qt objects being placed inside a Qt layout or alternatively by doing
        ones own calculations to re-scale the application when scaling is changed. 
        """
        if str(obj_eve[1]).startswith('<PyQt5.QtGui.QResizeEvent'):
            print('-- [ObjEveFilter]: Handling resize event')
        return False


class App(QMainWindow):
    cursorMove = QtCore.pyqtSignal(object)

    def __init__(self):
        super(App, self).__init__()
        global bool_backend_install, event_filter_self
        create_new()
        if bool_backend_install is True:
            sys.exit()

        initialize_scaling_dpi()
        initialize_priority()

        self.prev_pos = ()
        self.cursorMove.connect(self.handleCursorMove)
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.pollCursor)
        self.timer.start()
        self.cursor = None

        self.setWindowIcon(QIcon('./icon.ico'))
        self.title = 'iCUE Display'
        print('-- [App.__init__] setting self.title as:', self.title)
        self.setWindowTitle(self.title)

        self.width = 390
        self.height = 304
        self.height_discrete = 180
        self.pos_w = ((QDesktopWidget().availableGeometry().width() / 2) - (self.width / 2))
        self.pos_h = ((QDesktopWidget().availableGeometry().height() / 2) - (self.height_discrete / 2))
        self.pos_w = int(self.pos_w)
        self.pos_h = int(self.pos_h)
        print('-- [App.__init__] setting window dimensions:', self.width, self.height_discrete)
        print('-- [App.__init__] setting window position:', self.pos_w, self.pos_h)
        self.setGeometry(int(self.pos_w), int(self.pos_h), self.width, self.height_discrete)

        event_filter_self.append(self)
        self.filter = ObjEveFilter()
        self.installEventFilter(self.filter)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setPalette(p)

        self.font_s7b = QFont("Segoe UI", 7, QFont.Bold)
        self.font_s8b = QFont("Segoe UI", 8, QFont.Bold)
        self.font_s10b = QFont("Segoe UI", 10, QFont.Bold)

        self.tooltip_style = """QToolTip {background-color: rgb(35, 35, 35);
                           color: rgb(200, 200, 200);
                           border-top:0px solid rgb(35, 35, 35);
                           border-bottom:0px solid rgb(35, 35, 35);
                           border-right:0px solid rgb(0, 0, 0);
                           border-left:0px solid rgb(0, 0, 0);}"""
        self.cmb_style = """QComboBox {background-color: rgb(15, 15, 15);
                   color: rgb(200, 200, 200);
                   border-top:2px solid rgb(15, 15, 15);
                   border-bottom:2px solid rgb(15, 15, 15);
                   border-right:2px solid rgb(15, 15, 15);
                   border-left:2px solid rgb(15, 15, 15);}"""

        self.lbl_stat_con_style_sub = """QLabel {background-color: rgb(0, 0, 0);
                   color: rgb(200, 200, 200);
                   border-top:2px solid rgb(15, 15, 15);
                   border-bottom:2px solid rgb(15, 15, 15);
                   border-right:2px solid rgb(15, 15, 15);
                   border-left:2px solid rgb(15, 15, 15);}"""

        self.lbl_data_style_title = """QLabel {background-color: rgb(0, 0, 0);
                   color: rgb(220, 220, 220);
                   border-top:0px solid rgb(30, 30, 30);
                   border-bottom:0px solid rgb(0, 0, 0);
                   border-right:0px solid rgb(0, 0, 0);
                   border-left:0px solid rgb(0, 0, 0);}"""

        self.lbl_settings_border_style = """QLabel {background-color: rgb(0, 0, 0);
                           color: rgb(0, 0, 0);
                           border-top:2px solid rgb(15, 15, 15);
                           border-bottom:2px solid rgb(15, 15, 15);
                           border-right:2px solid rgb(15, 15, 15);
                           border-left:2px solid rgb(15, 15, 15);}"""

        self.lbl_data_style_sep = """QLabel {background-color: rgb(33, 33, 33);
                           color: rgb(220, 220, 220);
                           border-top:0px solid rgb(0, 0, 0);
                           border-bottom:0px solid rgb(0, 0, 0);
                           border-right:0px solid rgb(0, 0, 0);
                           border-left:0px solid rgb(0, 0, 0);}"""

        self.btn_tog_switch_style = """QPushButton{background-color: rgb(0, 0, 0);
                           color: rgb(0, 0, 0);
                           border-bottom:0px solid rgb(0, 0, 0);
                           border-right:0px solid rgb(0, 0, 0);
                           border-top:0px solid rgb(0, 0, 0);
                           border-left:0px solid rgb(0, 0, 0);}"""

        self.btn_stat_img_style = """QPushButton{background-color: rgb(15, 15, 15);
                                   color: rgb(0, 0, 0);
                                   border-bottom:0px solid rgb(0, 0, 0);
                                   border-right:0px solid rgb(0, 0, 0);
                                   border-top:0px solid rgb(0, 0, 0);
                                   border-left:0px solid rgb(0, 0, 0);}"""

        self.lbl_white_txt_style = """QLabel {background-color: rgb(15, 15, 15);
                   color: rgb(200, 200, 200);
                   border-bottom:2px solid rgb(15, 15, 15);
                   border-right:2px solid rgb(15, 15, 15);
                   border-top:2px solid rgb(15, 15, 15);
                   border-left:2px solid rgb(15, 15, 15);}"""

        self.lbl_white_txt_black_bg_style = """QLabel {background-color: rgb(0, 0, 0);
                           color: rgb(200, 200, 200);
                           border-bottom:2px solid rgb(0, 0, 0);
                           border-right:2px solid rgb(0, 0, 0);
                           border-top:2px solid rgb(0, 0, 0);
                           border-left:2px solid rgb(0, 0, 0);}"""

        self.lbl_visually_combine_left_to_right = """QLabel {background-color: rgb(10, 10, 10);
                           color: rgb(200, 200, 200);
                           border-bottom:2px solid rgb(15, 15, 15);
                           border-right:2px solid rgb(15, 15, 15);
                           border-top:2px solid rgb(15, 15, 15);
                           border-left:2px solid rgb(15, 15, 15);}"""

        self.btn_settings_style = """QPushButton{background-color: rgb(15, 15, 15);
                           color: rgb(0, 0, 0);
                           border-bottom:2px solid rgb(15, 15, 15);
                           border-right:2px solid rgb(15, 15, 15);
                           border-top:2px solid rgb(15, 15, 15);}"""

        self.btn_hotbar_on_style = """QPushButton{background-color: rgb(15, 15, 15);
                                   color: rgb(0, 255, 0);
                                   border-bottom:2px solid rgb(25, 25, 25);
                                   border-right:1px solid rgb(15, 15, 15);
                                   border-top:1px solid rgb(15, 15, 15);
                                   border-left:1px solid rgb(15, 15, 15);}"""

        self.btn_hotbar_off_style = """QPushButton{background-color: rgb(15, 15, 15);
                                   color: rgb(0, 255, 0);
                                   border-bottom:2px solid rgb(15, 15, 15);
                                   border-right:1px solid rgb(15, 15, 15);
                                   border-top:1px solid rgb(15, 15, 15);
                                   border-left:1px solid rgb(15, 15, 15);}"""

        self.visually_combine_hotbar_on_settings_window_style = """QPushButton{background-color: rgb(25, 25, 25);
                                           color: rgb(0, 225, 0);
                                           border-bottom:2px solid rgb(35, 35, 35);
                                           border-right:1px solid rgb(18, 18, 18);
                                           border-top:2px solid rgb(0, 200, 0);
                                           border-left:1px solid rgb(18, 18, 18);}"""

        self.visually_combine_hotbar_off_settings_window_style = """QPushButton{background-color: rgb(25, 25, 25);
                                                   color: rgb(0, 225, 0);
                                                   border-bottom:2px solid rgb(15, 15, 15);
                                                   border-right:1px solid rgb(18, 18, 18);
                                                   border-top:2px solid rgb(0, 200, 0);
                                                   border-left:1px solid rgb(18, 18, 18);}"""

        self.btn_scroll_style = """QPushButton{background-color: rgb(15, 15, 15);
                                   color: rgb(30, 30, 30);
                                   border-bottom:2px solid rgb(15, 15, 15);
                                   border-right:2px solid rgb(15, 15, 15);
                                   border-top:2px solid rgb(15, 15, 15);
                                   border-left:2px solid rgb(15, 15, 15);}"""

        self.qle_unselected = """QLineEdit{background-color: rgb(15, 15, 15);
                       color: rgb(200, 200, 200);
                       border-bottom:2px solid rgb(15, 15, 15);
                       border-right:2px solid rgb(15, 15, 15);
                       border-top:2px solid rgb(15, 15, 15);
                       border-left:2px solid rgb(15, 15, 15);}"""

        self.setStyleSheet(self.tooltip_style)

        self.title_bar_h = 20
        self.title_bar_btn_w = (self.title_bar_h * 1.5)
        self.monitor_btn_h = 20
        self.monitor_btn_w = 72

        self.inner_group_spacing_h = 4
        self.group_spacing_h = 10
        self.object_height = 20
        self.scroll_w = 24
        self.feature_title_w = self.width - 48
        self.feature_title_pos_w = 24
        self.anchor_status_h = 28
        self.anchor_settings_h = (self.anchor_status_h + (36 * 3) + (self.inner_group_spacing_h * 8) + self.group_spacing_h * 2)
        self.anchor_settings_h = (36 * 3) + 10 + 16 + 28
        self.tog_switch_ico_sz = QSize(40, 20)
        self.tog_switch_ico_sz_x2h = QSize(18, 44)

        self.lbl_title = QLabel(self)
        self.lbl_title.move(37, 3)
        self.lbl_title.resize(self.width, 20)
        self.lbl_title.setFont(self.font_s10b)
        self.lbl_title.setText('iCUE Display')
        self.lbl_title.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
            color: rgb(230, 230, 230);
            border:0px solid rgb(0, 255, 0);}""")
        print('-- [App.__init__] created:', self.lbl_title)

        self.btn_title_logo = QLabel(self)
        self.btn_title_logo.move(5, -4)
        self.btn_title_logo.resize(28, 28)
        pixmap = QPixmap("./image/logo.png")
        # pixmap = pixmap.scaledToHeight(28)
        self.btn_title_logo.setPixmap(pixmap)
        self.btn_title_logo.setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 255, 255);}"""
        )
        print('-- [App.__init__] created:', self.btn_title_logo)

        self.btn_quit = QPushButton(self)
        self.btn_quit.move((self.width - 28), 0)
        self.btn_quit.resize(28, 28)
        self.btn_quit.setIcon(QIcon("./image/img_close.png"))
        self.btn_quit.setIconSize(QSize(8, 8))
        self.btn_quit.clicked.connect(QCoreApplication.instance().quit)
        self.btn_quit.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
        )
        print('-- [App.__init__] created:', self.btn_quit)

        self.btn_minimize = QPushButton(self)
        self.btn_minimize.move((self.width - 56), 0)
        self.btn_minimize.resize(28, 28)
        self.btn_minimize.setIcon(QIcon("./image/img_minimize.png"))
        self.btn_minimize.setIconSize(QSize(20, 20))
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.btn_minimize.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
        )
        print('-- [App.__init__] created:', self.btn_minimize)

        self.btn_show_discrete = QPushButton(self)
        self.btn_show_discrete.move(0, self.height_discrete - 20)
        self.btn_show_discrete.resize(self.width, 20)
        self.btn_show_discrete.setFont(self.font_s8b)
        self.btn_show_discrete.setIcon(QIcon("./image/img_scrollbar_down.png"))
        self.btn_show_discrete.setStyleSheet(self.btn_scroll_style)
        self.btn_show_discrete.clicked.connect(self.btn_show_discrete_function)
        print('-- [App.__init__] created:', self.btn_show_discrete)

        self.btn_scroll_l = QPushButton(self)
        self.btn_scroll_l.move(0, self.anchor_settings_h + self.inner_group_spacing_h - 4)
        self.btn_scroll_l.resize(18, 120)
        self.btn_scroll_l.setFont(self.font_s8b)
        self.btn_scroll_l.setIcon(QIcon("./image/img_scrollbar_left.png"))
        self.btn_scroll_l.setStyleSheet(self.btn_scroll_style)
        self.btn_scroll_l.clicked.connect(self.btn_scroll_l_function)
        print('-- [App.__init__] created:', self.btn_scroll_l)

        self.btn_scroll_r = QPushButton(self)
        self.btn_scroll_r.move((self.width - 18),  self.anchor_settings_h + self.inner_group_spacing_h - 4)
        self.btn_scroll_r.resize(18, 120)
        self.btn_scroll_r.setFont(self.font_s8b)
        self.btn_scroll_r.setIcon(QIcon("./image/img_scrollbar_right.png"))
        self.btn_scroll_r.setStyleSheet(self.btn_scroll_style)
        self.btn_scroll_r.clicked.connect(self.btn_scroll_r_function)
        print('-- [App.__init__] created:', self.btn_scroll_r)

        self.lbl_con_stat_name = QLabel(self)
        self.lbl_con_stat_name.move(2, self.anchor_status_h + self.inner_group_spacing_h)
        self.lbl_con_stat_name.resize(self.width - 4, self.monitor_btn_h)
        self.lbl_con_stat_name.setFont(self.font_s8b)
        self.lbl_con_stat_name.setText(' Connected: ')
        self.lbl_con_stat_name.setAlignment(Qt.AlignCenter)
        self.lbl_con_stat_name.setStyleSheet(self.lbl_stat_con_style_sub)
        print('-- [App.__init__] created:', self.lbl_con_stat_name)
        self.lbl_con_stat_name.hide()

        self.hotbar_btn_w = 36
        self.hotbar_btn_h = 36
        self.inner_group_spacing_hotbar_w = 2

        self.btn_refresh_recompile = QPushButton(self)
        self.btn_refresh_recompile.move((self.width - self.hotbar_btn_w) - (self.inner_group_spacing_hotbar_w) - 4, self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_refresh_recompile.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_refresh_recompile.setFont(self.font_s8b)
        self.btn_refresh_recompile.setIcon(QIcon("./image/img_refresh.png"))
        self.icon_sz_18_18 = QSize(20, 20)
        self.btn_refresh_recompile.setIconSize(self.icon_sz_18_18)
        self.btn_refresh_recompile.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_refresh_recompile.clicked.connect(self.recompile)
        print('-- [App.__init__] created:', self.btn_refresh_recompile)

        self.btn_bck_light = QPushButton(self)
        self.btn_bck_light.move((self.width - self.hotbar_btn_w * 2) - (self.inner_group_spacing_hotbar_w * 2) - 4, self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_bck_light.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_bck_light.setFont(self.font_s8b)
        self.btn_bck_light.setIcon(QIcon("./image/img_backlight_on.png"))
        self.icon_sz_18_18 = QSize(36, 36)
        self.btn_bck_light.setIconSize(self.icon_sz_18_18)
        self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_bck_light.clicked.connect(self.btn_bck_light_function)
        print('-- [App.__init__] created:', self.btn_bck_light)

        self.btn_hotbar_cpu_mon = QPushButton(self)
        self.btn_hotbar_cpu_mon.move(6, self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_cpu_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_cpu_mon.setFont(self.font_s8b)
        self.btn_hotbar_cpu_mon.setIcon(QIcon("./image/img_cpu.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_cpu_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_cpu_mon.setText('1')
        self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_cpu_mon.clicked.connect(self.btn_cpu_mon_function)
        print('-- [App.__init__] created:', self.btn_hotbar_cpu_mon)

        self.btn_hotbar_dram_mon = QPushButton(self)
        self.btn_hotbar_dram_mon.move(6 + (self.hotbar_btn_w * 1) + (self.inner_group_spacing_hotbar_w * 1), self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_dram_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_dram_mon.setFont(self.font_s8b)
        self.btn_hotbar_dram_mon.setIcon(QIcon("./image/img_dram.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_dram_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_dram_mon.setText('2')
        self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_dram_mon.clicked.connect(self.btn_dram_mon_function)
        print('-- [App.__init__] created:', self.btn_hotbar_dram_mon)

        self.btn_hotbar_vram_mon = QPushButton(self)
        self.btn_hotbar_vram_mon.move(6 + (self.hotbar_btn_w * 2) + (self.inner_group_spacing_hotbar_w * 2), self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_vram_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_vram_mon.setFont(self.font_s8b)
        self.btn_hotbar_vram_mon.setIcon(QIcon("./image/img_gpu.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_vram_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_vram_mon.setText('3')
        self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_vram_mon.clicked.connect(self.btn_vram_mon_function)
        print('-- [App.__init__] created:', self.btn_hotbar_vram_mon)

        self.btn_hotbar_diskrw_mon = QPushButton(self)
        self.btn_hotbar_diskrw_mon.move(6 + (self.hotbar_btn_w * 3) + (self.inner_group_spacing_hotbar_w * 3), self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_diskrw_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_diskrw_mon.setFont(self.font_s8b)
        self.btn_hotbar_diskrw_mon.setIcon(QIcon("./image/img_ssd.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_diskrw_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_diskrw_mon.setText('4')
        self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_diskrw_mon.clicked.connect(self.btn_hdd_mon_function)
        print('-- [App.__init__] created:', self.btn_hotbar_diskrw_mon)

        self.btn_hotbar_nettraffic_mon = QPushButton(self)
        self.btn_hotbar_nettraffic_mon.move(6 + (self.hotbar_btn_w * 4) + (self.inner_group_spacing_hotbar_w * 4), self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_nettraffic_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_nettraffic_mon.setFont(self.font_s8b)
        self.btn_hotbar_nettraffic_mon.setIcon(QIcon("./image/img_network.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_nettraffic_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_nettraffic_mon.setText('5')
        self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_nettraffic_mon.clicked.connect(self.btn_network_adapter_function)
        print('-- [App.__init__] created:', self.btn_hotbar_nettraffic_mon)

        self.btn_hotbar_netshare_mon = QPushButton(self)
        self.btn_hotbar_netshare_mon.move((self.width - self.hotbar_btn_w * 3) - (self.inner_group_spacing_hotbar_w * 3) - 4, self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_netshare_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_netshare_mon.setFont(self.font_s8b)
        self.btn_hotbar_netshare_mon.setIcon(QIcon("./image/img_netshare.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_netshare_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_netshare_mon.setText('8')
        self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_netshare_mon.clicked.connect(self.btn_defnetshare_function)
        print('-- [App.__init__] created:', self.btn_hotbar_netshare_mon)

        self.btn_hotbar_netcon_ms_mon = QPushButton(self)
        self.btn_hotbar_netcon_ms_mon.move((self.width - self.hotbar_btn_w * 4) - (self.inner_group_spacing_hotbar_w * 4) - 4, self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_netcon_ms_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_netcon_ms_mon.setFont(self.font_s8b)
        self.btn_hotbar_netcon_ms_mon.setIcon(QIcon("./image/img_netcon_ms.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_netcon_ms_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_netcon_ms_mon.setText('7')
        self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_netcon_ms_mon.clicked.connect(self.btn_net_con_mouse_function)
        print('-- [App.__init__] created:', self.btn_hotbar_netcon_ms_mon)

        self.btn_hotbar_netcon_kb_mon = QPushButton(self)
        self.btn_hotbar_netcon_kb_mon.move((self.width - self.hotbar_btn_w * 5) - (self.inner_group_spacing_hotbar_w * 5) - 4, self.anchor_status_h + self.inner_group_spacing_h)
        self.btn_hotbar_netcon_kb_mon.resize(self.hotbar_btn_w, self.hotbar_btn_h)
        self.btn_hotbar_netcon_kb_mon.setFont(self.font_s8b)
        self.btn_hotbar_netcon_kb_mon.setIcon(QIcon("./image/img_netcon_kb.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.btn_hotbar_netcon_kb_mon.setIconSize(self.icon_sz_18_18)
        # self.btn_hotbar_netcon_kb_mon.setText('6')
        self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_off_style)
        self.btn_hotbar_netcon_kb_mon.clicked.connect(self.btn_net_con_kb_function)
        print('-- [App.__init__] created:', self.btn_hotbar_netcon_kb_mon)

        self.btn_stat_w = 36
        self.btn_stat_h = 36
        self.inner_group_spacing_stat_w = 2
        self.inner_group_spacing_stat_h = 4

        self.lbl_con_stat_kb_img = QPushButton(self)
        self.lbl_con_stat_kb_img.move(6, self.anchor_status_h + (self.object_height * 1) + (self.inner_group_spacing_h * 7))
        self.lbl_con_stat_kb_img.resize(self.btn_stat_w, self.btn_stat_h)
        self.lbl_con_stat_kb_img.setFont(self.font_s8b)
        self.lbl_con_stat_kb_img.setIcon(QIcon("./image/img_kb.png"))
        self.icon_sz_18_18 = QSize(24, 24)
        self.lbl_con_stat_kb_img.setIconSize(self.icon_sz_18_18)
        # self.lbl_con_stat_kb_img.setText('')
        self.lbl_con_stat_kb_img.setStyleSheet(self.btn_stat_img_style)
        print('-- [App.__init__] created:', self.lbl_con_stat_kb_img)

        self.lbl_con_stat_kb = QLabel(self)
        self.lbl_con_stat_kb.move(6 + self.btn_stat_w + self.inner_group_spacing_stat_w, self.anchor_status_h + (self.object_height * 1) + (self.inner_group_spacing_h * 6) + 4)
        self.lbl_con_stat_kb.resize(150, 36)
        self.lbl_con_stat_kb.setFont(self.font_s8b)
        self.lbl_con_stat_kb.setText('')
        self.lbl_con_stat_kb.setStyleSheet(self.lbl_stat_con_style_sub)
        print('-- [App.__init__] created:', self.lbl_con_stat_kb)

        self.lbl_con_stat_ms_img = QPushButton(self)
        self.lbl_con_stat_ms_img.move(6, self.anchor_status_h + (self.object_height * 1) + (self.inner_group_spacing_h * 7) + 36 + 4)
        self.lbl_con_stat_ms_img.resize(self.btn_stat_w, self.btn_stat_h)
        self.lbl_con_stat_ms_img.setFont(self.font_s8b)
        self.lbl_con_stat_ms_img.setIcon(QIcon("./image/img_ms.png"))
        self.icon_sz_18_18 = QSize(20, 20)
        self.lbl_con_stat_ms_img.setIconSize(self.icon_sz_18_18)
        # self.lbl_con_stat_ms_img.setText('')
        self.lbl_con_stat_ms_img.setStyleSheet(self.btn_stat_img_style)
        print('-- [App.__init__] created:', self.lbl_con_stat_ms_img)

        self.lbl_con_stat_mouse = QLabel(self)
        self.lbl_con_stat_mouse.move(6 + self.btn_stat_w + self.inner_group_spacing_stat_w, self.anchor_status_h + (self.object_height * 1) + (self.inner_group_spacing_h * 7) + 36 + 4)
        self.lbl_con_stat_mouse.resize(150, 36)
        self.lbl_con_stat_mouse.setFont(self.font_s8b)
        self.lbl_con_stat_mouse.setText('')
        self.lbl_con_stat_mouse.setStyleSheet(self.lbl_stat_con_style_sub)
        print('-- [App.__init__] created:', self.lbl_con_stat_mouse)

        self.lbl_settings_border = QLabel(self)
        self.lbl_settings_border.move(20, self.anchor_settings_h + self.inner_group_spacing_h - 4)
        self.lbl_settings_border.resize(self.width - 40, 120)
        self.lbl_settings_border.setStyleSheet(self.lbl_settings_border_style)
        print('-- [App.__init__] created:', self.lbl_settings_border)

        self.lbl_utilization = QLabel(self)
        self.lbl_utilization.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_utilization.resize(self.feature_title_w, self.object_height)
        self.lbl_utilization.setFont(self.font_s8b)
        self.lbl_utilization.setText('UTILIZATION')
        self.lbl_utilization.setAlignment(Qt.AlignCenter)
        self.lbl_utilization.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_utilization)

        self.lbl_feature_standard_w_0 = 48

        self.lbl_cpu_mon = QLabel(self)
        self.lbl_cpu_mon.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_cpu_mon.resize(52, 20)
        self.lbl_cpu_mon.setFont(self.font_s8b)
        self.lbl_cpu_mon.setText('CPU')
        self.lbl_cpu_mon.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_cpu_mon)

        self.btn_cpu_mon = QPushButton(self)
        self.btn_cpu_mon.move(self.scroll_w + 2 + 52 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_cpu_mon.resize(18, 18)
        self.btn_cpu_mon.setStyleSheet(self.btn_tog_switch_style)
        self.btn_cpu_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_cpu_mon.clicked.connect(self.btn_cpu_mon_function)
        print('-- [App.__init__] created:', self.btn_cpu_mon)

        self.qle_cpu_mon_rgb_on = QLineEdit(self)
        self.qle_cpu_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_cpu_mon_rgb_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.qle_cpu_mon_rgb_on.setFont(self.font_s8b)
        self.qle_cpu_mon_rgb_on.returnPressed.connect(self.btn_cpu_mon_rgb_on_function)
        self.qle_cpu_mon_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_cpu_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_cpu_mon_rgb_on)

        self.qle_cpu_led_time_on = QLineEdit(self)
        self.qle_cpu_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_cpu_led_time_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4 + 72 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.qle_cpu_led_time_on.setFont(self.font_s8b)
        self.qle_cpu_led_time_on.returnPressed.connect(self.btn_cpu_led_time_on_function)
        self.qle_cpu_led_time_on.setStyleSheet(self.qle_unselected)
        self.qle_cpu_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_cpu_led_time_on)

        self.lbl_dram_mon = QLabel(self)
        self.lbl_dram_mon.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_dram_mon.resize(52, self.monitor_btn_h)
        self.lbl_dram_mon.setFont(self.font_s8b)
        self.lbl_dram_mon.setText('DRAM')
        self.lbl_dram_mon.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_dram_mon)

        self.btn_dram_mon = QPushButton(self)
        self.btn_dram_mon.move(self.scroll_w + 2 + 52 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_dram_mon.resize(18, 18)
        self.btn_dram_mon.setStyleSheet(self.btn_tog_switch_style)
        self.btn_dram_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_dram_mon.clicked.connect(self.btn_dram_mon_function)
        print('-- [App.__init__] created:', self.btn_dram_mon)

        self.qle_dram_mon_rgb_on = QLineEdit(self)
        self.qle_dram_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_dram_mon_rgb_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.qle_dram_mon_rgb_on.setFont(self.font_s8b)
        self.qle_dram_mon_rgb_on.returnPressed.connect(self.btn_dram_mon_rgb_on_function)
        self.qle_dram_mon_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_dram_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_dram_mon_rgb_on)

        self.qle_dram_led_time_on = QLineEdit(self)
        self.qle_dram_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_dram_led_time_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4 + 72 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.qle_dram_led_time_on.setFont(self.font_s8b)
        self.qle_dram_led_time_on.returnPressed.connect(self.btn_dram_led_time_on_function)
        self.qle_dram_led_time_on.setStyleSheet(self.qle_unselected)
        self.qle_dram_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_dram_led_time_on)

        self.lbl_vram_mon = QLabel(self)
        self.lbl_vram_mon.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.lbl_vram_mon.resize(52, self.monitor_btn_h)
        self.lbl_vram_mon.setFont(self.font_s8b)
        self.lbl_vram_mon.setText('VRAM')
        self.lbl_vram_mon.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_vram_mon)

        self.btn_vram_mon = QPushButton(self)
        self.btn_vram_mon.move(self.scroll_w + 2 + 52 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_vram_mon.resize(18, 18)
        self.btn_vram_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_vram_mon.setStyleSheet(self.btn_tog_switch_style)
        self.btn_vram_mon.clicked.connect(self.btn_vram_mon_function)
        print('-- [App.__init__] created:', self.btn_vram_mon)

        self.qle_vram_mon_rgb_on = QLineEdit(self)
        self.qle_vram_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_vram_mon_rgb_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.qle_vram_mon_rgb_on.setFont(self.font_s8b)
        self.qle_vram_mon_rgb_on.returnPressed.connect(self.btn_vram_mon_rgb_on_function)
        self.qle_vram_mon_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_vram_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_vram_mon_rgb_on)

        self.qle_vram_led_time_on = QLineEdit(self)
        self.qle_vram_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_vram_led_time_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4 + 72 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.qle_vram_led_time_on.setFont(self.font_s8b)
        self.qle_vram_led_time_on.returnPressed.connect(self.btn_vram_led_time_on_function)
        self.qle_vram_led_time_on.setStyleSheet(self.qle_unselected)
        self.qle_vram_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_vram_led_time_on)

        self.lbl_hdd_mon = QLabel(self)
        self.lbl_hdd_mon.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_hdd_mon.resize(self.feature_title_w, self.object_height)
        self.lbl_hdd_mon.setFont(self.font_s8b)
        self.lbl_hdd_mon.setText('DISKS')
        self.lbl_hdd_mon.setAlignment(Qt.AlignCenter)
        self.lbl_hdd_mon.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_hdd_mon)

        self.lbl_hdd_write_mon = QLabel(self)
        self.lbl_hdd_write_mon.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_hdd_write_mon.resize(52, self.monitor_btn_h)
        self.lbl_hdd_write_mon.setFont(self.font_s8b)
        self.lbl_hdd_write_mon.setText('WRITES')
        self.lbl_hdd_write_mon.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_hdd_write_mon)

        self.btn_hdd_mon = QPushButton(self)
        self.btn_hdd_mon.move(self.scroll_w + 2 + 52 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_hdd_mon.resize(18, 44)
        self.btn_hdd_mon.setStyleSheet(self.btn_tog_switch_style)
        self.btn_hdd_mon.setIconSize(self.tog_switch_ico_sz_x2h)
        self.btn_hdd_mon.clicked.connect(self.btn_hdd_mon_function)
        print('-- [App.__init__] created:', self.btn_hdd_mon)

        self.qle_hdd_mon_rgb_on = QLineEdit(self)
        self.qle_hdd_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_hdd_mon_rgb_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.qle_hdd_mon_rgb_on.setFont(self.font_s8b)
        self.qle_hdd_mon_rgb_on.returnPressed.connect(self.btn_hdd_mon_rgb_on_function)
        self.qle_hdd_mon_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_hdd_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_hdd_mon_rgb_on)

        self.lbl_hdd_led_time_on_vis_combine = QLabel(self)
        self.lbl_hdd_led_time_on_vis_combine.resize(24, 44)
        self.lbl_hdd_led_time_on_vis_combine.move(self.scroll_w + 2 + 52 + 4 + 18 + 4 + 72 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_hdd_led_time_on_vis_combine.setStyleSheet(self.lbl_visually_combine_left_to_right)
        print('-- [App.__init__] created:', self.lbl_hdd_led_time_on_vis_combine)

        self.qle_hdd_led_time_on = QLineEdit(self)
        self.qle_hdd_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_hdd_led_time_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4 + 72 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3 + 12)
        self.qle_hdd_led_time_on.setFont(self.font_s8b)
        self.qle_hdd_led_time_on.returnPressed.connect(self.btn_hdd_led_time_on_function)
        self.qle_hdd_led_time_on.setStyleSheet(self.qle_unselected)
        self.qle_hdd_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_hdd_led_time_on)

        self.lbl_hdd_read_mon = QLabel(self)
        self.lbl_hdd_read_mon.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_hdd_read_mon.resize(52, self.monitor_btn_h)
        self.lbl_hdd_read_mon.setFont(self.font_s8b)
        self.lbl_hdd_read_mon.setText('READS')
        self.lbl_hdd_read_mon.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_hdd_read_mon)

        self.qle_hdd_read_mon_rgb_on = QLineEdit(self)
        self.qle_hdd_read_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_hdd_read_mon_rgb_on.move(self.scroll_w + 2 + 52 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.qle_hdd_read_mon_rgb_on.setFont(self.font_s8b)
        self.qle_hdd_read_mon_rgb_on.returnPressed.connect(self.btn_hdd_read_mon_rgb_on_function)
        self.qle_hdd_read_mon_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_hdd_read_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_hdd_read_mon_rgb_on)

        self.lbl_network_traffic = QLabel(self)
        self.lbl_network_traffic.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_network_traffic.resize(self.feature_title_w, self.object_height)
        self.lbl_network_traffic.setFont(self.font_s8b)
        self.lbl_network_traffic.setText('NETWORK TRAFFIC')
        self.lbl_network_traffic.setAlignment(Qt.AlignCenter)
        self.lbl_network_traffic.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_network_traffic)

        self.lbl_network_adapter = QLabel(self)
        self.lbl_network_adapter.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_network_adapter.resize(72, self.monitor_btn_h)
        self.lbl_network_adapter.setFont(self.font_s8b)
        self.lbl_network_adapter.setText('ADAPTER')
        self.lbl_network_adapter.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_network_adapter)

        self.cmb_network_adapter_name = QComboBox(self)
        self.cmb_network_adapter_name.resize((self.monitor_btn_w * 3) + 4 + 18, self.monitor_btn_h)
        self.cmb_network_adapter_name.move(self.scroll_w + 2 + 72 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.cmb_network_adapter_name.setStyleSheet(self.cmb_style)
        self.cmb_network_adapter_name.setFont(self.font_s8b)
        self.cmb_network_adapter_name.activated[str].connect(self.cmb_network_adapter_name_function)
        print('-- [App.__init__] created:', self.cmb_network_adapter_name)

        self.btn_network_adapter_refresh = QPushButton(self)
        self.btn_network_adapter_refresh.move(self.width - (self.scroll_w * 2) + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_network_adapter_refresh.resize(20, 20)
        self.btn_network_adapter_refresh.setIcon(QIcon("./image/baseline_refresh_white_24dp.png"))
        self.btn_network_adapter_refresh.setIconSize(QSize(14, 14))
        self.btn_network_adapter_refresh.setStyleSheet(self.btn_settings_style)
        self.btn_network_adapter_refresh.clicked.connect(self.btn_network_adapter_refresh_function)
        print('-- [App.__init__] created:', self.btn_network_adapter_refresh)

        self.btn_network_adapter = QPushButton(self)
        self.btn_network_adapter.move(self.width - (self.scroll_w * 2) + 2, self.anchor_settings_h + (self.object_height * 2) + self.inner_group_spacing_h * 4)
        self.btn_network_adapter.resize(18, 18)
        self.btn_network_adapter.setStyleSheet(self.btn_tog_switch_style)
        self.btn_network_adapter.setIconSize(self.tog_switch_ico_sz)
        self.btn_network_adapter.clicked.connect(self.btn_network_adapter_function)
        print('-- [App.__init__] created:', self.btn_network_adapter)

        self.qle_network_adapter_led_time_on = QLineEdit(self)
        self.qle_network_adapter_led_time_on.resize(24, 20)
        self.qle_network_adapter_led_time_on.move(self.width - (self.scroll_w * 2) - 2, self.anchor_settings_h + (self.object_height * 3) + self.inner_group_spacing_h * 5)
        self.qle_network_adapter_led_time_on.setFont(self.font_s8b)
        self.qle_network_adapter_led_time_on.returnPressed.connect(self.btn_network_adapter_led_time_on_function)
        self.qle_network_adapter_led_time_on.setStyleSheet(self.qle_unselected)
        self.qle_network_adapter_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_network_adapter_led_time_on)

        self.lbl_connectivity = QLabel(self)
        self.lbl_connectivity.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_connectivity.resize(self.feature_title_w, self.object_height)
        self.lbl_connectivity.setFont(self.font_s8b)
        self.lbl_connectivity.setText('INTERNET CONNECTIVITY')
        self.lbl_connectivity.setAlignment(Qt.AlignCenter)
        self.lbl_connectivity.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_connectivity)

        self.lbl_net_con_mouse = QLabel(self)
        self.lbl_net_con_mouse.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_net_con_mouse.resize(72, self.monitor_btn_h)
        self.lbl_net_con_mouse.setFont(self.font_s8b)
        self.lbl_net_con_mouse.setText('MOUSE')
        self.lbl_net_con_mouse.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_net_con_mouse)

        self.btn_net_con_mouse = QPushButton(self)
        self.btn_net_con_mouse.move(self.scroll_w + 2 + 72 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_net_con_mouse.resize(18, 18)
        self.btn_net_con_mouse.setStyleSheet(self.btn_tog_switch_style)
        self.btn_net_con_mouse.setIconSize(self.tog_switch_ico_sz)
        self.btn_net_con_mouse.clicked.connect(self.btn_net_con_mouse_function)
        print('-- [App.__init__] created:', self.btn_net_con_mouse)

        self.btn_net_con_mouse_led_selected_prev = QPushButton(self)
        self.btn_net_con_mouse_led_selected_prev.move(self.scroll_w + 2 + 72 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_net_con_mouse_led_selected_prev.resize(20, 20)
        self.btn_net_con_mouse_led_selected_prev.setFont(self.font_s10b)
        self.btn_net_con_mouse_led_selected_prev.setIcon(QIcon("./image/img_minus.png"))
        self.btn_net_con_mouse_led_selected_prev.setStyleSheet(self.btn_settings_style)
        self.btn_net_con_mouse_led_selected_prev.clicked.connect(self.btn_net_con_mouse_led_selected_prev_function)
        print('-- [App.__init__] created:', self.btn_net_con_mouse_led_selected_prev)

        self.lbl_net_con_mouse_led_selected = QLabel(self)
        self.lbl_net_con_mouse_led_selected.move(self.scroll_w + 2 + 72 + 4 + 18 + 4 + 20 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_net_con_mouse_led_selected.resize(20, self.monitor_btn_h)
        self.lbl_net_con_mouse_led_selected.setFont(self.font_s8b)
        self.lbl_net_con_mouse_led_selected.setStyleSheet(self.lbl_white_txt_style)
        self.lbl_net_con_mouse_led_selected.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_led_selected)

        self.btn_net_con_mouse_led_selected_next = QPushButton(self)
        self.btn_net_con_mouse_led_selected_next.move(self.scroll_w + 2 + 72 + 4 + 18 + 4 + 20 + 4 + 20 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_net_con_mouse_led_selected_next.resize(20, self.monitor_btn_h)
        self.btn_net_con_mouse_led_selected_next.setFont(self.font_s10b)
        self.btn_net_con_mouse_led_selected_next.setIcon(QIcon("./image/img_plus.png"))
        self.btn_net_con_mouse_led_selected_next.setStyleSheet(self.btn_settings_style)
        self.btn_net_con_mouse_led_selected_next.clicked.connect(self.btn_net_con_mouse_led_selected_next_function)
        print('-- [App.__init__] created:', self.btn_net_con_mouse_led_selected_next)

        self.lbl_net_con_kb = QLabel(self)
        self.lbl_net_con_kb.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_net_con_kb.resize(72, self.monitor_btn_h)
        self.lbl_net_con_kb.setFont(self.font_s8b)
        self.lbl_net_con_kb.setText('KEYBOARD')
        self.lbl_net_con_kb.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_net_con_kb)

        self.btn_net_con_kb = QPushButton(self)
        self.btn_net_con_kb.move(self.scroll_w + 2 + 72 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_net_con_kb.resize(18, 18)
        self.btn_net_con_kb.setStyleSheet(self.btn_tog_switch_style)
        self.btn_net_con_kb.setIconSize(self.tog_switch_ico_sz)
        self.btn_net_con_kb.clicked.connect(self.btn_net_con_kb_function)
        print('-- [App.__init__] created:', self.btn_net_con_kb)

        self.lbl_netshare = QLabel(self)
        self.lbl_netshare.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_netshare.resize(self.feature_title_w, self.object_height)
        self.lbl_netshare.setFont(self.font_s8b)
        self.lbl_netshare.setText('NETWORK SHARE MONITOR')
        self.lbl_netshare.setAlignment(Qt.AlignCenter)
        self.lbl_netshare.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_netshare)

        self.lbl_netshare_mon = QLabel(self)
        self.lbl_netshare_mon.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_netshare_mon.resize(126, self.monitor_btn_h)
        self.lbl_netshare_mon.setFont(self.font_s8b)
        self.lbl_netshare_mon.setText('NETWORK SHARES')
        self.lbl_netshare_mon.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_netshare_mon)

        self.btn_netshare_mon = QPushButton(self)
        self.btn_netshare_mon.move(self.scroll_w + 2 + 126 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_netshare_mon.resize(18, 18)
        self.btn_netshare_mon.setStyleSheet(self.btn_tog_switch_style)
        self.btn_netshare_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_netshare_mon.clicked.connect(self.btn_defnetshare_function)
        print('-- [App.__init__] created:', self.btn_netshare_mon)

        self.qle_netshare_mon_rgb_on = QLineEdit(self)
        self.qle_netshare_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_netshare_mon_rgb_on.move(self.scroll_w + 2 + 126 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.qle_netshare_mon_rgb_on.setFont(self.font_s8b)
        self.qle_netshare_mon_rgb_on.returnPressed.connect(self.netshare_active_rgb_function)
        self.qle_netshare_mon_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_netshare_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_netshare_mon_rgb_on)

        self.lbl_settings = QLabel(self)
        self.lbl_settings.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_settings.resize(self.feature_title_w, self.object_height)
        self.lbl_settings.setFont(self.font_s8b)
        self.lbl_settings.setText('SETTINGS')
        self.lbl_settings.setAlignment(Qt.AlignCenter)
        self.lbl_settings.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_settings)

        self.lbl_exclusive_con = QLabel(self)
        self.lbl_exclusive_con.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_exclusive_con.resize(126, self.monitor_btn_h)
        self.lbl_exclusive_con.setFont(self.font_s8b)
        self.lbl_exclusive_con.setText('EXCLUSIVE CONTROL')
        self.lbl_exclusive_con.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_exclusive_con)

        self.btn_exclusive_con = QPushButton(self)
        self.btn_exclusive_con.move(self.scroll_w + 2 + 126 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_exclusive_con.resize(18, 18)
        self.btn_exclusive_con.setStyleSheet(self.btn_tog_switch_style)
        self.btn_exclusive_con.setIconSize(self.tog_switch_ico_sz)
        self.btn_exclusive_con.clicked.connect(self.btn_exclusive_con_function)
        print('-- [App.__init__] created:', self.btn_exclusive_con)

        self.lbl_run_startup = QLabel(self)
        self.lbl_run_startup.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_run_startup.resize(126, self.monitor_btn_h)
        self.lbl_run_startup.setFont(self.font_s8b)
        self.lbl_run_startup.setText('AUTOMATIC STARTUP')
        self.lbl_run_startup.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_run_startup)

        self.btn_run_startup = QPushButton(self)
        self.btn_run_startup.move(self.scroll_w + 2 + 126 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_run_startup.resize(18, 18)
        self.btn_run_startup.setStyleSheet(self.btn_tog_switch_style)
        self.btn_run_startup.setIconSize(self.tog_switch_ico_sz)
        self.btn_run_startup.clicked.connect(self.btn_run_startup_function)
        print('-- [App.__init__] created:', self.btn_run_startup)

        self.lbl_start_minimized = QLabel(self)
        self.lbl_start_minimized.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.lbl_start_minimized.resize(126, self.monitor_btn_h)
        self.lbl_start_minimized.setFont(self.font_s8b)
        self.lbl_start_minimized.setText('START MINIMIZED')
        self.lbl_start_minimized.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_start_minimized)

        self.btn_start_minimized = QPushButton(self)
        self.btn_start_minimized.move(self.scroll_w + 2 + 126 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_start_minimized.resize(18, 18)
        self.btn_start_minimized.setStyleSheet(self.btn_tog_switch_style)
        self.btn_start_minimized.setIconSize(self.tog_switch_ico_sz)
        self.btn_start_minimized.clicked.connect(self.btn_start_minimized_function)
        print('-- [App.__init__] created:', self.btn_start_minimized)

        self.lbl_backlight = QLabel(self)
        self.lbl_backlight.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_backlight.resize(self.feature_title_w, self.object_height)
        self.lbl_backlight.setFont(self.font_s8b)
        self.lbl_backlight.setText('BACKLIGHT')
        self.lbl_backlight.setAlignment(Qt.AlignCenter)
        self.lbl_backlight.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_backlight)

        self.lbl_backlight_sub = QLabel(self)
        self.lbl_backlight_sub.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_backlight_sub.resize(72, 20)
        self.lbl_backlight_sub.setFont(self.font_s8b)
        self.lbl_backlight_sub.setText('BACKLIGHT')
        self.lbl_backlight_sub.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_backlight_sub)

        self.btn_backlight_sub = QPushButton(self)
        self.btn_backlight_sub.move(self.scroll_w + 2 + 72 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_backlight_sub.resize(18, 18)
        self.btn_backlight_sub.setStyleSheet(self.btn_tog_switch_style)
        self.btn_backlight_sub.setIconSize(self.tog_switch_ico_sz)
        self.btn_backlight_sub.clicked.connect(self.btn_bck_light_function)
        print('-- [App.__init__] created:', self.btn_backlight_sub)

        self.qle_backlight_rgb_on = QLineEdit(self)
        self.qle_backlight_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_backlight_rgb_on.move(self.scroll_w + 2 + 72 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.qle_backlight_rgb_on.setFont(self.font_s8b)
        self.qle_backlight_rgb_on.returnPressed.connect(self.btn_backlight_rgb_on_function)
        self.qle_backlight_rgb_on.setStyleSheet(self.qle_unselected)
        self.qle_backlight_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_backlight_rgb_on)

        self.lbl_event_notification = QLabel(self)
        self.lbl_event_notification.move(self.feature_title_pos_w, self.anchor_settings_h + self.inner_group_spacing_h)
        self.lbl_event_notification.resize(self.feature_title_w, self.object_height)
        self.lbl_event_notification.setFont(self.font_s8b)
        self.lbl_event_notification.setText('EVENT NOTIFICATION (ADVANCED USERS ONLY)')
        self.lbl_event_notification.setAlignment(Qt.AlignCenter)
        self.lbl_event_notification.setStyleSheet(self.lbl_data_style_title)
        print('-- [App.__init__] created:', self.lbl_event_notification)
        self.lbl_event_notification.setToolTip('EVENT NOTIFICATION\n\n'
                                               'Enables notifications to be displayed via a G key led and has the option to run a file when the pertaining G key is short pressed.\n\n'
                                               'USE:\nShort Press G Key (0-0.75 Seconds): Turns off notification LED and if enabled runs a program/file.\n'
                                               'Long Press G Key (0.75+ Seconds): Turns off Notification LED (ignores the notification).\n\n'
                                               'REQUIREMENTS:\n'
                                               '1. A K95 Platinum keyboard or similar with G1-G6 keys.\n'
                                               '2. True must be written to any of the event_notification_gx.dat files to trigger a notification event.\n\n'
                                               'EXAMPLES:\n[Example 1] G1 Notify On with G1 Run Off: Event Notification\n'
                                               '[Example 2] G1 Notify On with G1 Run On: Event Notification + Event Response\n\n'
                                               'NOTE:\n1. G Notify must be enabled for G Run to function.\n'
                                               '2. Event response (Run) will only work when notification of event is active (LED is blinking).\n'
                                               '3. Event response can be triggered only once per notification by pressing the G key while G key is showing the notification.\n\n'
                                               'This feature is for advanced users.')

        self.lbl_event_notification_g1 = QLabel(self)
        self.lbl_event_notification_g1.move(self.scroll_w + 2, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_event_notification_g1.resize(60, 20)
        self.lbl_event_notification_g1.setFont(self.font_s8b)
        self.lbl_event_notification_g1.setText('G1 Notify')
        self.lbl_event_notification_g1.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_g1)

        self.btn_event_notification_g1 = QPushButton(self)
        self.btn_event_notification_g1.move(self.scroll_w + 2 + 60 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_event_notification_g1.resize(18, 18)
        self.btn_event_notification_g1.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_g1.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_g1.clicked.connect(self.btn_event_notification_g1_function)
        print('-- [App.__init__] created:', self.btn_event_notification_g1)

        self.lbl_event_notification_run_g1 = QLabel(self)
        self.lbl_event_notification_run_g1.move(self.scroll_w + 2 + 60 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.lbl_event_notification_run_g1.resize(30, 20)
        self.lbl_event_notification_run_g1.setFont(self.font_s8b)
        self.lbl_event_notification_run_g1.setText('Run')
        self.lbl_event_notification_run_g1.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_run_g1)

        self.btn_event_notification_run_g1 = QPushButton(self)
        self.btn_event_notification_run_g1.move(self.scroll_w + 2 + 60 + 4 + 18 + 4 + 30 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_event_notification_run_g1.resize(18, 18)
        self.btn_event_notification_run_g1.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_run_g1.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_run_g1.clicked.connect(self.btn_event_notification_run_g1_function)
        print('-- [App.__init__] created:', self.btn_event_notification_run_g1)

        self.btn_event_notification_select_file_g1 = QPushButton(self)
        self.btn_event_notification_select_file_g1.move(self.scroll_w + 2 + 60 + 4 + 18 + 4 + 30 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_event_notification_select_file_g1.resize(20, 20)
        self.btn_event_notification_select_file_g1.setFont(self.font_s10b)
        self.btn_event_notification_select_file_g1.setIcon(QIcon("./image/img_plus.png"))
        self.btn_event_notification_select_file_g1.setStyleSheet(self.btn_settings_style)
        self.btn_event_notification_select_file_g1.clicked.connect(self.openFileNameDialogG1)
        print('-- [App.__init__] created:', self.btn_event_notification_select_file_g1)

        self.lbl_event_notification_g2 = QLabel(self)
        self.lbl_event_notification_g2.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_event_notification_g2.resize(60, self.monitor_btn_h)
        self.lbl_event_notification_g2.setFont(self.font_s8b)
        self.lbl_event_notification_g2.setText('G2 Notify')
        self.lbl_event_notification_g2.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_g2)

        self.btn_event_notification_g2 = QPushButton(self)
        self.btn_event_notification_g2.move(self.scroll_w + 2 + 60 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_event_notification_g2.resize(18, 18)
        self.btn_event_notification_g2.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_g2.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_g2.clicked.connect(self.btn_event_notification_g2_function)
        print('-- [App.__init__] created:', self.btn_event_notification_g2)

        self.lbl_event_notification_run_g2 = QLabel(self)
        self.lbl_event_notification_run_g2.move(self.scroll_w + 2 + 60 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_event_notification_run_g2.resize(30, 20)
        self.lbl_event_notification_run_g2.setFont(self.font_s8b)
        self.lbl_event_notification_run_g2.setText('Run')
        self.lbl_event_notification_run_g2.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_run_g2)

        self.btn_event_notification_run_g2 = QPushButton(self)
        self.btn_event_notification_run_g2.move(self.scroll_w + 2 + 60 + 4 + 18 + 4 + 30 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_event_notification_run_g2.resize(18, 18)
        self.btn_event_notification_run_g2.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_run_g2.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_run_g2.clicked.connect(self.btn_event_notification_run_g2_function)
        print('-- [App.__init__] created:', self.btn_event_notification_run_g2)

        self.btn_event_notification_select_file_g2 = QPushButton(self)
        self.btn_event_notification_select_file_g2.move(self.scroll_w + 2 + 60 + 4 + 18 + 4 + 30 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_event_notification_select_file_g2.resize(20, 20)
        self.btn_event_notification_select_file_g2.setFont(self.font_s10b)
        self.btn_event_notification_select_file_g2.setIcon(QIcon("./image/img_plus.png"))
        self.btn_event_notification_select_file_g2.setStyleSheet(self.btn_settings_style)
        self.btn_event_notification_select_file_g2.clicked.connect(self.openFileNameDialogG2)
        print('-- [App.__init__] created:', self.btn_event_notification_select_file_g2)

        self.lbl_event_notification_g3 = QLabel(self)
        self.lbl_event_notification_g3.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.lbl_event_notification_g3.resize(60, self.monitor_btn_h)
        self.lbl_event_notification_g3.setFont(self.font_s8b)
        self.lbl_event_notification_g3.setText('G3 Notify')
        self.lbl_event_notification_g3.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_g3)

        self.btn_event_notification_g3 = QPushButton(self)
        self.btn_event_notification_g3.move(self.scroll_w + 2 + 60 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_event_notification_g3.resize(18, 18)
        self.btn_event_notification_g3.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_g3.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_g3.clicked.connect(self.btn_event_notification_g3_function)
        print('-- [App.__init__] created:', self.btn_event_notification_g3)

        self.lbl_event_notification_run_g3 = QLabel(self)
        self.lbl_event_notification_run_g3.move(self.scroll_w + 2 + 60 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.lbl_event_notification_run_g3.resize(30, 20)
        self.lbl_event_notification_run_g3.setFont(self.font_s8b)
        self.lbl_event_notification_run_g3.setText('Run')
        self.lbl_event_notification_run_g3.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_run_g3)

        self.btn_event_notification_run_g3 = QPushButton(self)
        self.btn_event_notification_run_g3.move(self.scroll_w + 2 + 60 + 4 + 18 + 4 + 30 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_event_notification_run_g3.resize(18, 18)
        self.btn_event_notification_run_g3.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_run_g3.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_run_g3.clicked.connect(self.btn_event_notification_run_g3_function)
        print('-- [App.__init__] created:', self.btn_event_notification_run_g3)

        self.btn_event_notification_select_file_g3 = QPushButton(self)
        self.btn_event_notification_select_file_g3.move(self.scroll_w + 2 + 60 + 4 + 18 + 4 + 30 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_event_notification_select_file_g3.resize(20, 20)
        self.btn_event_notification_select_file_g3.setFont(self.font_s10b)
        self.btn_event_notification_select_file_g3.setIcon(QIcon("./image/img_plus.png"))
        self.btn_event_notification_select_file_g3.setStyleSheet(self.btn_settings_style)
        self.btn_event_notification_select_file_g3.clicked.connect(self.openFileNameDialogG3)
        print('-- [App.__init__] created:', self.btn_event_notification_select_file_g3)

        self.lbl_event_notification_g4 = QLabel(self)
        self.lbl_event_notification_g4.move(191 + 9, self.anchor_settings_h + (self.object_height * 1) + (self.inner_group_spacing_h * 3))
        self.lbl_event_notification_g4.resize(60, self.monitor_btn_h)
        self.lbl_event_notification_g4.setFont(self.font_s8b)
        self.lbl_event_notification_g4.setText('G4 Notify')
        self.lbl_event_notification_g4.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_g4)
        # self.lbl_event_notification_g4.hide()

        self.btn_event_notification_g4 = QPushButton(self)
        self.btn_event_notification_g4.move(191 + 9 + 60 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_event_notification_g4.resize(18, 18)
        self.btn_event_notification_g4.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_g4.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_g4.clicked.connect(self.btn_event_notification_g4_function)
        print('-- [App.__init__] created:', self.btn_event_notification_g4)
        # self.btn_event_notification_g4.hide()

        self.lbl_event_notification_run_g4 = QLabel(self)
        self.lbl_event_notification_run_g4.move(191 + 9 + 18 + 4 + 60 + 4, self.anchor_settings_h + (self.object_height * 1) + (self.inner_group_spacing_h * 3))
        self.lbl_event_notification_run_g4.resize(30, self.monitor_btn_h)
        self.lbl_event_notification_run_g4.setFont(self.font_s8b)
        self.lbl_event_notification_run_g4.setText('Run')
        self.lbl_event_notification_run_g4.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_run_g4)
        # self.lbl_event_notification_g4.hide()

        self.btn_event_notification_run_g4 = QPushButton(self)
        self.btn_event_notification_run_g4.move(191 + 9 + 30 + 4 + 60 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_event_notification_run_g4.resize(18, 18)
        self.btn_event_notification_run_g4.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_run_g4.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_run_g4.clicked.connect(self.btn_event_notification_run_g4_function)
        print('-- [App.__init__] created:', self.btn_event_notification_run_g4)
        # self.btn_event_notification_g4.hide()

        self.btn_event_notification_select_file_g4 = QPushButton(self)
        self.btn_event_notification_select_file_g4.move(191 + 9 + 30 + 4 + 60 + 4 + 18 + 4 + 18 + 4, self.anchor_settings_h + self.object_height + self.inner_group_spacing_h * 3)
        self.btn_event_notification_select_file_g4.resize(20, 20)
        self.btn_event_notification_select_file_g4.setFont(self.font_s10b)
        self.btn_event_notification_select_file_g4.setIcon(QIcon("./image/img_plus.png"))
        self.btn_event_notification_select_file_g4.setStyleSheet(self.btn_settings_style)
        self.btn_event_notification_select_file_g4.clicked.connect(self.openFileNameDialogG4)
        print('-- [App.__init__] created:', self.btn_event_notification_select_file_g4)

        self.lbl_event_notification_g5 = QLabel(self)
        self.lbl_event_notification_g5.move(191 + 9, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_event_notification_g5.resize(60, self.monitor_btn_h)
        self.lbl_event_notification_g5.setFont(self.font_s8b)
        self.lbl_event_notification_g5.setText('G5 Notify')
        self.lbl_event_notification_g5.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_g5)
        # self.lbl_event_notification_g5.hide()

        self.btn_event_notification_g5 = QPushButton(self)
        self.btn_event_notification_g5.move(191 + 9 + 60 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_event_notification_g5.resize(18, 18)
        self.btn_event_notification_g5.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_g5.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_g5.clicked.connect(self.btn_event_notification_g5_function)
        print('-- [App.__init__] created:', self.btn_event_notification_g5)
        # self.btn_event_notification_g5.hide()

        self.lbl_event_notification_run_g5 = QLabel(self)
        self.lbl_event_notification_run_g5.move(191 + 9 + 18 + 4 + 60 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_event_notification_run_g5.resize(30, self.monitor_btn_h)
        self.lbl_event_notification_run_g5.setFont(self.font_s8b)
        self.lbl_event_notification_run_g5.setText('Run')
        self.lbl_event_notification_run_g5.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_run_g5)
        # self.lbl_event_notification_g4.hide()

        self.btn_event_notification_run_g5 = QPushButton(self)
        self.btn_event_notification_run_g5.move(191 + 9 + 30 + 4 + 60 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_event_notification_run_g5.resize(18, 18)
        self.btn_event_notification_run_g5.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_run_g5.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_run_g5.clicked.connect(self.btn_event_notification_run_g5_function)
        print('-- [App.__init__] created:', self.btn_event_notification_run_g5)
        # self.btn_event_notification_g4.hide()

        self.btn_event_notification_select_file_g5 = QPushButton(self)
        self.btn_event_notification_select_file_g5.move(191 + 9 + 30 + 4 + 60 + 4 + 18 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_event_notification_select_file_g5.resize(20, 20)
        self.btn_event_notification_select_file_g5.setFont(self.font_s10b)
        self.btn_event_notification_select_file_g5.setIcon(QIcon("./image/img_plus.png"))
        self.btn_event_notification_select_file_g5.setStyleSheet(self.btn_settings_style)
        self.btn_event_notification_select_file_g5.clicked.connect(self.openFileNameDialogG5)
        print('-- [App.__init__] created:', self.btn_event_notification_select_file_g5)

        self.lbl_event_notification_g6 = QLabel(self)
        self.lbl_event_notification_g6.move(191 + 9, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.lbl_event_notification_g6.resize(60, self.monitor_btn_h)
        self.lbl_event_notification_g6.setFont(self.font_s8b)
        self.lbl_event_notification_g6.setText('G6 Notify')
        self.lbl_event_notification_g6.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_g6)
        # self.lbl_event_notification_g6.hide()

        self.btn_event_notification_g6 = QPushButton(self)
        self.btn_event_notification_g6.move(191 + 9 + 60 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_event_notification_g6.resize(18, 18)
        self.btn_event_notification_g6.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_g6.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_g6.clicked.connect(self.btn_event_notification_g6_function)
        print('-- [App.__init__] created:', self.btn_event_notification_g6)
        # self.btn_event_notification_g6.hide()

        self.lbl_event_notification_run_g6 = QLabel(self)
        self.lbl_event_notification_run_g6.move(191 + 9 + 4 + 60 + 4 + 18, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.lbl_event_notification_run_g6.resize(30, self.monitor_btn_h)
        self.lbl_event_notification_run_g6.setFont(self.font_s8b)
        self.lbl_event_notification_run_g6.setText('Run')
        self.lbl_event_notification_run_g6.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_event_notification_run_g6)
        # self.lbl_event_notification_g6.hide()

        self.btn_event_notification_run_g6 = QPushButton(self)
        self.btn_event_notification_run_g6.move(191 + 9 + 60 + 4 + 18 + 4 + 30 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_event_notification_run_g6.resize(18, 18)
        self.btn_event_notification_run_g6.setIconSize(self.tog_switch_ico_sz)
        self.btn_event_notification_run_g6.setStyleSheet(self.btn_tog_switch_style)
        self.btn_event_notification_run_g6.clicked.connect(self.btn_event_notification_run_g6_function)
        print('-- [App.__init__] created:', self.btn_event_notification_run_g6)
        # self.btn_event_notification_g6.hide()

        self.btn_event_notification_select_file_g6 = QPushButton(self)
        self.btn_event_notification_select_file_g6.move(191 + 9 + 60 + 4 + 18 + 4 + 30 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 3) + (self.inner_group_spacing_h * 5))
        self.btn_event_notification_select_file_g6.resize(20, 20)
        self.btn_event_notification_select_file_g6.setFont(self.font_s10b)
        self.btn_event_notification_select_file_g6.setIcon(QIcon("./image/img_plus.png"))
        self.btn_event_notification_select_file_g6.setStyleSheet(self.btn_settings_style)
        self.btn_event_notification_select_file_g6.clicked.connect(self.openFileNameDialogG6)
        print('-- [App.__init__] created:', self.btn_event_notification_select_file_g6)

        self.lbl_backlight_auto = QLabel(self)
        self.lbl_backlight_auto.move(self.scroll_w + 2, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.lbl_backlight_auto.resize(104, self.monitor_btn_h)
        self.lbl_backlight_auto.setFont(self.font_s8b)
        self.lbl_backlight_auto.setText('AUTO BACKLIGHT')
        self.lbl_backlight_auto.setStyleSheet(self.lbl_white_txt_style)
        print('-- [App.__init__] created:', self.lbl_backlight_auto)

        self.btn_backlight_auto = QPushButton(self)
        self.btn_backlight_auto.move(self.scroll_w + 2 + 104 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_backlight_auto.resize(18, 18)
        self.btn_backlight_auto.setStyleSheet(self.btn_tog_switch_style)
        self.btn_backlight_auto.setIconSize(self.tog_switch_ico_sz)
        self.btn_backlight_auto.clicked.connect(self.backlight_auto_function)
        print('-- [App.__init__] created:', self.btn_backlight_auto)

        self.btn_backlight_auto_time_0 = QLineEdit(self)
        self.btn_backlight_auto_time_0.resize(42, self.monitor_btn_h)
        self.btn_backlight_auto_time_0.move(self.scroll_w + 2 + 104 + 4 + 18 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_backlight_auto_time_0.setFont(self.font_s8b)
        self.btn_backlight_auto_time_0.returnPressed.connect(self.btn_backlight_auto_time_0_function)
        self.btn_backlight_auto_time_0.setStyleSheet(self.qle_unselected)
        self.btn_backlight_auto_time_0.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.btn_backlight_auto_time_0)
        self.btn_backlight_auto_time_0.setToolTip('Automatic Backlight Time On\n\nAccepts only 24h Format.\n\nExample 1: 0000\nExample 2: 0030\nExample 3: 0900')

        self.btn_backlight_auto_time_1 = QLineEdit(self)
        self.btn_backlight_auto_time_1.resize(42, self.monitor_btn_h)
        self.btn_backlight_auto_time_1.move(self.scroll_w + 2 + 104 + 4 + 18 + 4 + 42 + 4, self.anchor_settings_h + (self.object_height * 2) + (self.inner_group_spacing_h * 4))
        self.btn_backlight_auto_time_1.setFont(self.font_s8b)
        self.btn_backlight_auto_time_1.returnPressed.connect(self.btn_backlight_auto_time_1_function)
        self.btn_backlight_auto_time_1.setStyleSheet(self.qle_unselected)
        self.btn_backlight_auto_time_1.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.btn_backlight_auto_time_1)
        self.btn_backlight_auto_time_1.setToolTip('Automatic Backlight Time Off\n\nAccepts only 24h Format.\n\nExample 1: 0000\nExample 2: 0030\nExample 3: 0900')

        self.btn_cpu_mon.setToolTip('CPU Utilization Monitor\n\nEnables/Disables CPU utilization monitor.')
        self.lbl_cpu_mon.setToolTip('CPU Utilization Monitor\n\nKeypad 1:       0-25%\nKeypad 4:       25-50%\nKeypad 7:       50-75%\nNumlock:       75-100%.')
        self.qle_cpu_mon_rgb_on.setToolTip('CPU Utilization Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_cpu_led_time_on.setToolTip('CPU Utilization Monitor\n\nTime Interval:\nMinimum: 0.1 Seconds\nMaximum: 5 seconds\n\nQuality: 0.1\nPerformance: 1-5.')
        self.btn_hotbar_cpu_mon.setToolTip('CPU Utilization Monitor\n\nEnable/Disable')

        self.btn_dram_mon.setToolTip('DRAM Utilization Monitor\n\nEnables/Disables DRAM utilization monitor.')
        self.lbl_dram_mon.setToolTip('DRAM Utilization Monitor\n\nKeypad 2:                  0-25%\nKeypad 5:                  25-50%\nKeypad 8:                  50-75%\nKeypad Slash:           75-100%.')
        self.qle_dram_mon_rgb_on.setToolTip('DRAM Utilization Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_dram_led_time_on.setToolTip('DRAM Utilization Monitor\n\nTime Interval:\nMinimum: 0.1 Seconds\nMaximum: 5 seconds\n\nQuality: 0.1\nPerformance: 1-5.')
        self.btn_hotbar_dram_mon.setToolTip('DRAM Utilization Monitor\n\nEnable/Disable')

        self.btn_vram_mon.setToolTip('VRAM Utilization Monitor\n\nEnables/Disables VRAM utilization monitor.')
        self.lbl_vram_mon.setToolTip( 'VRAM Utilization Monitor\n\nKeypad 3:                     0-25%\nKeypad 6:                     25-50%\nKeypad 9:                     50-75%\nKeypad Asterisk:         75-100%.')
        self.qle_vram_mon_rgb_on.setToolTip('VRAM Utilization Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_vram_led_time_on.setToolTip('VRAM Utilization Monitor\n\nTime Interval:\nMinimum: 0.1 Seconds\nMaximum: 5 seconds\n\nQuality: 0.1\nPerformance: 1-5.')
        self.btn_hotbar_vram_mon.setToolTip('VRAM Utilization Monitor\n\nEnable/Disable')

        self.btn_hdd_mon.setToolTip('Disk Read/Write Monitor\n\nEnables/Disables read/write monitor.')
        self.lbl_hdd_write_mon.setToolTip( "Disk Write Monitor\n\nWrites to disks assigned a disk letter will be displayed on\ncorresponding letters on the keyboard.")
        self.qle_hdd_mon_rgb_on.setToolTip('Disk Write Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_hdd_led_time_on.setToolTip('Disk Read/Write Monitor\n\nTime Interval:\nMinimum: 0 Seconds\nMaximum: 5 seconds\n\nQuality: 0\nPerformance: 1-5\n\n(Applies to both disk reads & disk writes).')
        self.lbl_hdd_read_mon.setToolTip("Disk Read Monitor\n\nDisks assigned a disk letter that are being read will be displayed on\ncorresponding letters on the keyboard.")
        self.qle_hdd_read_mon_rgb_on.setToolTip('Disk Read Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.btn_hotbar_diskrw_mon.setToolTip('Disk Read/Write Monitor\n\nEnable/Disable')

        self.btn_network_adapter.setToolTip('Network Traffic Monitor\n\nEnables/Disables network traffic monitor.')
        self.lbl_network_adapter.setToolTip('Network Traffic Monitor\n\nNetwork Bytes Sent:\nNumber of Bytes: F1 - F9\nBytes: Red\nKB: Green\nMB: Blue\nGB: Light Blue\nTB: White\nF10: Units (Red) Tens (Blue) Hundreds (Light Blue) Thousands+ (White).\n\nNetwork Bytes Received:\nNumber of Bytes: 1 - 9\nBytes: Red\nKB: Green\nMB: Blue\nGB: Light Blue\nTB: White\n10: Units (Red) Tens (Blue) Hundreds (Light Blue) Thousands+ (White).')
        self.cmb_network_adapter_name.setToolTip('Network Traffic Monitor\n\nSelect network adapter to monitor sent/received\nnetwork traffic information which will\nbe displayed on the keyboard.')
        self.btn_network_adapter_refresh.setToolTip('Network Traffic Monitor\n\nRefresh list of network adapters.')
        self.qle_network_adapter_led_time_on.setToolTip('Network Traffic Monitor\n\nTime Interval:\nMinimum: 0.0 Seconds\nMaximum: 5 seconds\n\nQuality: 0.0\nPerformance: 1-5.')
        self.btn_hotbar_nettraffic_mon.setToolTip('Network Traffic Monitor\n\nEnable/Disable')

        self.btn_net_con_kb.setToolTip('Internet Connection Monitor\n\nEnables/Disables internet connection monitor on the keyboard.')
        self.btn_net_con_mouse.setToolTip('Internet Connection Monitor\n\nEnables/Disables internet connection monitor on the mouse.')
        self.lbl_net_con_mouse.setToolTip( 'Internet Connection Monitor\n\nInternet connection status is\ndisplayed on a mouse.')
        self.lbl_net_con_kb.setToolTip(  'Internet Connection Monitor\n\nInternet connection status is\ndisplayed on a keyboard.')
        self.btn_net_con_mouse_led_selected_prev.setToolTip('Internet Connection Monitor\n\nSelect Previous mouse LED in which to\ndisplay internet connection status.')
        self.btn_net_con_mouse_led_selected_next.setToolTip('Internet Connection Monitor\n\nSelect Next mouse LED in which to\ndisplay internet connection status.')
        self.lbl_net_con_mouse_led_selected.setToolTip('Internet Connection Monitor\n\nDisplays which mouse LED will display internet connection status.')
        self.btn_hotbar_netcon_ms_mon.setToolTip('Internet Connection Monitor (Displayed On Mouse)\n\nEnable/Disable')
        self.btn_hotbar_netcon_kb_mon.setToolTip('Internet Connection Monitor (Displayed On Keyboard)\n\nEnable/Disable')

        self.lbl_exclusive_con.setToolTip('Exclusive Control\n\nThis setting when enabled gives iCUE-Display full\ncontrol of connected iCUE devices.\n\nThis is recommended however you may leave this\noption disabled if you have particular customization preferences.')
        self.btn_exclusive_con.setToolTip('Exclusive Control\n\nEnables/Disables iCUE-Display exclusive control.')

        self.lbl_run_startup.setToolTip('Start Automatically\n\niCUE-Display can start automatically when you log in.')
        self.btn_run_startup.setToolTip('Start Automatically\n\nEnables/Disables iCUE-Display automatic startup.')
        self.lbl_start_minimized.setToolTip('Start Minimized\n\nWhen launching iCUE-Display, the\napplication will be minimized to taskbar.\n\nThis Feature is useful when automatic\nstartup is also enabled.')
        self.btn_start_minimized.setToolTip('Start Minimized\n\nEnables/Disables iCUE-Display window starting minimized\nwhen launched.')

        self.lbl_netshare_mon.setToolTip("Network Share Monitor\n\nPrntScr: IPC$ Default Share\nScrLck: ADMIN$ Default Share\nPause/Break: Disks Default Share\nHome: Non-Default Shares")
        self.btn_netshare_mon.setToolTip('Network Share Monitor\n\nEnables/Disables iCUE-Display Network Share Monitor.')
        self.btn_hotbar_netshare_mon.setToolTip('Network Share Monitor\n\nEnable/Disable')

        self.btn_bck_light.setToolTip('Backlight\n\nEnable/Disable')
        self.btn_refresh_recompile.setToolTip('Refresh\n\n')

        self.cpu_led_color_str = ""
        self.dram_led_color_str = ""
        self.vram_led_color_str = ""
        self.hdd_led_color_str = ""
        self.hdd_led_read_color_str = ""

        self.cpu_led_time_on_str = ""
        self.dram_led_time_on_str = ""
        self.vram_led_time_on_str = ""
        self.hdd_led_time_on_str = ""

        self.network_adapter_led_time_on_str = ""

        self.write_var = ''
        self.write_var_bool = False
        self.write_var_key = -1
        self.write_engaged = False

        self.hide_all_features()

        self.initUI()

    def openFileNameDialogG1(self):
        global str_event_notification_run_path_g1, devices_kb
        print('-- [App.openFileNameDialogG1]: plugged in')

        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select G1 File To Run", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.openFileNameDialogG1] file selected:', fileName)
                str_event_notification_run_path_g1 = fileName
                self.setFocus()
                if self.write_engaged is False:
                    print('-- [App.btn_event_notification_g1_function] changing str_event_notification_run_path_g1:', str_event_notification_run_path_g1)
                    self.write_var = 'str_event_notification_run_path_g1: '+str_event_notification_run_path_g1
                    self.write_changes()

    def openFileNameDialogG2(self):
        global str_event_notification_run_path_g2, devices_kb
        print('-- [App.openFileNameDialogG2]: plugged in')
        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select G2 File To Run", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.openFileNameDialogG2] file selected:', fileName)
                str_event_notification_run_path_g2 = fileName
                self.setFocus()
                if self.write_engaged is False:
                    print('-- [App.btn_event_notification_g2_function] changing str_event_notification_run_path_g2:', str_event_notification_run_path_g2)
                    self.write_var = 'str_event_notification_run_path_g2: '+str_event_notification_run_path_g2
                    self.write_changes()

    def openFileNameDialogG3(self):
        global str_event_notification_run_path_g3, devices_kb
        print('-- [App.openFileNameDialogG3]: plugged in')
        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select G3 File To Run", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.openFileNameDialogG3] file selected:', fileName)
                str_event_notification_run_path_g3 = fileName
                self.setFocus()
                if self.write_engaged is False:
                    print('-- [App.btn_event_notification_g3_function] changing str_event_notification_run_path_g3:', str_event_notification_run_path_g3)
                    self.write_var = 'str_event_notification_run_path_g3: '+str_event_notification_run_path_g3
                    self.write_changes()

    def openFileNameDialogG4(self):
        global str_event_notification_run_path_g4, devices_kb
        print('-- [App.openFileNameDialogG4]: plugged in')
        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select G4 File To Run", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.openFileNameDialogG4] file selected:', fileName)
                str_event_notification_run_path_g4 = fileName
                self.setFocus()
                if self.write_engaged is False:
                    print('-- [App.btn_event_notification_g4_function] changing str_event_notification_run_path_g4:', str_event_notification_run_path_g4)
                    self.write_var = 'str_event_notification_run_path_g4: '+str_event_notification_run_path_g4
                    self.write_changes()

    def openFileNameDialogG5(self):
        global str_event_notification_run_path_g5, devices_kb
        print('-- [App.openFileNameDialogG5]: plugged in')
        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select G5 File To Run", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.openFileNameDialogG5] file selected:', fileName)
                str_event_notification_run_path_g5 = fileName
                self.setFocus()
                if self.write_engaged is False:
                    print('-- [App.btn_event_notification_g5_function] changing str_event_notification_run_path_g5:', str_event_notification_run_path_g5)
                    self.write_var = 'str_event_notification_run_path_g5: '+str_event_notification_run_path_g5
                    self.write_changes()

    def openFileNameDialogG6(self):
        global str_event_notification_run_path_g6, devices_kb
        print('-- [App.openFileNameDialogG6]: plugged in')
        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select G6 File To Run", "",
                                                      "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.openFileNameDialogG6] file selected:', fileName)
                str_event_notification_run_path_g6 = fileName
                self.setFocus()
                if self.write_engaged is False:
                    print('-- [App.btn_event_notification_g6_function] changing str_event_notification_run_path_g6:', str_event_notification_run_path_g6)
                    self.write_var = 'str_event_notification_run_path_g6: '+str_event_notification_run_path_g6
                    self.write_changes()

    def btn_event_notification_g1_function(self):
        print('-- [App.btn_event_notification_g1_function]: plugged in')
        global bool_switch_event_notification_g1, devices_kb
        self.setFocus()
        
        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_g1 is False:
                    bool_switch_event_notification_g1 = True
                    print('-- [App.btn_event_notification_g1_function] changing bool_switch_event_notification_g1: true')
                    self.write_var = 'bool_switch_event_notification_g1: true'
                    self.write_changes()
                    self.btn_event_notification_g1.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_g1 is True:
                    bool_switch_event_notification_g1 = False
                    print('-- [App.btn_event_notification_g1_function] changing bool_switch_event_notification_g1: false')
                    self.write_var = 'bool_switch_event_notification_g1: false'
                    self.write_changes()
                    self.btn_event_notification_g1.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_run_g1_function(self):
        print('-- [App.btn_event_notification_run_g1_function]: plugged in')
        global bool_switch_event_notification_run_g1, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_run_g1 is False:
                    bool_switch_event_notification_run_g1 = True
                    print('-- [App.btn_event_notification_run_g1_function] changing bool_switch_event_notification_run_g1: true')
                    self.write_var = 'bool_switch_event_notification_run_g1: true'
                    self.write_changes()
                    self.btn_event_notification_run_g1.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_run_g1 is True:
                    bool_switch_event_notification_run_g1 = False
                    print('-- [App.btn_event_notification_run_g1_function] changing bool_switch_event_notification_run_g1: false')
                    self.write_var = 'bool_switch_event_notification_run_g1: false'
                    self.write_changes()
                    self.btn_event_notification_run_g1.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_g2_function(self):
        print('-- [App.btn_event_notification_g2_function]: plugged in')
        global bool_switch_event_notification_g2, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_g2 is False:
                    bool_switch_event_notification_g2 = True
                    print('-- [App.btn_event_notification_g2_function] changing bool_switch_event_notification_g2: true')
                    self.write_var = 'bool_switch_event_notification_g2: true'
                    self.write_changes()
                    self.btn_event_notification_g2.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_g2 is True:
                    bool_switch_event_notification_g2 = False
                    print('-- [App.btn_event_notification_g2_function] changing bool_switch_event_notification_g2: false')
                    self.write_var = 'bool_switch_event_notification_g2: false'
                    self.write_changes()
                    self.btn_event_notification_g2.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_run_g2_function(self):
        print('-- [App.btn_event_notification_run_g2_function]: plugged in')
        global bool_switch_event_notification_run_g2, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_run_g2 is False:
                    bool_switch_event_notification_run_g2 = True
                    print('-- [App.btn_event_notification_run_g2_function] changing bool_switch_event_notification_run_g2: true')
                    self.write_var = 'bool_switch_event_notification_run_g2: true'
                    self.write_changes()
                    self.btn_event_notification_run_g2.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_run_g2 is True:
                    bool_switch_event_notification_run_g2 = False
                    print('-- [App.btn_event_notification_run_g2_function] changing bool_switch_event_notification_run_g2: false')
                    self.write_var = 'bool_switch_event_notification_run_g2: false'
                    self.write_changes()
                    self.btn_event_notification_run_g2.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_g3_function(self):
        print('-- [App.btn_event_notification_g3_function]: plugged in')
        global bool_switch_event_notification_g3, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_g3 is False:
                    bool_switch_event_notification_g3 = True
                    print('-- [App.btn_event_notification_g3_function] changing bool_switch_event_notification_g3: true')
                    self.write_var = 'bool_switch_event_notification_g3: true'
                    self.write_changes()
                    self.btn_event_notification_g3.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_g3 is True:
                    bool_switch_event_notification_g3 = False
                    print('-- [App.btn_event_notification_g3_function] changing bool_switch_event_notification_g3: false')
                    self.write_var = 'bool_switch_event_notification_g3: false'
                    self.write_changes()
                    self.btn_event_notification_g3.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_run_g3_function(self):
        print('-- [App.btn_event_notification_run_g3_function]: plugged in')
        global bool_switch_event_notification_run_g3, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_run_g3 is False:
                    bool_switch_event_notification_run_g3 = True
                    print('-- [App.btn_event_notification_run_g3_function] changing bool_switch_event_notification_run_g3: true')
                    self.write_var = 'bool_switch_event_notification_run_g3: true'
                    self.write_changes()
                    self.btn_event_notification_run_g3.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_run_g3 is True:
                    bool_switch_event_notification_run_g3 = False
                    print('-- [App.btn_event_notification_run_g3_function] changing bool_switch_event_notification_run_g3: false')
                    self.write_var = 'bool_switch_event_notification_run_g3: false'
                    self.write_changes()
                    self.btn_event_notification_run_g3.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_g4_function(self):
        print('-- [App.btn_event_notification_g4_function]: plugged in')
        global bool_switch_event_notification_g4, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_g4 is False:
                    bool_switch_event_notification_g4 = True
                    print('-- [App.btn_event_notification_g4_function] changing bool_switch_event_notification_g4: true')
                    self.write_var = 'bool_switch_event_notification_g4: true'
                    self.write_changes()
                    self.btn_event_notification_g4.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_g4 is True:
                    bool_switch_event_notification_g4 = False
                    print('-- [App.btn_event_notification_g4_function] changing bool_switch_event_notification_g4: false')
                    self.write_var = 'bool_switch_event_notification_g4: false'
                    self.write_changes()
                    self.btn_event_notification_g4.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_run_g4_function(self):
        print('-- [App.btn_event_notification_run_g4_function]: plugged in')
        global bool_switch_event_notification_run_g4, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_run_g4 is False:
                    bool_switch_event_notification_run_g4 = True
                    print('-- [App.btn_event_notification_run_g4_function] changing bool_switch_event_notification_run_g4: true')
                    self.write_var = 'bool_switch_event_notification_run_g4: true'
                    self.write_changes()
                    self.btn_event_notification_run_g4.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_run_g4 is True:
                    bool_switch_event_notification_run_g4 = False
                    print('-- [App.btn_event_notification_run_g4_function] changing bool_switch_event_notification_run_g4: false')
                    self.write_var = 'bool_switch_event_notification_run_g4: false'
                    self.write_changes()
                    self.btn_event_notification_run_g4.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_g5_function(self):
        print('-- [App.btn_event_notification_g5_function]: plugged in')
        global bool_switch_event_notification_g5, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_g5 is False:
                    bool_switch_event_notification_g5 = True
                    print('-- [App.btn_event_notification_g5_function] changing bool_switch_event_notification_g5: true')
                    self.write_var = 'bool_switch_event_notification_g5: true'
                    self.write_changes()
                    self.btn_event_notification_g5.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_g5 is True:
                    bool_switch_event_notification_g5 = False
                    print('-- [App.btn_event_notification_g5_function] changing bool_switch_event_notification_g5: false')
                    self.write_var = 'bool_switch_event_notification_g5: false'
                    self.write_changes()
                    self.btn_event_notification_g5.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_run_g5_function(self):
        print('-- [App.btn_event_notification_run_g5_function]: plugged in')
        global bool_switch_event_notification_run_g5, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_run_g5 is False:
                    bool_switch_event_notification_run_g5 = True
                    print('-- [App.btn_event_notification_run_g5_function] changing bool_switch_event_notification_run_g5: true')
                    self.write_var = 'bool_switch_event_notification_run_g5: true'
                    self.write_changes()
                    self.btn_event_notification_run_g5.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_run_g5 is True:
                    bool_switch_event_notification_run_g5 = False
                    print('-- [App.btn_event_notification_run_g5_function] changing bool_switch_event_notification_run_g5: false')
                    self.write_var = 'bool_switch_event_notification_run_g5: false'
                    self.write_changes()
                    self.btn_event_notification_run_g5.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_g6_function(self):
        print('-- [App.btn_event_notification_g6_function]: plugged in')
        global bool_switch_event_notification_g6, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_g6 is False:
                    bool_switch_event_notification_g6 = True
                    print('-- [App.btn_event_notification_g6_function] changing bool_switch_event_notification_g6: true')
                    self.write_var = 'bool_switch_event_notification_g6: true'
                    self.write_changes()
                    self.btn_event_notification_g6.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_g6 is True:
                    bool_switch_event_notification_g6 = False
                    print('-- [App.btn_event_notification_g6_function] changing bool_switch_event_notification_g6: false')
                    self.write_var = 'bool_switch_event_notification_g6: false'
                    self.write_changes()
                    self.btn_event_notification_g6.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_event_notification_run_g6_function(self):
        print('-- [App.btn_event_notification_run_g6_function]: plugged in')
        global bool_switch_event_notification_run_g6, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_event_notification_run_g6 is False:
                    bool_switch_event_notification_run_g6 = True
                    print('-- [App.btn_event_notification_run_g6_function] changing bool_switch_event_notification_run_g6: true')
                    self.write_var = 'bool_switch_event_notification_run_g6: true'
                    self.write_changes()
                    self.btn_event_notification_run_g6.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                elif bool_switch_event_notification_run_g6 is True:
                    bool_switch_event_notification_run_g6 = False
                    print('-- [App.btn_event_notification_run_g6_function] changing bool_switch_event_notification_run_g6: false')
                    self.write_var = 'bool_switch_event_notification_run_g6: false'
                    self.write_changes()
                    self.btn_event_notification_run_g6.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def recompile(self):
        print('-- [App.recompile]: plugged in')
        global thread_compile_devices, devices_previous
        print('-- [App.recompile] stopping thread: thread_compile_devices:')
        thread_compile_devices[0].stop()
        devices_previous = []
        print('-- [App.recompile] starting thread: thread_compile_devices:')
        thread_compile_devices[0].start()

    def default_hotbar_style(self):
        print('-- [App.default_hotbar_style]: plugged in')
        global bool_switch_startup_cpu_util, bool_switch_startup_dram_util, bool_switch_startup_vram_util
        global bool_switch_startup_hdd_read_write, bool_switch_startup_net_traffic
        global bool_switch_startup_net_con_ms, bool_switch_startup_net_con_kb
        global bool_switch_startup_net_share_mon, bool_switch_backlight

        if bool_switch_startup_cpu_util is True:
            self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_cpu_util is False:
            self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_dram_util is True:
            self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_dram_util is False:
            self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_vram_util is True:
            self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_dram_util is False:
            self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_hdd_read_write is True:
            self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_hdd_read_write is False:
            self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_net_traffic is True:
            self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_net_traffic is False:
            self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_net_con_ms is True:
            self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_net_con_ms is False:
            self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_net_con_kb is True:
            self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_net_con_kb is False:
            self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_startup_net_share_mon is True:
            self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_startup_net_share_mon is False:
            self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_off_style)

        if bool_switch_backlight is True:
            self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
        elif bool_switch_backlight is False:
            self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)

    def utilization_style(self):
        print('-- [App.utilization_style]: plugged in')
        if bool_switch_startup_cpu_util is True:
            self.btn_hotbar_cpu_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_cpu_util is False:
            self.btn_hotbar_cpu_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

        if bool_switch_startup_dram_util is True:
            self.btn_hotbar_dram_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_dram_util is False:
            self.btn_hotbar_dram_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

        if bool_switch_startup_vram_util is True:
            self.btn_hotbar_vram_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_dram_util is False:
            self.btn_hotbar_vram_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

    def disk_rw_style(self):
        print('-- [App.disk_rw_style]: plugged in')
        if bool_switch_startup_hdd_read_write is True:
            self.btn_hotbar_diskrw_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_hdd_read_write is False:
            self.btn_hotbar_diskrw_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

    def net_traffic_style(self):
        print('-- [App.net_traffic_style]: plugged in')
        if bool_switch_startup_net_traffic is True:
            self.btn_hotbar_nettraffic_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_net_traffic is False:
            self.btn_hotbar_nettraffic_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

    def netcon_style(self):
        print('-- [App.netcon_style]: plugged in')
        if bool_switch_startup_net_con_ms is True:
            self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_net_con_ms is False:
            self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

        if bool_switch_startup_net_con_kb is True:
            self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_net_con_kb is False:
            self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

    def netshare_style(self):
        print('-- [App.netshare_style]: plugged in')
        if bool_switch_startup_net_share_mon is True:
            self.btn_hotbar_netshare_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_startup_net_share_mon is False:
            self.btn_hotbar_netshare_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

    def backlight_style(self):
        print('-- [App.netshare_style]: plugged in')
        if bool_switch_backlight is True:
            self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
        elif bool_switch_backlight is False:
            self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)

    def hide_all_features(self):
        print('-- [App.hide_all_features]: plugged in')
        try:
            self.setFocus()
            self.btn_scroll_r.hide()
            self.btn_scroll_l.hide()

            self.lbl_hdd_led_time_on_vis_combine.hide()
            self.lbl_settings_border.hide()
            self.lbl_utilization.hide()
            self.lbl_cpu_mon.hide()
            self.btn_cpu_mon.hide()
            self.qle_cpu_mon_rgb_on.hide()
            self.qle_cpu_led_time_on.hide()
            self.lbl_dram_mon.hide()
            self.btn_dram_mon.hide()
            self.qle_dram_mon_rgb_on.hide()
            self.qle_dram_led_time_on.hide()
            self.lbl_vram_mon.hide()
            self.btn_vram_mon.hide()
            self.qle_vram_mon_rgb_on.hide()
            self.qle_vram_led_time_on.hide()

            self.lbl_backlight.hide()
            self.lbl_backlight_sub.hide()
            self.btn_backlight_sub.hide()
            self.qle_backlight_rgb_on.hide()

            self.lbl_backlight.hide()
            self.lbl_backlight_sub.hide()
            self.btn_backlight_sub.hide()
            self.qle_backlight_rgb_on.hide()
            self.lbl_backlight_auto.hide()
            self.btn_backlight_auto.hide()
            self.btn_backlight_auto_time_0.hide()
            self.btn_backlight_auto_time_1.hide()

            self.lbl_event_notification.hide()
            self.lbl_event_notification_g1.hide()
            self.btn_event_notification_g1.hide()
            self.lbl_event_notification_g2.hide()
            self.btn_event_notification_g2.hide()
            self.lbl_event_notification_g3.hide()
            self.btn_event_notification_g3.hide()
            self.lbl_event_notification_g4.hide()
            self.btn_event_notification_g4.hide()
            self.lbl_event_notification_g5.hide()
            self.btn_event_notification_g5.hide()
            self.lbl_event_notification_g6.hide()
            self.btn_event_notification_g6.hide()

            self.lbl_event_notification_run_g1.hide()
            self.btn_event_notification_run_g1.hide()
            self.btn_event_notification_select_file_g1.hide()

            self.lbl_event_notification_run_g2.hide()
            self.btn_event_notification_run_g2.hide()
            self.btn_event_notification_select_file_g2.hide()

            self.lbl_event_notification_run_g3.hide()
            self.btn_event_notification_run_g3.hide()
            self.btn_event_notification_select_file_g3.hide()

            self.lbl_event_notification_run_g4.hide()
            self.btn_event_notification_run_g4.hide()
            self.btn_event_notification_select_file_g4.hide()

            self.lbl_event_notification_run_g5.hide()
            self.btn_event_notification_run_g5.hide()
            self.btn_event_notification_select_file_g5.hide()

            self.lbl_event_notification_run_g6.hide()
            self.btn_event_notification_run_g6.hide()
            self.btn_event_notification_select_file_g6.hide()

            self.lbl_hdd_mon.hide()
            self.lbl_hdd_write_mon.hide()
            self.btn_hdd_mon.hide()
            self.qle_hdd_mon_rgb_on.hide()
            self.qle_hdd_led_time_on.hide()
            self.lbl_hdd_read_mon.hide()
            self.qle_hdd_read_mon_rgb_on.hide()

            self.lbl_network_traffic.hide()
            self.lbl_network_adapter.hide()
            self.cmb_network_adapter_name.hide()
            self.btn_network_adapter_refresh.hide()
            self.btn_network_adapter.hide()
            self.qle_network_adapter_led_time_on.hide()

            self.lbl_connectivity.hide()
            self.lbl_net_con_mouse.hide()
            self.btn_net_con_mouse.hide()
            self.btn_net_con_mouse_led_selected_prev.hide()
            self.lbl_net_con_mouse_led_selected.hide()
            self.btn_net_con_mouse_led_selected_next.hide()
            self.lbl_net_con_kb.hide()
            self.btn_net_con_kb.hide()

            self.lbl_netshare.hide()
            self.lbl_netshare_mon.hide()
            self.btn_netshare_mon.hide()
            self.qle_netshare_mon_rgb_on.hide()

            self.lbl_settings.hide()
            self.lbl_exclusive_con.hide()
            self.btn_exclusive_con.hide()
            self.lbl_run_startup.hide()
            self.btn_run_startup.hide()
            self.lbl_start_minimized.hide()
            self.btn_start_minimized.hide()

            if bool_switch_startup_cpu_util is True:
                self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_cpu_util is False:
                self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_dram_util is True:
                self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_dram_util is False:
                self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_vram_util is True:
                self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_vram_util is False:
                self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_hdd_read_write is True:
                self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_hdd_read_write is False:
                self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_net_traffic is True:
                self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_net_traffic is False:
                self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_net_con_kb is True:
                self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_net_con_kb is False:
                self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_net_con_ms is True:
                self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_net_con_ms is False:
                self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_startup_net_share_mon is True:
                self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_startup_net_share_mon is False:
                self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_off_style)

            if bool_switch_backlight is True:
                self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
            elif bool_switch_backlight is False:
                self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)

        except Exception as e:
            print(e)

    def show_utilization(self):
        print('-- [App.show_utilization]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_settings_border.show()
            self.lbl_utilization.show()
            self.lbl_cpu_mon.show()
            self.btn_cpu_mon.show()
            self.qle_cpu_mon_rgb_on.show()
            self.qle_cpu_led_time_on.show()
            self.lbl_dram_mon.show()
            self.btn_dram_mon.show()
            self.qle_dram_mon_rgb_on.show()
            self.qle_dram_led_time_on.show()
            self.lbl_vram_mon.show()
            self.btn_vram_mon.show()
            self.qle_vram_mon_rgb_on.show()
            self.qle_vram_led_time_on.show()

            self.utilization_style()
        except Exception as e:
            print(e)

    def show_disks(self):
        print('-- [App.show_disks]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_hdd_led_time_on_vis_combine.show()
            self.lbl_settings_border.show()
            self.lbl_hdd_mon.show()
            self.lbl_hdd_write_mon.show()
            self.btn_hdd_mon.show()
            self.qle_hdd_mon_rgb_on.show()
            self.qle_hdd_led_time_on.show()
            self.lbl_hdd_read_mon.show()
            self.qle_hdd_read_mon_rgb_on.show()

            self.disk_rw_style()
        except Exception as e:
            print(e)

    def show_net_traffic(self):
        print('-- [App.show_net_traffic]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_settings_border.show()
            self.lbl_network_traffic.show()
            self.lbl_network_adapter.show()
            self.cmb_network_adapter_name.show()
            self.btn_network_adapter_refresh.show()
            self.btn_network_adapter.show()
            self.qle_network_adapter_led_time_on.show()

            self.net_traffic_style()
        except Exception as e:
            print(e)

    def show_net_con(self):
        print('-- [App.show_net_con]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_settings_border.show()
            self.lbl_connectivity.show()
            self.lbl_net_con_mouse.show()
            self.btn_net_con_mouse.show()
            self.btn_net_con_mouse_led_selected_prev.show()
            self.lbl_net_con_mouse_led_selected.show()
            self.btn_net_con_mouse_led_selected_next.show()
            self.lbl_net_con_kb.show()
            self.btn_net_con_kb.show()

            self.netcon_style()
        except Exception as e:
            print(e)

    def show_net_share(self):
        print('-- [App.show_net_share]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_settings_border.show()
            self.lbl_netshare.show()
            self.lbl_netshare_mon.show()
            self.btn_netshare_mon.show()
            self.qle_netshare_mon_rgb_on.show()

            self.netshare_style()
        except Exception as e:
            print(e)

    def show_backlight(self):
        print('-- [App.show_backlight]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_settings_border.show()
            self.lbl_backlight.show()
            self.lbl_backlight_sub.show()
            self.btn_backlight_sub.show()
            self.qle_backlight_rgb_on.show()

            self.lbl_backlight_auto.show()
            self.btn_backlight_auto.show()
            self.btn_backlight_auto_time_0.show()
            self.btn_backlight_auto_time_1.show()

            self.backlight_style()
        except Exception as e:
            print(e)

    def show_set(self):
        print('-- [App.show_set]: plugged in')
        try:
            self.btn_scroll_r.show()
            self.btn_scroll_l.show()

            self.lbl_settings_border.show()
            self.lbl_settings.show()
            self.lbl_exclusive_con.show()
            self.btn_exclusive_con.show()
            self.lbl_run_startup.show()
            self.btn_run_startup.show()
            self.lbl_start_minimized.show()
            self.btn_start_minimized.show()
        except Exception as e:
            print(e)

    def show_event_notification(self):
        print('-- [App.show_event_notification]: plugged in')
        self.btn_scroll_r.show()
        self.btn_scroll_l.show()

        self.lbl_settings_border.show()

        self.lbl_event_notification.show()
        self.lbl_event_notification_g1.show()
        self.btn_event_notification_g1.show()
        self.lbl_event_notification_g2.show()
        self.btn_event_notification_g2.show()
        self.lbl_event_notification_g3.show()
        self.btn_event_notification_g3.show()
        self.lbl_event_notification_g4.show()
        self.btn_event_notification_g4.show()
        self.lbl_event_notification_g5.show()
        self.btn_event_notification_g5.show()
        self.lbl_event_notification_g6.show()
        self.btn_event_notification_g6.show()

        self.lbl_event_notification_run_g1.show()
        self.btn_event_notification_run_g1.show()
        self.btn_event_notification_select_file_g1.show()

        self.lbl_event_notification_run_g2.show()
        self.btn_event_notification_run_g2.show()
        self.btn_event_notification_select_file_g2.show()

        self.lbl_event_notification_run_g3.show()
        self.btn_event_notification_run_g3.show()
        self.btn_event_notification_select_file_g3.show()

        self.lbl_event_notification_run_g4.show()
        self.btn_event_notification_run_g4.show()
        self.btn_event_notification_select_file_g4.show()

        self.lbl_event_notification_run_g5.show()
        self.btn_event_notification_run_g5.show()
        self.btn_event_notification_select_file_g5.show()

        self.lbl_event_notification_run_g6.show()
        self.btn_event_notification_run_g6.show()
        self.btn_event_notification_select_file_g6.show()

    def btn_scroll_l_function(self):
        print('-- [App.btn_scroll_l_function]: plugged in')
        global ui_feature_page
        self.setFocus()
        self.hide_all_features()
        if ui_feature_page == 0:
            ui_feature_page = 7
        else:
            ui_feature_page -= 1
        print('-- [App.btn_scroll_l_function] setting ui_feature_page:', ui_feature_page)
        if ui_feature_page == 0:
            self.show_utilization()
        elif ui_feature_page == 1:
            self.show_disks()
        elif ui_feature_page == 2:
            self.show_net_traffic()
        elif ui_feature_page == 3:
            self.show_net_con()
        elif ui_feature_page == 4:
            self.show_net_share()
        elif ui_feature_page == 5:
            self.show_backlight()
        elif ui_feature_page == 6:
            self.show_set()
        # elif ui_feature_page == 7:
            # self.show_key_event_pg_1()
        elif ui_feature_page == 7:
            self.show_event_notification()

    def btn_scroll_r_function(self):
        print('-- [App.btn_scroll_r_function]: plugged in')
        global ui_feature_page
        self.setFocus()
        self.hide_all_features()
        if ui_feature_page == 7:
            ui_feature_page = 0
        else:
            ui_feature_page += 1
        print('-- [App.btn_scroll_r_function] setting ui_feature_page:', ui_feature_page)
        if ui_feature_page == 0:
            self.show_utilization()
        elif ui_feature_page == 1:
            self.show_disks()
        elif ui_feature_page == 2:
            self.show_net_traffic()
        elif ui_feature_page == 3:
            self.show_net_con()
        elif ui_feature_page == 4:
            self.show_net_share()
        elif ui_feature_page == 5:
            self.show_backlight()
        elif ui_feature_page == 6:
            self.show_set()
        # elif ui_feature_page == 7:
        #     self.show_key_event_pg_1()
        elif ui_feature_page == 7:
            self.show_event_notification()

    def sanitize_rgb_values(self):
        print('-- [App.sanitize_rgb_values]: plugged in')
        global sdk_color_cpu_on, sdk_color_dram_on, sdk_color_vram_on, sdk_color_hddwrite_on, sdk_color_hddread_on, sdk_color_netshare_on, sdk_color_backlight_on
        print('-- [App.sanitize_rgb_values] attempting to sanitize input:', self.write_var)
        print('-- [App.sanitize_rgb_values] write_var_key:', self.write_var_key)
        try:
            var_str = self.write_var
            var_str = var_str.replace(' ', '')
            var_str = var_str.split(',')
            self.write_var_bool = False
            if len(var_str) == 3:
                if len(var_str[0]) >= 1 and len(var_str[0]) <= 3:
                    if len(var_str[1]) >= 1 and len(var_str[1]) <= 3:
                        if len(var_str[2]) >= 1 and len(var_str[2]) <= 3:
                            if var_str[0].isdigit():
                                if var_str[1].isdigit():
                                    if var_str[2].isdigit():
                                        var_int_0 = int(var_str[0])
                                        var_int_1 = int(var_str[1])
                                        var_int_2 = int(var_str[2])
                                        if var_int_0 >= 0 and var_int_0 <= 255:
                                            if var_int_1 >= 0 and var_int_1 <= 255:
                                                if var_int_2 >= 0 and var_int_2 <= 255:
                                                    self.write_var_bool = True
                                                    if self.write_var_key == 0:
                                                        sdk_color_cpu_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_cpu_on: ' + self.qle_cpu_mon_rgb_on.text().replace(' ', '')
                                                    elif self.write_var_key == 1:
                                                        sdk_color_dram_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_dram_on: ' + self.qle_dram_mon_rgb_on.text().replace(' ', '')
                                                    elif self.write_var_key == 2:
                                                        sdk_color_vram_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_vram_on: ' + self.qle_vram_mon_rgb_on.text().replace(' ', '')
                                                    elif self.write_var_key == 3:
                                                        sdk_color_hddwrite_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_hddwrite_on: ' + self.qle_hdd_mon_rgb_on.text().replace(' ', '')
                                                    elif self.write_var_key == 9:
                                                        sdk_color_hddread_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_hddread_on: ' + self.qle_hdd_read_mon_rgb_on.text().replace(' ', '')
                                                    elif self.write_var_key == 7:
                                                        sdk_color_netshare_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_netshare_on: ' + self.qle_netshare_mon_rgb_on.text().replace(' ', '')
                                                    elif self.write_var_key == 8:
                                                        sdk_color_backlight_on = [var_int_0, var_int_1, var_int_2]
                                                        self.write_var = 'sdk_color_backlight_on: ' + self.qle_backlight_rgb_on.text().replace(' ', '')
        except Exception as e:
            print('-- [App.sanitize_rgb_values] Error:', e)

    def sanitize_interval(self):
        print('-- [App.sanitize_interval]: plugged in')
        global timing_cpu_util, timing_dram_util, timing_vram_util, timing_hdd_util, timing_net_traffic_util
        self.write_var_bool = False
        self.write_var = self.write_var.replace(' ', '')
        print('-- [App.sanitize_interval] attempting to sanitize input:', self.write_var)
        print('-- [App.sanitize_interval] write_var_key:', self.write_var_key)
        try:
            self.write_var_float = float(float(self.write_var))
            if float(self.write_var_float) >= 0.1 and float(self.write_var_float) <= 5 and self.write_var_key != 3:
                if self.write_var_key == 0:
                    timing_cpu_util = self.write_var_float
                    self.write_var = 'timing_cpu_util: ' + self.write_var
                    self.write_var_bool = True
                elif self.write_var_key == 1:
                    timing_dram_util = self.write_var_float
                    self.write_var = 'timing_dram_util: ' + self.write_var
                    self.write_var_bool = True
                elif self.write_var_key == 2:
                    timing_vram_util = self.write_var_float
                    self.write_var = 'timing_vram_util: ' + self.write_var
                    self.write_var_bool = True
            elif float(self.write_var_float) >= 0 and float(self.write_var_float) <= 5 and self.write_var_key == 4:
                    timing_net_traffic_util = self.write_var_float
                    self.write_var = 'timing_net_traffic_util: ' + self.write_var
                    self.write_var_bool = True
            elif float(self.write_var_float) >= 0 and float(self.write_var_float) <= 5 and self.write_var_key == 3:
                    timing_hdd_util = self.write_var_float
                    self.write_var = 'timing_hdd_util: ' + self.write_var
                    self.write_var_bool = True
        except Exception as e:
            print('-- [App.sanitize_interval] Error:', e)

    def isenabled_true(self):
        print('-- [App.isenabled_true]: plugged in')
        self.btn_cpu_mon.setEnabled(True)
        self.btn_dram_mon.setEnabled(True)
        self.btn_vram_mon.setEnabled(True)
        self.btn_hdd_mon.setEnabled(True)
        self.btn_network_adapter.setEnabled(True)
        self.btn_net_con_kb.setEnabled(True)
        self.btn_net_con_mouse.setEnabled(True)
        self.btn_net_con_mouse_led_selected_next.setEnabled(True)
        self.btn_net_con_mouse_led_selected_prev.setEnabled(True)
        self.btn_netshare_mon.setEnabled(True)
        self.btn_exclusive_con.setEnabled(True)
        self.btn_start_minimized.setEnabled(True)
        self.btn_run_startup.setEnabled(True)
        self.cmb_network_adapter_name.setEnabled(True)

    def isenabled_false(self):
        print('-- [App.isenabled_false]: plugged in')
        self.btn_cpu_mon.setEnabled(False)
        self.btn_dram_mon.setEnabled(False)
        self.btn_vram_mon.setEnabled(False)
        self.btn_hdd_mon.setEnabled(False)
        self.btn_network_adapter.setEnabled(False)
        self.btn_net_con_kb.setEnabled(False)
        self.btn_net_con_mouse.setEnabled(False)
        self.btn_net_con_mouse_led_selected_next.setEnabled(False)
        self.btn_net_con_mouse_led_selected_prev.setEnabled(False)
        self.btn_netshare_mon.setEnabled(False)
        self.btn_exclusive_con.setEnabled(False)
        self.btn_start_minimized.setEnabled(False)
        self.btn_run_startup.setEnabled(False)
        self.cmb_network_adapter_name.setEnabled(False)

    def read_only_true(self):
        print('-- [App.read_only_true]: plugged in')
        self.qle_cpu_mon_rgb_on.setReadOnly(True)
        self.qle_dram_mon_rgb_on.setReadOnly(True)
        self.qle_vram_mon_rgb_on.setReadOnly(True)
        self.qle_hdd_mon_rgb_on.setReadOnly(True)
        self.qle_hdd_read_mon_rgb_on.setReadOnly(True)
        self.qle_netshare_mon_rgb_on.setReadOnly(True)

        self.qle_cpu_led_time_on.setReadOnly(True)
        self.qle_dram_led_time_on.setReadOnly(True)
        self.qle_vram_led_time_on.setReadOnly(True)
        self.qle_hdd_led_time_on.setReadOnly(True)
        self.qle_network_adapter_led_time_on.setReadOnly(True)

    def read_only_false(self):
        print('-- [App.read_only_false]: plugged in')
        self.qle_cpu_mon_rgb_on.setReadOnly(False)
        self.qle_dram_mon_rgb_on.setReadOnly(False)
        self.qle_vram_mon_rgb_on.setReadOnly(False)
        self.qle_hdd_mon_rgb_on.setReadOnly(False)
        self.qle_hdd_read_mon_rgb_on.setReadOnly(False)
        self.qle_netshare_mon_rgb_on.setReadOnly(False)

        self.qle_cpu_led_time_on.setReadOnly(False)
        self.qle_dram_led_time_on.setReadOnly(False)
        self.qle_vram_led_time_on.setReadOnly(False)
        self.qle_hdd_led_time_on.setReadOnly(False)
        self.qle_network_adapter_led_time_on.setReadOnly(False)

    def write_changes(self):
        print('-- [App.write_changes]: plugged in')
        self.write_engaged = True
        try:
            self.read_only_true()
            self.isenabled_false()
            write_var_split = self.write_var.split()
            write_var_split_key = write_var_split[0]
            self.write_var = self.write_var.strip()
            new_config_data = []
            with open('./config.dat', 'r') as fo:
                for line in fo:
                    line = line.strip()
                    # print('-- [App.write_changes] reading configuration line:', line)
                    if line.startswith(write_var_split_key):
                        print('-- [App.write_changes] swapping configuration line:', line)
                        new_config_data.append(self.write_var)
                    else:
                        new_config_data.append(line)
            fo.close()
            open('./config.dat', 'w').close()
            print('-- [App.write_changes] writing changes to configuration file:', self.write_var)
            with open('./config.dat', 'a') as fo:
                i = 0
                for _ in new_config_data:
                    fo.writelines(new_config_data[i] + '\n')
                    i += 1
            fo.close()
            self.read_only_false()
            self.isenabled_true()
        except Exception as e:
            print('-- [App.write_changes] Error:', e)
        self.write_engaged = False

    def btn_show_discrete_function(self):
        print('-- [App.btn_show_discrete_function]: plugged in')
        global bool_switch_show_discrete, ui_feature_page
        self.setFocus()
        if bool_switch_show_discrete is True:
            bool_switch_show_discrete = False
            print('-- [App.btn_show_discrete_function] setting window dimensions:', self.width, self.height)
            self.setFixedSize(self.width, self.height)
            self.btn_show_discrete.setIcon(QIcon("./image/img_scrollbar_up.png"))
            self.btn_show_discrete.move(0, self.height - 20)
            self.show_utilization()
            ui_feature_page = 0
            print('-- [App.btn_show_discrete_function] resetting ui_feature_page:', ui_feature_page)

        elif bool_switch_show_discrete is False:
            bool_switch_show_discrete = True
            print('-- [App.btn_show_discrete_function] setting window dimensions:', self.width, self.height_discrete)
            self.setFixedSize(self.width, self.height_discrete)
            self.btn_show_discrete.setIcon(QIcon("./image/img_scrollbar_down.png"))
            self.btn_show_discrete.move(0, self.height_discrete - 20)
            self.hide_all_features()

    def color_all_id(self):
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight, bool_switch_backlight, ui_feature_page, bool_switch_show_discrete, sdk_color_backlight_on

        global devices_kb, devices_ms
        global thread_net_connection

        if len(devices_kb) > 0:
            for _ in corsairled_id_num_kb_complete:
                itm = [{_: sdk_color_backlight}]
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
            sdk.set_led_colors_flush_buffer()

        if len(devices_ms) > 0:
            for _ in corsairled_id_num_ms_complete:
                itm = [{_: sdk_color_backlight}]
                sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], itm[0])
            sdk.set_led_colors_flush_buffer()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if bool_switch_startup_net_con_kb is True or bool_switch_startup_net_con_ms is True:
                thread_net_connection[0].stop()
                thread_net_connection[0].start()

    def btn_bck_light_function(self):
        print('-- [App.btn_bck_light_function]: plugged in')
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight
        global sdk_color_backlight, bool_switch_backlight, ui_feature_page, bool_switch_show_discrete, sdk_color_backlight_on
        global thread_disk_rw
        self.setFocus()
        if self.write_engaged is False:
            if bool_switch_backlight is False:
                self.write_var = 'bool_switch_backlight: true'
                self.write_changes()
                sdk_color_backlight = sdk_color_backlight_on
                bool_switch_backlight = True
                print('-- [App.btn_bck_light_function] setting bool_switch_backlight:', bool_switch_backlight)
                self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
                if bool_switch_show_discrete is False and ui_feature_page == 5:
                    self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                self.btn_bck_light.setIcon(QIcon("./image/img_backlight_on.png"))
                self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            elif bool_switch_backlight is True:
                self.write_var = 'bool_switch_backlight: false'
                self.write_changes()
                sdk_color_backlight = (0, 0, 0)
                bool_switch_backlight = False
                print('-- [App.btn_bck_light_function] setting bool_switch_backlight:', bool_switch_backlight)
                self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)
                if bool_switch_show_discrete is False and ui_feature_page == 5:
                    self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                self.btn_bck_light.setIcon(QIcon("./image/img_backlight_off.png"))
                self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.color_all_id()

    def backlight_auto_function(self):
        print('-- [App.backlight_auto_function]: plugged in')
        global bool_switch_backlight_auto, thread_backlight_auto, backlight_time_0, backlight_time_1
        global devices_kb, devices_ms
        self.setFocus()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if backlight_time_0.isdigit() and backlight_time_1.isdigit():

                    if bool_switch_backlight_auto is True:
                        thread_backlight_auto[0].stop()
                        bool_switch_backlight_auto = False
                        self.write_var = 'bool_switch_backlight_auto: false'
                        self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                        self.write_changes()

                    elif bool_switch_backlight_auto is False:
                        thread_backlight_auto[0].start()
                        bool_switch_backlight_auto = True
                        self.write_var = 'bool_switch_backlight_auto: true'
                        self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                        self.write_changes()

    def btn_backlight_auto_time_0_function(self):
        print('-- [App.btn_backlight_auto_time_0_function]: plugged in')
        global backlight_time_0
        self.setFocus()
        if self.write_engaged is False:

            self.btn_backlight_auto_time_0_str = str(self.btn_backlight_auto_time_0.text()).strip()
            if self.btn_backlight_auto_time_0_str.isdigit() and len(self.btn_backlight_auto_time_0_str) == 4:
                print('-- [App.btn_backlight_auto_time_0_function] btn_backlight_auto_time_0.text(): passed digit check')

                self.write_var = 'backlight_time_0: ' + self.btn_backlight_auto_time_0_str
                backlight_time_0 = self.btn_backlight_auto_time_0_str
                self.write_changes()
            else:
                self.btn_backlight_auto_time_0.setText(backlight_time_0)

    def btn_backlight_auto_time_1_function(self):
        print('-- [App.btn_backlight_auto_time_1_function]: plugged in')
        global backlight_time_1
        self.setFocus()
        if self.write_engaged is False:

            self.btn_backlight_auto_time_1_str = str(self.btn_backlight_auto_time_1.text()).strip()
            if self.btn_backlight_auto_time_1_str.isdigit() and len(self.btn_backlight_auto_time_1_str) == 4:
                print('-- [App.btn_backlight_auto_time_0_function] btn_backlight_auto_time_1.text(): passed digit check')

                self.write_var = 'backlight_time_1: ' + self.btn_backlight_auto_time_1_str
                backlight_time_1 = self.btn_backlight_auto_time_1_str
                self.write_changes()
            else:
                self.btn_backlight_auto_time_1.setText(backlight_time_1)

    def btn_backlight_rgb_on_function(self):
        print('-- [App.btn_backlight_rgb_on_function]: plugged in')
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight
        global sdk_color_backlight_on, sdk_color_backlight, bool_switch_backlight, bool_switch_backlight
        self.setFocus()
        print('sdk_color_backlight_on_str:', self.qle_backlight_rgb_on.text())
        if self.write_engaged is False:
            self.write_var_key = 8
            self.write_var = self.qle_backlight_rgb_on.text()
            self.sanitize_rgb_values()
            if self.write_var_bool is True:
                print('-- [App.btn_backlight_rgb_on_function] self.write_var passed sanitization checks:', self.qle_backlight_rgb_on.text())
                self.write_changes()
                self.sdk_color_backlight_on_str = self.qle_backlight_rgb_on.text().replace(' ', '')
                self.sdk_color_backlight_on_str = self.sdk_color_backlight_on_str.replace(',', ', ')
                self.qle_backlight_rgb_on.setText(self.sdk_color_backlight_on_str)
                print('sdk_color_backlight_on_str True:', self.sdk_color_backlight_on_str)
                print('sdk_color_backlight_on_str:', self.sdk_color_backlight_on_str)
                var = self.sdk_color_backlight_on_str.replace(',', '')
                var = var.split()
                var_0, var_1, var_2 = var[0], var[1], var[2]
                var_0_int, var_1_int, var_2_int = int(var_0), int(var_1), int(var_2)
                sdk_color_backlight = [var_0_int, var_1_int, var_2_int]

            else:
                print('-- [App.btn_backlight_rgb_on_function] self.write_var failed sanitization checks:', self.qle_backlight_rgb_on.text())
                self.sdk_color_backlight_on_str = str(sdk_color_backlight_on).replace('[', '')
                self.sdk_color_backlight_on_str = self.sdk_color_backlight_on_str.replace(']', '')
                self.sdk_color_backlight_on_str = self.sdk_color_backlight_on_str.replace(' ', '')
                self.sdk_color_backlight_on_str = self.sdk_color_backlight_on_str.replace(',', ', ')
                self.qle_backlight_rgb_on.setText(self.sdk_color_backlight_on_str)
                print('sdk_color_backlight_on_str False:', self.sdk_color_backlight_on_str)
            self.qle_backlight_rgb_on.setAlignment(Qt.AlignCenter)

            self.color_all_id()

    def btn_exclusive_con_function(self):
        print('-- [App.btn_exclusive_con_function]: plugged in')
        global bool_switch_startup_exclusive_control, sdk, devices_kb, devices_ms
        self.setFocus()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_exclusive_control is False:
                    print('-- [App.btn_exclusive_con_function] exclusive access request changed: requesting control')
                    self.write_var = 'exclusive_access: true'
                    sdk.request_control()
                    bool_switch_startup_exclusive_control = True
                    self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                elif bool_switch_startup_exclusive_control is True:
                    print('-- [App.btn_exclusive_con_function] exclusive access request changed: releasing control')
                    self.write_var = 'exclusive_access: false'
                    sdk.release_control()
                    bool_switch_startup_exclusive_control = False
                    self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                self.write_changes()
                self.recompile()

    def btn_run_startup_function(self):
        print('-- [App.btn_run_startup_function]: plugged in')
        global bool_switch_startup_autorun
        self.setFocus()
        if self.write_engaged is False:
            cwd = os.getcwd()
            shortcut_in = os.path.join(cwd + '\\iCUEDisplay.vbs')
            shortcut_out = os.path.join(os.path.expanduser('~') + '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/iCUEDisplay.lnk')

            # Remove shortcut
            if bool_switch_startup_autorun is True:
                bool_switch_startup_autorun = False
                print('-- [App.btn_run_startup_function] setting bool_switch_startup_autorun:', bool_switch_startup_autorun)
                self.write_var = 'run_startup: false'
                self.write_changes()
                print('-- [App.btn_run_startup_function] searching for:', shortcut_out)
                if os.path.exists(shortcut_out):
                    print('-- [App.btn_run_startup_function] removing:', shortcut_out)
                    try:
                        os.remove(shortcut_out)
                    except Exception as e:
                        print('-- [App.btn_run_startup_function] btn_run_startup_function:', e)
                self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

            # Create shortcut
            elif bool_switch_startup_autorun is False:
                if os.path.exists(shortcut_in):
                    print('-- [App.btn_run_startup_function] copying:', shortcut_in)
                    try:
                        target = os.path.join(cwd + '\\iCUEDisplay.vbs')
                        icon = cwd + './icon.ico'
                        shell = win32com.client.Dispatch("WScript.Shell")
                        shortcut = shell.CreateShortCut(shortcut_out)
                        shortcut.Targetpath = target
                        shortcut.WorkingDirectory = cwd
                        shortcut.IconLocation = icon
                        shortcut.save()
                    except Exception as e:
                        print('-- [App.btn_run_startup_function] Error:', e)

                # Check new shortcut file exists
                if os.path.exists(shortcut_out):
                    print('-- [App.btn_run_startup_function]: file copied successfully')
                    self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    bool_switch_startup_autorun = True
                    self.write_var = 'run_startup: true'
                    self.write_changes()
                elif not os.path.exists(shortcut_out):
                    print('-- [App.btn_run_startup_function]: shortcut file failed to be created')
                    self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

    def btn_start_minimized_function(self):
        print('-- [App.btn_start_minimized_function]: plugged in')
        self.setFocus()
        global bool_switch_startup_minimized
        if self.write_engaged is False:
            if bool_switch_startup_minimized is True:
                bool_switch_startup_minimized = False
                print('-- [App.btn_start_minimized_function] setting bool_switch_startup_minimized:', bool_switch_startup_minimized)
                self.write_var = 'start_minimized: false'
                self.write_changes()
                self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

            elif bool_switch_startup_minimized is False:
                bool_switch_startup_minimized = True
                print('-- [App.btn_start_minimized_function] setting bool_switch_startup_minimized:', bool_switch_startup_minimized)
                self.write_var = 'start_minimized: true'
                self.write_changes()
                self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

    def btn_cpu_mon_function(self):
        print('-- [App.btn_cpu_mon_function]: plugged in')
        global bool_switch_startup_cpu_util, thread_cpu_util, bool_switch_show_discrete, ui_feature_page
        global devices_kb, devices_ms
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_startup_cpu_util is True:
                    print('-- [App.btn_cpu_mon_function] stopping thread: thread_cpu_util:')
                    thread_cpu_util[0].stop()
                    self.write_var = 'cpu_startup: false'
                    bool_switch_startup_cpu_util = False
                    self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_off_style)
                    self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    if bool_switch_show_discrete is False and ui_feature_page == 0:
                        self.btn_hotbar_cpu_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.write_changes()

                elif bool_switch_startup_cpu_util is False:
                    print('-- [App.btn_cpu_mon_function] starting thread: thread_cpu_util:')
                    thread_cpu_util[0].start()
                    self.write_var = 'cpu_startup: true'
                    bool_switch_startup_cpu_util = True
                    self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_on_style)
                    self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    if bool_switch_show_discrete is False and ui_feature_page == 0:
                        self.btn_hotbar_cpu_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.write_changes()

    def btn_cpu_led_time_on_function(self):
        print('-- [App.btn_cpu_led_time_on_function]: plugged in')
        global timing_cpu_util
        self.setFocus()
        if self.write_engaged is False:
            self.write_var_key = 0
            self.write_var = self.qle_cpu_led_time_on.text()
            self.sanitize_interval()
            if self.write_var_bool is True:
                print('-- [App.btn_cpu_led_time_on_function] self.write_var passed sanitization checks:', self.qle_cpu_led_time_on.text())
                self.write_changes()
                self.cpu_led_time_on_str = self.qle_cpu_led_time_on.text().replace(' ', '')
                self.qle_cpu_led_time_on.setText(self.cpu_led_time_on_str)
            else:
                print('-- [App.btn_cpu_led_time_on_function] failed sanitization checks:', self.qle_cpu_led_time_on.text())
                self.cpu_led_time_on_str = str(timing_cpu_util).replace(' ', '')
                self.qle_cpu_led_time_on.setText(self.cpu_led_time_on_str)
            self.qle_cpu_led_time_on.setAlignment(Qt.AlignCenter)
            timing_cpu_util = float(self.cpu_led_time_on_str)

    def btn_cpu_mon_rgb_on_function(self):
        print('-- [App.btn_cpu_mon_rgb_on_function]: plugged in')
        global sdk_color_cpu_on, thread_cpu_util, bool_switch_startup_cpu_util
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                self.write_var_key = 0
                self.write_var = self.qle_cpu_mon_rgb_on.text()
                self.sanitize_rgb_values()
                if self.write_var_bool is True:
                    print('-- [App.btn_cpu_mon_rgb_on_function] self.write_var passed sanitization checks:', self.qle_cpu_mon_rgb_on.text())
                    self.write_changes()
                    self.cpu_led_color_str = self.qle_cpu_mon_rgb_on.text().replace(' ', '')
                    self.cpu_led_color_str = self.cpu_led_color_str.replace(',', ', ')
                    self.qle_cpu_mon_rgb_on.setText(self.cpu_led_color_str)
                else:
                    print('-- [App.btn_cpu_mon_rgb_on_function] self.write_var failed sanitization checks:', self.qle_cpu_mon_rgb_on.text())
                    self.cpu_led_color_str = str(sdk_color_cpu_on).replace('[', '')
                    self.cpu_led_color_str = self.cpu_led_color_str.replace(']', '')
                    self.cpu_led_color_str = self.cpu_led_color_str.replace(' ', '')
                    self.cpu_led_color_str = self.cpu_led_color_str.replace(',', ', ')
                    self.qle_cpu_mon_rgb_on.setText(self.cpu_led_color_str)
                self.qle_cpu_mon_rgb_on.setAlignment(Qt.AlignCenter)

                if bool_switch_startup_cpu_util is True:
                    thread_cpu_util[0].stop()
                    thread_cpu_util[0].start()

    def btn_dram_mon_function(self):
        print('-- [App.btn_dram_mon_function]: plugged in')
        global bool_switch_startup_dram_util, thread_dram_util, bool_switch_show_discrete, ui_feature_page
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_startup_dram_util is True:
                    print('-- [App.btn_dram_mon_function] stopping thread: thread_dram_util:')
                    thread_dram_util[0].stop()
                    self.write_var = 'dram_startup: false'
                    bool_switch_startup_dram_util = False
                    self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 0:
                        self.btn_hotbar_dram_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

                elif bool_switch_startup_dram_util is False:
                    print('-- [App.btn_dram_mon_function] starting thread: thread_dram_util:')
                    thread_dram_util[0].start()
                    self.write_var = 'dram_startup: true'
                    bool_switch_startup_dram_util = True
                    self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 0:
                        self.btn_hotbar_dram_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                self.write_changes()

    def btn_dram_led_time_on_function(self):
        print('-- [App.btn_dram_led_time_on_function]: plugged in')
        global timing_dram_util
        self.setFocus()
        if self.write_engaged is False:
            self.write_var_key = 1
            self.write_var = self.qle_dram_led_time_on.text()
            self.sanitize_interval()
            if self.write_var_bool is True:
                print('-- [App.btn_dram_led_time_on_function] self.write_var passed sanitization checks:', self.qle_dram_led_time_on.text())
                self.write_changes()
                self.dram_led_time_on_str = self.qle_dram_led_time_on.text().replace(' ', '')
                self.qle_dram_led_time_on.setText(self.dram_led_time_on_str)
            else:
                print('-- [App.btn_dram_led_time_on_function] self.write_var failed sanitization checks:', self.qle_dram_led_time_on.text())
                self.dram_led_time_on_str = str(timing_dram_util).replace(' ', '')
                self.qle_dram_led_time_on.setText(self.dram_led_time_on_str)
            self.qle_dram_led_time_on.setAlignment(Qt.AlignCenter)
            timing_dram_util = float(self.dram_led_time_on_str)

    def btn_dram_mon_rgb_on_function(self):
        print('-- [App.btn_dram_mon_rgb_on_function]: plugged in')
        global sdk_color_dram_on, thread_dram_util, bool_switch_startup_dram_util
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                self.write_var_key = 1
                self.write_var = self.qle_dram_mon_rgb_on.text()
                self.sanitize_rgb_values()
                if self.write_var_bool is True:
                    print('-- [App.btn_dram_mon_rgb_on_function] self.write_var passed sanitization checks:', self.qle_dram_mon_rgb_on.text())
                    self.write_changes()
                    self.dram_led_color_str = self.qle_dram_mon_rgb_on.text().replace(' ', '')
                    self.dram_led_color_str = self.dram_led_color_str.replace(',', ', ')
                    self.qle_dram_mon_rgb_on.setText(self.dram_led_color_str)
                else:
                    print('-- [App.btn_dram_mon_rgb_on_function] self.write_var failed sanitization checks:', self.qle_dram_mon_rgb_on.text())
                    self.dram_led_color_str = str(sdk_color_dram_on).replace('[', '')
                    self.dram_led_color_str = self.dram_led_color_str.replace(']', '')
                    self.dram_led_color_str = self.dram_led_color_str.text().replace(' ', '')
                    self.dram_led_color_str = self.dram_led_color_str.replace(',', ', ')
                    self.qle_dram_mon_rgb_on.setText(self.dram_led_color_str)
                self.qle_dram_mon_rgb_on.setAlignment(Qt.AlignCenter)

                if bool_switch_startup_dram_util is True:
                    thread_dram_util[0].stop()
                    thread_dram_util[0].start()

    def btn_vram_mon_function(self):
        print('-- [App.btn_vram_mon_function]: plugged in')
        global bool_switch_startup_vram_util, thread_vram_util, bool_switch_show_discrete, ui_feature_page
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:

                if bool_switch_startup_vram_util is True:
                    print('-- [App.btn_vram_mon_function] stopping thread: thread_vram_util:')
                    thread_vram_util[0].stop()
                    self.write_var = 'vram_startup: false'
                    bool_switch_startup_vram_util = False
                    self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 0:
                        self.btn_hotbar_vram_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

                elif bool_switch_startup_vram_util is False:
                    print('-- [App.btn_vram_mon_function] starting thread: thread_vram_util:')
                    thread_vram_util[0].start()
                    self.write_var = 'vram_startup: true'
                    bool_switch_startup_vram_util = True
                    self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 0:
                        self.btn_hotbar_vram_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                self.write_changes()

    def btn_vram_led_time_on_function(self):
        print('-- [App.btn_vram_led_time_on_function]: plugged in')
        global timing_vram_util
        self.setFocus()
        if self.write_engaged is False:
            self.write_var_key = 2
            self.write_var = self.qle_vram_led_time_on.text()
            self.sanitize_interval()
            if self.write_var_bool is True:
                print('-- [App.btn_vram_led_time_on_function] self.write_var passed sanitization checks:', self.qle_vram_led_time_on.text())
                self.write_changes()
                self.vram_led_time_on_str = self.qle_vram_led_time_on.text().replace(' ', '')
                self.qle_vram_led_time_on.setText(self.vram_led_time_on_str)
            else:
                print('-- [App.btn_vram_led_time_on_function] self.write_var failed sanitization checks:', self.qle_vram_led_time_on.text())
                self.vram_led_time_on_str = str(timing_vram_util).replace(' ', '')
                self.qle_vram_led_time_on.setText(self.vram_led_time_on_str)
            self.qle_vram_led_time_on.setAlignment(Qt.AlignCenter)
            timing_vram_util = float(self.vram_led_time_on_str)

    def btn_vram_mon_rgb_on_function(self):
        print('-- [App.btn_vram_mon_rgb_on_function]: plugged in')
        global sdk_color_vram_on, thread_vram_util, bool_switch_startup_vram_util
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                self.write_var_key = 2
                self.write_var = self.qle_vram_mon_rgb_on.text()
                self.sanitize_rgb_values()
                if self.write_var_bool is True:
                    print('-- [App.btn_vram_mon_rgb_on_function] self.write_var passed sanitization checks:', self.qle_vram_mon_rgb_on.text())
                    self.write_changes()
                    self.vram_led_color_str = self.qle_vram_mon_rgb_on.text().replace(' ', '')
                    self.vram_led_color_str = self.vram_led_color_str.replace(',', ', ')
                    self.qle_vram_mon_rgb_on.setText(self.vram_led_color_str)
                else:
                    print('-- [App.btn_vram_mon_rgb_on_function] self.write_var failed sanitization checks:', self.qle_vram_mon_rgb_on.text())
                    self.vram_led_color_str = str(sdk_color_vram_on).replace('[', '')
                    self.vram_led_color_str = self.vram_led_color_str.replace(']', '')
                    self.vram_led_color_str = self.vram_led_color_str.replace(' ', '')
                    self.vram_led_color_str = self.vram_led_color_str.replace(',', ', ')
                    self.qle_vram_mon_rgb_on.setText(self.vram_led_color_str)
                self.qle_vram_mon_rgb_on.setAlignment(Qt.AlignCenter)

                if bool_switch_startup_vram_util is True:
                    thread_vram_util[0].stop()
                    thread_vram_util[0].start()

    def btn_hdd_mon_function(self):
        print('-- [App.btn_hdd_mon_function]: plugged in')
        global bool_switch_startup_hdd_read_write, thread_disk_rw, bool_switch_show_discrete, ui_feature_page
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_hdd_read_write is True:
                    print('-- [App.btn_hdd_mon_function] stopping thread: thread_disk_rw:')
                    thread_disk_rw[0].stop()
                    self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_disabledx2h.png"))
                    self.write_var = 'hdd_startup: false'
                    self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 1:
                        self.btn_hotbar_diskrw_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    bool_switch_startup_hdd_read_write = False
                    self.write_changes()
                elif bool_switch_startup_hdd_read_write is False:
                    print('-- [App.btn_hdd_mon_function] starting thread: thread_disk_rw:')
                    thread_disk_rw[0].start()
                    self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_enabledx2h.png"))
                    self.write_var = 'hdd_startup: true'
                    self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 1:
                        self.btn_hotbar_diskrw_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    bool_switch_startup_hdd_read_write = True
                    self.write_changes()

    def btn_hdd_led_time_on_function(self):
        print('-- [App.btn_hdd_led_time_on_function]: plugged in')
        global timing_hdd_util
        self.setFocus()
        if self.write_engaged is False:
            self.write_var_key = 3
            self.write_var = self.qle_hdd_led_time_on.text()
            self.sanitize_interval()
            if self.write_var_bool is True:
                print('-- [App.btn_hdd_led_time_on_function] self.write_var passed sanitization checks:', self.qle_hdd_led_time_on.text())
                self.write_changes()
                self.hdd_led_time_on_str = self.qle_hdd_led_time_on.text().replace(' ', '')
                self.qle_hdd_led_time_on.setText(self.hdd_led_time_on_str)
            else:
                print('-- [App.btn_hdd_led_time_on_function] self.write_var failed sanitization checks:', self.qle_hdd_led_time_on.text())
                self.hdd_led_time_on_str = str(timing_hdd_util).replace(' ', '')
                self.qle_hdd_led_time_on.setText(self.hdd_led_time_on_str)
            self.qle_hdd_led_time_on.setAlignment(Qt.AlignCenter)
            timing_hdd_util = float(self.hdd_led_time_on_str)

    def btn_hdd_mon_rgb_on_function(self):
        print('-- [App.btn_hdd_mon_rgb_on_function]: plugged in')
        global sdk_color_hddwrite_on, thread_disk_rw, bool_switch_startup_hdd_read_write
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                self.write_var_key = 3
                self.write_var = self.qle_hdd_mon_rgb_on.text()
                self.sanitize_rgb_values()
                if self.write_var_bool is True:
                    print('-- [App.btn_hdd_mon_rgb_on_function] self.write_var passed sanitization checks:', self.qle_hdd_mon_rgb_on.text())
                    self.write_changes()
                    self.hdd_led_color_str = self.qle_hdd_mon_rgb_on.text().replace(' ', '')
                    self.hdd_led_color_str = self.hdd_led_color_str.replace(',', ', ')
                    self.qle_hdd_mon_rgb_on.setText(self.hdd_led_color_str)
                else:
                    print('-- [App.btn_hdd_mon_rgb_on_function] self.write_var failed sanitization checks:', self.qle_hdd_mon_rgb_on.text())
                    self.hdd_led_color_str = str(sdk_color_hddwrite_on).replace('[', '')
                    self.hdd_led_color_str = self.hdd_led_color_str.replace(']', '')
                    self.hdd_led_color_str = self.hdd_led_color_str.replace(' ', '')
                    self.hdd_led_color_str = self.hdd_led_color_str.replace(',', ', ')
                    self.qle_hdd_mon_rgb_on.setText(self.hdd_led_color_str)
                self.qle_hdd_mon_rgb_on.setAlignment(Qt.AlignCenter)

                if bool_switch_startup_hdd_read_write is True:
                    thread_disk_rw[0].stop()
                    thread_disk_rw[0].start()

    def btn_hdd_read_mon_rgb_on_function(self):
        print('-- [App.btn_hdd_read_mon_rgb_on_function]: plugged in')
        global sdk_color_hddread_on, thread_disk_rw, bool_switch_startup_hdd_read_write
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                self.write_var_key = 9
                self.write_var = self.qle_hdd_read_mon_rgb_on.text()
                self.sanitize_rgb_values()
                if self.write_var_bool is True:
                    print('-- [App.btn_hdd_read_mon_rgb_on_function] self.write_var passed sanitization checks:', self.qle_hdd_read_mon_rgb_on.text())
                    self.write_changes()
                    self.hdd_led_read_color_str = self.qle_hdd_read_mon_rgb_on.text().replace(' ', '')
                    self.hdd_led_read_color_str = self.hdd_led_read_color_str.replace(',', ', ')
                    self.qle_hdd_read_mon_rgb_on.setText(self.hdd_led_read_color_str)
                else:
                    print('-- [App.btn_hdd_read_mon_rgb_on_function] self.write_var failed sanitization checks:', self.qle_hdd_read_mon_rgb_on.text())
                    self.hdd_led_read_color_str = str(sdk_color_hddread_on).replace('[', '')
                    self.hdd_led_read_color_str = self.hdd_led_read_color_str.replace(']', '')
                    self.hdd_led_read_color_str = self.hdd_led_read_color_str.replace(' ', '')
                    self.hdd_led_read_color_str = self.hdd_led_read_color_str.replace(',', ', ')
                    self.qle_hdd_read_mon_rgb_on.setText(self.hdd_led_read_color_str)
                self.qle_hdd_read_mon_rgb_on.setAlignment(Qt.AlignCenter)

                if bool_switch_startup_hdd_read_write is True:
                    thread_disk_rw[0].stop()
                    thread_disk_rw[0].start()

    def btn_network_adapter_function(self):
        print('-- [App.btn_network_adapter_function]: plugged in')
        global bool_switch_startup_net_traffic, thread_net_traffic, bool_switch_show_discrete, ui_feature_page
        global devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_traffic is True:
                    bool_switch_startup_net_traffic = False
                    print('-- [App.btn_network_adapter_function] stopping thread: thread_net_traffic:')
                    thread_net_traffic[0].stop()
                    self.write_var = 'network_adapter_startup: false'
                    self.write_changes()
                    self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 2:
                        self.btn_hotbar_nettraffic_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                elif bool_switch_startup_net_traffic is False:
                    bool_switch_startup_net_traffic = True
                    print('-- [App.btn_network_adapter_function] starting thread: thread_net_traffic:')
                    thread_net_traffic[0].start()
                    self.write_var = 'network_adapter_startup: true'
                    self.write_changes()
                    self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 2:
                        self.btn_hotbar_nettraffic_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

    def cmb_network_adapter_name_function(self, text):
        print('-- [App.cmb_network_adapter_name_function]: plugged in')
        global devices_network_adapter_name, thread_net_traffic, devices_kb

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                devices_network_adapter_name = text
                print('-- [App.cmb_network_adapter_name_function] setting devices_network_adapter_name:', devices_network_adapter_name)
                self.setFocus()
                self.write_var = 'devices_network_adapter_name: ' + devices_network_adapter_name
                self.write_changes()
                if bool_switch_startup_net_traffic is True:
                    print('-- [App.cmb_network_adapter_name_function] stopping thread: thread_net_traffic')
                    thread_net_traffic[0].stop()
                    print('-- [App.cmb_network_adapter_name_function] starting thread: thread_net_traffic')
                    thread_net_traffic[0].start()

    def btn_network_adapter_refresh_function(self, text):
        print('-- [App.btn_network_adapter_refresh_function]: plugged in')
        print('-- [App.btn_network_adapter_refresh_function] cmb_network_adapter_name_update_function:', text)
        if self.write_engaged is False:
            pythoncom.CoInitialize()
            self.cmb_network_adapter_name.clear()
            try:
                wmis = win32com.client.Dispatch("WbemScripting.SWbemLocator")
                wbems = wmis.ConnectServer(".", "root\\cimv2")
                col_items = wbems.ExecQuery('SELECT * FROM Win32_PerfFormattedData_Tcpip_NetworkAdapter')
                for objItem in col_items:
                    if objItem.Name != None:
                        print('-- [App.btn_network_adapter_refresh_function] found:', objItem.Name)
                        self.cmb_network_adapter_name.addItem(objItem.Name)
            except Exception as e:
                print('-- [App.btn_network_adapter_refresh_function] Error.', e)

    def btn_network_adapter_led_time_on_function(self):
        print('-- [App.btn_network_adapter_led_time_on_function]: plugged in')
        global timing_net_traffic_util
        self.setFocus()
        if self.write_engaged is False:
            self.write_var_key = 4
            self.write_var = self.qle_network_adapter_led_time_on.text()
            self.sanitize_interval()
            if self.write_var_bool is True:
                print('-- [App.btn_network_adapter_led_time_on_function] self.write_var passed sanitization checks:', self.qle_network_adapter_led_time_on.text())
                self.write_changes()
                self.network_adapter_led_time_on_str = self.qle_network_adapter_led_time_on.text().replace(' ', '')
                self.qle_network_adapter_led_time_on.setText(self.network_adapter_led_time_on_str)
            else:
                print('-- [App.btn_network_adapter_led_time_on_function] self.write_var failed sanitization checks:', self.qle_network_adapter_led_time_on.text())
                self.network_adapter_led_time_on_str = str(timing_net_traffic_util).replace(' ', '')
                self.qle_network_adapter_led_time_on.setText(self.network_adapter_led_time_on_str)
            self.qle_network_adapter_led_time_on.setAlignment(Qt.AlignCenter)
            timing_net_traffic_util = float(self.network_adapter_led_time_on_str)

    def btn_net_con_mouse_function(self):
        print('-- [App.btn_net_con_mouse_function]: plugged in')
        global bool_switch_startup_net_con_ms, bool_switch_startup_net_con_kb, bool_switch_startup_net_con
        global thread_net_connection, bool_switch_show_discrete, ui_feature_page, devices_kb, devices_ms
        self.setFocus()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_con_ms is True:
                    bool_switch_startup_net_con_ms = False
                    print('-- [App.btn_net_con_mouse_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    self.write_var = 'bool_switch_startup_net_con_ms: false'
                    self.write_changes()
                    self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 3:
                        self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    if bool_switch_startup_net_con_kb is False:
                        self.write_var = 'bool_switch_startup_net_con: false'
                        self.write_changes()
                        bool_switch_startup_net_con = False
                        self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    elif bool_switch_startup_net_con_kb is True:
                        print('-- [App.btn_net_con_mouse_function] starting thread: thread_net_connection')
                        thread_net_connection[0].start()
                elif bool_switch_startup_net_con_ms is False:
                    print('-- [App.btn_net_con_mouse_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    bool_switch_startup_net_con_ms = True
                    print('-- [App.btn_net_con_mouse_function] starting thread: thread_net_connection')
                    thread_net_connection[0].start()
                    self.write_var = 'bool_switch_startup_net_con_ms: true'
                    self.write_changes()
                    self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 3:
                        self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.write_var = 'bool_switch_startup_net_con: true'
                    self.write_changes()
                    bool_switch_startup_net_con = True

    def btn_net_con_kb_function(self):
        print('-- [App.btn_net_con_kb_function]: plugged in')
        global bool_switch_startup_net_con_kb, bool_switch_startup_net_con, bool_switch_startup_net_con_ms
        global thread_net_connection, bool_switch_show_discrete, ui_feature_page, devices_ms, devices_kb
        self.setFocus()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_con_kb is True:
                    bool_switch_startup_net_con_kb = False
                    print('-- [App.btn_net_con_kb_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    self.write_var = 'bool_switch_startup_net_con_kb: false'
                    self.write_changes()
                    self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 3:
                        self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

                    if bool_switch_startup_net_con_ms is False:
                        self.write_var = 'bool_switch_startup_net_con: false'
                        self.write_changes()
                        bool_switch_startup_net_con = False
                    elif bool_switch_startup_net_con_ms is True:
                        print('-- [App.btn_net_con_kb_function] starting thread: thread_net_connection')
                        thread_net_connection[0].start()

                elif bool_switch_startup_net_con_kb is False:
                    print('-- [App.btn_net_con_kb_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    bool_switch_startup_net_con_kb = True
                    self.write_var = 'bool_switch_startup_net_con_kb: true'
                    self.write_changes()
                    self.write_var = 'bool_switch_startup_net_con: true'
                    self.write_changes()
                    bool_switch_startup_net_con = True
                    self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 3:
                        self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    print('-- [App.btn_net_con_kb_function] starting thread: thread_net_connection')
                    thread_net_connection[0].start()

    def btn_net_con_mouse_led_selected_prev_function(self):
        print('-- [App.btn_net_con_mouse_led_selected_prev_function]: plugged in')
        global corsairled_id_num_netcon_ms, corsairled_id_num_ms_complete, sdk, devices_ms_selected, bool_switch_startup_net_con_ms, sdk_color_backlight
        global thread_net_connection, devices_kb, devices_ms
        self.setFocus()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if corsairled_id_num_netcon_ms > 0:
                    print('-- [App.btn_net_con_mouse_led_selected_prev_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
                    corsairled_id_num_netcon_ms = int(corsairled_id_num_netcon_ms - 1)
                    print('-- [App.btn_net_con_mouse_led_selected_prev_function] setting lbl_net_con_mouse_led_selected:', corsairled_id_num_netcon_ms)
                    self.write_var = 'corsairled_id_num_netcon_ms: ' + str(corsairled_id_num_netcon_ms)
                    self.write_changes()
                    self.lbl_net_con_mouse_led_selected.setText(str(corsairled_id_num_netcon_ms))
                    if bool_switch_startup_net_con_ms is True or bool_switch_startup_net_con_kb is True:
                        print('-- [App.btn_net_con_mouse_led_selected_prev_function] bool_switch_startup_net_con_ms:', bool_switch_startup_net_con_ms)
                        print('-- [App.btn_net_con_mouse_led_selected_prev_function] bool_switch_startup_net_con_kb:', bool_switch_startup_net_con_kb)
                        print('-- [App.btn_net_con_mouse_led_selected_prev_function] starting thread: thread_net_connection')
                        thread_net_connection[0].start()
                    elif bool_switch_startup_net_con_ms is False and bool_switch_startup_net_con_kb is False:
                        print('-- [App.btn_net_con_mouse_led_selected_prev_function] bool_switch_startup_net_con_ms:', bool_switch_startup_net_con_ms)
                        print('-- [App.btn_net_con_mouse_led_selected_prev_function] bool_switch_startup_net_con_kb:', bool_switch_startup_net_con_kb)
                        print('-- [App.btn_net_con_mouse_led_selected_prev_function]: skipping thread start')

    def btn_net_con_mouse_led_selected_next_function(self):
        print('-- [App.btn_net_con_mouse_led_selected_next_function]: plugged in')
        global corsairled_id_num_netcon_ms, corsairled_id_num_ms_complete, sdk, devices_ms_selected, bool_switch_startup_net_con_ms, sdk_color_backlight
        global thread_net_connection, devices_kb, devices_ms
        self.setFocus()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if corsairled_id_num_netcon_ms < len(corsairled_id_num_ms_complete) - 1:
                    print('-- [App.btn_net_con_mouse_led_selected_next_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
                    corsairled_id_num_netcon_ms = int(corsairled_id_num_netcon_ms + 1)
                    print('-- [App.btn_net_con_mouse_led_selected_next_function] setting lbl_net_con_mouse_led_selected:', corsairled_id_num_netcon_ms)
                    self.write_var = 'corsairled_id_num_netcon_ms: ' + str(corsairled_id_num_netcon_ms)
                    self.write_changes()
                    self.lbl_net_con_mouse_led_selected.setText(str(corsairled_id_num_netcon_ms))
                    if bool_switch_startup_net_con_ms is True or bool_switch_startup_net_con_kb is True:
                        print('-- [App.btn_net_con_mouse_led_selected_next_function] bool_switch_startup_net_con_ms:', bool_switch_startup_net_con_ms)
                        print('-- [App.btn_net_con_mouse_led_selected_next_function] bool_switch_startup_net_con_kb:', bool_switch_startup_net_con_kb)
                        print('-- [App.btn_net_con_mouse_led_selected_next_function] starting thread: thread_net_connection')
                        thread_net_connection[0].start()
                    elif bool_switch_startup_net_con_ms is False and bool_switch_startup_net_con_kb is False:
                        print('-- [App.btn_net_con_mouse_led_selected_next_function] bool_switch_startup_net_con_ms:', bool_switch_startup_net_con_ms)
                        print('-- [App.btn_net_con_mouse_led_selected_next_function] bool_switch_startup_net_con_kb:', bool_switch_startup_net_con_kb)
                        print('-- [App.btn_net_con_mouse_led_selected_next_function]: skipping thread start')

    def btn_defnetshare_function(self):
        print('-- [App.btn_defnetshare_function]: plugged in')
        global bool_switch_startup_net_share_mon, thread_net_share, bool_switch_show_discrete, ui_feature_page
        global devices_ms, devices_kb
        self.setFocus()

        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_share_mon is True:
                    print('-- [App.btn_defnetshare_function] stopping: thread_net_share')
                    thread_net_share[0].stop()
                    self.write_var = 'netshare_startup: false'
                    bool_switch_startup_net_share_mon = False
                    self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_off_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 4:
                        self.btn_hotbar_netshare_mon.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                    self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                elif bool_switch_startup_net_share_mon is False:
                    print('-- [App.btn_defnetshare_function] starting: thread_net_share')
                    thread_net_share[0].start()
                    self.write_var = 'netshare_startup: true'
                    bool_switch_startup_net_share_mon = True
                    self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_on_style)
                    if bool_switch_show_discrete is False and ui_feature_page == 4:
                        self.btn_hotbar_netshare_mon.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                    self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                self.write_changes()

    def netshare_active_rgb_function(self):
        print('-- [App.netshare_active_rgb_function]: plugged in')
        global sdk_color_netshare_on
        self.setFocus()
        if self.write_engaged is False:
            self.write_var_key = 7
            self.write_var = self.qle_netshare_mon_rgb_on.text()
            self.sanitize_rgb_values()
            if self.write_var_bool is True:
                print('-- [App.netshare_active_rgb_function] self.write_var passed sanitization checks:', self.qle_netshare_mon_rgb_on.text())
                self.write_changes()
                self.netshare_active_color_str = self.qle_netshare_mon_rgb_on.text().replace(' ', '')
                self.netshare_active_color_str = self.netshare_active_color_str.replace(',', ', ')
                self.qle_netshare_mon_rgb_on.setText(self.netshare_active_color_str)
            else:
                print('-- [App.netshare_active_rgb_function] self.write_var failed sanitization checks:', self.qle_netshare_mon_rgb_on.text())
                self.netshare_active_color_str = str(sdk_color_netshare_on).replace('[', '')
                self.netshare_active_color_str = self.netshare_active_color_str.replace(']', '')
                self.netshare_active_color_str = self.netshare_active_color_str.replace(' ', '')
                self.netshare_active_color_str = self.netshare_active_color_str.replace(',', ', ')
                self.qle_netshare_mon_rgb_on.setText(self.netshare_active_color_str)
            self.qle_netshare_mon_rgb_on.setAlignment(Qt.AlignCenter)

    def g1_function_short(self):
        global thread_g1_notify, bool_allow_g1_short, bool_switch_event_notification_run_g1, str_event_notification_run_path_g1
        global devices_kb
        print('-- [App.g1_function_short]: plugged in')
        if len(devices_kb):
            thread_g1_notify[0].stop()
            if bool_allow_g1_short is True:
                bool_allow_g1_short = False
                if bool_switch_event_notification_run_g1 is True:
                    if os.path.exists(str_event_notification_run_path_g1):
                        print('-- [App.g1_function_short]: attempting to run:', str_event_notification_run_path_g1)
                        try:
                            cmd = str_event_notification_run_path_g1
                            cmd = cmd.strip()
                            print('running command:', cmd)
                            xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)
                        except Exception as e:
                            print('-- [App.g1_function_short] Error:', e)
                    else:
                        print('-- [App.g1_function_short]: cannot find:', str_event_notification_run_path_g1)

    def g1_function_long(self):
        global thread_g1_notify, bool_allow_g1_short, devices_kb
        print('-- [App.g1_function_long]: plugged in')
        print('-- [App.g1_function_long]: ignoring notification')
        if len(devices_kb):
            bool_allow_g1_short = False
            thread_g1_notify[0].stop()

    def g2_function_short(self):
        global thread_g2_notify, bool_allow_g2_short, bool_switch_event_notification_run_g2, str_event_notification_run_path_g2
        global devices_kb
        print('-- [App.g2_function_short]: plugged in')
        if len(devices_kb):
            thread_g2_notify[0].stop()
            if bool_allow_g2_short is True:
                bool_allow_g2_short = False
                if bool_switch_event_notification_run_g2 is True:
                    if os.path.exists(str_event_notification_run_path_g2):
                        print('-- [App.g2_function_short]: attempting to run:', str_event_notification_run_path_g2)
                        try:
                            cmd = str_event_notification_run_path_g2
                            cmd = cmd.strip()
                            print('running command:', cmd)
                            xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)
                        except Exception as e:
                            print('-- [App.g2_function_short] Error:', e)
                    else:
                        print('-- [App.g2_function_short]: cannot find:', str_event_notification_run_path_g2)

    def g2_function_long(self):
        global thread_g2_notify, bool_allow_g2_short, devices_kb
        print('-- [App.g2_function_long]: plugged in')
        print('-- [App.g2_function_long]: ignoring notification')
        if len(devices_kb):
            bool_allow_g2_short = False
            thread_g2_notify[0].stop()

    def g3_function_short(self):
        global thread_g3_notify, bool_allow_g3_short, bool_switch_event_notification_run_g3, str_event_notification_run_path_g3
        global devices_kb
        print('-- [App.g3_function_short]: plugged in')
        if len(devices_kb):
            thread_g3_notify[0].stop()
            if bool_allow_g3_short is True:
                bool_allow_g3_short = False
                if bool_switch_event_notification_run_g3 is True:
                    if os.path.exists(str_event_notification_run_path_g3):
                        print('-- [App.g3_function_short]: attempting to run:', str_event_notification_run_path_g3)
                        try:
                            cmd = str_event_notification_run_path_g3
                            cmd = cmd.strip()
                            print('running command:', cmd)
                            xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)
                        except Exception as e:
                            print('-- [App.g3_function_short] Error:', e)
                    else:
                        print('-- [App.g3_function_short]: cannot find:', str_event_notification_run_path_g3)

    def g3_function_long(self):
        global thread_g3_notify, bool_allow_g3_short, devices_kb
        print('-- [App.g3_function_long]: plugged in')
        print('-- [App.g3_function_long]: ignoring notification')
        if len(devices_kb):
            bool_allow_g3_short = False
            thread_g3_notify[0].stop()

    def g4_function_short(self):
        global thread_g4_notify, bool_allow_g4_short, bool_switch_event_notification_run_g4, str_event_notification_run_path_g4
        global devices_kb
        print('-- [App.g4_function_short]: plugged in')
        if len(devices_kb):
            thread_g4_notify[0].stop()
            if bool_allow_g4_short is True:
                bool_allow_g4_short = False
                if bool_switch_event_notification_run_g4 is True:
                    if os.path.exists(str_event_notification_run_path_g4):
                        print('-- [App.g4_function_short]: attempting to run:', str_event_notification_run_path_g4)
                        try:
                            cmd = str_event_notification_run_path_g4
                            cmd = cmd.strip()
                            print('running command:', cmd)
                            xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)
                        except Exception as e:
                            print('-- [App.g4_function_short] Error:', e)
                    else:
                        print('-- [App.g4_function_short]: cannot find:', str_event_notification_run_path_g4)

    def g4_function_long(self):
        global thread_g4_notify, bool_allow_g4_short
        global devices_kb
        print('-- [App.g4_function_long]: plugged in')
        print('-- [App.g4_function_long]: ignoring notification')
        if len(devices_kb):
            bool_allow_g4_short = False
            thread_g4_notify[0].stop()

    def g5_function_short(self):
        global thread_g5_notify, bool_allow_g5_short, bool_switch_event_notification_run_g5, str_event_notification_run_path_g5
        global devices_kb
        print('-- [App.g5_function_short]: plugged in')
        if len(devices_kb):
            thread_g5_notify[0].stop()
            if bool_allow_g5_short is True:
                bool_allow_g5_short = False
                if bool_switch_event_notification_run_g5 is True:
                    if os.path.exists(str_event_notification_run_path_g5):
                        print('-- [App.g5_function_short]: attempting to run:', str_event_notification_run_path_g5)
                        try:
                            cmd = str_event_notification_run_path_g5
                            cmd = cmd.strip()
                            print('running command:', cmd)
                            xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)
                        except Exception as e:
                            print('-- [App.g5_function_short] Error:', e)
                    else:
                        print('-- [App.g5_function_short]: cannot find:', str_event_notification_run_path_g5)

    def g5_function_long(self):
        global thread_g5_notify, bool_allow_g5_short, devices_kb
        print('-- [App.g5_function_long]: plugged in')
        print('-- [App.g5_function_long]: ignoring notification')
        if len(devices_kb):
            bool_allow_g5_short = False
            thread_g5_notify[0].stop()

    def g6_function_short(self):
        global thread_g6_notify, bool_allow_g6_short, bool_switch_event_notification_run_g6, str_event_notification_run_path_g6
        global devices_kb
        print('-- [App.g6_function_short]: plugged in')
        if len(devices_kb):
            thread_g6_notify[0].stop()
            if bool_allow_g6_short is True:
                bool_allow_g6_short = False
                if bool_switch_event_notification_run_g6 is True:
                    if os.path.exists(str_event_notification_run_path_g6):
                        print('-- [App.g6_function_short]: attempting to run:', str_event_notification_run_path_g6)
                        try:
                            cmd = str_event_notification_run_path_g6
                            cmd = cmd.strip()
                            print('running command:', cmd)
                            xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)
                        except Exception as e:
                            print('-- [App.g6_function_short] Error:', e)
                    else:
                        print('-- [App.g6_function_short]: cannot find:', str_event_notification_run_path_g6)

    def g6_function_long(self):
        global thread_g6_notify, bool_allow_g6_short, devices_kb
        print('-- [App.g6_function_long]: plugged in')
        print('-- [App.g6_function_long]: ignoring notification')
        bool_allow_g6_short = False
        if len(devices_kb):
            thread_g6_notify[0].stop()

    def initUI(self):
        print('-- [App.initUI]: plugged in')
        global sdk
        global bool_backend_allow_display, bool_switch_startup_exclusive_control
        global bool_switch_startup_cpu_util, bool_switch_startup_dram_util, bool_switch_startup_vram_util, bool_switch_startup_hdd_read_write, bool_switch_backlight
        global sdk_color_cpu_on, sdk_color_dram_on, sdk_color_vram_on, sdk_color_hddwrite_on, sdk_color_hddread_on, sdk_color_netshare_on, sdk_color_backlight, sdk_color_backlight_on
        global bool_switch_startup_net_share_mon
        global bool_switch_startup_minimized
        global thread_compile_devices
        global thread_disk_rw
        global thread_cpu_util
        global thread_dram_util
        global thread_vram_util
        global thread_net_traffic
        global thread_net_connection
        global thread_net_share
        global thread_sdk_event_handler
        global thread_sdk_event_handler_read_file_events
        global thread_g1_notify, thread_g2_notify, thread_g3_notify, thread_g4_notify, thread_g5_notify, thread_g6_notify
        global bool_switch_event_notification_g1, bool_switch_event_notification_g2, bool_switch_event_notification_g3
        global bool_switch_event_notification_g4, bool_switch_event_notification_g5, bool_switch_event_notification_g6

        global bool_switch_event_notification_run_g1, bool_switch_event_notification_run_g2, bool_switch_event_notification_run_g3
        global bool_switch_event_notification_run_g4, bool_switch_event_notification_run_g5, bool_switch_event_notification_run_g6

        global str_event_notification_run_path_g1, str_event_notification_run_path_g2, str_event_notification_run_path_g3
        global str_event_notification_run_path_g4, str_event_notification_run_path_g5, str_event_notification_run_path_g6

        global bool_switch_backlight_auto, thread_backlight_auto, backlight_time_0, backlight_time_1

        hdd_mon_thread = HddMonClass()
        thread_disk_rw.append(hdd_mon_thread)

        cpu_mon_thread = CpuMonClass()
        thread_cpu_util.append(cpu_mon_thread)

        dram_mon_thread = DramMonClass()
        thread_dram_util.append(dram_mon_thread)

        vram_mon_thread = VramMonClass()
        thread_vram_util.append(vram_mon_thread)

        network_mon_thread = NetworkMonClass()
        thread_net_traffic.append(network_mon_thread)

        ping_test_thread = PingTestClass()
        thread_net_connection.append(ping_test_thread)

        def_netshare_thread = NetShareClass()
        thread_net_share.append(def_netshare_thread)

        sdk_event_handler = SdkEventHandlerClass(self.g1_function_short, self.g1_function_long,
                                                        self.g2_function_short, self.g2_function_long,
                                                        self.g3_function_short, self.g3_function_long,
                                                        self.g4_function_short, self.g4_function_long,
                                                        self.g5_function_short, self.g5_function_long,
                                                        self.g6_function_short, self.g6_function_long)
        thread_sdk_event_handler.append(sdk_event_handler)
        # thread_sdk_event_handler[0].start()

        sdk_event_handler_read_file_events = EventHandlerReadFileEvents()
        thread_sdk_event_handler_read_file_events.append(sdk_event_handler_read_file_events)
        # sdk_event_handler_read_file_events.start()

        g1_notify = EventHandlerG1Notify()
        thread_g1_notify.append(g1_notify)

        g2_notify = EventHandlerG2Notify()
        thread_g2_notify.append(g2_notify)

        g3_notify = EventHandlerG3Notify()
        thread_g3_notify.append(g3_notify)

        g4_notify = EventHandlerG4Notify()
        thread_g4_notify.append(g4_notify)

        g5_notify = EventHandlerG5Notify()
        thread_g5_notify.append(g5_notify)

        g6_notify = EventHandlerG6Notify()
        thread_g6_notify.append(g6_notify)

        backlight_auto = BackLightClass(self.color_all_id,
                                        self.btn_bck_light,
                                        self.btn_hotbar_on_style, self.btn_hotbar_off_style,
                                        self.visually_combine_hotbar_on_settings_window_style, self.visually_combine_hotbar_off_settings_window_style,
                                        self.btn_backlight_sub)
        thread_backlight_auto.append(backlight_auto)

        compile_devices_thread = CompileDevicesClass(self.lbl_con_stat_name, self.lbl_con_stat_kb,
                                                     self.lbl_con_stat_mouse, self.btn_refresh_recompile,
                                                     self.btn_hotbar_off_style, self.btn_hotbar_on_style)
        thread_compile_devices.append(compile_devices_thread)
        thread_compile_devices[0].start()

        print('-- [App.initUI]: waiting to display application')
        while bool_backend_allow_display is False:
            time.sleep(1)
        print('-- [App.initUI]: displaying application')

        if bool_switch_backlight_auto is False:
            self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_backlight_auto is True:
            self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            if len(devices_kb) > 0 or len(devices_ms) > 0:
                thread_backlight_auto[0].start()

        if bool_switch_startup_autorun is True:
            self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_startup_autorun is False:
            self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_startup_minimized is True:
            self.showMinimized()
            self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_startup_minimized is False:
            self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_startup_cpu_util is True:
            self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_startup_cpu_util is False:
            self.btn_hotbar_cpu_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_startup_dram_util is True:
            self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_startup_dram_util is False:
            self.btn_hotbar_dram_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_startup_vram_util is True:
            self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_startup_vram_util is False:
            self.btn_hotbar_vram_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_startup_hdd_read_write is True:
            self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_enabledx2h.png"))
        elif bool_switch_startup_hdd_read_write is False:
            self.btn_hotbar_diskrw_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_disabledx2h.png"))

        if bool_switch_startup_exclusive_control is True:
            self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_startup_exclusive_control is False:
            self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_backend_icue_connected is False:
            self.lbl_con_stat_name.setText(' Connected:  False')
        elif bool_backend_icue_connected is True:
            self.lbl_con_stat_name.setText(' Connected:  True')

        if bool_switch_startup_net_traffic is False:
            self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_startup_net_traffic is True:
            self.btn_hotbar_nettraffic_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_startup_net_con_ms is False:
            self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_startup_net_con_ms is True:
            self.btn_hotbar_netcon_ms_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_startup_net_con_kb is False:
            self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_startup_net_con_kb is True:
            self.btn_hotbar_netcon_kb_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_startup_net_share_mon is False:
            self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_startup_net_share_mon is True:
            self.btn_hotbar_netshare_mon.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        self.lbl_net_con_mouse_led_selected.setText(str(corsairled_id_num_netcon_ms))

        if bool_switch_backlight is True:
            self.btn_bck_light.setIcon(QIcon("./image/img_backlight_on.png"))
            self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.color_all_id()
        elif bool_switch_backlight is False:
            self.btn_bck_light.setIcon(QIcon("./image/img_backlight_off.png"))
            self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)
            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_event_notification_g1 is False:
            self.btn_event_notification_g1.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_g1 is True:
            self.btn_event_notification_g1.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_g2 is False:
            self.btn_event_notification_g2.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_g2 is True:
            self.btn_event_notification_g2.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_g3 is False:
            self.btn_event_notification_g3.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_g3 is True:
            self.btn_event_notification_g3.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_g4 is False:
            self.btn_event_notification_g4.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_g4 is True:
            self.btn_event_notification_g4.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_g5 is False:
            self.btn_event_notification_g5.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_g5 is True:
            self.btn_event_notification_g5.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_g6 is False:
            self.btn_event_notification_g6.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_g6 is True:
            self.btn_event_notification_g6.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_run_g1 is False:
            self.btn_event_notification_run_g1.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_run_g1 is True:
            self.btn_event_notification_run_g1.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_run_g2 is False:
            self.btn_event_notification_run_g2.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_run_g2 is True:
            self.btn_event_notification_run_g2.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_run_g3 is False:
            self.btn_event_notification_run_g3.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_run_g3 is True:
            self.btn_event_notification_run_g3.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_run_g4 is False:
            self.btn_event_notification_run_g4.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_run_g4 is True:
            self.btn_event_notification_run_g4.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_run_g5 is False:
            self.btn_event_notification_run_g5.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_run_g5 is True:
            self.btn_event_notification_run_g5.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        if bool_switch_event_notification_run_g6 is False:
            self.btn_event_notification_run_g6.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
        elif bool_switch_event_notification_run_g6 is True:
            self.btn_event_notification_run_g6.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

        self.btn_backlight_auto_time_0_str = str(backlight_time_0).strip()
        self.btn_backlight_auto_time_0.setText(backlight_time_0)

        self.btn_backlight_auto_time_1_str = str(backlight_time_1).strip()
        self.btn_backlight_auto_time_1.setText(backlight_time_1)

        self.sdk_color_backlight_str = str(sdk_color_backlight_on).strip()
        self.sdk_color_backlight_str = self.sdk_color_backlight_str.replace('[', '')
        self.sdk_color_backlight_str = self.sdk_color_backlight_str.replace(']', '')
        self.sdk_color_backlight_str = self.sdk_color_backlight_str.replace('(', '')
        self.sdk_color_backlight_str = self.sdk_color_backlight_str.replace(')', '')
        self.qle_backlight_rgb_on.setText(self.sdk_color_backlight_str)

        self.cpu_led_color_str = str(sdk_color_cpu_on).strip()
        self.cpu_led_color_str = self.cpu_led_color_str.replace('[', '')
        self.cpu_led_color_str = self.cpu_led_color_str.replace(']', '')
        self.qle_cpu_mon_rgb_on.setText(self.cpu_led_color_str)

        self.dram_led_color_str = str(sdk_color_dram_on).strip()
        self.dram_led_color_str = self.dram_led_color_str.replace('[', '')
        self.dram_led_color_str = self.dram_led_color_str.replace(']', '')
        self.qle_dram_mon_rgb_on.setText(self.dram_led_color_str)

        self.vram_led_color_str = str(sdk_color_vram_on).strip()
        self.vram_led_color_str = self.vram_led_color_str.replace('[', '')
        self.vram_led_color_str = self.vram_led_color_str.replace(']', '')
        self.qle_vram_mon_rgb_on.setText(self.vram_led_color_str)

        self.hdd_led_color_str = str(sdk_color_hddwrite_on).strip()
        self.hdd_led_color_str = self.hdd_led_color_str.replace('[', '')
        self.hdd_led_color_str = self.hdd_led_color_str.replace(']', '')
        self.qle_hdd_mon_rgb_on.setText(self.hdd_led_color_str)

        self.hdd_led_read_color_str = str(sdk_color_hddread_on).strip()
        self.hdd_led_read_color_str = self.hdd_led_read_color_str.replace('[', '')
        self.hdd_led_read_color_str = self.hdd_led_read_color_str.replace(']', '')
        self.qle_hdd_read_mon_rgb_on.setText(self.hdd_led_read_color_str)

        self.cpu_led_time_on_str = str(timing_cpu_util).strip()
        self.qle_cpu_led_time_on.setText(self.cpu_led_time_on_str)

        self.dram_led_time_on_str = str(timing_dram_util).strip()
        self.qle_dram_led_time_on.setText(self.dram_led_time_on_str)

        self.vram_led_time_on_str = str(timing_vram_util).strip()
        self.qle_vram_led_time_on.setText(self.vram_led_time_on_str)

        self.hdd_led_time_on_str = str(timing_hdd_util).strip()
        self.qle_hdd_led_time_on.setText(self.hdd_led_time_on_str)

        self.hdd_led_time_on_str = str(timing_net_traffic_util).strip()
        self.qle_network_adapter_led_time_on.setText(self.hdd_led_time_on_str)

        self.cmb_network_adapter_name.addItem(devices_network_adapter_name)

        self.netshare_mon_rgb_on_str = str(sdk_color_netshare_on).strip()
        self.netshare_mon_rgb_on_str = self.netshare_mon_rgb_on_str.replace('[', '')
        self.netshare_mon_rgb_on_str = self.netshare_mon_rgb_on_str.replace(']', '')
        self.qle_netshare_mon_rgb_on.setText(self.netshare_mon_rgb_on_str)

        self.show()

    def changeEvent(self, event):
        # print('-- [App.changeEvent]: plugged in')
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.setFocus()
            else:
                self.setFocus()

    def mousePressEvent(self, event):
        # print('-- [App.mousePressEvent]: plugged in')
        self.prev_pos = event.globalPos()
        self.setFocus()

    def mouseMoveEvent(self, event):
        # print('-- [App.mouseMoveEvent]: plugged in')
        delta = QPoint(event.globalPos() - self.prev_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.prev_pos = event.globalPos()

    def pollCursor(self):
        # print('-- [App.pollCursor]: plugged in')
        pos = QCursor.pos()
        if pos != self.cursor:
            self.cursor = pos
            self.cursorMove.emit(pos)

    def handleCursorMove(self, pos):
        # print('-- [App.handleCursorMove]: plugged in')
        pass


class EventHandlerG1Notify(QThread):
    print('-- [EventHandlerG1Notify]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def send_instruction_on(self):
        # print('-- [EventHandlerG1Notify.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_g1_event_notification
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: sdk_color_g1_event_notification}))

    def send_instruction_off(self):
        # print('-- [EventHandlerG1Notify.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: sdk_color_backlight}))

    def run(self):
        print('-- [EventHandlerG1Notify.run]: plugged in')
        global bool_allow_g1_short
        bool_allow_g1_short = True
        # i = 0
        while True:
            # print('-- [EventHandlerG1Notify] testing:', i)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            sdk.set_led_colors_flush_buffer()
            # i += 1

    def stop(self):
        print('-- [EventHandlerG1Notify.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [EventHandlerG2Notify.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        sdk.set_led_colors_flush_buffer()
        self.terminate()


class EventHandlerG2Notify(QThread):
    print('-- [EventHandlerG2Notify]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def send_instruction_on(self):
        # print('-- [EventHandlerG2Notify.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_g2_event_notification
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_g2_event_notification}))

    def send_instruction_off(self):
        # print('-- [EventHandlerG2Notify.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))

    def run(self):
        print('-- [EventHandlerG2Notify.run]: plugged in')
        global bool_allow_g2_short
        bool_allow_g2_short = True
        # i = 0
        while True:
            # print('-- [EventHandlerG2Notify] testing:', i)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            sdk.set_led_colors_flush_buffer()
            # i += 1

    def stop(self):
        print('-- [EventHandlerG2Notify.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [EventHandlerG2Notify.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        sdk.set_led_colors_flush_buffer()
        self.terminate()


class EventHandlerG3Notify(QThread):
    print('-- [EventHandlerG3Notify]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def send_instruction_on(self):
        # print('-- [EventHandlerG3Notify.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_g3_event_notification
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: sdk_color_g3_event_notification}))

    def send_instruction_off(self):
        # print('-- [EventHandlerG3Notify.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: sdk_color_backlight}))

    def run(self):
        print('-- [EventHandlerG3Notify.run]: plugged in')
        global bool_allow_g3_short
        bool_allow_g3_short = True
        # i = 0
        while True:
            # print('-- [EventHandlerG3Notify] testing:', i)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            sdk.set_led_colors_flush_buffer()
            # i += 1

    def stop(self):
        print('-- [EventHandlerG3Notify.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [EventHandlerG3Notify.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        sdk.set_led_colors_flush_buffer()
        self.terminate()


class EventHandlerG4Notify(QThread):
    print('-- [EventHandlerG4Notify]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def send_instruction_on(self):
        # print('-- [EventHandlerG4Notify.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_g4_event_notification
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: sdk_color_g4_event_notification}))

    def send_instruction_off(self):
        # print('-- [EventHandlerG4Notify.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: sdk_color_backlight}))

    def run(self):
        print('-- [EventHandlerG4Notify.run]: plugged in')
        global bool_allow_g4_short
        bool_allow_g4_short = True
        # i = 0
        while True:
            # print('-- [EventHandlerG4Notify] testing:', i)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            sdk.set_led_colors_flush_buffer()
            # i += 1

    def stop(self):
        print('-- [EventHandlerG4Notify.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [EventHandlerG4Notify.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        sdk.set_led_colors_flush_buffer()
        self.terminate()


class EventHandlerG5Notify(QThread):
    print('-- [EventHandlerG5Notify]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def send_instruction_on(self):
        # print('-- [EventHandlerG5Notify.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_g5_event_notification
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: sdk_color_g5_event_notification}))

    def send_instruction_off(self):
        # print('-- [EventHandlerG5Notify.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: sdk_color_backlight}))

    def run(self):
        print('-- [EventHandlerG5Notify.run]: plugged in')
        global bool_allow_g5_short
        bool_allow_g5_short = True
        # i = 0
        while True:
            # print('-- [EventHandlerG5Notify] testing:', i)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            sdk.set_led_colors_flush_buffer()
            # i += 1

    def stop(self):
        print('-- [EventHandlerG5Notify.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [EventHandlerG5Notify.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        sdk.set_led_colors_flush_buffer()
        self.terminate()


class EventHandlerG6Notify(QThread):
    print('-- [EventHandlerG6Notify]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def send_instruction_on(self):
        # print('-- [EventHandlerG6Notify.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_g6_event_notification
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: sdk_color_g6_event_notification}))

    def send_instruction_off(self):
        # print('-- [EventHandlerG6Notify.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: sdk_color_backlight}))

    def run(self):
        print('-- [EventHandlerG6Notify.run]: plugged in')
        global bool_allow_g6_short
        bool_allow_g6_short = True
        i = 0
        while True:
            # print('-- [EventHandlerG6Notify] testing:', i)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            sdk.set_led_colors_flush_buffer()
            # i += 1

    def stop(self):
        print('-- [EventHandlerG6Notify.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [EventHandlerG6Notify.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        sdk.set_led_colors_flush_buffer()
        self.terminate()


class EventHandlerReadFileEvents(QThread):
    print('-- [EventHandlerReadFileEvents]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-- [EventHandlerReadFileEvents.run]: plugged in')
        global bool_switch_event_notification_g1, bool_switch_event_notification_g2, bool_switch_event_notification_g3
        global bool_switch_event_notification_g4, bool_switch_event_notification_g5, bool_switch_event_notification_g6

        global bool_event_notification_g1, bool_event_notification_g2, bool_event_notification_g3
        global bool_event_notification_g4, bool_event_notification_g5, bool_event_notification_g6

        global thread_g1_notify, thread_g2_notify, thread_g3_notify, thread_g4_notify, thread_g5_notify, thread_g6_notify

        global devices_kb

        if len(devices_kb) > 0:

            while True:
                bool_event_notification_g1 = False
                if bool_switch_event_notification_g1 is True:
                    if os.path.exists('./data/event_notification_g1.dat'):
                        try:
                            with open('./data/event_notification_g1.dat', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    if line == 'True':
                                        print('-- [EventHandlerReadFileEvents.run] setting bool_event_notification_g1: true')
                                        bool_event_notification_g1 = True
                                        break
                            if bool_event_notification_g1 is True:
                                open('./data/event_notification_g1.dat', 'w').close()
                                bool_event_notification_g1 = False
                                thread_g1_notify[0].start()
                        except Exception as e:
                            print('-- [EventHandlerReadFileEvents.run g1] Error:', e)

                if bool_switch_event_notification_g2 is True:
                    if os.path.exists('./data/event_notification_g2.dat'):
                        try:
                            with open('./data/event_notification_g2.dat', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    if line == 'True':
                                        print('-- [EventHandlerReadFileEvents.run] setting bool_event_notification_g2: true')
                                        bool_event_notification_g2 = True
                                        break
                            if bool_event_notification_g2 is True:
                                open('./data/event_notification_g2.dat', 'w').close()
                                bool_event_notification_g2 = False
                                thread_g2_notify[0].start()
                        except Exception as e:
                            print('-- [EventHandlerReadFileEvents.run g2] Error:', e)

                if bool_switch_event_notification_g3 is True:
                    if os.path.exists('./data/event_notification_g3.dat'):
                        try:
                            with open('./data/event_notification_g3.dat', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    if line == 'True':
                                        print('-- [EventHandlerReadFileEvents.run] setting bool_event_notification_g3: true')
                                        bool_event_notification_g3 = True
                                        break
                            if bool_event_notification_g3 is True:
                                open('./data/event_notification_g3.dat', 'w').close()
                                bool_event_notification_g3 = False
                                thread_g3_notify[0].start()
                        except Exception as e:
                            print('-- [EventHandlerReadFileEvents.run g3] Error:', e)

                if bool_switch_event_notification_g4 is True:
                    if os.path.exists('./data/event_notification_g4.dat'):
                        try:
                            with open('./data/event_notification_g4.dat', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    if line == 'True':
                                        print('-- [EventHandlerReadFileEvents.run] setting bool_event_notification_g4: true')
                                        bool_event_notification_g4 = True
                                        break
                            if bool_event_notification_g4 is True:
                                open('./data/event_notification_g4.dat', 'w').close()
                                bool_event_notification_g4 = False
                                thread_g4_notify[0].start()
                        except Exception as e:
                            print('-- [EventHandlerReadFileEvents.run g4] Error:', e)

                if bool_switch_event_notification_g5 is True:
                    if os.path.exists('./data/event_notification_g5.dat'):
                        try:
                            with open('./data/event_notification_g5.dat', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    if line == 'True':
                                        print('-- [EventHandlerReadFileEvents.run] setting bool_event_notification_g5: true')
                                        bool_event_notification_g5 = True
                                        break
                            if bool_event_notification_g5 is True:
                                open('./data/event_notification_g5.dat', 'w').close()
                                bool_event_notification_g5 = False
                                thread_g5_notify[0].start()
                        except Exception as e:
                            print('-- [EventHandlerReadFileEvents.run g5] Error:', e)

                if bool_switch_event_notification_g6 is True:
                    if os.path.exists('./data/event_notification_g6.dat'):
                        try:
                            with open('./data/event_notification_g6.dat', 'r') as fo:
                                for line in fo:
                                    line = line.strip()
                                    if line == 'True':
                                        print('-- [EventHandlerReadFileEvents.run] setting bool_event_notification_g6: true')
                                        bool_event_notification_g6 = True
                                        break
                            if bool_event_notification_g6 is True:
                                open('./data/event_notification_g6.dat', 'w').close()
                                bool_event_notification_g6 = False
                                thread_g6_notify[0].start()
                        except Exception as e:
                            print('-- [EventHandlerReadFileEvents.run g6] Error:', e)

                time.sleep(1)

    def stop(self):
        print('-- [EventHandlerReadFileEvents.stop]: plugged in')


class SdkEventHandlerClass(QThread):
    print('-- [SdkEventHandlerClass]: plugged in')

    def __init__(self, g1_function_short, g1_function_long,
                 g2_function_short, g2_function_long,
                 g3_function_short, g3_function_long,
                 g4_function_short, g4_function_long,
                 g5_function_short, g5_function_long,
                 g6_function_short, g6_function_long):
        QThread.__init__(self)

        self.g1_function_short = g1_function_short
        self.g1_function_long = g1_function_long

        self.g2_function_short = g2_function_short
        self.g2_function_long = g2_function_long

        self.g3_function_short = g3_function_short
        self.g3_function_long = g3_function_long

        self.g4_function_short = g4_function_short
        self.g4_function_long = g4_function_long

        self.g5_function_short = g5_function_short
        self.g5_function_long = g5_function_long

        self.g6_function_short = g6_function_short
        self.g6_function_long = g6_function_long

        self.time_now_press = float()
        self.time_now_press_keyId = ''
        self.time_now_release = float()
        self.time_now_release_keyId = ''
        self.eId = []

    def on_press(self, event_id, data):
        # print('-- [SdkEventHandlerClass.on_press]: plugged in')
        date_time_now = str(datetime.datetime.now())
        var = date_time_now.split(' ')
        var = var[1].split(':')[2]
        self.time_now_press = float(var)
        self.time_now_press_keyId = str(data.keyId).strip()
        print('-- [SdkEventHandlerClass.on_press] captured event: time_now_0: {0} pressed {1}'.format(self.time_now_press, data.keyId))

    def on_release(self, event_id, data):
        # print('-- [SdkEventHandlerClass.on_release]: plugged in')
        global bool_switch_event_notification_g1, bool_switch_event_notification_g2, bool_switch_event_notification_g3
        global bool_switch_event_notification_g4, bool_switch_event_notification_g5, bool_switch_event_notification_g6

        date_time_now = str(datetime.datetime.now())
        var = date_time_now.split(' ')
        var = var[1].split(':')[2]
        time_now_release = float(var)
        self.time_now_release_keyId = str(data.keyId).strip()

        if self.time_now_release_keyId == 'CorsairKeyId.Kb_G1':
            # (notification) short press: reset ledId color and run pertaining function
            if time_now_release < (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g1 is True:
                    self.g1_function_short()
            # (notification) long release: reset ledId color and disconnect key from function
            elif time_now_release >= (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} long released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g1 is True:
                    self.g1_function_long()

        elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G2':
            # (notification) short press: reset ledId color and run pertaining function
            if time_now_release < (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g2 is True:
                    self.g2_function_short()
            # (notification) long release: reset ledId color and disconnect key from function
            elif time_now_release >= (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} long released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g2 is True:
                    self.g2_function_long()

        elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G3':
            # (notification) short press: reset ledId color and run pertaining function
            if time_now_release < (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g3 is True:
                    self.g3_function_short()
            # (notification) long release: reset ledId color and disconnect key from function
            elif time_now_release >= (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} long released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g3 is True:
                    self.g3_function_long()

        elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G4':
            # (notification) short press: reset ledId color and run pertaining function
            if time_now_release < (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g4 is True:
                    self.g4_function_short()
            # (notification) long release: reset ledId color and disconnect key from function
            elif time_now_release >= (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} long released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g4 is True:
                    self.g4_function_long()

        elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G5':
            # (notification) short press: reset ledId color and run pertaining function
            if time_now_release < (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g5 is True:
                    self.g5_function_short()
            # (notification) long release: reset ledId color and disconnect key from function
            elif time_now_release >= (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} long released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g5 is True:
                    self.g5_function_long()

        elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G6':
            # (notification) short press: reset ledId color and run pertaining function
            if time_now_release < (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g6 is True:
                    self.g6_function_short()
            # (notification) long release: reset ledId color and disconnect key from function
            elif time_now_release >= (self.time_now_press + 0.75) and self.time_now_press_keyId == self.time_now_release_keyId:
                print('-- [App.on_press] captured event: time_now_1: {0} long released {1}'.format(self.time_now_press, data.keyId))
                if bool_switch_event_notification_g6 is True:
                    self.g6_function_long()

    def sdk_event_handler(self, event_id, data):
        if event_id == CorsairEventId.KeyEvent:
            # print('-- [SdkEventHandlerClass.sdk_event_handler] Event:', event_id, data.keyId, "pressed" if data.isPressed else "released")
            self.eId = event_id
            if data.isPressed:
                self.on_press(event_id, data)
            else:
                self.on_release(event_id, data)

        elif event_id == CorsairEventId.DeviceConnectionStatusChangedEvent:
            print("-- [SdkEventHandlerClass.sdk_event_handler]: Device id: %s   Status: %s" % (data.deviceId.decode(), "connected" if data.isConnected else "disconnected"))
        else:
            print("-- [SdkEventHandlerClass.sdk_event_handler]: invalid event")

    def run(self):
        global sdk, devices_kb, devices_kb_name
        # sdk_0 = CueSdk()
        connected = sdk.connect()
        if not connected:
            err = sdk.get_last_error()
            print("-- [SdkEventHandlerClass.run]: handshake failed: %s" % err)
            return

        subscribed = sdk.subscribe_for_events(self.sdk_event_handler)
        if not subscribed:
            err = sdk.get_last_error()
            print("-- [SdkEventHandlerClass.run]: subscribe for events error: %s" % err)
            return

        while (True):
            input_str = input()

        sdk.unsubscribe_from_events()

    def stop(self):
        print('-- [SdkEventHandlerClass.stop]: plugged in')
        global sdk
        try:
            sdk.unsubscribe_from_events()
        except Exception as e:
            print(e)
        self.terminate()


class CompileDevicesClass(QThread):
    print('-- [CompileDevicesClass]: plugged in')

    def __init__(self, lbl_con_stat_name, lbl_con_stat_kb, lbl_con_stat_mouse, btn_refresh_compile, btn_hotbar_off_style, btn_hotbar_on_style):
        QThread.__init__(self)
        global sdk_color_hddread_on, sdk_color_backlight, sdk_color_backlight_on
        self.lbl_con_stat_name = lbl_con_stat_name
        self.lbl_con_stat_kb = lbl_con_stat_kb
        self.lbl_con_stat_mouse = lbl_con_stat_mouse
        self.btn_refresh_recompile = btn_refresh_compile
        self.btn_hotbar_off_style = btn_hotbar_off_style
        self.btn_hotbar_on_style = btn_hotbar_on_style
        self.device_str = ''
        self.device_index = ()
        self.bool_backend_comprehensive_enumeration = True

    def enum_kb(self):
        global sdk
        global bool_backend_enum_kb
        global devices_kb, devices_kb_name, corsairled_id_num_kb_complete
        # 1. Get Key Names & Key IDs
        led_position = sdk.get_led_positions_by_device_index(self.device_index)
        led_position_str = str(led_position).split('), ')
        led_position_str_tmp = led_position_str[0].split()

        if 'CorsairLedId.K_' in led_position_str_tmp[0]:
            corsairled_id_num_kb_complete = []
            devices_kb = []
            devices_kb_name = []
            devices_kb.append(self.device_index)
            devices_kb_name.append(sdk.get_device_info(devices_kb[0]))
            print('-- [CompileDevicesClass.enumerate_device]  Keyboard Name:', devices_kb_name)
            for _ in led_position_str:
                var = _.split()
                var_0 = var[0]
                var_0 = var_0.replace('{', '')
                var_0 = var_0.replace('<', '')
                var_0 = var_0.replace(':', '')
                var_1 = var[1].replace('>:', '')
                corsairled_id_num_kb_complete.append(int(var_1))
            print('-- [CompileDevicesClass.enumerate_device]  corsairled_id_num_kb_complete:', corsairled_id_num_kb_complete)
            bool_backend_enum_kb = True

    def enum_ms(self):
        global sdk
        global bool_backend_enum_ms
        global devices_ms, devices_ms_name, corsairled_id_num_ms_complete

        led_position = sdk.get_led_positions_by_device_index(self.device_index)
        led_position_str = str(led_position).split('), ')
        led_position_str_tmp = led_position_str[0].split()

        if 'CorsairLedId.M_' in led_position_str_tmp[0]:
            devices_ms = []
            corsairled_id_num_ms_complete = []
            devices_ms_name = []
            devices_ms.append(int(self.device_index))
            devices_ms_name.append(sdk.get_device_info(devices_ms[0]))
            print('-- [CompileDevicesClass.enumerate_device]  Mouse Name:', devices_ms_name[0])
            for _ in led_position_str:
                var = _.split()
                var_0 = var[0]
                var_0 = var_0.replace('{', '')
                var_0 = var_0.replace('<', '')
                var_0 = var_0.replace(':', '')
                var_1 = var[1].replace('>:', '')
                corsairled_id_num_ms_complete.append(int(var_1))
            print('-- [CompileDevicesClass.enumerate_device]  corsairled_id_num_ms_complete:', corsairled_id_num_ms_complete)
            bool_backend_enum_ms = True

    def stop_all_threads(self):
        print('-- [CompileDevicesClass.stop_all_threads]: plugged in')
        global thread_disk_rw
        global thread_cpu_util
        global thread_dram_util
        global thread_vram_util
        global thread_net_traffic
        global thread_net_connection
        global thread_net_share
        global thread_sdk_event_handler
        global thread_sdk_event_handler_read_file_events
        global thread_backlight_auto
        global devices_kb, devices_ms

        print('-- [CompileDevicesClass.stop_all_threads] stopping all threads:', )
        if len(devices_kb) >= 1 or len(devices_ms) >= 1:
            try:
                thread_disk_rw[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
            try:
                thread_cpu_util[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
                thread_dram_util[0].stop()
            try:
                thread_vram_util[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
                thread_net_traffic[0].stop()
            try:
                thread_net_connection[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
                thread_net_share[0].stop()
            try:
                thread_sdk_event_handler[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
                thread_sdk_event_handler_read_file_events[0].stop()
            try:
                thread_backlight_auto[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

    def start_all_threads(self):
        print('-- [CompileDevicesClass.start_all_threads]: plugged in')
        global bool_switch_startup_cpu_util, bool_switch_startup_dram_util, bool_switch_startup_vram_util, bool_switch_startup_net_traffic
        global bool_switch_startup_hdd_read_write
        global thread_net_connection, bool_switch_startup_net_con, bool_switch_startup_net_con_ms, bool_switch_startup_net_con_kb
        global bool_switch_startup_net_share_mon, bool_switch_startup_hdd_read_write
        global bool_backend_config_read_complete, bool_switch_startup_exclusive_control
        global thread_backlight_auto, bool_switch_backlight_auto

        if len(devices_kb) > 0:

            thread_sdk_event_handler[0].start()
            thread_sdk_event_handler_read_file_events[0].start()

            if bool_switch_startup_hdd_read_write:
                thread_disk_rw[0].start()
            if bool_switch_startup_cpu_util:
                thread_cpu_util[0].start()
            if bool_switch_startup_dram_util:
                thread_dram_util[0].start()
            if bool_switch_startup_vram_util:
                thread_vram_util[0].start()
            if bool_switch_startup_net_traffic:
                thread_net_traffic[0].start()
            if bool_switch_startup_net_share_mon:
                thread_net_share[0].start()

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if bool_switch_startup_net_con_ms is True or bool_switch_startup_net_con_kb is True:
                thread_net_connection[0].start()

            if bool_switch_startup_exclusive_control is True:
                sdk.request_control()
            if bool_switch_startup_exclusive_control is False:
                sdk.release_control()

            if bool_switch_backlight_auto is True and len(devices_kb) > 0:
                thread_backlight_auto[0].start()

    def attempt_connect(self):
        # print('-- [CompileDevicesClass.attempt_connect]: plugged in')
        global sdk, bool_backend_icue_connected, devices_previous, bool_backend_icue_connected_previous
        connected = sdk.connect()

        if not connected:
            bool_backend_icue_connected = False
            if bool_backend_icue_connected != bool_backend_icue_connected_previous:
                # print('-- [CompileDevicesClass.attempt_connect] bool_backend_icue_connected:',bool_backend_icue_connected)
                bool_backend_icue_connected_previous = bool_backend_icue_connected
                self.stop_all_threads()
            devices_previous = []
            self.lbl_con_stat_name.setText('Connected:  False')
            self.lbl_con_stat_name.setAlignment(Qt.AlignCenter)
            time.sleep(2)
            self.attempt_connect()

        elif connected:
            sdk.request_control()
            bool_backend_icue_connected = True
            # print('-- [CompileDevicesClass.attempt_connect] bool_backend_icue_connected:', bool_backend_icue_connected)
            self.lbl_con_stat_name.setText('Connected:  True')
            self.lbl_con_stat_name.setAlignment(Qt.AlignCenter)
            self.get_devices()

    def entry_sequence(self):
        print('-- [CompileDevicesClass.entry_sequence]: plugged in')
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight
        global sdk_color_backlight, bool_switch_backlight, ui_feature_page, bool_switch_show_discrete, sdk_color_backlight_on

        if len(devices_kb) >= 1:
            for _ in corsairled_id_num_kb_complete:
                itm = [{_: (255, 255, 255)}]
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
            sdk.set_led_colors_flush_buffer()
        if len(devices_ms) >= 1:
            for _ in corsairled_id_num_ms_complete:
                itm = [{_: (255, 255, 255)}]
                sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], itm[0])
            sdk.set_led_colors_flush_buffer()
        time.sleep(1)
        if len(devices_kb) >= 1:
            for _ in corsairled_id_num_kb_complete:
                itm = [{_: sdk_color_backlight}]
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
            sdk.set_led_colors_flush_buffer()
        if len(devices_ms) >= 1:
            for _ in corsairled_id_num_ms_complete:
                itm = [{_: sdk_color_backlight}]
                sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], itm[0])
            sdk.set_led_colors_flush_buffer()

    def get_devices(self):
        # print('-- [CompileDevicesClass.get_devices]: plugged in')
        global sdk, devices_previous, bool_backend_enum_kb, bool_backend_enum_ms, devices_kb, devices_ms, devices_kb_name
        bool_backend_enum_kb = False
        bool_backend_enum_ms = False
        fresh_start = False

        if self.bool_backend_comprehensive_enumeration is True:
            device = sdk.get_devices()
            device_i = 0
            for _ in device:
                target_name = str(device[device_i])
                self.device_index = device_i
                self.device_str = target_name
                if str(device) != str(devices_previous):
                    if fresh_start is False:
                        devices_kb = []
                        devices_ms = []
                    fresh_start = True
                    self.btn_refresh_recompile.setStyleSheet(self.btn_hotbar_on_style)
                    try:
                        self.enum_kb()
                    except Exception as e:
                        print(e)
                    try:
                        self.enum_ms()
                    except Exception as e:
                        print(e)
                    time.sleep(0.5)
                    self.btn_refresh_recompile.setStyleSheet(self.btn_hotbar_off_style)
                device_i += 1

            if fresh_start is True:
                print('-- [CompileDevicesClass.get_devices] fresh start: True')
                if len(devices_kb) >= 1:
                    self.lbl_con_stat_kb.setText(str(devices_kb_name[0]))
                elif len(devices_kb) < 1:
                    self.lbl_con_stat_kb.setText('')
                if len(devices_ms) >= 1:
                    self.lbl_con_stat_mouse.setText(str(devices_ms_name[0]))
                elif len(devices_ms) < 1:
                    self.lbl_con_stat_mouse.setText('')

                if len(devices_kb) >= 1 or len(devices_ms) >= 1:
                    self.entry_sequence()
                    devices_previous = device
                    self.stop_all_threads()
                    time.sleep(2)
                    self.start_all_threads()

    def sanitize_rgb_values(self):
        print('-- [Config_Compile.sanitize_rgb_values]: plugged in')
        print('-- [Config_Compile.sanitize_rgb_values] attempting to sanitize input:', self.sanitize_str)
        var_str = self.sanitize_str
        self.sanitize_passed = False
        if len(var_str) == 3:
            if len(var_str[0]) >= 1 and len(var_str[0]) <= 3:
                if len(var_str[1]) >= 1 and len(var_str[1]) <= 3:
                    if len(var_str[2]) >= 1 and len(var_str[2]) <= 3:
                        if var_str[0].isdigit():
                            if var_str[1].isdigit():
                                if var_str[2].isdigit():
                                    var_int_0 = int(var_str[0])
                                    var_int_1 = int(var_str[1])
                                    var_int_2 = int(var_str[2])
                                    if var_int_0 >= 0 and var_int_0 <= 255:
                                        if var_int_1 >= 0 and var_int_1 <= 255:
                                            if var_int_2 >= 0 and var_int_2 <= 255:
                                                self.sanitize_passed = True

    def read_config(self):
        print('-- [ConfigCompile.read_config]: plugged in')
        global bool_switch_event_notification_g1
        global bool_switch_event_notification_g2
        global bool_switch_event_notification_g3
        global bool_switch_event_notification_g4
        global bool_switch_event_notification_g5
        global bool_switch_event_notification_g6
        global bool_switch_event_notification_run_g1
        global bool_switch_event_notification_run_g2
        global bool_switch_event_notification_run_g3
        global bool_switch_event_notification_run_g4
        global bool_switch_event_notification_run_g5
        global bool_switch_event_notification_run_g6
        global str_event_notification_run_path_g1
        global str_event_notification_run_path_g2
        global str_event_notification_run_path_g3
        global str_event_notification_run_path_g4
        global str_event_notification_run_path_g5
        global str_event_notification_run_path_g6
        global sdk_color_cpu_on, timing_cpu_util, bool_switch_startup_cpu_util
        global sdk_color_dram_on, timing_dram_util, bool_switch_startup_dram_util
        global sdk_color_vram_on, timing_vram_util, devices_gpu_selected, bool_switch_startup_vram_util
        global sdk_color_hddwrite_on, timing_hdd_util, sdk_color_hddread_on, bool_switch_startup_hdd_read_write
        global bool_switch_startup_net_traffic, timing_net_traffic_util
        global devices_network_adapter_name, bool_backend_valid_network_adapter_name
        global corsairled_id_num_netsnt, corsairled_id_num_netrcv
        global bool_switch_startup_net_con_ms, corsairled_id_num_netcon_ms, bool_switch_startup_net_con_kb, bool_switch_startup_net_con
        global bool_switch_startup_net_share_mon
        global sdk_color_backlight, sdk_color_backlight_on, bool_switch_backlight
        global backlight_time_0, backlight_time_1, bool_switch_backlight_auto
        global bool_switch_startup_minimized, bool_switch_startup_autorun, bool_switch_startup_exclusive_control

        global bool_backend_allow_display, bool_backend_icue_connected, bool_backend_config_read_complete

        startup_loc = '/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/iCUEDisplay.lnk'
        bool_backend_valid_network_adapter_name = False

        with open('.\\config.dat', 'r') as fo:
            for line in fo:
                line = line.strip()

                if line.startswith('sdk_color_cpu_on: '):
                    var = line.replace('sdk_color_cpu_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        sdk_color_cpu_on[0] = int(var[0])
                        sdk_color_cpu_on[1] = int(var[1])
                        sdk_color_cpu_on[2] = int(var[2])
                    elif self.sanitize_passed is False:
                        print('-- [ConfigCompile.cpu_sanitize] sdk_color_cpu_on: sanitize_failed')
                if line.startswith('timing_cpu_util: '):
                    line = line.replace('timing_cpu_util: ', '')
                    try:
                        var = float(float(line))
                        if var >= 0.1 and var <= 5:
                            timing_cpu_util = var
                    except Exception as e:
                        timing_cpu_util = 0.5
                        print('[ConfigCompile.cpu_sanitize] Error:', e)
                if line == 'cpu_startup: true':
                    bool_switch_startup_cpu_util = True
                elif line == 'cpu_startup: false':
                    bool_switch_startup_cpu_util = False

                if line.startswith('sdk_color_dram_on: '):
                    var = line.replace('sdk_color_dram_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        print(
                            '-- [ConfigCompile.dram_sanitize] sdk_color_dram_on: sanitize_passed')
                        sdk_color_dram_on[0] = int(var[0])
                        sdk_color_dram_on[1] = int(var[1])
                        sdk_color_dram_on[2] = int(var[2])
                    elif self.sanitize_passed is False:
                        print(
                            '-- [ConfigCompile.dram_sanitize] sdk_color_dram_on: sanitize_failed')
                if line.startswith('timing_dram_util: '):
                    line = line.replace('timing_dram_util: ', '')
                    try:
                        var = float(float(line))
                        if var >= 0.1 and var <= 5:
                            timing_dram_util = var
                    except Exception as e:
                        timing_dram_util = 0.5
                        print('[ConfigCompile.dram_sanitize] Error:', e)
                if line == 'dram_startup: true':
                    bool_switch_startup_dram_util = True
                elif line == 'dram_startup: false':
                    bool_switch_startup_dram_util = False

                if line.startswith('sdk_color_vram_on: '):
                    var = line.replace('sdk_color_vram_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        print(
                            '-- [ConfigCompile.vram_sanitize] sdk_color_vram_on: sanitize_passed')
                        sdk_color_vram_on[0] = int(var[0])
                        sdk_color_vram_on[1] = int(var[1])
                        sdk_color_vram_on[2] = int(var[2])
                    elif self.sanitize_passed is False:
                        print(
                            '-- [ConfigCompile.vram_sanitize] sdk_color_vram_on: sanitize_failed')
                if line.startswith('timing_vram_util: '):
                    vram_led_time_on_tmp = line.replace('timing_vram_util: ', '')
                    try:
                        vram_led_time_on_tmp = float(float(vram_led_time_on_tmp))
                        if vram_led_time_on_tmp >= 0.1 and vram_led_time_on_tmp <= 5:
                            timing_vram_util = vram_led_time_on_tmp
                    except Exception as e:
                        timing_vram_util = 0.5
                        print('[ConfigCompile.vram_sanitize] Error:', e)
                if line == 'vram_startup: true':
                    bool_switch_startup_vram_util = True
                elif line == 'vram_startup: false':
                    bool_switch_startup_vram_util = False
                if line.startswith('devices_gpu_selected: '):
                    gpu_num_tmp = line.replace('devices_gpu_selected: ', '')
                    if gpu_num_tmp.isdigit():
                        gpu_num_tmp = int(gpu_num_tmp)
                        gpus = GPUtil.getGPUs()
                        if len(gpus) >= gpu_num_tmp:
                            devices_gpu_selected = gpu_num_tmp
                        else:
                            print('-- [ConfigCompile.vram_sanitize] devices_gpu_selected: may exceed gpus currently available on the system. using default value')
                            devices_gpu_selected = 0
                    else:
                        devices_gpu_selected = 0

                if line.startswith('sdk_color_hddwrite_on: '):
                    var = line.replace('sdk_color_hddwrite_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        sdk_color_hddwrite_on[0] = int(var[0])
                        sdk_color_hddwrite_on[1] = int(var[1])
                        sdk_color_hddwrite_on[2] = int(var[2])
                    elif self.sanitize_passed is False:
                        print('-- [ConfigCompile.hdd_sanitize] sdk_color_hddwrite_on: sanitize_failed')
                if line.startswith('sdk_color_hddread_on: '):
                    var = line.replace('sdk_color_hddread_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        sdk_color_hddread_on[0] = int(var[0])
                        sdk_color_hddread_on[1] = int(var[1])
                        sdk_color_hddread_on[2] = int(var[2])
                    elif self.sanitize_passed is False:
                        print('-- [ConfigCompile.hdd_sanitize] sdk_color_hddread_on: sanitize_failed')
                if line.startswith('timing_hdd_util: '):
                    var_0 = line.replace('timing_hdd_util: ', '')
                    try:
                        var = float(float(var_0))
                        if var >= 0 and var <= 5:
                            timing_hdd_util = var
                    except Exception as e:
                        timing_hdd_util = 0.5
                        print('[ConfigCompile.timing_hdd_util] Error:', e)
                if line == 'hdd_startup: true':
                    bool_switch_startup_hdd_read_write = True
                elif line == 'hdd_startup: false':
                    bool_switch_startup_hdd_read_write = False

                if line == 'exclusive_access: true':
                    bool_switch_startup_exclusive_control = True
                elif line == 'exclusive_access: false':
                    bool_switch_startup_exclusive_control = False
                if line == 'start_minimized: true':
                    bool_switch_startup_minimized = True
                elif line == 'bool_switch_startup_minimized: false':
                    bool_switch_startup_minimized = False
                if line == 'run_startup: true' and os.path.exists(os.path.join(os.path.expanduser('~') + startup_loc)):
                    bool_switch_startup_autorun = True
                elif line == 'run_startup: false' or not os.path.exists(os.path.join(os.path.expanduser('~') + startup_loc)):
                    bool_switch_startup_autorun = False

                if line.startswith('timing_net_traffic_util: '):
                    var_0 = line.replace('timing_net_traffic_util: ', '')
                    try:
                        var = float(float(var_0))
                        if var >= 0.0 and var <= 5:
                            timing_net_traffic_util = var
                    except Exception as e:
                        timing_net_traffic_util = 0.0
                        print('-- [ConfigCompile.timing_net_traffic_util] Error:', e)

                if line.startswith('devices_network_adapter_name: '):
                    var = line.replace('devices_network_adapter_name: ', '')
                    print('-- [ConfigCompile.devices_network_adapter_name] checking existance:', var)
                    pythoncom.CoInitialize()
                    try:
                        wmis = win32com.client.Dispatch("WbemScripting.SWbemLocator")
                        wbems = wmis.ConnectServer(".", "root\\cimv2")
                        col_items = wbems.ExecQuery(
                            'SELECT * FROM Win32_PerfFormattedData_Tcpip_NetworkAdapter')
                        for objItem in col_items:
                            if objItem.Name != None:
                                if var == str(objItem.Name.strip()):
                                    print('-- [ConfigCompile.network_adapter_sanitize] found:',
                                          objItem.Name)
                                    var = objItem.Name
                                    bool_backend_valid_network_adapter_name = True
                    except Exception as e:
                        print('-- [ConfigCompile.network_adapter_sanitize] Error:', e)
                    if bool_backend_valid_network_adapter_name is True:
                        devices_network_adapter_name = var
                    elif bool_backend_valid_network_adapter_name is False:
                        devices_network_adapter_name = ""

                if line == 'network_adapter_startup: true':
                    bool_switch_startup_net_traffic = True
                if line == 'network_adapter_startup: false':
                    bool_switch_startup_net_traffic = False

                elif line == 'bool_switch_startup_net_con_ms: true':
                    bool_switch_startup_net_con_ms = True
                elif line == 'bool_switch_startup_net_con_ms: false':
                    bool_switch_startup_net_con_ms = False
                elif line.startswith('corsairled_id_num_netcon_ms: '):
                    var = line.replace('corsairled_id_num_netcon_ms: ', '')
                    if var.isdigit():
                        var = int(var)
                        if var >= 1 and var <= 3:
                            corsairled_id_num_netcon_ms = var
                        else:
                            corsairled_id_num_netcon_ms = 0
                    else:
                        corsairled_id_num_netcon_ms = 0
                elif line == 'bool_switch_startup_net_con_kb: true':
                    bool_switch_startup_net_con_kb = True
                elif line == 'bool_switch_startup_net_con_kb: false':
                    bool_switch_startup_net_con_kb = False
                elif line == 'bool_switch_startup_net_con: true':
                    bool_switch_startup_net_con = True
                elif line == 'bool_switch_startup_net_con: false':
                    bool_switch_startup_net_con = False

                elif line == 'netshare_startup: true':
                    bool_switch_startup_net_share_mon = True
                elif line == 'netshare_startup: false':
                    bool_switch_startup_net_share_mon = False
                elif line.startswith('sdk_color_netshare_on:'):
                    var = line.replace('sdk_color_netshare_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        sdk_color_netshare_on[0] = int(var[0])
                        sdk_color_netshare_on[1] = int(var[1])
                        sdk_color_netshare_on[2] = int(var[2])
                elif line.startswith('sdk_color_backlight_on:'):
                    var = line.replace('sdk_color_backlight_on: ', '')
                    var = var.split(',')
                    self.sanitize_str = var
                    self.sanitize_rgb_values()
                    if self.sanitize_passed is True:
                        sdk_color_backlight_on[0] = int(var[0])
                        sdk_color_backlight_on[1] = int(var[1])
                        sdk_color_backlight_on[2] = int(var[2])
                if line == 'bool_switch_backlight: true':
                    bool_switch_backlight = True
                    sdk_color_backlight = sdk_color_backlight_on
                elif line == 'bool_switch_backlight: false':
                    bool_switch_backlight = False

                if line == 'bool_switch_backlight_auto: true':
                    bool_switch_backlight_auto = True
                if line == 'bool_switch_backlight_auto: false':
                    bool_switch_backlight_auto = False
                if line.startswith('backlight_time_0:'):
                    var = line.replace('backlight_time_0:', '')
                    var = str(var).strip()
                    if var.isdigit() and len(var) == 4:
                        print('-- [ReadConfigurationClass.backlight] backlight_time_0 passed digit check:', var)
                        backlight_time_0 = str(var.strip())
                    else:
                        print('-- [ReadConfigurationClass.backlight] backlight_time_0 failed digit check:', var)
                        backlight_time_0 = ''
                if line.startswith('backlight_time_1:'):
                    var = line.replace('backlight_time_1:', '')
                    var = str(var).strip()
                    if var.isdigit() and len(var) == 4:
                        print('-- [ReadConfigurationClass.backlight] backlight_time_1 passed digit check:', var)
                        backlight_time_1 = str(var.strip())
                    else:
                        print('-- [ReadConfigurationClass.backlight] backlight_time_1 failed digit check:', var)
                        backlight_time_1 = ''

                if line == 'bool_switch_event_notification_g1: true':
                    bool_switch_event_notification_g1 = True
                elif line == 'bool_switch_event_notification_g1: false':
                    bool_switch_event_notification_g1 = False
                elif line == 'bool_switch_event_notification_g2: true':
                    bool_switch_event_notification_g2 = True
                elif line == 'bool_switch_event_notification_g2: false':
                    bool_switch_event_notification_g2 = False
                elif line == 'bool_switch_event_notification_g3: true':
                    bool_switch_event_notification_g3 = True
                elif line == 'bool_switch_event_notification_g3: false':
                    bool_switch_event_notification_g3 = False
                elif line == 'bool_switch_event_notification_g4: true':
                    bool_switch_event_notification_g4 = True
                elif line == 'bool_switch_event_notification_g4: false':
                    bool_switch_event_notification_g4 = False
                elif line == 'bool_switch_event_notification_g5: true':
                    bool_switch_event_notification_g5 = True
                elif line == 'bool_switch_event_notification_g5: false':
                    bool_switch_event_notification_g5 = False
                elif line == 'bool_switch_event_notification_g6: true':
                    bool_switch_event_notification_g6 = True
                elif line == 'bool_switch_event_notification_g6: false':
                    bool_switch_event_notification_g6 = False
                elif line == 'bool_switch_event_notification_run_g1: true':
                    bool_switch_event_notification_run_g1 = True
                elif line == 'bool_switch_event_notification_run_g1: false':
                    bool_switch_event_notification_run_g1 = False
                elif line == 'bool_switch_event_notification_run_g2: true':
                    bool_switch_event_notification_run_g2 = True
                elif line == 'bool_switch_event_notification_run_g2: false':
                    bool_switch_event_notification_run_g2 = False
                elif line == 'bool_switch_event_notification_run_g3: true':
                    bool_switch_event_notification_run_g3 = True
                elif line == 'bool_switch_event_notification_run_g3: false':
                    bool_switch_event_notification_run_g3 = False
                elif line == 'bool_switch_event_notification_run_g4: true':
                    bool_switch_event_notification_run_g4 = True
                elif line == 'bool_switch_event_notification_run_g4: false':
                    bool_switch_event_notification_run_g4 = False
                elif line == 'bool_switch_event_notification_run_g5: true':
                    bool_switch_event_notification_run_g5 = True
                elif line == 'bool_switch_event_notification_run_g5: false':
                    bool_switch_event_notification_run_g5 = False
                elif line == 'bool_switch_event_notification_run_g6: true':
                    bool_switch_event_notification_run_g6 = True
                elif line == 'bool_switch_event_notification_run_g6: false':
                    bool_switch_event_notification_run_g6 = False
                elif line.startswith('str_event_notification_run_path_g1:'):
                    str_event_notification_run_path_g1 = line.replace('str_event_notification_run_path_g1: ', '')
                elif line.startswith('str_event_notification_run_path_g2:'):
                    str_event_notification_run_path_g2 = line.replace('str_event_notification_run_path_g2: ', '')
                elif line.startswith('str_event_notification_run_path_g3:'):
                    str_event_notification_run_path_g3 = line.replace('str_event_notification_run_path_g3: ', '')
                elif line.startswith('str_event_notification_run_path_g4:'):
                    str_event_notification_run_path_g4 = line.replace('str_event_notification_run_path_g4: ', '')
                elif line.startswith('str_event_notification_run_path_g5:'):
                    str_event_notification_run_path_g5 = line.replace('str_event_notification_run_path_g5: ', '')
                elif line.startswith('str_event_notification_run_path_g6:'):
                    str_event_notification_run_path_g6 = line.replace('str_event_notification_run_path_g6: ', '')

        print('-- [ConfigCompile.config_read] bool_switch_event_notification_g1:', bool_switch_event_notification_g1)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_g2:', bool_switch_event_notification_g2)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_g3:', bool_switch_event_notification_g3)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_g4:', bool_switch_event_notification_g4)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_g5:', bool_switch_event_notification_g5)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_g5:', bool_switch_event_notification_g5)
        print('-- [ConfigCompile.config_read] bool_switch_event_notification_run_g1:', bool_switch_event_notification_run_g1)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_run_g2:', bool_switch_event_notification_run_g2)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_run_g3:', bool_switch_event_notification_run_g3)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_run_g4:', bool_switch_event_notification_run_g4)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_run_g5:', bool_switch_event_notification_run_g5)
        print('-- [ConfigCompile.read_config] bool_switch_event_notification_run_g6:', bool_switch_event_notification_run_g6)
        print('-- [ConfigCompile.config_read] str_event_notification_run_path_g1:', str_event_notification_run_path_g1)
        print('-- [ConfigCompile.config_check] str_event_notification_run_path_g2:', str_event_notification_run_path_g2)
        print('-- [ConfigCompile.config_check] str_event_notification_run_path_g3:', str_event_notification_run_path_g3)
        print('-- [ConfigCompile.config_check] str_event_notification_run_path_g4:', str_event_notification_run_path_g4)
        print('-- [ConfigCompile.config_check] str_event_notification_run_path_g5:', str_event_notification_run_path_g5)
        print('-- [ConfigCompile.config_check] str_event_notification_run_path_g6:', str_event_notification_run_path_g6)

        print('-- [ConfigCompile.read_config] sdk_color_cpu_on:', sdk_color_cpu_on)
        print('-- [ConfigCompile.read_config] timing_cpu_util:', timing_cpu_util)
        print('-- [ConfigCompile.read_config] bool_switch_startup_cpu_util:', bool_switch_startup_cpu_util)

        print('-- [ConfigCompile.read_config] sdk_color_dram_on:', sdk_color_dram_on)
        print('-- [ConfigCompile.read_config] timing_dram_util:', timing_dram_util)
        print('-- [ConfigCompile.read_config] bool_switch_startup_dram_util:', bool_switch_startup_dram_util)

        print('-- [ConfigCompile.read_config] sdk_color_vram_on:', sdk_color_vram_on)
        print('-- [ConfigCompile.read_config] timing_vram_util:', timing_vram_util)
        print('-- [ConfigCompile.read_config] devices_gpu_selected:', devices_gpu_selected)
        print('-- [ConfigCompile.read_config] bool_switch_startup_vram_util:', bool_switch_startup_vram_util)

        print('-- [ConfigCompile.read_config] sdk_color_hddwrite_on:', sdk_color_hddwrite_on)
        print('-- [ConfigCompile.read_config] timing_hdd_util:', timing_hdd_util)
        print('-- [ConfigCompile.read_config] sdk_color_hddread_on:', sdk_color_hddread_on)
        print('-- [ConfigCompile.read_config] bool_switch_startup_hdd_read_write:', bool_switch_startup_hdd_read_write)

        print('-- [ConfigCompile.read_config] bool_switch_startup_net_traffic:', bool_switch_startup_net_traffic)
        print('-- [ConfigCompile.read_config] timing_net_traffic_util:', timing_net_traffic_util)
        print('-- [ConfigCompile.read_config] devices_network_adapter_name:', devices_network_adapter_name)
        print('-- [ConfigCompile.read_config] bool_backend_valid_network_adapter_name:', bool_backend_valid_network_adapter_name)
        print('-- [ConfigCompile.read_config] bool_backend_valid_network_adapter_name:', bool_backend_valid_network_adapter_name)

        print('-- [ConfigCompile.read_config] bool_switch_startup_net_con_ms:', bool_switch_startup_net_con_ms)
        print('-- [ConfigCompile.read_config] corsairled_id_num_netcon_ms:', corsairled_id_num_netcon_ms)
        print('-- [ConfigCompile.read_config] bool_switch_startup_net_con_kb:', bool_switch_startup_net_con_kb)
        print('-- [ConfigCompile.read_config] bool_switch_startup_net_con:', bool_switch_startup_net_con)

        print('-- [ConfigCompile.read_config] bool_switch_startup_minimized:', bool_switch_startup_minimized)
        print('-- [ConfigCompile.read_config] bool_switch_startup_autorun:', bool_switch_startup_autorun)
        print('-- [ConfigCompile.read_config] bool_switch_startup_exclusive_control:', bool_switch_startup_exclusive_control)

        bool_backend_config_read_complete = True

    def run(self):
        print('-- [CompileDevicesClass.run]: plugged in')
        global bool_backend_allow_display, bool_backend_icue_connected, bool_backend_config_read_complete
        bool_backend_config_read_complete = False
        bool_backend_allow_display = False

        while True:
            # try:
            if bool_backend_config_read_complete is False:
                self.read_config()
            elif bool_backend_config_read_complete is True:
                self.attempt_connect()
                if bool_backend_allow_display is False:
                    bool_backend_allow_display = True
            else:
                print('-- [CompileDevicesClass.run] bool_backend_config_read_complete:', bool_backend_config_read_complete)
            time.sleep(1)

            # except Exception as e:
            #     print('[-- [CompileDevicesClass.run] Error:', e)
            time.sleep(3)

    def stop(self):
        print('-- [CompileDevicesClass.stop]: plugged in')
        self.stop_all_threads()
        print('-- [CompileDevicesClass.stop] terminating')
        self.terminate()


class BackLightClass(QThread):
    print('-- [BackLightClass]: plugged in')

    def __init__(self, color_all_id, btn_bck_light, btn_hotbar_on_style, btn_hotbar_off_style, visually_combine_hotbar_on_settings_window_style, visually_combine_hotbar_off_settings_window_style, btn_backlight_sub):
        QThread.__init__(self)
        self.color_all_id = color_all_id
        self.btn_bck_light = btn_bck_light
        self.btn_hotbar_on_style = btn_hotbar_on_style
        self.btn_hotbar_off_style = btn_hotbar_off_style
        self.visually_combine_hotbar_on_settings_window_style = visually_combine_hotbar_on_settings_window_style
        self.visually_combine_hotbar_off_settings_window_style = visually_combine_hotbar_off_settings_window_style
        self.btn_backlight_sub = btn_backlight_sub

    def run(self):
        print('-- [BackLightClass.run]: plugged in')
        global backlight_time_0, backlight_time_1, bool_switch_backlight, sdk_color_backlight, sdk_color_backlight_on
        global bool_switch_show_discrete, ui_feature_page

        while True:
            date_time_now = str(datetime.datetime.now())
            time_now = date_time_now.split(' ')

            time_now_str = time_now[1].replace(':', '')
            time_now_str = time_now_str[:4]
            time_now_int = int(time_now_str)

            backlight_time_0_int = int(backlight_time_0)
            backlight_time_1_int = int(backlight_time_1)

            """ Hard Coded Time Testing
            time_now_str = '0330' 
            time_now_int = int(time_now_str)
            """

            # print('-- [BackLightClass.run] target_time_0:', backlight_time_0, '   target_time_1:', backlight_time_1,'   time_now:', time_now[1], '   time_now_str:', time_now_str)

            if backlight_time_0_int < backlight_time_1_int:
                # print('-- [BackLightClass.run] auto backlight: backlight_time_0_int < backlight_time_1_int')
                if time_now_int >= backlight_time_0_int and time_now_int < backlight_time_1_int:
                    if bool_switch_backlight is False:
                        print('-- [BackLightClass.run] auto backlight: turning on')

                        bool_switch_backlight = True
                        self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
                        if bool_switch_show_discrete is False and ui_feature_page == 5:
                            self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                        self.btn_bck_light.setIcon(QIcon("./image/img_backlight_on.png"))
                        self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                        sdk_color_backlight = sdk_color_backlight_on
                        self.color_all_id()

                if time_now_int < backlight_time_0_int or time_now_int >= backlight_time_1_int:
                    if bool_switch_backlight is True:
                        print('-- [BackLightClass.run] auto backlight: turning off')

                        bool_switch_backlight = False
                        self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)
                        if bool_switch_show_discrete is False and ui_feature_page == 5:
                            self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                        self.btn_bck_light.setIcon(QIcon("./image/img_backlight_off.png"))
                        self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

                        sdk_color_backlight = (0, 0, 0)
                        self.color_all_id()

            elif backlight_time_0_int > backlight_time_1_int:
                # print('-- [BackLightClass.run] auto backlight: backlight_time_0_int > backlight_time_1_int')
                if time_now_str.startswith('0'):
                    if time_now_int <= backlight_time_0_int and time_now_int < backlight_time_1_int:
                        if bool_switch_backlight is False:
                            print('-- [BackLightClass.run] auto backlight: turning on')

                            bool_switch_backlight = True
                            self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
                            if bool_switch_show_discrete is False and ui_feature_page == 5:
                                self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                            self.btn_bck_light.setIcon(QIcon("./image/img_backlight_on.png"))
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                            sdk_color_backlight = sdk_color_backlight_on
                            self.color_all_id()
                    else:
                        if bool_switch_backlight is True:
                            print('-- [BackLightClass.run] auto backlight: turning off')

                            bool_switch_backlight = False
                            self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)
                            if bool_switch_show_discrete is False and ui_feature_page == 5:
                                self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                            self.btn_bck_light.setIcon(QIcon("./image/img_backlight_off.png"))
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

                            sdk_color_backlight = (0, 0, 0)
                            self.color_all_id()
                else:
                    if time_now_int <= backlight_time_1_int or time_now_int >= backlight_time_0_int:
                        if bool_switch_backlight is False:
                            print('-- [BackLightClass.run] auto backlight: turning on')

                            bool_switch_backlight = True
                            self.btn_bck_light.setStyleSheet(self.btn_hotbar_on_style)
                            if bool_switch_show_discrete is False and ui_feature_page == 5:
                                self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_on_settings_window_style)
                            self.btn_bck_light.setIcon(QIcon("./image/img_backlight_on.png"))
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))

                            sdk_color_backlight = sdk_color_backlight_on
                            self.color_all_id()
                    else:
                        if bool_switch_backlight is True:
                            print('-- [BackLightClass.run] auto backlight: turning off')

                            bool_switch_backlight = False
                            self.btn_bck_light.setStyleSheet(self.btn_hotbar_off_style)
                            if bool_switch_show_discrete is False and ui_feature_page == 5:
                                self.btn_bck_light.setStyleSheet(self.visually_combine_hotbar_off_settings_window_style)
                            self.btn_bck_light.setIcon(QIcon("./image/img_backlight_off.png"))
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

                            sdk_color_backlight = (0, 0, 0)
                            self.color_all_id()
            time.sleep(1)

    def stop(self):
        print('-- [BackLightClass.stop]: plugged in')
        print('-- [BackLightClass.stop] terminating')
        self.terminate()


class NetShareClass(QThread):
    print('-- [NetShareClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.def_share_bool = [False]
        self.rem_ipc_bool = False
        self.rem_admin_bool = False
        self.gen_share_bool = [False]

    def run(self):
        print('-- [NetShareClass.run]: plugged in')
        while True:
            if len(devices_kb) >= 1:
                try:
                    self.send_instruction()
                except Exception as e:
                    print('-- [NetShareClass.run] Error:', e)
                time.sleep(2)
            else:
                time.sleep(1)

    def send_instruction(self):
        # print('-- [NetShareClass.send_instruction]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_netshare, sdk_color_netshare_on, sdk_color_backlight
        cmd_output = []
        cmd = 'net share /n'
        xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = xcmd.stdout.readline()
            if output == '' and xcmd.poll() is not None:
                break
            if output:
                cmd_output.append(str(output.decode("utf-8").strip()))
            else:
                break
        rc = xcmd.poll()

        for _ in cmd_output:
            if 'Remote IPC' in _:
                self.rem_ipc_bool = True
                # print('-- [NetShareClass.send_instruction] self.rem_ipc_bool:', self.rem_ipc_bool)

            if 'Remote Admin' in _:
                self.rem_admin_bool = True
                # print('-- [NetShareClass.send_instruction] self.rem_admin_bool:', self.rem_admin_bool)

            if 'Default share' in _:
                self.def_share_bool.append(True)
                # print('-- [NetShareClass.send_instruction] self.def_share_bool:', self.def_share_bool)

            # if len(_.split('    ')) == 2:
            if len(_.split('   ')) >= 2 and not _.split()[0].endswith('$'):

                if os.path.exists(_.split()[1]):
                    self.gen_share_bool.append(True)
                elif os.path.exists(_.split('   ')[1]):
                    self.gen_share_bool.append(True)

            if 'The Server service is not started.' in cmd_output:
                self.def_share_bool = [False]
                self.rem_ipc_bool = False
                self.rem_admin_bool = False
                self.gen_share_bool = [False]

        # Default Shares
        if True in self.def_share_bool:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[2]: sdk_color_netshare_on}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)
        elif self.def_share_bool[0] is False:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[2]: sdk_color_backlight}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)

        # Remote IPC
        if self.rem_ipc_bool is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[0]: sdk_color_netshare_on}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)
        elif self.rem_ipc_bool is False:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[0]: sdk_color_backlight}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)

        # Remote Admin Share
        if self.rem_admin_bool is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[1]: sdk_color_netshare_on}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)
        elif self.rem_admin_bool is False:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[1]: sdk_color_backlight}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)

        # Other Shares
        if True in self.gen_share_bool:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[3]: sdk_color_netshare_on}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)
        elif self.gen_share_bool[0] is False:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[3]: sdk_color_backlight}))
            except Exception as e:
                print('-- [NetShareClass.send_instruction] Error:', e)

        sdk.set_led_colors_flush_buffer()

        self.def_share_bool = [False]
        self.rem_ipc_bool = False
        self.rem_admin_bool = False
        self.gen_share_bool = [False]

    def stop(self):
        print('-- [NetShareClass.stop]: plugged in')
        global sdk_color_backlight
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_netshare
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[0]: sdk_color_backlight}))
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[1]: sdk_color_backlight}))
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[2]: sdk_color_backlight}))
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[3]: sdk_color_backlight}))
        except Exception as e:
            print('-- [NetShareClass.stop] Error:', e)
        sdk.set_led_colors_flush_buffer()
        print('-- [NetShareClass.stop] terminating')
        self.terminate()


class NetworkMonClass(QThread):
    print('-- [NetworkMonClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.b_type = ()
        self.u_type = ()
        self.b_type_1 = ()
        self.u_type_1 = ()
        self.num_len_key = ()
        self.switch_num = ()
        self.switch_num_key = ()
        self.switch_num_1 = ()
        self.b_type_key = ()
        self.network_adapter_display_rcv_bool_prev = [False, False, False, False, False, False, False, False, False]
        self.network_adapter_display_snt_bool_prev = [False, False, False, False, False, False, False, False, False]
        self.network_adapter_display_rcv_bool = [False, False, False, False, False, False, False, False, False]
        self.network_adapter_display_snt_bool = [False, False, False, False, False, False, False, False, False]

        self.switch_count = 0

    def run(self):
        print('-- [NetworkMonClass.run]: plugged in')
        pythoncom.CoInitialize()
        global devices_kb, timing_net_traffic_util
        while True:
            if len(devices_kb) >= 1:
                self.send_instruction()
                time.sleep(timing_net_traffic_util)
            else:
                time.sleep(1)

    def snd_ins_netr(self):
        # print('-- [NetworkMonClass.snd_ins_netr]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        global sdk_color_net_traffic_bytes, sdk_color_net_traffic_kb, sdk_color_net_traffic_mb, sdk_color_net_traffic_gb, sdk_color_net_traffic_tb
        global corsairled_id_num_netrcv, corsairled_id_num_netsnt
        global corsairled_id_num_netrcv_utype
        global corsairled_id_num_netsnt_utype
        net_rcv_i = 0
        for _ in self.network_adapter_display_rcv_bool:
            if self.network_adapter_display_rcv_bool[net_rcv_i] is True and self.network_adapter_display_rcv_bool_prev[net_rcv_i] != self.network_adapter_display_rcv_bool[net_rcv_i]:
                self.network_adapter_display_rcv_bool_prev[net_rcv_i] = True
                self.switch_count += 1
                if self.u_type == 0:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_0}))
                elif self.u_type == 1:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_1}))
                elif self.u_type == 2:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_2}))
                elif self.u_type == 3:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_3}))
                sdk.set_led_colors_flush_buffer()
                if self.b_type == 0:
                    net_set = 0
                    while net_set < self.switch_num:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_bytes}))
                        net_set += 1
                elif self.b_type == 1:
                    net_set = 0
                    while net_set < self.switch_num:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_kb}))
                        net_set += 1
                elif self.b_type == 2:
                    net_set = 0
                    while net_set < self.switch_num:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_mb}))
                        net_set += 1
                elif self.b_type == 3:
                    net_set = 0
                    while net_set < self.switch_num:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_gb}))
                        net_set += 1
                elif self.b_type == 4:
                    net_set = 0
                    while net_set < self.switch_num:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_tb}))
                        net_set += 1
                sdk.set_led_colors_flush_buffer()
            if self.network_adapter_display_rcv_bool[net_rcv_i] is False and self.network_adapter_display_rcv_bool_prev[net_rcv_i] != self.network_adapter_display_rcv_bool[net_rcv_i]:
                self.network_adapter_display_rcv_bool_prev[net_rcv_i] = False
                self.switch_count += 1
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_rcv_i]: sdk_color_backlight}))
            if self.network_adapter_display_rcv_bool == [False, False, False, False, False, False, False, False, False]:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_backlight}))
            net_rcv_i += 1

    def snd_ins_nets(self):
        # print('-- [NetworkMonClass.snd_ins_nets]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        global sdk_color_net_traffic_bytes, sdk_color_net_traffic_kb, sdk_color_net_traffic_mb, sdk_color_net_traffic_gb, sdk_color_net_traffic_tb
        global corsairled_id_num_netrcv, corsairled_id_num_netsnt
        global corsairled_id_num_netrcv_utype
        global corsairled_id_num_netsnt_utype

        net_snd_i = 0
        for _ in self.network_adapter_display_snt_bool:
            if self.network_adapter_display_snt_bool[net_snd_i] is True and self.network_adapter_display_snt_bool_prev[net_snd_i] != self.network_adapter_display_snt_bool[net_snd_i]:
                self.network_adapter_display_snt_bool_prev[net_snd_i] = True
                self.switch_count += 1
                if self.u_type_1 == 0:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_0}))
                elif self.u_type_1 == 1:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_1}))
                elif self.u_type_1 == 2:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_2}))
                elif self.u_type_1 == 3:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_3}))
                sdk.set_led_colors_flush_buffer()
                if self.b_type_1 == 0:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_bytes}))
                        net_set += 1
                elif self.b_type_1 == 1:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_kb}))
                        net_set += 1
                elif self.b_type_1 == 2:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_mb}))
                        net_set += 1
                elif self.b_type_1 == 3:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_gb}))
                        net_set += 1
                elif self.b_type_1 == 4:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_tb}))
                        net_set += 1
                sdk.set_led_colors_flush_buffer()
            if self.network_adapter_display_snt_bool[net_snd_i] is False and self.network_adapter_display_snt_bool_prev[net_snd_i] != self.network_adapter_display_snt_bool[net_snd_i]:
                self.network_adapter_display_snt_bool_prev[net_snd_i] = False
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_snd_i]: sdk_color_backlight}))
            if self.network_adapter_display_snt_bool == [False, False, False, False, False, False, False, False, False]:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_backlight}))
            net_snd_i += 1

    def send_instruction(self):
        # print('-- [NetworkMonClass.send_instruction]: plugged in')
        self.get_stat()
        try:
            self.snd_ins_netr()
            self.snd_ins_nets()
        except Exception as e:
            print('-- [NetworkMonClass.send_instruction] Error:', e)
            sdk.set_led_colors_flush_buffer()

    def get_stat(self):
        # print('-- [NetworkMonClass.get_stat]: plugged in')
        global devices_network_adapter_name
        network_adapter_exists_bool = False
        try:
            self.network_adapter_display_rcv_bool = [False, False, False, False, False, False, False, False, False]
            self.network_adapter_display_snt_bool = [False, False, False, False, False, False, False, False, False]
            rec_item = ''
            sen_item = ''
            wmis = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            wbems = wmis.ConnectServer(".", "root\\cimv2")
            col_items = wbems.ExecQuery('SELECT * FROM Win32_PerfFormattedData_Tcpip_NetworkAdapter')
            for objItem in col_items:
                if objItem.Name != None:
                    if devices_network_adapter_name == objItem.Name:
                        rec_item = objItem.BytesReceivedPersec
                        sen_item = objItem.BytesSentPersec
                        network_adapter_exists_bool = True
            if network_adapter_exists_bool is True:
                self.b_type_key = 0
                rec_bytes = self.convert_bytes(float(rec_item))
                self.b_type_key = 1
                sen_bytes = self.convert_bytes(float(sen_item))
                rec_bytes_int = int(rec_bytes)
                sen_bytes_int = int(sen_bytes)
                self.num_len_key = 0
                self.num_len(rec_bytes_int)
                self.num_len_key = 1
                self.num_len(sen_bytes_int)
                self.switch_num_key = 0
                self.switch_num_function(rec_bytes_int)
                self.switch_num_key = 1
                self.switch_num_function(sen_bytes_int)
        except Exception as e:
            print('-- [NetworkMonClass.get_stat] Error:', e)
            sdk.set_led_colors_flush_buffer()

    def convert_bytes(self, num):
        # print('-- [NetworkMonClass.convert_bytes]: plugged in')
        i = 0
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                if self.b_type_key == 0:
                    self.b_type = i
                elif self.b_type_key == 1:
                    self.b_type_1 = i
                return num
            num /= 1024.0
            i += 1

    def switch_num_function(self, num):
        # print('-- [NetworkMonClass.switch_num_function]: plugged in')
        n = str(num)
        n = n[0]
        for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if n == x:
                if self.switch_num_key == 0:
                    self.switch_num = int(n)
                    i_rcv = 0
                    for _ in self.network_adapter_display_rcv_bool:
                        if i_rcv < int(self.switch_num):
                            self.network_adapter_display_rcv_bool[i_rcv] = True
                        i_rcv += 1
                elif self.switch_num_key == 1:
                    self.switch_num_1 = int(n)
                    i_snt = 0
                    for _ in self.network_adapter_display_snt_bool:
                        if i_snt < int(self.switch_num_1):
                            self.network_adapter_display_snt_bool[i_snt] = True
                        i_snt += 1

    def num_len(self, num):
        # print('-- [NetworkMonClass.num_len]: plugged in')
        n = len(str(num))
        if n == 1:
            if self.num_len_key == 0:
                self.u_type = 0
            elif self.num_len_key == 1:
                self.u_type_1 = 0
        elif n == 2:
            if self.num_len_key == 0:
                self.u_type = 1
            elif self.num_len_key == 1:
                self.u_type_1 = 1
        elif n == 3:
            if self.num_len_key == 0:
                self.u_type = 2
            elif self.num_len_key == 1:
                self.u_type_1 = 2
        elif n >= 4:
            if self.num_len_key == 0:
                self.u_type = 3
            elif self.num_len_key == 1:
                self.u_type_1 = 3

    def stop(self):
        print('-- [NetworkMonClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        global sdk_color_net_traffic_bytes, sdk_color_net_traffic_kb, sdk_color_net_traffic_mb, sdk_color_net_traffic_gb, sdk_color_net_traffic_tb
        global corsairled_id_num_netrcv, corsairled_id_num_netsnt
        global corsairled_id_num_netrcv_utype
        global corsairled_id_num_netsnt_utype
        try:
            net_rcv_i = 0
            for _ in corsairled_id_num_netrcv:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_rcv_i]: sdk_color_backlight}))
                net_rcv_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [NetworkMonClass.stop] Error:', e)
            pass
        try:
            net_rcv_i = 0
            for _ in corsairled_id_num_netsnt:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_rcv_i]: sdk_color_backlight}))
                net_rcv_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [NetworkMonClass.stop] Error:', e)
            pass
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_backlight}))
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_backlight}))
        except Exception as e:
            print('-- [NetworkMonClass.stop] Error:', e)
            pass
        print('-- [NetworkMonClass.stop] terminating')
        self.terminate()


class PingTestClass(QThread):
    print('-- [PingTestClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.ping_bool = False
        self.ping_bool_prev = None
        self.ping_fail_i = 0
        self.rgb_key = ()

    def run(self):
        print('-- [PingTestClass.run]: plugged in')
        global devices_kb
        while True:
            try:
                if len(devices_kb) >= 1 or len(devices_ms) >= 1:
                    self.ping_fail_i = 0
                    self.ping()
                    self.send_instruction()
                    time.sleep(5)
                else:
                    time.sleep(3)
            except Exception as e:
                print('-- [PingTestClass.stop] Error:', e)

    def send_instruction_on(self):
        # print('-- [PingTestClass.send_instruction_on]: plugged in')
        global devices_ms, bool_switch_startup_net_con_ms, corsairled_id_num_netcon_ms, corsairled_id_num_ms_complete, devices_ms_selected, devices_kb, bool_switch_startup_net_con_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_ms) >= 1 and bool_switch_startup_net_con_ms is True:
            if corsairled_id_num_netcon_ms < len(corsairled_id_num_ms_complete):
                sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: (self.rgb_key)}))
        if len(devices_kb) >= 1 and bool_switch_startup_net_con_kb is True:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({1: (self.rgb_key)}))

    def send_instruction_off(self):
        # print('-- [PingTestClass.send_instruction_off]: plugged in')
        global devices_ms, bool_switch_startup_net_con_ms, corsairled_id_num_netcon_ms, corsairled_id_num_ms_complete, devices_ms_selected, devices_kb, bool_switch_startup_net_con_kb, devices_kb_selected
        if len(devices_ms) >= 1 and bool_switch_startup_net_con_ms is True:
            if corsairled_id_num_netcon_ms < len(corsairled_id_num_ms_complete):
                sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
        if len(devices_kb) >= 1 and bool_switch_startup_net_con_kb is True:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({1: sdk_color_backlight}))

    def send_instruction(self):
        # print('-- [PingTestClass.send_instruction]: plugged in')
        global sdk, devices_ms, devices_ms_selected, corsairled_id_num_ms_complete, ping_test_key_id, corsairled_id_num_netcon_kb
        global corsairled_id_num_netcon_ms, bool_switch_startup_net_con_ms, bool_switch_startup_net_con_kb, devices_kb, devices_kb_selected
        global bool_switch_startup_net_traffic
        if self.ping_fail_i == 1:
            self.ping()
        if self.ping_fail_i == 2:
            self.ping_bool = False
            self.ping_fail_i = 0

        if self.ping_bool is True and self.ping_bool != self.ping_bool_prev:
            print('-- [PingTestClass.send_instruction] sending instruction off')
            self.rgb_key = (100, 255, 0)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            self.ping_bool_prev = True
            sdk.set_led_colors_flush_buffer()

        elif self.ping_bool is False and self.ping_bool != self.ping_bool_prev:
            print('-- [PingTestClass.send_instruction] sending instruction on')
            time.sleep(0.1)
            self.rgb_key = (255, 0, 0)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            time.sleep(0.35)
            self.send_instruction_off()
            time.sleep(0.35)
            self.send_instruction_on()
            self.ping_bool_prev = False
            sdk.set_led_colors_flush_buffer()

    def ping(self):
        # print('-- [PingTestClass.ping]: plugged in')
        self.ping_bool = False
        cmd = 'ping -n 1 -l 1 8.8.8.8'  # Google
        if self.ping_fail_i == 1:
            cmd = 'ping -n 1 -l 1 9.9.9.9'  # Quad9. The free DNS service was co-developed by the Global Cyber Alliance, IBM, and Packet Clearing House.
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdout, stderror = p.communicate()
            output = stdout.decode('UTF-8')
            lines = output.split(os.linesep)
            for _ in lines:
                if 'Packets: Sent = 1, Received = 1, Lost = 0 (0% loss)' in _ and 'Destination host unreachable' not in str(lines).strip():
                    self.ping_bool = True
                else:
                    self.ping_fail_i += 1
        except Exception as e:
            print('-- [PingTestClass.ping] Error:', e)

    def stop(self):
        print('-- [PingTestClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_ms_complete, corsairled_id_num_netcon_ms
        self.ping_bool_prev = None
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [PingTestClass.stop] Error:', e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({1: sdk_color_backlight}))
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [PingTestClass.stop] Error:', e)
            sdk.set_led_colors_flush_buffer()
        print('-- [PingTestClass.stop] terminating')
        self.terminate()


class HddMonClass(QThread):
    print('-- [HddMonClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        global corsairled_id_num_hddreadwrite
        self.i_w = int()
        self.i_r = int()
        self.b_type_key = ()
        self.bool_dwps_greater = False
        self.dwps = ()
        self.drps = ()
        self.disk_letter_complete = []
        self.i_umount = int()

    def run(self):
        print('-- [HddMonClass.run]: plugged in')
        pythoncom.CoInitialize()
        global devices_kb
        while True:
            if len(devices_kb) >= 1:
                self.get_stat()
                time.sleep(timing_hdd_util)
            else:
                time.sleep(1)

    def send_write_instruction(self):
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddwrite_on
        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_w]: sdk_color_hddwrite_on}))
        sdk.set_led_colors_flush_buffer()

    def send_read_instruction(self):
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddread_on
        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_r]: sdk_color_hddread_on}))
        sdk.set_led_colors_flush_buffer()

    def send_write_instruction_1(self):
        global bool_switch_display_disk_mount
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddwrite_on, sdk_color_backlight
        if bool_switch_display_disk_mount is True:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_w]: (0, 0, 255)}))
        else:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_w]: sdk_color_backlight}))
        sdk.set_led_colors_flush_buffer()

    def send_read_instruction_1(self):
        global bool_switch_display_disk_mount
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddread_on, sdk_color_backlight
        if bool_switch_display_disk_mount is True:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_r]: (0, 0, 255)}))
        else:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_r]: sdk_color_backlight}))
        sdk.set_led_colors_flush_buffer()

    def send_read_instruction_umounted(self):
        global bool_switch_display_disk_mount
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddread_on, sdk_color_backlight
        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_umount]: sdk_color_backlight}))
        sdk.set_led_colors_flush_buffer()

    def get_stat(self):
        # print('-- [HddMonClass.get_stat]: plugged in')
        global alpha_str, hdd_bytes_type_w, hdd_bytes_type_r, hdd_bytes_str
        try:
            self.disk_letter_complete = []
            wmis = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            wbems = wmis.ConnectServer(".", "root\\cimv2")
            col_items = wbems.ExecQuery("SELECT * FROM Win32_PerfFormattedData_PerfDisk_PhysicalDisk")
            for objItem in col_items:
                if objItem.Name is not None:
                    disk_letter_0 = objItem.Name.split()
                    if len(disk_letter_0) >= 2:
                        disk_letter_0 = disk_letter_0[1].replace(':', '')
                        self.disk_letter_complete.append(disk_letter_0)
                if objItem.DiskWriteBytesPersec is not None:
                    if objItem.DiskReadBytesPersec is not None:
                        if '_Total' not in objItem.Name:
                            if os.path.exists(str(disk_letter_0)+':/'):
                                self.dwps = int(objItem.DiskWriteBytesPersec)
                                self.drps = int(objItem.DiskReadBytesPersec)

                                """ # Uncomment to use convert_bytes function if more data required
                                if int(objItem.DiskWriteBytesPersec) > 0:
                                    self.b_type_key = 0
                                    hdd_bytes_type_w = self.convert_bytes(self.dwps)
                                    print('writes:', disk_letter_0, self.dwps, hdd_bytes_type_w, hdd_bytes_str)
                                if int(objItem.DiskReadBytesPersec) > 0:
                                    self.b_type_key = 1
                                    hdd_bytes_type_r = self.convert_bytes(self.drps)
                                    print('reads:', disk_letter_0, self.drps, hdd_bytes_type_r, hdd_bytes_str)
                                """
    
                                if self.dwps == 0 or self.drps == 0:
                                    self.i_w = 0
                                    for _ in alpha_str:
                                        if canonical_caseless(disk_letter_0) == canonical_caseless(alpha_str[self.i_w]):
                                            self.send_write_instruction_1()
                                        self.i_w += 1
    
                                if self.dwps > 0:
                                    if self.dwps >= self.drps:
                                        self.bool_dwps_greater = True
                                        self.i_w = 0
                                        for _ in alpha_str:
                                            if canonical_caseless(disk_letter_0) == canonical_caseless(alpha_str[self.i_w]):
                                                self.send_write_instruction()
                                            self.i_w += 1
    
                                elif self.drps >= 0:
                                    if self.dwps < self.drps:
                                        self.bool_dwps_greater = False
                                        self.i_r = 0
                                        for _ in alpha_str:
                                            if canonical_caseless(disk_letter_0) == canonical_caseless(alpha_str[self.i_r]):
                                                self.send_read_instruction()
                                            self.i_r += 1
            self.i_umount = 0
            for _ in alpha_str:
                if _.upper() not in self.disk_letter_complete:
                    # print(_, self.disk_letter_complete)
                    self.send_read_instruction_umounted()
                self.i_umount += 1

        except Exception as e:
            print('-- [HddMonClass.get_stat] Error:', e)
            sdk.set_led_colors_flush_buffer()

    def convert_bytes(self, num):
        global hdd_bytes_type_w, hdd_bytes_type_r, hdd_bytes_str
        # print('-- [NetworkMonClass.convert_bytes]: plugged in')
        x = ['bytes', 'KB', 'MB', 'GB', 'TB']
        i = 0
        for _ in x:
            if num < 1024.0:
                hdd_bytes_str = x[i]
                if self.b_type_key == 0:
                    hdd_bytes_type_w = x[i]
                elif self.b_type_key == 1:
                    hdd_bytes_type_r = x[i]
                return num
            num /= 1024.0
            i += 1

    def stop(self):
        print('-- [HddMonClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_hddread_on, sdk_color_hddwrite_on, sdk_color_backlight, corsairled_id_num_hddreadwrite
        try:
            hdd_i = 0
            for _ in corsairled_id_num_hddreadwrite:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[hdd_i]: sdk_color_backlight}))
                hdd_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [HddMonClass.stop] Error:', e)
            pass
        print('-- [HddMonClass.stop] terminating')
        self.terminate()


class CpuMonClass(QThread):
    print('-- [CpuMonClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.cpu_key = [True, False, False, False]
        self.cpu_key_0 = [True, False, False, False]
        self.cpu_key_1 = [True, True, False, False]
        self.cpu_key_2 = [True, True, True, False]
        self.cpu_key_3 = [True, True, True, True]
        self.cpu_key_prev = [None, None, None, None]

    def run(self):
        print('-- [CpuMonClass.run]: plugged in')
        global devices_kb, timing_cpu_util
        while True:
            if len(devices_kb) >= 1:
                self.get_stat()
                self.send_instruction()
                time.sleep(timing_cpu_util)
            else:
                time.sleep(1)

    def send_instruction(self):
        # print('-- [CpuMonClass.send_instruction]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_cpu, sdk_color_cpu_on, sdk_color_backlight
        try:
            cpu_i = 0
            for _ in corsairled_id_num_cpu:
                if self.cpu_key[cpu_i] is True:
                    # itm = [{_: sdk_color_cpu_on}]
                    # sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_cpu[cpu_i]: sdk_color_cpu_on}))
                    self.cpu_key_prev[cpu_i] = True
                elif self.cpu_key[cpu_i] is False:
                    # itm = [{_: sdk_color_backlight}]
                    # sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_cpu[cpu_i]: sdk_color_backlight}))
                    self.cpu_key_prev[cpu_i] = False
                cpu_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [CpuMonClass.send_instruction] Error:', e)

    def get_stat(self):
        # print('-- [CpuMonClass.get_stat]: plugged in')
        try:
            c = psutil.cpu_percent()
            if c < 25:
                self.cpu_key = self.cpu_key_0
            elif 25 <= c < 50:
                self.cpu_key = self.cpu_key_1
            elif 50 <= c < 75:
                self.cpu_key = self.cpu_key_2
            elif c >= 75:
                self.cpu_key = self.cpu_key_3
        except Exception as e:
            print('-- [CpuMonClass.get_stat] Error:', e)

    def stop(self):
        print('-- [CpuMonClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_cpu, sdk_color_cpu_on, sdk_color_backlight
        try:
            cpu_i = 0
            for _ in corsairled_id_num_cpu:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_cpu[cpu_i]: sdk_color_backlight}))
                cpu_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [CpuMonClass.stop] Error:', e)
            pass
        print('-- [CpuMonClass.stop] terminating')
        self.terminate()


class DramMonClass(QThread):
    print('-- [DramMonClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.dram_key = [True, False, False, False]
        self.dram_key_0 = [True, False, False, False]
        self.dram_key_1 = [True, True, False, False]
        self.dram_key_2 = [True, True, True, False]
        self.dram_key_3 = [True, True, True, True]
        self.dram_key_prev = [None, None, None, None]

    def run(self):
        print('-- [DramMonClass.run]: plugged in')
        global devices_kb, timing_dram_util
        while True:
            if len(devices_kb) >= 1:
                self.get_stat()
                self.send_instruction()
                time.sleep(timing_dram_util)
            else:
                time.sleep(1)

    def send_instruction(self):
        # print('-- [DramMonClass.send_instruction]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_dram, sdk_color_dram_on, sdk_color_backlight
        try:
            dram_i = 0
            for _ in corsairled_id_num_dram:
                if self.dram_key[dram_i] is True:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_dram[dram_i]: sdk_color_dram_on}))
                    self.dram_key_prev[dram_i] = True
                elif self.dram_key[dram_i] is False:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_dram[dram_i]: sdk_color_backlight}))
                    self.dram_key_prev[dram_i] = False
                dram_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [DramMonClass.send_instruction] Error:', e)

    def get_stat(self):
        # print('-- [DramMonClass.get_stat]: plugged in')
        try:
            d = psutil.virtual_memory().percent
            if d < 25:
                self.dram_key = self.dram_key_0
            elif 25 <= d < 50:
                self.dram_key = self.dram_key_1
            elif 50 <= d < 75:
                self.dram_key = self.dram_key_2
            elif d >= 75:
                self.dram_key = self.dram_key_3
        except Exception as e:
            print('-- [DramMonClass.get_stat] Error:', e)

    def stop(self):
        print('-- [DramMonClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_dram, sdk_color_dram_on, sdk_color_backlight
        try:
            dram_i = 0
            for _ in corsairled_id_num_dram:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_dram[dram_i]: sdk_color_backlight}))
                dram_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [DramMonClass.stop] Error:', e)
            pass
        print('-- [DramMonClass.stop] terminating')
        self.terminate()


class VramMonClass(QThread):
    print('-- [VramMonClass]: plugged in')
    def __init__(self):
        QThread.__init__(self)
        self.vram_key = [True, False, False, False]
        self.vram_key_0 = [True, False, False, False]
        self.vram_key_1 = [True, True, False, False]
        self.vram_key_2 = [True, True, True, False]
        self.vram_key_3 = [True, True, True, True]
        self.vram_key_prev = [None, None, None, None]

    def run(self):
        print('-- [VramMonClass]: plugged in')
        global devices_kb, timing_vram_util
        while True:
            if len(devices_kb) >= 1:
                self.get_stat()
                self.send_instruction()
                time.sleep(timing_vram_util)
            else:
                time.sleep(1)

    def send_instruction(self):
        # print('-- [VramMonClass.send_instruction]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_vram, sdk_color_vram_on, sdk_color_backlight
        try:
            vram_i = 0
            for _ in corsairled_id_num_vram:
                if self.vram_key[vram_i] is True:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_vram[vram_i]: sdk_color_vram_on}))
                    self.vram_key_prev[vram_i] = True
                elif self.vram_key[vram_i] is False:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_vram[vram_i]: sdk_color_backlight}))
                    self.vram_key_prev[vram_i] = False
                vram_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [VramMonClass.send_instruction] Error:', e)

    def get_stat(self):
        # print('-- [VramMonClass.get_stat]: plugged in')
        global devices_gpu_selected
        try:
            gpus = GPUtil.getGPUs()
            if len(gpus) >= 0:
                v = float(f"{gpus[devices_gpu_selected].load * 100}")
                v = float(float(v))
                v = int(v)
                if v < 25:
                    self.vram_key = self.vram_key_0
                elif 25 <= v < 50:
                    self.vram_key = self.vram_key_1
                elif 50 <= v < 75:
                    self.vram_key = self.vram_key_2
                elif v >= 75:
                    self.vram_key = self.vram_key_3
        except Exception as e:
            print('-- [VramMonClass.get_stat] Error:', e)

    def stop(self):
        print('-- [VramMonClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_vram, sdk_color_vram_on, sdk_color_backlight
        try:
            vram_i = 0
            for _ in corsairled_id_num_vram:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_vram[vram_i]: sdk_color_backlight}))
                vram_i += 1
            sdk.set_led_colors_flush_buffer()
        except Exception as e:
            print('-- [VramMonClass.stop] Error:', e)
            pass
        print('-- [VramMonClass.stop] terminating')
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
