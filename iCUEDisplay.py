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
import shutil
import distutils.dir_util
from cuesdk import CueSdk, CorsairEventId
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QCursor, QFont, QPixmap
from PyQt5.QtCore import Qt, QThread, QSize, QPoint, QCoreApplication, QTimer, QEvent, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QDesktopWidget, QLineEdit, QComboBox, QFileDialog
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
import asyncio
import winrt.windows.media.control as wmc
import keyboard
from pathlib import Path

info = subprocess.STARTUPINFO()
info.dwFlags = 1
info.wShowWindow = 0
main_pid = int()
sdk = ''

print('-- [CueSdk] searching for CueSDK in: bin\\CUESDK.x64_2017.dll')
if os.path.exists('.\\bin\\CUESDK.x64_2017.dll'):
    print('-- [CueSDK]: found')
    sdk = CueSdk(os.path.join(os.getcwd(), 'bin\\CUESDK.x64_2017.dll'))
elif not os.path.exists('.\\bin\\CUESDK.x64_2017.dll'):
    print('-- [CueSDK]: missing from iCUEDisplay bin directory')


def NFD(text):
    return unicodedata.normalize('NFD', text)


def canonical_caseless(text):
    return NFD(NFD(text).casefold())


def initialize_scaling_dpi():
    # print('-- [initialize_scaling_dpi]: initializing:')
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # print('-- [initialize_scaling_dpi]: QT_AUTO_SCREEN_SCALE_FACTOR = 1')
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        # print('-- [initialize_scaling_dpi]: AA_EnableHighDpiScaling: True')
    # elif not hasattr(Qt, 'AA_EnableHighDpiScaling'):
        # print('-- [initialize_scaling_dpi]: AA_EnableHighDpiScaling: False')
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        # print('-- [initialize_scaling_dpi]: AA_UseHighDpiPixmaps: True')
    # elif not hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        # print('-- [initialize_scaling_dpi]: AA_UseHighDpiPixmaps: False')


def initialize_priority():
    global main_pid
    priority_classes = [win32process.IDLE_PRIORITY_CLASS,
                        win32process.BELOW_NORMAL_PRIORITY_CLASS,
                        win32process.NORMAL_PRIORITY_CLASS,
                        win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                        win32process.HIGH_PRIORITY_CLASS,
                        win32process.REALTIME_PRIORITY_CLASS]
    main_pid = win32api.GetCurrentProcessId()
    print('-- [initialize_priority] main_pid:', main_pid)
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, main_pid)
    win32process.SetPriorityClass(handle, priority_classes[4])
    print('-- [initialize_priority]: settings win32process priority class:', priority_classes[4])

bool_instruction_eject = False
bool_instruction_eject_end = False
bool_instruction_mount = False
bool_instruction_mount_end = False
bool_instruction_unmount = False
bool_instruction_unmount_end = False

notification_key = 0

bool_g2_input = False
kb_event = False
avail_w = ()
avail_h = ()
ui_object_complete = []
disk_guid = []
power_plan = ['', '', '', '']
power_plan_index = 0
backlight_time_0 = ''
backlight_time_1 = ''
hdd_bytes_type_w = ''
hdd_bytes_type_r = ''
hdd_bytes_str = ''
str_path_kb_img = ''
str_path_ms_img = ''
g_key_pressed = ''
umount_alpha = ''
time_now_press = float()
bool_alpha_stage_engaged = False
bool_exclsuive_g2key_allow = True
bool_switch_g2_disks = False
bool_onpress_clause_g1 = False
bool_onpress_clause_g2 = False
bool_onpress_clause_g3 = False
bool_onpress_clause_g4 = False
bool_onpress_clause_g5 = False
bool_onpress_clause_g6 = False
bool_switch_fahrenheit = False
bool_backlight_interact = False
bool_powershell_interact = False
bool_show_overlay = False
bool_power_plan_interact = False
bool_execution_policy = True
bool_execution_policy_show = False
bool_cpu_temperature = False
bool_vram_temperature = False
bool_switch_display_disk_mount = True
bool_switch_backlight = False
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
bool_backend_install = False
bool_backend_allow_display = False
bool_backend_icue_connected = False
bool_backend_icue_connected_previous = None
bool_backend_config_read_complete = False
bool_backend_valid_network_adapter_name = False
bool_switch_startup_media_display = False
thread_windows_update_monitor = []
thread_dir_sz_monitor = []
thread_notification = []
thread_sdk_instruction = []
thread_eject = []
thread_mount = []
thread_unmount = []
thread_exclusive_gkey_event_eject = []
thread_exclusive_gkey_event_mount = []
thread_disk_guid = []
thread_exclusive_gkey_event_unmount = []
thread_gkey_pressed = []
thread_keyevents = []
thread_overlay = []
thread_test_locked = []
thread_power = []
thread_pause_loop = []
thread_media_display = []
thread_compile_devices = []
thread_disk_rw = []
thread_cpu_util = []
thread_dram_util = []
thread_vram_util = []
thread_net_traffic = []
thread_net_connection = []
thread_net_share = []
thread_sdk_event_handler = []
thread_backlight_auto = []
thread_temperatures = []
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
alpha_str = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
             'u', 'v', 'w', 'x', 'y', 'z']
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
timing_cpu_util = 1.0
timing_dram_util = 1.0
timing_vram_util = 1.0
timing_hdd_util = 0.0
timing_net_traffic_util = 0.0

if os.path.exists('./py/bin/OpenHardwareMonitorLib.dll'):
    distutils.dir_util.mkpath(os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay'))
    try:
        dll_in = './py/bin/OpenHardwareMonitorLib.dll'
        dll_out = os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay\\OpenHardwareMonitorLib.dll')
        if os.path.exists(dll_in):
            shutil.copyfile(dll_in, dll_out)
            cmd = 'powershell Unblock-File '+dll_out
            print('-- running command:', cmd)
            xcmd = subprocess.Popen(cmd, shell=True)
            if os.path.exists(dll_out):
                shutil.copyfile(dll_out, dll_in)
    except Exception as e:
        print('-- error unblocking OpenHardwareMonitorLib.dll:', e)
    try:
        dll_in = './bin/CUESDK.x64_2017.dll'
        dll_out = os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay\\CUESDK.x64_2017.dll')
        if os.path.exists(dll_in):
            shutil.copyfile(dll_in, dll_out)
            cmd = 'powershell Unblock-File '+dll_out
            print('-- running command:', cmd)
            xcmd = subprocess.Popen(cmd, shell=True)
            if os.path.exists(dll_out):
                shutil.copyfile(dll_out, dll_in)
    except Exception as e:
        print('-- error unblocking OpenHardwareMonitorLib.dll:', e)
    try:
        dll_in = './bin/CUESDK_2017.dll'
        dll_out = os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay\\CUESDK_2017.dll')
        if os.path.exists(dll_in):
            shutil.copyfile(dll_in, dll_out)
            cmd = 'powershell Unblock-File ' + dll_out
            print('-- running command:', cmd)
            xcmd = subprocess.Popen(cmd, shell=True)
            if os.path.exists(dll_out):
                shutil.copyfile(dll_out, dll_in)
    except Exception as e:
        print('-- error unblocking OpenHardwareMonitorLib.dll:', e)

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
               'sdk_color_backlight_on: 13,13,13',
               'backlight_time_0: 2200',
               'backlight_time_1: 0500',
               'bool_switch_backlight_auto: false',
               'bool_cpu_temperature: False',
               'bool_vram_temperature: False',
               'str_path_kb_img: ',
               'str_path_ms_img: ',
               'bool_switch_startup_media_display: false',
               'bool_power_plan_interact: false',
               'bool_powershell_interact: false',
               'bool_backlight_interact: false',
               'bool_switch_fahrenheit: false',
               'bool_switch_g2_disks: false']


def create_new():
    global bool_backend_install
    print('-- [create_new]: started')
    distutils.dir_util.mkpath(os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay'))
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
                os.startfile(cwd + './iCUEDisplay.lnk')
                # time.sleep(1)
                bool_backend_install = True
    app_data_path = os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay\\icue_display_py_config.dat')
    py_config_line = os.path.join(os.getcwd()+'\\py\\temp_sys.dat')
    open(app_data_path, 'w').close()
    with open(app_data_path, 'a') as fo:
        fo.writelines('PATH: '+py_config_line)
    fo.close()
    py_temp_mon_bat_line = os.path.join('"'+os.getcwd() + '\\py\\python.exe" "'+(os.getcwd()+'\\py\\temp_mon.py"'))
    print('-- updating temp_mon.bat:', py_temp_mon_bat_line)
    open('./py/temp_mon.bat', 'w').close()
    with open('./py/temp_mon.bat', 'a') as fo:
        fo.writelines(py_temp_mon_bat_line)
    fo.close()
    cwd = os.getcwd()
    path_to_bat = os.path.join('"' + cwd + '\\py\\temp_mon.bat"')
    path_for_in_vbs_1 = 'WshShell.Run chr(34) & ' + path_to_bat + ' & Chr(34), 0'
    open('./py/temp_mon.vbs', 'w').close()
    with open('./py/temp_mon.vbs', 'a') as fo:
        fo.writelines('Set WshShell = CreateObject("WScript.Shell")\n')
        fo.writelines(path_for_in_vbs_1 + '\n')
        fo.writelines('Set WshShell = Nothing\n')
    fo.close()
    # time.sleep(2)


first_load = True
obj_geo_item = []
obj_icon_geo = []
obj_icon = []
prev_multiplier_w = int(1)
prev_multiplier_h = int(1)
ui_object_font_list_s6b = []
ui_object_font_list_s7b = []
ui_object_font_list_s8b = []
ui_object_font_list_s9b = []
bool_wmi_engaged = False


class ObjEveFilter(QObject):

    def eventFilter(self, obj, event):
        global event_filter_self, avail_w, avail_h, ui_object_complete, event_filter_self, first_load, obj_geo_item, prev_multiplier_w, prev_multiplier_h
        global ui_object_font_list_s6b, ui_object_font_list_s7b, ui_object_font_list_s8b, ui_object_font_list_s9b
        global main_pid
        global obj_icon_geo, obj_icon
        obj_eve = obj, event
        # Uncomment This Line To See All Object Events
        # print('-- ObjEveFilter(QObject).eventFilter(self, obj, event):', obj_eve)
        if str(obj_eve[1]).startswith('<PyQt5.QtGui.QResizeEvent') or str(obj_eve[1]).startswith('<PyQt5.QtGui.QMoveEvent'):
            if first_load is True:
                first_load = False
                for _ in ui_object_complete:
                    obj_geo_width = _.geometry().width()
                    obj_geo_height = _.geometry().height()
                    obj_geo_pos_w = _.geometry().x()
                    obj_geo_pos_h = _.geometry().y()
                    # print('[object geometry]', _, obj_geo_width, obj_geo_height, obj_geo_pos_w, obj_geo_pos_h)
                    var = obj_geo_width, obj_geo_height, obj_geo_pos_w, obj_geo_pos_h
                    obj_geo_item.append(var)
                    try:
                        obj_icon_geo.append(_.iconSize())
                        obj_icon.append(_)
                    except:
                        pass
            # print("previous width:", avail_w)
            # print("previous height:", avail_h)
            new_avail_w = QDesktopWidget().availableGeometry().width()
            new_avail_h = QDesktopWidget().availableGeometry().height()
            # print("new width:", new_avail_w)
            # print("new height:", new_avail_h)
            multiplier_w = int()
            multiplier_h = int()
            if new_avail_w >= 1000 and new_avail_h >= 1000:
                multiplier_w = str(new_avail_w)[0]
                multiplier_h = str(new_avail_h)[0]
                multiplier_w = int(multiplier_w)
                multiplier_h = int(multiplier_h)
            elif new_avail_w < 1000 and new_avail_h < 1000:
                multiplier_w = 1
                multiplier_h = 1
            else:
                multiplier_w = 1
                multiplier_h = 1
            multiplier_w = multiplier_h
            # print('multiplier_w:', multiplier_w)
            # print('multiplier_h:', multiplier_h)

            if prev_multiplier_w != multiplier_w or prev_multiplier_h != multiplier_h or new_avail_w != avail_w or new_avail_h != avail_h:
                avail_h = new_avail_h
                avail_w = new_avail_w
                app_width = 584 * multiplier_w
                app_height = 330 * multiplier_h
                pos_w = ((QDesktopWidget().availableGeometry().width() / 2) - (app_width / 2))
                pos_h = ((QDesktopWidget().availableGeometry().height() / 2) - (app_height / 2))
                event_filter_self[0].setGeometry(int(pos_w), int(pos_h), app_width, app_height)
                i = 0
                for _ in ui_object_complete:
                    # Default Width
                    obj_w = obj_geo_item[i]
                    obj_w = obj_w[0]
                    # Default Height
                    obj_h = obj_geo_item[i]
                    obj_h = obj_h[1]
                    # Default Position Width
                    obj_pos_w = obj_geo_item[i]
                    obj_pos_w = obj_pos_w[2]
                    # Default Position Height
                    obj_pos_h = obj_geo_item[i]
                    obj_pos_h = obj_pos_h[3]
                    print('-- [ObjEveFilter.eventFilter] default geometry:', obj_w, obj_h, obj_pos_w, obj_pos_h)
                    new_obj_w = obj_w * multiplier_w
                    new_obj_h = obj_h * multiplier_h
                    new_obj_pos_w = obj_pos_w * multiplier_w
                    new_obj_pos_h = obj_pos_h * multiplier_h
                    print('-- [ObjEveFilter.eventFilter] new geometry:', new_obj_w, new_obj_h, new_obj_pos_w, new_obj_pos_h)
                    _.move(new_obj_pos_w, new_obj_pos_h)
                    _.resize(new_obj_w, new_obj_h)
                    i += 1

                i = 0
                for _ in obj_icon_geo:
                    try:
                        geo_var = str(_)
                        geo_var = geo_var.replace('PyQt5.QtCore.QSize(', '')
                        geo_var = geo_var.replace(')', '')
                        geo_var = geo_var.replace(',', '')
                        geo_var_split = geo_var.split()
                        icon_sz_w = int(geo_var_split[0])
                        icon_sz_h = int(geo_var_split[1])
                        print('-- [ObjEveFilter.eventFilter] original icon_sz_w:', icon_sz_w, '  original icon_sz_h:', icon_sz_h)
                        icon_size_w = icon_sz_w * multiplier_w
                        icon_size_h = icon_sz_h * multiplier_h
                        print('-- [ObjEveFilter.eventFilter] [multiply result] new icon_sz_w:', icon_size_w, '  new icon_sz_h:', icon_size_h)
                        obj_icon[i].setIconSize(QSize(icon_size_w, icon_size_h))
                    except Exception as e:
                        print('-- [ObjEveFilter.eventFilter] object icon size may be inapplicable:', _, e)
                    i += 1

                font_size_6b = int(6 * multiplier_h)
                font_size_7b = int(7 * multiplier_h)
                font_size_8b = int(8 * multiplier_h)
                font_size_9b = int(9 * multiplier_h)
                font_s6b = QFont("Segoe UI", (font_size_6b), QFont.Bold)
                font_s7b = QFont("Segoe UI", (font_size_7b), QFont.Bold)
                font_s8b = QFont("Segoe UI", (font_size_8b), QFont.Bold)
                font_s9b = QFont("Segoe UI", (font_size_9b), QFont.Bold)
                for _ in ui_object_font_list_s6b:
                    _.setFont(font_s6b)
                for _ in ui_object_font_list_s7b:
                    _.setFont(font_s7b)
                for _ in ui_object_font_list_s8b:
                    _.setFont(font_s8b)
                for _ in ui_object_font_list_s9b:
                    _.setFont(font_s9b)

                # ToDo -->  Geometry set Above. Finalize by displaying the new geometry automatically without user needing to click/move the app for the changes to visibly take effect

                prev_multiplier_w = multiplier_w
                prev_multiplier_h = multiplier_h
        return False


class App(QMainWindow):
    cursorMove = QtCore.pyqtSignal(object)

    def __init__(self):
        super(App, self).__init__()
        global bool_backend_install, event_filter_self, avail_w, avail_h, ui_object_complete
        global ui_object_font_list_s6b, ui_object_font_list_s7b, ui_object_font_list_s8b, ui_object_font_list_s9b
        global bool_execution_policy_show, bool_execution_policy

        avail_w = QDesktopWidget().availableGeometry().width()
        avail_h = QDesktopWidget().availableGeometry().height()
        print("-- [App.__init__] available geometry:", 'width=', avail_w, ' height=', avail_h)
        create_new()
        if bool_backend_install is True:
            sys.exit()
        initialize_scaling_dpi()
        initialize_priority()
        self.object_interaction_enabled = []
        self.object_interaction_readonly = []

        """ Used for moving the app with l.mouse button down """
        self.prev_pos = ()
        self.cursorMove.connect(self.handleCursorMove)
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.pollCursor)
        self.timer.start()
        self.cursor = None

        """ Title & Icon """
        self.setWindowIcon(QIcon('./icon.ico'))
        self.title = 'iCUE Display'
        print('-- [App.__init__] setting self.title as:', self.title)
        self.setWindowTitle(self.title)

        """ Main Window Geometry """
        self.width = 584
        self.height = 330
        self.height_discrete = 180
        self.pos_w = int(((QDesktopWidget().availableGeometry().width() / 2) - (self.width / 2)))
        self.pos_h = int(((QDesktopWidget().availableGeometry().height() / 2) - (self.height / 2)))
        print('-- [App.__init__] setting window dimensions:', self.width, self.height)
        print('-- [App.__init__] setting window position:', self.pos_w, self.pos_h)
        self.setGeometry(int(self.pos_w), int(self.pos_h), self.width, self.height)

        """ Main Window Color & Window Frame Style """
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setPalette(p)

        """ Initialize Fonts """
        self.font_s6b = QFont("Segoe UI", 6, QFont.Bold)
        self.font_s7b = QFont("Segoe UI", 7, QFont.Bold)
        self.font_s8b = QFont("Segoe UI", 8, QFont.Bold)
        self.font_s9b = QFont("Segoe UI", 9, QFont.Bold)

        """ Tooltip """
        self.tooltip_style = """QToolTip {background-color: rgb(35, 35, 35);
                           color: rgb(200, 200, 200);
                           border-top:0px solid rgb(35, 35, 35);
                           border-bottom:0px solid rgb(35, 35, 35);
                           border-right:0px solid rgb(0, 0, 0);
                           border-left:0px solid rgb(0, 0, 0);}"""
        """ Title Bar """
        self.btn_title_bar_style_0 = """QPushButton{background-color: rgb(10, 10, 10);
                                                           color: rgb(255, 255, 255);
                                                           border-bottom:2px solid rgb(5, 5, 5);
                                                           border-right:2px solid rgb(5, 5, 5);
                                                           border-top:2px solid rgb(5, 5, 5);
                                                           border-left:2px solid rgb(5, 5, 5);}"""
        self.btn_title_bar_style_1 = """QPushButton{background-color: rgb(10, 10, 10);
                                                           color: rgb(200, 200, 200);
                                                           border-bottom:2px solid rgb(5, 5, 5);
                                                           border-right:2px solid rgb(5, 5, 5);
                                                           border-top:2px solid rgb(5, 5, 5);
                                                           border-left:2px solid rgb(5, 5, 5);}"""
        """ Status """
        self.btn_status_style = """QPushButton{background-color: rgb(0, 0, 0);
                                                                   color: rgb(200, 200, 200);
                                                                   border-bottom:2px solid rgb(0, 0, 0);
                                                                   border-right:2px solid rgb(0, 0, 0);
                                                                   border-top:2px solid rgb(0, 0, 0);
                                                                   border-left:2px solid rgb(0, 0, 0);}"""
        self.btn_status_style_0 = """QPushButton{background-color: rgb(0, 0, 0);
                                   color: rgb(200, 200, 200);
                                   border-bottom:2px solid rgb(15, 15, 15);
                                   border-right:2px solid rgb(15, 15, 15);
                                   border-top:2px solid rgb(15, 15, 15);
                                   border-left:2px solid rgb(15, 15, 15);}"""
        self.lbl_status_style = """QLabel {background-color: rgb(0, 0, 0);
                           color: rgb(200, 200, 200);
                           border-top:2px solid rgb(0, 0, 0);
                           border-bottom:2px solid rgb(0, 0, 0);
                           border-right:2px solid rgb(0, 0, 0);
                           border-left:2px solid rgb(0, 0, 0);}"""
        """ Side Menu """
        self.btn_side_menu_style = """QPushButton{background-color: rgb(17, 17, 17);
                                                   color: rgb(255, 255, 255);
                                                   border-bottom:2px solid rgb(0, 0, 10);
                                                   border-right:2px solid rgb(0, 0, 10);
                                                   border-top:2px solid rgb(0, 0, 10);
                                                   border-left:2px solid rgb(0, 0, 10);}"""
        self.btn_side_menu_style_1 = """QPushButton{background-color: rgb(10, 10, 10);
                                                           color: rgb(200, 200, 200);
                                                           border-bottom:2px solid rgb(5, 5, 5);
                                                           border-right:2px solid rgb(5, 5, 5);
                                                           border-top:2px solid rgb(5, 5, 5);
                                                           border-left:2px solid rgb(0, 0, 0);}"""
        """ Menu """
        self.lbl_menu_background_style = """QLabel {background-color: rgb(0, 0, 0);
                                   color: rgb(5, 5, 5);
                                   border-top:0px solid rgb(5, 5, 5);
                                   border-bottom:0px solid rgb(5, 5, 5);
                                   border-right:0px solid rgb(5, 5, 5);
                                   border-left:0px solid rgb(5, 5, 5);}"""
        self.lbl_menu_key_style = """QLabel {background-color: rgb(0, 0, 0);
                                           color: rgb(150, 150, 150);
                                           border-top:2px solid rgb(10, 10, 10);
                                           border-bottom:2px solid rgb(10, 10, 10);
                                           border-right:2px solid rgb(10, 10, 10);
                                           border-left:2px solid rgb(10, 10, 10);}"""
        self.cmb_menu_style = """QComboBox {background-color: rgb(10, 10, 10);
                   color: rgb(200, 200, 200);
                   border-top:2px solid rgb(5, 5, 5);
                   border-bottom:2px solid rgb(5, 5, 5);
                   border-right:2px solid rgb(5, 5, 5);
                   border-left:2px solid rgb(0, 0, 0);}"""
        self.btn_menu_style = """QPushButton{background-color: rgb(10, 10, 10);
                                                           color: rgb(200, 200, 200);
                                                           border-bottom:2px solid rgb(5, 5, 5);
                                                           border-right:2px solid rgb(5, 5, 5);
                                                           border-top:2px solid rgb(5, 5, 5);
                                                           border-left:2px solid rgb(0, 0, 0);}"""
        self.btn_menu_style_1 = """QPushButton{background-color: rgb(10, 10, 10);
                                                                   color: rgb(200, 200, 200);
                                                                   border-bottom:2px solid rgb(5, 5, 5);
                                                                   border-right:2px solid rgb(5, 5, 5);
                                                                   border-top:2px solid rgb(5, 5, 5);
                                                                   border-left:2px solid rgb(0, 0, 0);}"""
        self.lbl_menu_description_style = """QLabel {background-color: rgb(15, 15, 15);
                   color: rgb(200, 200, 200);
                   border-bottom:2px solid rgb(8, 8, 8);
                   border-right:2px solid rgb(8, 8, 8);
                   border-top:2px solid rgb(8, 8, 8);
                   border-left:2px solid rgb(8, 8, 8);}"""
        self.lbl_menu_style = """QLabel{background-color: rgb(10, 10, 10);
                                                           color: rgb(200, 200, 200);
                                                           border-bottom:2px solid rgb(5, 5, 5);
                                                           border-right:2px solid rgb(5, 5, 5);
                                                           border-top:2px solid rgb(5, 5, 5);
                                                           border-left:2px solid rgb(0, 0, 0);}"""
        self.qle_menu_style = """QLineEdit{background-color: rgb(10, 10, 10);
                                                           color: rgb(200, 200, 200);
                                                           border-bottom:2px solid rgb(5, 5, 5);
                                                           border-right:2px solid rgb(5, 5, 5);
                                                           border-top:2px solid rgb(5, 5, 5);
                                                           border-left:2px solid rgb(0, 0, 0);}"""
        self.setStyleSheet(self.tooltip_style)

        """ Object Geometry """
        self.monitor_btn_h = 28
        self.monitor_btn_w = 72
        self.menu_obj_pos_w = 134
        self.tog_switch_ico_sz = QSize(40, 20)

        """ Begin Initiating Objects"""

        self.btn_title_logo = QLabel(self)
        self.btn_title_logo.move(2, 2)
        self.btn_title_logo.resize(28, 28)
        pixmap = QPixmap("./image/dev_target_20x20.png")
        self.btn_title_logo.setPixmap(pixmap)
        self.btn_title_logo.setStyleSheet(
            """QLabel{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 255, 255);}"""
        )
        print('-- [App.__init__] created:', self.btn_title_logo)
        ui_object_complete.append(self.btn_title_logo)

        self.lbl_title = QLabel(self)
        self.lbl_title.move(0, 3)
        self.lbl_title.resize(126, 20)
        self.lbl_title.setFont(self.font_s8b)
        self.lbl_title.setText('iCUE Display')
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                    color: rgb(230, 230, 230);
                    border:0px solid rgb(0, 255, 0);}""")
        print('-- [App.__init__] created:', self.lbl_title)
        ui_object_complete.append(self.lbl_title)
        ui_object_font_list_s8b.append(self.lbl_title)

        self.btn_quit = QPushButton(self)
        self.btn_quit.move((self.width - 28), 0)
        self.btn_quit.resize(28, 28)
        self.btn_quit.setIcon(QIcon("./image/img_close.png"))
        self.btn_quit.setIconSize(QSize(8, 8))
        self.btn_quit.clicked.connect(self.icuedisplay_quit_function)
        # self.btn_quit.clicked.connect(QCoreApplication.instance().quit)
        self.btn_quit.setStyleSheet(
            """QPushButton{background-color: rgb(0, 0, 0);
               border:0px solid rgb(0, 0, 0);}"""
        )
        print('-- [App.__init__] created:', self.btn_quit)
        ui_object_complete.append(self.btn_quit)

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
        ui_object_complete.append(self.btn_minimize)
        
        """ Displays connection to iCUE Service """
        self.btn_con_stat_name = QPushButton(self)
        self.btn_con_stat_name.move(31, 36)
        self.btn_con_stat_name.resize(64, 64)
        self.icon_sz = QSize(64, 64)
        self.btn_con_stat_name.setIconSize(self.icon_sz)
        self.btn_con_stat_name.setStyleSheet(self.btn_status_style)
        print('-- [App.__init__] created:', self.btn_con_stat_name)
        ui_object_complete.append(self.btn_con_stat_name)
        ui_object_font_list_s8b.append(self.btn_con_stat_name)

        self.btn_refresh_recompile = QPushButton(self)
        self.btn_refresh_recompile.move(126 + 4 + 64 + 4, 6)
        self.btn_refresh_recompile.resize(64, 28)
        self.btn_refresh_recompile.setIcon(QIcon("./image/img_refresh.png"))
        self.icon_sz = QSize(15, 15)
        self.btn_refresh_recompile.setIconSize(self.icon_sz)
        self.btn_refresh_recompile.setStyleSheet(self.btn_title_bar_style_1)
        self.btn_refresh_recompile.clicked.connect(self.recompile)
        print('-- [App.__init__] created:', self.btn_refresh_recompile)
        self.object_interaction_enabled.append(self.btn_refresh_recompile)
        ui_object_complete.append(self.btn_refresh_recompile)

        self.btn_bck_light = QPushButton(self)
        self.btn_bck_light.move(126 + 4, 6)
        self.btn_bck_light.resize(64, 28)
        self.btn_bck_light.setFont(self.font_s7b)
        self.btn_bck_light.setText('BACKLIGHT')
        self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_1)
        self.btn_bck_light.clicked.connect(self.btn_bck_light_function)
        print('-- [App.__init__] created:', self.btn_bck_light)
        self.object_interaction_enabled.append(self.btn_bck_light)
        ui_object_complete.append(self.btn_bck_light)
        ui_object_font_list_s7b.append(self.btn_bck_light)

        self.btn_feature_page_home = QPushButton(self)
        self.btn_feature_page_home.move(0, self.height - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28)
        self.btn_feature_page_home.resize(126, 28)
        self.btn_feature_page_home.setFont(self.font_s8b)
        self.btn_feature_page_home.setText('Home')
        self.btn_feature_page_home.setStyleSheet(self.btn_side_menu_style)
        self.btn_feature_page_home.clicked.connect(self.feature_pg_home)
        print('-- [App.__init__] created:', self.btn_feature_page_home)
        self.object_interaction_enabled.append(self.btn_feature_page_home)
        ui_object_complete.append(self.btn_feature_page_home)
        ui_object_font_list_s8b.append(self.btn_feature_page_home)

        self.btn_feature_page_util = QPushButton(self)
        self.btn_feature_page_util.move(0, self.height - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28)
        self.btn_feature_page_util.resize(126, 28)
        self.btn_feature_page_util.setFont(self.font_s8b)
        self.btn_feature_page_util.setText('Basic Utilization')
        self.btn_feature_page_util.setStyleSheet(self.btn_side_menu_style_1)
        self.btn_feature_page_util.clicked.connect(self.feature_pg_util)
        print('-- [App.__init__] created:', self.btn_feature_page_util)
        self.object_interaction_enabled.append(self.btn_feature_page_util)
        ui_object_complete.append(self.btn_feature_page_util)
        ui_object_font_list_s8b.append(self.btn_feature_page_util)

        self.btn_feature_page_disks = QPushButton(self)
        self.btn_feature_page_disks.move(0, self.height - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28)
        self.btn_feature_page_disks.resize(126, 28)
        self.btn_feature_page_disks.setFont(self.font_s8b)
        self.btn_feature_page_disks.setText('Disks Utilization')
        self.btn_feature_page_disks.setStyleSheet(self.btn_side_menu_style_1)
        self.btn_feature_page_disks.clicked.connect(self.btn_feature_page_disk_util)
        print('-- [App.__init__] created:', self.btn_feature_page_disks)
        self.object_interaction_enabled.append(self.btn_feature_page_disks)
        ui_object_complete.append(self.btn_feature_page_disks)
        ui_object_font_list_s8b.append(self.btn_feature_page_disks)

        self.btn_feature_page_network_traffic = QPushButton(self)
        self.btn_feature_page_network_traffic.move(0, self.height - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28)
        self.btn_feature_page_network_traffic.resize(126, 28)
        self.btn_feature_page_network_traffic.setFont(self.font_s8b)
        self.btn_feature_page_network_traffic.setText('Network Traffic')
        self.btn_feature_page_network_traffic.setStyleSheet(self.btn_side_menu_style_1)
        self.btn_feature_page_network_traffic.clicked.connect(self.btn_feature_page_network_traffic_function)
        print('-- [App.__init__] created:', self.btn_feature_page_network_traffic)
        self.object_interaction_enabled.append(self.btn_feature_page_network_traffic)
        ui_object_complete.append(self.btn_feature_page_network_traffic)
        ui_object_font_list_s8b.append(self.btn_feature_page_network_traffic)

        self.btn_feature_page_networking = QPushButton(self)
        self.btn_feature_page_networking.move(0, self.height - 4 - 28 - 4 - 28 - 4 - 28)
        self.btn_feature_page_networking.resize(126, 28)
        self.btn_feature_page_networking.setFont(self.font_s8b)
        self.btn_feature_page_networking.setText('Networking')
        self.btn_feature_page_networking.setStyleSheet(self.btn_side_menu_style_1)
        self.btn_feature_page_networking.clicked.connect(self.btn_feature_page_networking_function)
        print('-- [App.__init__] created:', self.btn_feature_page_networking)
        self.object_interaction_enabled.append(self.btn_feature_page_networking)
        ui_object_complete.append(self.btn_feature_page_networking)
        ui_object_font_list_s8b.append(self.btn_feature_page_networking)

        self.btn_feature_page_gkeys = QPushButton(self)
        self.btn_feature_page_gkeys.move(0, self.height - 4 - 28 - 4 - 28)
        self.btn_feature_page_gkeys.resize(126, 28)
        self.btn_feature_page_gkeys.setFont(self.font_s8b)
        self.btn_feature_page_gkeys.setText('G Keys')
        self.btn_feature_page_gkeys.setStyleSheet(self.btn_side_menu_style_1)
        self.btn_feature_page_gkeys.clicked.connect(self.feature_page_gkeys_function)
        print('-- [App.__init__] created:', self.btn_feature_page_gkeys)
        self.object_interaction_enabled.append(self.btn_feature_page_gkeys)
        ui_object_complete.append(self.btn_feature_page_gkeys)
        ui_object_font_list_s8b.append(self.btn_feature_page_gkeys)

        self.btn_feature_page_settings = QPushButton(self)
        self.btn_feature_page_settings.move(0, self.height - 4 - 28)
        self.btn_feature_page_settings.resize(126, 28)
        self.btn_feature_page_settings.setFont(self.font_s8b)
        self.btn_feature_page_settings.setText('Settings')
        self.btn_feature_page_settings.setStyleSheet(self.btn_side_menu_style_1)
        self.btn_feature_page_settings.clicked.connect(self.btn_feature_page_settings_function)
        print('-- [App.__init__] created:', self.btn_feature_page_settings)
        self.object_interaction_enabled.append(self.btn_feature_page_settings)
        ui_object_complete.append(self.btn_feature_page_settings)
        ui_object_font_list_s8b.append(self.btn_feature_page_settings)

        self.btn_con_stat_kb_img = QPushButton(self)
        self.btn_con_stat_kb_img.move(126 + 4, 38)
        self.btn_con_stat_kb_img.resize(64, 64)
        self.btn_con_stat_kb_img.setIcon(QIcon(""))
        self.icon_sz = QSize(64, 64)
        self.btn_con_stat_kb_img.setIconSize(self.icon_sz)
        self.btn_con_stat_kb_img.setFont(self.font_s8b)
        self.btn_con_stat_kb_img.setText('+')
        self.btn_con_stat_kb_img.setStyleSheet(self.btn_status_style_0)
        self.btn_con_stat_kb_img.clicked.connect(self.btn_con_stat_kb_img_function)
        print('-- [App.__init__] created:', self.btn_con_stat_kb_img)
        self.object_interaction_enabled.append(self.btn_con_stat_kb_img)
        ui_object_complete.append(self.btn_con_stat_kb_img)

        self.lbl_con_stat_kb = QLabel(self)
        self.lbl_con_stat_kb.move(126 + 4 + 64, 38)
        self.lbl_con_stat_kb.resize(180, 64)
        self.lbl_con_stat_kb.setFont(self.font_s8b)
        self.lbl_con_stat_kb.setText('')
        self.lbl_con_stat_kb.setStyleSheet(self.lbl_status_style)
        print('-- [App.__init__] created:', self.lbl_con_stat_kb)
        ui_object_complete.append(self.lbl_con_stat_kb)
        ui_object_font_list_s8b.append(self.lbl_con_stat_kb)

        self.btn_con_stat_ms_img = QPushButton(self)
        self.btn_con_stat_ms_img.move(126 + 4 + 36 + 180, 38)
        self.btn_con_stat_ms_img.resize(64, 64)
        self.btn_con_stat_ms_img.setIcon(QIcon(""))
        self.icon_sz = QSize(64, 64)
        self.btn_con_stat_ms_img.setIconSize(self.icon_sz)
        self.btn_con_stat_ms_img.setFont(self.font_s8b)
        self.btn_con_stat_ms_img.setText('+')
        self.btn_con_stat_ms_img.setStyleSheet(self.btn_status_style_0)
        self.btn_con_stat_ms_img.clicked.connect(self.btn_con_stat_ms_img_function)
        print('-- [App.__init__] created:', self.btn_con_stat_ms_img)
        self.object_interaction_enabled.append(self.btn_con_stat_ms_img)
        ui_object_complete.append(self.btn_con_stat_ms_img)

        self.lbl_con_stat_mouse = QLabel(self)
        self.lbl_con_stat_mouse.move(126 + 4 + 64 + 180 + 36, 38)
        self.lbl_con_stat_mouse.resize(150, 64)
        self.lbl_con_stat_mouse.setFont(self.font_s8b)
        self.lbl_con_stat_mouse.setText('')
        self.lbl_con_stat_mouse.setStyleSheet(self.lbl_status_style)
        print('-- [App.__init__] created:', self.lbl_con_stat_mouse)
        ui_object_complete.append(self.lbl_con_stat_mouse)
        ui_object_font_list_s8b.append(self.lbl_con_stat_mouse)

        self.lbl_settings_bg = QLabel(self)
        self.lbl_settings_bg.move(130, self.height - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28 - 4 - 28)
        self.lbl_settings_bg.resize(426, self.height - 68)
        self.lbl_settings_bg.setStyleSheet(self.lbl_menu_background_style)
        print('-- [App.__init__] created:', self.lbl_settings_bg)
        ui_object_complete.append(self.lbl_settings_bg)
        ui_object_font_list_s8b.append(self.lbl_settings_bg)

        self.lbl_cpu_mon = QPushButton(self)
        self.lbl_cpu_mon.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_cpu_mon.resize(100, self.monitor_btn_h)
        self.lbl_cpu_mon.setFont(self.font_s8b)
        self.lbl_cpu_mon.setText('CPU Monitor')
        self.lbl_cpu_mon.setStyleSheet(self.btn_menu_style)
        self.lbl_cpu_mon.clicked.connect(self.btn_cpu_mon_function)
        print('-- [App.__init__] created:', self.lbl_cpu_mon)
        ui_object_complete.append(self.lbl_cpu_mon)
        ui_object_font_list_s8b.append(self.lbl_cpu_mon)

        self.btn_cpu_mon = QPushButton(self)
        self.btn_cpu_mon.move(self.menu_obj_pos_w + 2 + 100 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_cpu_mon.resize(28, 28)
        self.btn_cpu_mon.setStyleSheet(self.btn_menu_style)
        self.btn_cpu_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_cpu_mon.clicked.connect(self.btn_cpu_mon_function)
        print('-- [App.__init__] created:', self.btn_cpu_mon)
        self.object_interaction_enabled.append(self.btn_cpu_mon)
        ui_object_complete.append(self.btn_cpu_mon)

        self.qle_cpu_mon_rgb_on = QLineEdit(self)
        self.qle_cpu_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_cpu_mon_rgb_on.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.qle_cpu_mon_rgb_on.setFont(self.font_s8b)
        self.qle_cpu_mon_rgb_on.returnPressed.connect(self.btn_cpu_mon_rgb_on_function)
        self.qle_cpu_mon_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_cpu_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_cpu_mon_rgb_on)
        self.object_interaction_readonly.append(self.qle_cpu_mon_rgb_on)
        ui_object_complete.append(self.qle_cpu_mon_rgb_on)
        ui_object_font_list_s8b.append(self.qle_cpu_mon_rgb_on)

        self.qle_cpu_led_time_on = QLineEdit(self)
        self.qle_cpu_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_cpu_led_time_on.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.qle_cpu_led_time_on.setFont(self.font_s8b)
        self.qle_cpu_led_time_on.returnPressed.connect(self.btn_cpu_led_time_on_function)
        self.qle_cpu_led_time_on.setStyleSheet(self.qle_menu_style)
        self.qle_cpu_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_cpu_led_time_on)
        self.object_interaction_readonly.append(self.qle_cpu_led_time_on)
        ui_object_complete.append(self.qle_cpu_led_time_on)
        ui_object_font_list_s8b.append(self.qle_cpu_led_time_on)

        """ blue"""
        self.lbl_util_key_1 = QLabel(self)
        self.lbl_util_key_1.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_util_key_1.resize(10, 10)
        self.lbl_util_key_1.setStyleSheet("""QLabel {background-color: rgb(0, 0, 255);
                                                   color: rgb(150, 150, 150);
                                                   border-top:2px solid rgb(10, 10, 10);
                                                   border-bottom:2px solid rgb(10, 10, 10);
                                                   border-right:2px solid rgb(10, 10, 10);
                                                   border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_1)
        ui_object_complete.append(self.lbl_util_key_1)

        self.lbl_util_key_2 = QLabel(self)
        self.lbl_util_key_2.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 10 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_util_key_2.resize(self.monitor_btn_w, 10)
        self.lbl_util_key_2.setFont(self.font_s7b)
        self.lbl_util_key_2.setText('<30°C')
        self.lbl_util_key_2.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                   color: rgb(150, 150, 150);
                                                   border-top:0px solid rgb(10, 10, 10);
                                                   border-bottom:0px solid rgb(10, 10, 10);
                                                   border-right:0px solid rgb(10, 10, 10);
                                                   border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_2)
        ui_object_complete.append(self.lbl_util_key_2)
        ui_object_font_list_s7b.append(self.lbl_util_key_2)

        """ yellow """
        self.lbl_util_key_3 = QLabel(self)
        self.lbl_util_key_3.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 20 - 4)
        self.lbl_util_key_3.resize(10, 10)
        self.lbl_util_key_3.setStyleSheet("""QLabel {background-color: rgb(255, 255, 0);
                                                           color: rgb(150, 150, 150);
                                                           border-top:2px solid rgb(10, 10, 10);
                                                           border-bottom:2px solid rgb(10, 10, 10);
                                                           border-right:2px solid rgb(10, 10, 10);
                                                           border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_3)
        ui_object_complete.append(self.lbl_util_key_3)

        self.lbl_util_key_4 = QLabel(self)
        self.lbl_util_key_4.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 10 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 20 - 4)
        self.lbl_util_key_4.resize(self.monitor_btn_w, 10)
        self.lbl_util_key_4.setFont(self.font_s7b)
        self.lbl_util_key_4.setText('>=30°C  <50°C')
        self.lbl_util_key_4.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                           color: rgb(150, 150, 150);
                                                           border-top:0px solid rgb(10, 10, 10);
                                                           border-bottom:0px solid rgb(10, 10, 10);
                                                           border-right:0px solid rgb(10, 10, 10);
                                                           border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_4)
        ui_object_complete.append(self.lbl_util_key_4)
        ui_object_font_list_s7b.append(self.lbl_util_key_4)

        """ amber """
        self.lbl_util_key_5 = QLabel(self)
        self.lbl_util_key_5.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 30 - 8)
        self.lbl_util_key_5.resize(10, 10)
        self.lbl_util_key_5.setStyleSheet("""QLabel {background-color: rgb(255, 100, 0);
                                                                   color: rgb(150, 150, 150);
                                                                   border-top:2px solid rgb(10, 10, 10);
                                                                   border-bottom:2px solid rgb(10, 10, 10);
                                                                   border-right:2px solid rgb(10, 10, 10);
                                                                   border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_5)
        ui_object_complete.append(self.lbl_util_key_5)

        self.lbl_util_key_6 = QLabel(self)
        self.lbl_util_key_6.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 10 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 30 - 8)
        self.lbl_util_key_6.resize(self.monitor_btn_w, 10)
        self.lbl_util_key_6.setFont(self.font_s7b)
        self.lbl_util_key_6.setText('>=50°C  <70°C')
        self.lbl_util_key_6.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                                   color: rgb(150, 150, 150);
                                                                   border-top:0px solid rgb(10, 10, 10);
                                                                   border-bottom:0px solid rgb(10, 10, 10);
                                                                   border-right:0px solid rgb(10, 10, 10);
                                                                   border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_6)
        ui_object_complete.append(self.lbl_util_key_6)
        ui_object_font_list_s7b.append(self.lbl_util_key_6)

        """ red """
        self.lbl_util_key_7 = QLabel(self)
        self.lbl_util_key_7.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 40 - 12)
        self.lbl_util_key_7.resize(10, 10)
        self.lbl_util_key_7.setStyleSheet("""QLabel {background-color: rgb(255, 0, 0);
                                                                           color: rgb(150, 150, 150);
                                                                           border-top:2px solid rgb(10, 10, 10);
                                                                           border-bottom:2px solid rgb(10, 10, 10);
                                                                           border-right:2px solid rgb(10, 10, 10);
                                                                           border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_7)
        ui_object_complete.append(self.lbl_util_key_7)

        self.lbl_util_key_8 = QLabel(self)
        self.lbl_util_key_8.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 10 + 4 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 40 - 12)
        self.lbl_util_key_8.resize(self.monitor_btn_w, 10)
        self.lbl_util_key_8.setFont(self.font_s7b)
        self.lbl_util_key_8.setText('>70°C')
        self.lbl_util_key_8.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                                           color: rgb(150, 150, 150);
                                                                           border-top:0px solid rgb(10, 10, 10);
                                                                           border-bottom:0px solid rgb(10, 10, 10);
                                                                           border-right:0px solid rgb(10, 10, 10);
                                                                           border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_util_key_8)
        ui_object_complete.append(self.lbl_util_key_8)
        ui_object_font_list_s7b.append(self.lbl_util_key_8)

        self.lbl_cpu_mon_temp = QPushButton(self)
        self.lbl_cpu_mon_temp.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_cpu_mon_temp.resize(100, self.monitor_btn_h)
        self.lbl_cpu_mon_temp.setFont(self.font_s8b)
        self.lbl_cpu_mon_temp.setText('Temperature')
        self.lbl_cpu_mon_temp.setStyleSheet(self.btn_menu_style)
        self.lbl_cpu_mon_temp.clicked.connect(self.btn_cpu_mon_temp_function)
        print('-- [App.__init__] created:', self.lbl_cpu_mon_temp)
        ui_object_complete.append(self.lbl_cpu_mon_temp)
        ui_object_font_list_s8b.append(self.lbl_cpu_mon_temp)
        self.lbl_cpu_mon_temp.setToolTip('CPU Temperature\n\nEnable/Disable CPU Temperature Monitor')

        self.btn_cpu_mon_temp = QPushButton(self)
        self.btn_cpu_mon_temp.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 100 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_cpu_mon_temp.resize(28, 28)
        self.btn_cpu_mon_temp.setStyleSheet(self.btn_menu_style)
        self.btn_cpu_mon_temp.setIconSize(self.tog_switch_ico_sz)
        self.btn_cpu_mon_temp.clicked.connect(self.btn_cpu_mon_temp_function)
        print('-- [App.__init__] created:', self.btn_cpu_mon_temp)
        self.object_interaction_enabled.append(self.btn_cpu_mon_temp)
        ui_object_complete.append(self.btn_cpu_mon_temp)
        self.btn_cpu_mon_temp.setToolTip('CPU Temperature\n\nEnable/Disable CPU Temperature Monitor')

        self.lbl_dram_mon = QPushButton(self)
        self.lbl_dram_mon.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_dram_mon.resize(100, self.monitor_btn_h)
        self.lbl_dram_mon.setFont(self.font_s8b)
        self.lbl_dram_mon.setText('DRAM Monitor')
        self.lbl_dram_mon.setStyleSheet(self.btn_menu_style)
        self.lbl_dram_mon.clicked.connect(self.btn_dram_mon_function)
        print('-- [App.__init__] created:', self.lbl_dram_mon)
        ui_object_complete.append(self.lbl_dram_mon)
        ui_object_font_list_s8b.append(self.lbl_dram_mon)

        self.btn_dram_mon = QPushButton(self)
        self.btn_dram_mon.move(self.menu_obj_pos_w + 2 + 100 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_dram_mon.resize(28, 28)
        self.btn_dram_mon.setStyleSheet(self.btn_menu_style)
        self.btn_dram_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_dram_mon.clicked.connect(self.btn_dram_mon_function)
        print('-- [App.__init__] created:', self.btn_dram_mon)
        self.object_interaction_enabled.append(self.btn_dram_mon)
        ui_object_complete.append(self.btn_dram_mon)

        self.qle_dram_mon_rgb_on = QLineEdit(self)
        self.qle_dram_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_dram_mon_rgb_on.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.qle_dram_mon_rgb_on.setFont(self.font_s8b)
        self.qle_dram_mon_rgb_on.returnPressed.connect(self.btn_dram_mon_rgb_on_function)
        self.qle_dram_mon_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_dram_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_dram_mon_rgb_on)
        self.object_interaction_readonly.append(self.qle_dram_mon_rgb_on)
        ui_object_complete.append(self.qle_dram_mon_rgb_on)
        ui_object_font_list_s8b.append(self.qle_dram_mon_rgb_on)

        self.qle_dram_led_time_on = QLineEdit(self)
        self.qle_dram_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_dram_led_time_on.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.qle_dram_led_time_on.setFont(self.font_s8b)
        self.qle_dram_led_time_on.returnPressed.connect(self.btn_dram_led_time_on_function)
        self.qle_dram_led_time_on.setStyleSheet(self.qle_menu_style)
        self.qle_dram_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_dram_led_time_on)
        self.object_interaction_readonly.append(self.qle_dram_led_time_on)
        ui_object_complete.append(self.qle_dram_led_time_on)
        ui_object_font_list_s8b.append(self.qle_dram_led_time_on)

        self.lbl_vram_mon = QPushButton(self)
        self.lbl_vram_mon.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h)
        self.lbl_vram_mon.resize(100, self.monitor_btn_h)
        self.lbl_vram_mon.setFont(self.font_s8b)
        self.lbl_vram_mon.setText('GPU Monitor')
        self.lbl_vram_mon.setStyleSheet(self.btn_menu_style)
        self.lbl_vram_mon.clicked.connect(self.btn_vram_mon_function)
        print('-- [App.__init__] created:', self.lbl_vram_mon)
        ui_object_complete.append(self.lbl_vram_mon)
        ui_object_font_list_s8b.append(self.lbl_vram_mon)

        self.btn_vram_mon = QPushButton(self)
        self.btn_vram_mon.move(self.menu_obj_pos_w + 2 + 100 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_vram_mon.resize(28, 28)
        self.btn_vram_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_vram_mon.setStyleSheet(self.btn_menu_style)
        self.btn_vram_mon.clicked.connect(self.btn_vram_mon_function)
        print('-- [App.__init__] created:', self.btn_vram_mon)
        self.object_interaction_enabled.append(self.btn_vram_mon)
        ui_object_complete.append(self.btn_vram_mon)

        self.qle_vram_mon_rgb_on = QLineEdit(self)
        self.qle_vram_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_vram_mon_rgb_on.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_vram_mon_rgb_on.setFont(self.font_s8b)
        self.qle_vram_mon_rgb_on.returnPressed.connect(self.btn_vram_mon_rgb_on_function)
        self.qle_vram_mon_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_vram_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_vram_mon_rgb_on)
        self.object_interaction_readonly.append(self.qle_vram_mon_rgb_on)
        ui_object_complete.append(self.qle_vram_mon_rgb_on)
        ui_object_font_list_s8b.append(self.qle_vram_mon_rgb_on)

        self.qle_vram_led_time_on = QLineEdit(self)
        self.qle_vram_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_vram_led_time_on.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_vram_led_time_on.setFont(self.font_s8b)
        self.qle_vram_led_time_on.returnPressed.connect(self.btn_vram_led_time_on_function)
        self.qle_vram_led_time_on.setStyleSheet(self.qle_menu_style)
        self.qle_vram_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_vram_led_time_on)
        self.object_interaction_readonly.append(self.qle_vram_led_time_on)
        ui_object_complete.append(self.qle_vram_led_time_on)
        ui_object_font_list_s8b.append(self.qle_vram_led_time_on)

        self.lbl_vram_mon_temp = QPushButton(self)
        self.lbl_vram_mon_temp.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4, self.height - 4 - self.monitor_btn_h)
        self.lbl_vram_mon_temp.resize(100, self.monitor_btn_h)
        self.lbl_vram_mon_temp.setFont(self.font_s8b)
        self.lbl_vram_mon_temp.setText('Temperature')
        self.lbl_vram_mon_temp.setStyleSheet(self.btn_menu_style)
        self.lbl_vram_mon_temp.clicked.connect(self.btn_vram_mon_temp_function)
        print('-- [App.__init__] created:', self.lbl_vram_mon_temp)
        ui_object_complete.append(self.lbl_vram_mon_temp)
        ui_object_font_list_s8b.append(self.lbl_vram_mon_temp)
        self.lbl_vram_mon_temp.setToolTip('GPU Temperature\n\nEnables/Disables GPU Temperature Monitor.')

        self.btn_vram_mon_temp = QPushButton(self)
        self.btn_vram_mon_temp.move(self.menu_obj_pos_w + 2 + 100 + 4 + 28 + 4 + 72 + 4 + 24 + 4 + 100 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_vram_mon_temp.resize(28, 28)
        self.btn_vram_mon_temp.setStyleSheet(self.btn_menu_style)
        self.btn_vram_mon_temp.setIconSize(self.tog_switch_ico_sz)
        self.btn_vram_mon_temp.clicked.connect(self.btn_vram_mon_temp_function)
        print('-- [App.__init__] created:', self.btn_vram_mon_temp)
        self.object_interaction_enabled.append(self.btn_vram_mon_temp)
        ui_object_complete.append(self.btn_vram_mon_temp)
        ui_object_font_list_s8b.append(self.btn_vram_mon_temp)
        self.btn_vram_mon_temp.setToolTip('GPU Temperature\n\nEnables/Disables GPU Temperature Monitor.')

        """ blue"""
        self.lbl_disk_key_2 = QLabel(self)
        self.lbl_disk_key_2.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_disk_key_2.resize(10, 10)
        self.lbl_disk_key_2.setStyleSheet("""QLabel {background-color: rgb(0, 0, 255);
                                                           color: rgb(150, 150, 150);
                                                           border-top:2px solid rgb(10, 10, 10);
                                                           border-bottom:2px solid rgb(10, 10, 10);
                                                           border-right:2px solid rgb(10, 10, 10);
                                                           border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_disk_key_2)
        ui_object_complete.append(self.lbl_disk_key_2)

        self.lbl_disk_key_3 = QLabel(self)
        self.lbl_disk_key_3.move(self.menu_obj_pos_w + 2 + 4 + 10, self.height - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_disk_key_3.resize(self.monitor_btn_w * 2, 10)
        self.lbl_disk_key_3.setFont(self.font_s7b)
        self.lbl_disk_key_3.setText('Mounted Drive Letters')
        self.lbl_disk_key_3.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                           color: rgb(150, 150, 150);
                                                           border-top:0px solid rgb(10, 10, 10);
                                                           border-bottom:0px solid rgb(10, 10, 10);
                                                           border-right:0px solid rgb(10, 10, 10);
                                                           border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_disk_key_3)
        ui_object_complete.append(self.lbl_disk_key_3)
        ui_object_font_list_s7b.append(self.lbl_disk_key_3)

        self.lbl_hdd_mon_sub = QPushButton(self)
        self.lbl_hdd_mon_sub.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h)
        self.lbl_hdd_mon_sub.resize(88, 28)
        self.lbl_hdd_mon_sub.setFont(self.font_s8b)
        self.lbl_hdd_mon_sub.setText('Disk Monitor')
        self.lbl_hdd_mon_sub.setStyleSheet(self.btn_menu_style)
        self.lbl_hdd_mon_sub.clicked.connect(self.btn_hdd_mon_function)
        print('-- [App.__init__] created:', self.lbl_hdd_mon_sub)
        ui_object_complete.append(self.lbl_hdd_mon_sub)
        ui_object_font_list_s8b.append(self.lbl_hdd_mon_sub)
        self.lbl_hdd_mon_sub.setToolTip('Disk Monitor\n\nEnables/Disables Disk Monitor.\n\nDisk Monitor displays mounted drives that have an assigned disk letter, disk reads & disk writes.\nThis information is displayed on the alpha area of the keyboard')

        self.btn_hdd_mon = QPushButton(self)
        self.btn_hdd_mon.move(self.menu_obj_pos_w + 2 + 88 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_hdd_mon.resize(28, 28)
        self.btn_hdd_mon.setStyleSheet(self.btn_menu_style)
        self.btn_hdd_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_hdd_mon.clicked.connect(self.btn_hdd_mon_function)
        print('-- [App.__init__] created:', self.btn_hdd_mon)
        self.object_interaction_enabled.append(self.btn_hdd_mon)
        ui_object_complete.append(self.btn_hdd_mon)
        self.btn_hdd_mon.setToolTip('Disk Monitor\n\nEnables/Disables Disk Monitor.')

        self.lbl_hdd_write_mon = QLabel(self)
        self.lbl_hdd_write_mon.move(self.menu_obj_pos_w + 2 + 88 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.lbl_hdd_write_mon.resize(52, self.monitor_btn_h)
        self.lbl_hdd_write_mon.setFont(self.font_s8b)
        self.lbl_hdd_write_mon.setText('Writes')
        self.lbl_hdd_write_mon.setStyleSheet(self.lbl_menu_style)
        print('-- [App.__init__] created:', self.lbl_hdd_write_mon)
        ui_object_complete.append(self.lbl_hdd_write_mon)
        ui_object_font_list_s8b.append(self.lbl_hdd_write_mon)

        self.qle_hdd_mon_rgb_on = QLineEdit(self)
        self.qle_hdd_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_hdd_mon_rgb_on.move(self.menu_obj_pos_w + 2 + 88 + 4 + 52 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_hdd_mon_rgb_on.setFont(self.font_s8b)
        self.qle_hdd_mon_rgb_on.returnPressed.connect(self.btn_hdd_mon_rgb_on_function)
        self.qle_hdd_mon_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_hdd_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_hdd_mon_rgb_on)
        self.object_interaction_readonly.append(self.qle_hdd_mon_rgb_on)
        ui_object_complete.append(self.qle_hdd_mon_rgb_on)
        ui_object_font_list_s8b.append(self.qle_hdd_mon_rgb_on)

        self.lbl_hdd_read_mon = QLabel(self)
        self.lbl_hdd_read_mon.move(self.menu_obj_pos_w + 2 + 88 + 4 + 52 + 4 + 28 + 4 + self.monitor_btn_w + 4, self.height - 4 - self.monitor_btn_h)
        self.lbl_hdd_read_mon.resize(52, self.monitor_btn_h)
        self.lbl_hdd_read_mon.setFont(self.font_s8b)
        self.lbl_hdd_read_mon.setText('Reads')
        self.lbl_hdd_read_mon.setStyleSheet(self.lbl_menu_style)
        print('-- [App.__init__] created:', self.lbl_hdd_read_mon)
        ui_object_complete.append(self.lbl_hdd_read_mon)
        ui_object_font_list_s8b.append(self.lbl_hdd_read_mon)

        self.qle_hdd_read_mon_rgb_on = QLineEdit(self)
        self.qle_hdd_read_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_hdd_read_mon_rgb_on.move(self.menu_obj_pos_w + 2 + 88 + 4 + 52 + 4 + 28 + 4 + self.monitor_btn_w + 4 + 52 + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_hdd_read_mon_rgb_on.setFont(self.font_s8b)
        self.qle_hdd_read_mon_rgb_on.returnPressed.connect(self.btn_hdd_read_mon_rgb_on_function)
        self.qle_hdd_read_mon_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_hdd_read_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_hdd_read_mon_rgb_on)
        self.object_interaction_readonly.append(self.qle_hdd_read_mon_rgb_on)
        ui_object_complete.append(self.qle_hdd_read_mon_rgb_on)
        ui_object_font_list_s8b.append(self.qle_hdd_read_mon_rgb_on)

        self.qle_hdd_led_time_on = QLineEdit(self)
        self.qle_hdd_led_time_on.resize(24, self.monitor_btn_h)
        self.qle_hdd_led_time_on.move(self.menu_obj_pos_w + 2 + 88 + 4 + 52 + 4 + 28 + 4 + self.monitor_btn_w + 4 + 52 + 4 + self.monitor_btn_w + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_hdd_led_time_on.setFont(self.font_s8b)
        self.qle_hdd_led_time_on.returnPressed.connect(self.btn_hdd_led_time_on_function)
        self.qle_hdd_led_time_on.setStyleSheet(self.qle_menu_style)
        self.qle_hdd_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_hdd_led_time_on)
        self.object_interaction_readonly.append(self.qle_hdd_led_time_on)
        ui_object_complete.append(self.qle_hdd_led_time_on)
        ui_object_font_list_s8b.append(self.qle_hdd_led_time_on)

        """ TB """
        self.lbl_nettraffic_key_0 = QLabel(self)
        self.lbl_nettraffic_key_0.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_nettraffic_key_0.resize(10, 10)
        self.lbl_nettraffic_key_0.setStyleSheet("""QLabel {background-color: rgb(255, 255, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_0)
        ui_object_complete.append(self.lbl_nettraffic_key_0)

        self.lbl_nettraffic_key_1 = QLabel(self)
        self.lbl_nettraffic_key_1.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_nettraffic_key_1.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_1.setFont(self.font_s7b)
        self.lbl_nettraffic_key_1.setText('TB')
        self.lbl_nettraffic_key_1.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_1)
        ui_object_complete.append(self.lbl_nettraffic_key_1)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_1)

        """ GB """
        self.lbl_nettraffic_key_2 = QLabel(self)
        self.lbl_nettraffic_key_2.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_nettraffic_key_2.resize(10, 10)
        self.lbl_nettraffic_key_2.setStyleSheet("""QLabel {background-color: rgb(0, 255, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_2)
        ui_object_complete.append(self.lbl_nettraffic_key_2)

        self.lbl_nettraffic_key_3 = QLabel(self)
        self.lbl_nettraffic_key_3.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_nettraffic_key_3.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_3.setFont(self.font_s7b)
        self.lbl_nettraffic_key_3.setText('GB')
        self.lbl_nettraffic_key_3.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_3)
        ui_object_complete.append(self.lbl_nettraffic_key_3)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_3)

        """ MB """
        self.lbl_nettraffic_key_4 = QLabel(self)
        self.lbl_nettraffic_key_4.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_4.resize(10, 10)
        self.lbl_nettraffic_key_4.setStyleSheet("""QLabel {background-color: rgb(0, 0, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_4)
        ui_object_complete.append(self.lbl_nettraffic_key_4)

        self.lbl_nettraffic_key_5 = QLabel(self)
        self.lbl_nettraffic_key_5.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_5.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_5.setFont(self.font_s7b)
        self.lbl_nettraffic_key_5.setText('MB')
        self.lbl_nettraffic_key_5.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_5)
        ui_object_complete.append(self.lbl_nettraffic_key_5)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_5)

        """ KB """
        self.lbl_nettraffic_key_6 = QLabel(self)
        self.lbl_nettraffic_key_6.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_6.resize(10, 10)
        self.lbl_nettraffic_key_6.setStyleSheet("""QLabel {background-color: rgb(0, 255, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_6)
        ui_object_complete.append(self.lbl_nettraffic_key_6)

        self.lbl_nettraffic_key_7 = QLabel(self)
        self.lbl_nettraffic_key_7.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_7.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_7.setFont(self.font_s7b)
        self.lbl_nettraffic_key_7.setText('KB')
        self.lbl_nettraffic_key_7.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_7)
        ui_object_complete.append(self.lbl_nettraffic_key_7)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_7)

        """ Bytes """
        self.lbl_nettraffic_key_8 = QLabel(self)
        self.lbl_nettraffic_key_8.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_8.resize(10, 10)
        self.lbl_nettraffic_key_8.setStyleSheet("""QLabel {background-color: rgb(255, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_8)
        ui_object_complete.append(self.lbl_nettraffic_key_8)

        self.lbl_nettraffic_key_9 = QLabel(self)
        self.lbl_nettraffic_key_9.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_9.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_9.setFont(self.font_s7b)
        self.lbl_nettraffic_key_9.setText('Bytes')
        self.lbl_nettraffic_key_9.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_9)
        ui_object_complete.append(self.lbl_nettraffic_key_9)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_9)

        self.lbl_nettraffic_key_20 = QLabel(self)
        self.lbl_nettraffic_key_20.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10- 4 - 10)
        self.lbl_nettraffic_key_20.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_20.setFont(self.font_s7b)
        self.lbl_nettraffic_key_20.setText('Received [1] - [9]')
        self.lbl_nettraffic_key_20.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_20)
        ui_object_complete.append(self.lbl_nettraffic_key_20)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_20)

        self.lbl_nettraffic_key_22 = QLabel(self)
        self.lbl_nettraffic_key_22.move(self.menu_obj_pos_w + 2 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10- 4 - 10)
        self.lbl_nettraffic_key_22.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_22.setFont(self.font_s7b)
        self.lbl_nettraffic_key_22.setText('Sent [F1] - [F9]')
        self.lbl_nettraffic_key_22.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_22)
        ui_object_complete.append(self.lbl_nettraffic_key_22)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_22)

        """ Thousand + """
        self.lbl_nettraffic_key_11 = QLabel(self)
        self.lbl_nettraffic_key_11.move(self.menu_obj_pos_w + 2 + 4 + 72 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_nettraffic_key_11.resize(10, 10)
        self.lbl_nettraffic_key_11.setStyleSheet("""QLabel {background-color: rgb(255, 255, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_11)
        ui_object_complete.append(self.lbl_nettraffic_key_11)

        self.lbl_nettraffic_key_12 = QLabel(self)
        self.lbl_nettraffic_key_12.move(self.menu_obj_pos_w + 2 + 4 + 72 + 4 + 10 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_nettraffic_key_12.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_12.setFont(self.font_s7b)
        self.lbl_nettraffic_key_12.setText('Thousand+')
        self.lbl_nettraffic_key_12.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_12)
        ui_object_complete.append(self.lbl_nettraffic_key_12)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_12)

        """ Hundreds """
        self.lbl_nettraffic_key_13 = QLabel(self)
        self.lbl_nettraffic_key_13.move(self.menu_obj_pos_w + 2 + 4 + 72 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_13.resize(10, 10)
        self.lbl_nettraffic_key_13.setStyleSheet("""QLabel {background-color: rgb(0, 255, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_13)
        ui_object_complete.append(self.lbl_nettraffic_key_13)

        self.lbl_nettraffic_key_14 = QLabel(self)
        self.lbl_nettraffic_key_14.move(self.menu_obj_pos_w + 2 + 4 + 72 + 4 + 10 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_14.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_14.setFont(self.font_s7b)
        self.lbl_nettraffic_key_14.setText('Hundreds')
        self.lbl_nettraffic_key_14.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_14)
        ui_object_complete.append(self.lbl_nettraffic_key_14)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_14)

        """ Tens """
        self.lbl_nettraffic_key_15 = QLabel(self)
        self.lbl_nettraffic_key_15.move(self.menu_obj_pos_w + 2 + 4 + 72 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_15.resize(10, 10)
        self.lbl_nettraffic_key_15.setStyleSheet("""QLabel {background-color: rgb(0, 0, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_15)
        ui_object_complete.append(self.lbl_nettraffic_key_15)

        self.lbl_nettraffic_key_16 = QLabel(self)
        self.lbl_nettraffic_key_16.move(self.menu_obj_pos_w + 2 + 4 + 72 + 4 + 10 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_16.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_16.setFont(self.font_s7b)
        self.lbl_nettraffic_key_16.setText('Tens')
        self.lbl_nettraffic_key_16.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_16)
        ui_object_complete.append(self.lbl_nettraffic_key_16)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_16)

        """ Units """
        self.lbl_nettraffic_key_17 = QLabel(self)
        self.lbl_nettraffic_key_17.move(self.menu_obj_pos_w + 2 + 4 + 72 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_17.resize(10, 10)
        self.lbl_nettraffic_key_17.setStyleSheet("""QLabel {background-color: rgb(255, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_17)
        ui_object_complete.append(self.lbl_nettraffic_key_17)

        self.lbl_nettraffic_key_18 = QLabel(self)
        self.lbl_nettraffic_key_18.move(self.menu_obj_pos_w + 2 + 4 + 72 + 4 + 10 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_18.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_18.setFont(self.font_s7b)
        self.lbl_nettraffic_key_18.setText('Units')
        self.lbl_nettraffic_key_18.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_18)
        ui_object_complete.append(self.lbl_nettraffic_key_18)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_18)

        self.lbl_nettraffic_key_19 = QLabel(self)
        self.lbl_nettraffic_key_19.move(self.menu_obj_pos_w + 2 + 4 + 72 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_19.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_19.setFont(self.font_s7b)
        self.lbl_nettraffic_key_19.setText('Received [0]]')
        self.lbl_nettraffic_key_19.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_19)
        ui_object_complete.append(self.lbl_nettraffic_key_19)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_19)

        self.lbl_nettraffic_key_21 = QLabel(self)
        self.lbl_nettraffic_key_21.move(self.menu_obj_pos_w + 2 + 4 + 72 + 20 + 4 + 72 + 100, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10 - 4 - 10)
        self.lbl_nettraffic_key_21.resize(self.monitor_btn_w * 2, 10)
        self.lbl_nettraffic_key_21.setFont(self.font_s7b)
        self.lbl_nettraffic_key_21.setText('Sent [F10]]')
        self.lbl_nettraffic_key_21.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                   color: rgb(150, 150, 150);
                                                   border-top:0px solid rgb(10, 10, 10);
                                                   border-bottom:0px solid rgb(10, 10, 10);
                                                   border-right:0px solid rgb(10, 10, 10);
                                                   border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_nettraffic_key_21)
        ui_object_complete.append(self.lbl_nettraffic_key_21)
        ui_object_font_list_s7b.append(self.lbl_nettraffic_key_21)

        self.lbl_network_adapter = QPushButton(self)
        self.lbl_network_adapter.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h)
        self.lbl_network_adapter.resize(72, self.monitor_btn_h)
        self.lbl_network_adapter.setFont(self.font_s8b)
        self.lbl_network_adapter.setText('Adapter')
        self.lbl_network_adapter.setStyleSheet(self.btn_menu_style)
        self.lbl_network_adapter.clicked.connect(self.btn_network_adapter_function)
        print('-- [App.__init__] created:', self.lbl_network_adapter)
        ui_object_complete.append(self.lbl_network_adapter)
        ui_object_font_list_s8b.append(self.lbl_network_adapter)

        self.cmb_network_adapter_name = QComboBox(self)
        self.cmb_network_adapter_name.resize(224, self.monitor_btn_h)
        self.cmb_network_adapter_name.move(self.menu_obj_pos_w + 2 + 72 + 4, self.height - 4 - self.monitor_btn_h)
        self.cmb_network_adapter_name.setStyleSheet(self.cmb_menu_style)
        self.cmb_network_adapter_name.setFont(self.font_s8b)
        self.cmb_network_adapter_name.activated[str].connect(self.cmb_network_adapter_name_function)
        print('-- [App.__init__] created:', self.cmb_network_adapter_name)
        self.object_interaction_enabled.append(self.cmb_network_adapter_name)
        ui_object_complete.append(self.cmb_network_adapter_name)
        ui_object_font_list_s8b.append(self.cmb_network_adapter_name)

        self.btn_network_adapter_refresh = QPushButton(self)
        self.btn_network_adapter_refresh.move(self.menu_obj_pos_w + 2 + 72 + 4 + 224 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_network_adapter_refresh.resize(28, 28)
        self.btn_network_adapter_refresh.setIcon(QIcon("./image/baseline_refresh_white_24dp.png"))
        self.btn_network_adapter_refresh.setIconSize(QSize(14, 14))
        self.btn_network_adapter_refresh.setStyleSheet(self.btn_menu_style)
        self.btn_network_adapter_refresh.clicked.connect(self.btn_network_adapter_refresh_function)
        print('-- [App.__init__] created:', self.btn_network_adapter_refresh)
        self.object_interaction_enabled.append(self.btn_network_adapter_refresh)
        ui_object_complete.append(self.btn_network_adapter_refresh)

        self.btn_network_adapter = QPushButton(self)
        self.btn_network_adapter.move(self.menu_obj_pos_w + 2 + 72 + 4 + 224 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_network_adapter.resize(28, 28)
        self.btn_network_adapter.setStyleSheet(self.btn_menu_style)
        self.btn_network_adapter.setIconSize(self.tog_switch_ico_sz)
        self.btn_network_adapter.clicked.connect(self.btn_network_adapter_function)
        print('-- [App.__init__] created:', self.btn_network_adapter)
        self.object_interaction_enabled.append(self.btn_network_adapter)
        ui_object_complete.append(self.btn_network_adapter)

        self.qle_network_adapter_led_time_on = QLineEdit(self)
        self.qle_network_adapter_led_time_on.resize(28, 28)
        self.qle_network_adapter_led_time_on.move(self.menu_obj_pos_w + 2 + 72 + 4 + 224 + 4 + 28 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_network_adapter_led_time_on.setFont(self.font_s8b)
        self.qle_network_adapter_led_time_on.returnPressed.connect(self.btn_network_adapter_led_time_on_function)
        self.qle_network_adapter_led_time_on.setStyleSheet(self.qle_menu_style)
        self.qle_network_adapter_led_time_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_network_adapter_led_time_on)
        self.object_interaction_readonly.append(self.qle_network_adapter_led_time_on)
        ui_object_complete.append(self.qle_network_adapter_led_time_on)
        ui_object_font_list_s8b.append(self.qle_network_adapter_led_time_on)

        self.lbl_net_con_mouse_key_1 = QLabel(self)
        self.lbl_net_con_mouse_key_1.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_net_con_mouse_key_1.resize(10, 10)
        self.lbl_net_con_mouse_key_1.setStyleSheet("""QLabel {background-color: rgb(0, 255, 0);
                                                       color: rgb(150, 150, 150);
                                                       border-top:2px solid rgb(10, 10, 10);
                                                       border-bottom:2px solid rgb(10, 10, 10);
                                                       border-right:2px solid rgb(10, 10, 10);
                                                       border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_key_1)
        ui_object_complete.append(self.lbl_net_con_mouse_key_1)

        self.lbl_net_con_mouse_key_2 = QLabel(self)
        self.lbl_net_con_mouse_key_2.move(self.menu_obj_pos_w + 2 + 4 + 10, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_net_con_mouse_key_2.resize(72, 10)
        self.lbl_net_con_mouse_key_2.setFont(self.font_s7b)
        self.lbl_net_con_mouse_key_2.setText('Online')
        self.lbl_net_con_mouse_key_2.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                       color: rgb(150, 150, 150);
                                                       border-top:0px solid rgb(10, 10, 10);
                                                       border-bottom:0px solid rgb(10, 10, 10);
                                                       border-right:0px solid rgb(10, 10, 10);
                                                       border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_key_2)
        ui_object_complete.append(self.lbl_net_con_mouse_key_2)
        ui_object_font_list_s7b.append(self.lbl_net_con_mouse_key_2)

        self.lbl_net_con_mouse_key_3 = QLabel(self)
        self.lbl_net_con_mouse_key_3.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_net_con_mouse_key_3.resize(10, 10)
        self.lbl_net_con_mouse_key_3.setStyleSheet("""QLabel {background-color: rgb(255, 0, 0);
                                                               color: rgb(150, 150, 150);
                                                               border-top:2px solid rgb(10, 10, 10);
                                                               border-bottom:2px solid rgb(10, 10, 10);
                                                               border-right:2px solid rgb(10, 10, 10);
                                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_key_3)
        ui_object_complete.append(self.lbl_net_con_mouse_key_3)

        self.lbl_net_con_mouse_key_4 = QLabel(self)
        self.lbl_net_con_mouse_key_4.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 10, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_net_con_mouse_key_4.resize(72, 10)
        self.lbl_net_con_mouse_key_4.setFont(self.font_s7b)
        self.lbl_net_con_mouse_key_4.setText('Offline')
        self.lbl_net_con_mouse_key_4.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                               color: rgb(150, 150, 150);
                                                               border-top:0px solid rgb(10, 10, 10);
                                                               border-bottom:0px solid rgb(10, 10, 10);
                                                               border-right:0px solid rgb(10, 10, 10);
                                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_key_4)
        ui_object_complete.append(self.lbl_net_con_mouse_key_4)
        ui_object_font_list_s7b.append(self.lbl_net_con_mouse_key_4)

        self.lbl_net_con_mouse_key_5 = QLabel(self)
        self.lbl_net_con_mouse_key_5.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 72, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_net_con_mouse_key_5.resize(10, 10)
        self.lbl_net_con_mouse_key_5.setStyleSheet("""QLabel {background-color: rgb(255, 100, 0);
                                                                       color: rgb(150, 150, 150);
                                                                       border-top:2px solid rgb(10, 10, 10);
                                                                       border-bottom:2px solid rgb(10, 10, 10);
                                                                       border-right:2px solid rgb(10, 10, 10);
                                                                       border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_key_5)
        ui_object_complete.append(self.lbl_net_con_mouse_key_5)

        self.lbl_net_con_mouse_key_6 = QLabel(self)
        self.lbl_net_con_mouse_key_6.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 72 + 4 + 10, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - 10)
        self.lbl_net_con_mouse_key_6.resize(72, 10)
        self.lbl_net_con_mouse_key_6.setFont(self.font_s7b)
        self.lbl_net_con_mouse_key_6.setText('Intermittent')
        self.lbl_net_con_mouse_key_6.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                                       color: rgb(150, 150, 150);
                                                                       border-top:0px solid rgb(10, 10, 10);
                                                                       border-bottom:0px solid rgb(10, 10, 10);
                                                                       border-right:0px solid rgb(10, 10, 10);
                                                                       border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_key_6)
        ui_object_complete.append(self.lbl_net_con_mouse_key_6)
        ui_object_font_list_s7b.append(self.lbl_net_con_mouse_key_6)

        self.lbl_net_con_mouse = QPushButton(self)
        self.lbl_net_con_mouse.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_net_con_mouse.resize(240, self.monitor_btn_h)
        self.lbl_net_con_mouse.setFont(self.font_s8b)
        self.lbl_net_con_mouse.setText('Display Internet Connection (Mouse)')
        self.lbl_net_con_mouse.setStyleSheet(self.btn_menu_style)
        self.lbl_net_con_mouse.clicked.connect(self.btn_net_con_mouse_function)
        print('-- [App.__init__] created:', self.lbl_net_con_mouse)
        ui_object_complete.append(self.lbl_net_con_mouse)
        ui_object_font_list_s8b.append(self.lbl_net_con_mouse)

        self.btn_net_con_mouse = QPushButton(self)
        self.btn_net_con_mouse.move(self.menu_obj_pos_w + 2 + 240 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_net_con_mouse.resize(28, 28)
        self.btn_net_con_mouse.setStyleSheet(self.btn_menu_style)
        self.btn_net_con_mouse.setIconSize(self.tog_switch_ico_sz)
        self.btn_net_con_mouse.clicked.connect(self.btn_net_con_mouse_function)
        print('-- [App.__init__] created:', self.btn_net_con_mouse)
        self.object_interaction_enabled.append(self.btn_net_con_mouse)
        ui_object_complete.append(self.btn_net_con_mouse)

        self.btn_net_con_mouse_led_selected_prev = QPushButton(self)
        self.btn_net_con_mouse_led_selected_prev.move(self.menu_obj_pos_w + 2 + 240 + 4 + 28 + 4,  self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_net_con_mouse_led_selected_prev.resize(20, 28)
        self.btn_net_con_mouse_led_selected_prev.setIcon(QIcon("./image/img_minus.png"))
        self.btn_net_con_mouse_led_selected_prev.setStyleSheet(self.btn_menu_style)
        self.btn_net_con_mouse_led_selected_prev.clicked.connect(self.btn_net_con_mouse_led_selected_prev_function)
        print('-- [App.__init__] created:', self.btn_net_con_mouse_led_selected_prev)
        self.object_interaction_enabled.append(self.btn_net_con_mouse_led_selected_prev)
        ui_object_complete.append(self.btn_net_con_mouse_led_selected_prev)

        self.lbl_net_con_mouse_led_selected = QLabel(self)
        self.lbl_net_con_mouse_led_selected.move(self.menu_obj_pos_w + 2 + 240 + 4 + 28 + 4 + 20 + 4,  self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_net_con_mouse_led_selected.resize(28, self.monitor_btn_h)
        self.lbl_net_con_mouse_led_selected.setFont(self.font_s8b)
        self.lbl_net_con_mouse_led_selected.setStyleSheet(self.lbl_menu_style)
        self.lbl_net_con_mouse_led_selected.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.lbl_net_con_mouse_led_selected)
        ui_object_complete.append(self.lbl_net_con_mouse_led_selected)
        ui_object_font_list_s8b.append(self.lbl_net_con_mouse_led_selected)

        self.btn_net_con_mouse_led_selected_next = QPushButton(self)
        self.btn_net_con_mouse_led_selected_next.move(self.menu_obj_pos_w + 2 + 240 + 4 + 28 + 4 + 20 + 4 + 28 + 4,  self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_net_con_mouse_led_selected_next.resize(20, self.monitor_btn_h)
        self.btn_net_con_mouse_led_selected_next.setIcon(QIcon("./image/img_plus.png"))
        self.btn_net_con_mouse_led_selected_next.setStyleSheet(self.btn_menu_style)
        self.btn_net_con_mouse_led_selected_next.clicked.connect(self.btn_net_con_mouse_led_selected_next_function)
        print('-- [App.__init__] created:', self.btn_net_con_mouse_led_selected_next)
        self.object_interaction_enabled.append(self.btn_net_con_mouse_led_selected_next)
        ui_object_complete.append(self.btn_net_con_mouse_led_selected_next)

        self.lbl_net_con_kb = QPushButton(self)
        self.lbl_net_con_kb.move(self.menu_obj_pos_w + 2,  self.height - 4 - self.monitor_btn_h)
        self.lbl_net_con_kb.resize(280, self.monitor_btn_h)
        self.lbl_net_con_kb.setFont(self.font_s8b)
        self.lbl_net_con_kb.setText('Display Internet Connection (Keyboard)')
        self.lbl_net_con_kb.setStyleSheet(self.btn_menu_style)
        self.lbl_net_con_kb.clicked.connect(self.btn_net_con_kb_function)
        print('-- [App.__init__] created:', self.lbl_net_con_kb)
        ui_object_complete.append(self.lbl_net_con_kb)
        ui_object_font_list_s8b.append(self.lbl_net_con_kb)

        self.btn_net_con_kb = QPushButton(self)
        self.btn_net_con_kb.move(self.menu_obj_pos_w + 2 + 280 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_net_con_kb.resize(28, 28)
        self.btn_net_con_kb.setStyleSheet(self.btn_menu_style)
        self.btn_net_con_kb.setIconSize(self.tog_switch_ico_sz)
        self.btn_net_con_kb.clicked.connect(self.btn_net_con_kb_function)
        print('-- [App.__init__] created:', self.btn_net_con_kb)
        self.object_interaction_enabled.append(self.btn_net_con_kb)
        ui_object_complete.append(self.btn_net_con_kb)

        self.lbl_netshare_mon = QPushButton(self)
        self.lbl_netshare_mon.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.lbl_netshare_mon.resize(126, self.monitor_btn_h)
        self.lbl_netshare_mon.setFont(self.font_s8b)
        self.lbl_netshare_mon.setText('Network Shares')
        self.lbl_netshare_mon.setStyleSheet(self.btn_menu_style)
        self.lbl_netshare_mon.clicked.connect(self.btn_defnetshare_function)
        print('-- [App.__init__] created:', self.lbl_netshare_mon)
        ui_object_complete.append(self.lbl_netshare_mon)
        ui_object_font_list_s8b.append(self.lbl_netshare_mon)

        self.btn_netshare_mon = QPushButton(self)
        self.btn_netshare_mon.move(self.menu_obj_pos_w + 2 + 126 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.btn_netshare_mon.resize(28, 28)
        self.btn_netshare_mon.setStyleSheet(self.btn_menu_style)
        self.btn_netshare_mon.setIconSize(self.tog_switch_ico_sz)
        self.btn_netshare_mon.clicked.connect(self.btn_defnetshare_function)
        print('-- [App.__init__] created:', self.btn_netshare_mon)
        self.object_interaction_enabled.append(self.btn_netshare_mon)
        ui_object_complete.append(self.btn_netshare_mon)

        self.qle_netshare_mon_rgb_on = QLineEdit(self)
        self.qle_netshare_mon_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_netshare_mon_rgb_on.move(self.menu_obj_pos_w + 2 + 126 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h - 4 - self.monitor_btn_h)
        self.qle_netshare_mon_rgb_on.setFont(self.font_s8b)
        self.qle_netshare_mon_rgb_on.returnPressed.connect(self.netshare_active_rgb_function)
        self.qle_netshare_mon_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_netshare_mon_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_netshare_mon_rgb_on)
        self.object_interaction_readonly.append(self.qle_netshare_mon_rgb_on)
        ui_object_complete.append(self.qle_netshare_mon_rgb_on)
        ui_object_font_list_s8b.append(self.qle_netshare_mon_rgb_on)

        self.lbl_exclusive_con = QPushButton(self)
        self.lbl_exclusive_con.move(self.menu_obj_pos_w + 2, self.height - (4 * 7) - (self.monitor_btn_h * 7))
        self.lbl_exclusive_con.resize(126, self.monitor_btn_h)
        self.lbl_exclusive_con.setFont(self.font_s8b)
        self.lbl_exclusive_con.setText('Exclusive Access')
        self.lbl_exclusive_con.setStyleSheet(self.btn_menu_style)
        self.lbl_exclusive_con.clicked.connect(self.btn_exclusive_con_function)
        print('-- [App.__init__] created:', self.lbl_exclusive_con)
        ui_object_complete.append(self.lbl_exclusive_con)
        ui_object_font_list_s8b.append(self.lbl_exclusive_con)

        self.btn_exclusive_con = QPushButton(self)
        self.btn_exclusive_con.move(self.menu_obj_pos_w + 2 + 126 + 4, self.height - (4 * 7) - (self.monitor_btn_h * 7))
        self.btn_exclusive_con.resize(28, 28)
        self.btn_exclusive_con.setStyleSheet(self.btn_menu_style)
        self.btn_exclusive_con.setIconSize(self.tog_switch_ico_sz)
        self.btn_exclusive_con.clicked.connect(self.btn_exclusive_con_function)
        print('-- [App.__init__] created:', self.btn_exclusive_con)
        self.object_interaction_enabled.append(self.btn_exclusive_con)
        ui_object_complete.append(self.btn_exclusive_con)

        self.lbl_run_startup = QPushButton(self)
        self.lbl_run_startup.move(self.menu_obj_pos_w + 2, self.height - (4 * 6) - (self.monitor_btn_h * 6))
        self.lbl_run_startup.resize(126, self.monitor_btn_h)
        self.lbl_run_startup.setFont(self.font_s8b)
        self.lbl_run_startup.setText('Automatic Startup')
        self.lbl_run_startup.setStyleSheet(self.btn_menu_style)
        self.lbl_run_startup.clicked.connect(self.btn_run_startup_function)
        print('-- [App.__init__] created:', self.lbl_run_startup)
        ui_object_complete.append(self.lbl_run_startup)
        ui_object_font_list_s8b.append(self.lbl_run_startup)

        self.btn_run_startup = QPushButton(self)
        self.btn_run_startup.move(self.menu_obj_pos_w + 2 + 126 + 4, self.height - (4 * 6) - (self.monitor_btn_h * 6))
        self.btn_run_startup.resize(28, 28)
        self.btn_run_startup.setStyleSheet(self.btn_menu_style)
        self.btn_run_startup.setIconSize(self.tog_switch_ico_sz)
        self.btn_run_startup.clicked.connect(self.btn_run_startup_function)
        print('-- [App.__init__] created:', self.btn_run_startup)
        self.object_interaction_enabled.append(self.btn_run_startup)
        ui_object_complete.append(self.btn_run_startup)

        self.lbl_start_minimized = QPushButton(self)
        self.lbl_start_minimized.move(self.menu_obj_pos_w + 2, self.height - (4 * 5) - (self.monitor_btn_h * 5))
        self.lbl_start_minimized.resize(126, self.monitor_btn_h)
        self.lbl_start_minimized.setFont(self.font_s8b)
        self.lbl_start_minimized.setText('Start Minimized')
        self.lbl_start_minimized.setStyleSheet(self.btn_menu_style)
        self.lbl_start_minimized.clicked.connect(self.btn_start_minimized_function)
        print('-- [App.__init__] created:', self.lbl_start_minimized)
        ui_object_complete.append(self.lbl_start_minimized)
        ui_object_font_list_s8b.append(self.lbl_start_minimized)

        self.btn_start_minimized = QPushButton(self)
        self.btn_start_minimized.move(self.menu_obj_pos_w + 2 + 126 + 4, self.height - (4 * 5) - (self.monitor_btn_h * 5))
        self.btn_start_minimized.resize(28, 28)
        self.btn_start_minimized.setStyleSheet(self.btn_menu_style)
        self.btn_start_minimized.setIconSize(self.tog_switch_ico_sz)
        self.btn_start_minimized.clicked.connect(self.btn_start_minimized_function)
        print('-- [App.__init__] created:', self.btn_start_minimized)
        self.object_interaction_enabled.append(self.btn_start_minimized)
        ui_object_complete.append(self.btn_start_minimized)

        self.lbl_backlight_sub = QPushButton(self)
        self.lbl_backlight_sub.move(self.menu_obj_pos_w + 2, self.height - 4 - self.monitor_btn_h)
        self.lbl_backlight_sub.resize(86, 28)
        self.lbl_backlight_sub.setFont(self.font_s8b)
        self.lbl_backlight_sub.setText('Backlight')
        self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style)
        self.lbl_backlight_sub.clicked.connect(self.btn_bck_light_function)
        print('-- [App.__init__] created:', self.lbl_backlight_sub)
        ui_object_complete.append(self.lbl_backlight_sub)
        ui_object_font_list_s8b.append(self.lbl_backlight_sub)

        self.btn_backlight_sub = QPushButton(self)
        self.btn_backlight_sub.move(self.menu_obj_pos_w + 2 + 86 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_backlight_sub.resize(28, 28)
        self.btn_backlight_sub.setStyleSheet(self.btn_menu_style)
        self.btn_backlight_sub.setIconSize(self.tog_switch_ico_sz)
        self.btn_backlight_sub.clicked.connect(self.btn_bck_light_function)
        print('-- [App.__init__] created:', self.btn_backlight_sub)
        self.object_interaction_enabled.append(self.btn_backlight_sub)
        ui_object_complete.append(self.btn_backlight_sub)

        self.qle_backlight_rgb_on = QLineEdit(self)
        self.qle_backlight_rgb_on.resize(self.monitor_btn_w, self.monitor_btn_h)
        self.qle_backlight_rgb_on.move(self.menu_obj_pos_w + 2 + 86 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.qle_backlight_rgb_on.setFont(self.font_s8b)
        self.qle_backlight_rgb_on.returnPressed.connect(self.btn_backlight_rgb_on_function)
        self.qle_backlight_rgb_on.setStyleSheet(self.qle_menu_style)
        self.qle_backlight_rgb_on.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.qle_backlight_rgb_on)
        self.object_interaction_readonly.append(self.qle_backlight_rgb_on)
        ui_object_complete.append(self.qle_backlight_rgb_on)
        ui_object_font_list_s8b.append(self.qle_backlight_rgb_on)

        self.lbl_backlight_auto = QPushButton(self)
        self.lbl_backlight_auto.move(self.menu_obj_pos_w + 2 + 86 + 4 + 28 + 4 + self.monitor_btn_w + 4, self.height - 4 - self.monitor_btn_h)
        self.lbl_backlight_auto.resize(92, self.monitor_btn_h)
        self.lbl_backlight_auto.setFont(self.font_s8b)
        self.lbl_backlight_auto.setText('Automatic')
        self.lbl_backlight_auto.setStyleSheet(self.btn_menu_style)
        self.lbl_backlight_auto.clicked.connect(self.backlight_auto_function)
        print('-- [App.__init__] created:', self.lbl_backlight_auto)
        ui_object_complete.append(self.lbl_backlight_auto)
        ui_object_font_list_s8b.append(self.lbl_backlight_auto)

        self.btn_backlight_auto = QPushButton(self)
        self.btn_backlight_auto.move(self.menu_obj_pos_w + 2 + 86 + 4 + 28 + 4 + self.monitor_btn_w + 4 + 92 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_backlight_auto.resize(28, 28)
        self.btn_backlight_auto.setStyleSheet(self.btn_menu_style)
        self.btn_backlight_auto.setIconSize(self.tog_switch_ico_sz)
        self.btn_backlight_auto.clicked.connect(self.backlight_auto_function)
        print('-- [App.__init__] created:', self.btn_backlight_auto)
        self.object_interaction_enabled.append(self.btn_backlight_auto)
        ui_object_complete.append(self.btn_backlight_auto)

        self.btn_backlight_auto_time_0 = QLineEdit(self)
        self.btn_backlight_auto_time_0.resize(42, self.monitor_btn_h)
        self.btn_backlight_auto_time_0.move(self.menu_obj_pos_w + 2 + 86 + 4 + 28 + 4 + self.monitor_btn_w + 4 + 92 + 4 + 28 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_backlight_auto_time_0.setFont(self.font_s8b)
        self.btn_backlight_auto_time_0.returnPressed.connect(self.btn_backlight_auto_time_0_function)
        self.btn_backlight_auto_time_0.setStyleSheet(self.qle_menu_style)
        self.btn_backlight_auto_time_0.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.btn_backlight_auto_time_0)
        self.btn_backlight_auto_time_0.setToolTip('Automatic Backlight Time On\n\nAccepts only 24h Format.\n\nExample 1: 0000\nExample 2: 0030\nExample 3: 0900')
        self.object_interaction_readonly.append(self.btn_backlight_auto_time_0)
        ui_object_complete.append(self.btn_backlight_auto_time_0)
        ui_object_font_list_s8b.append(self.btn_backlight_auto_time_0)

        self.btn_backlight_auto_time_1 = QLineEdit(self)
        self.btn_backlight_auto_time_1.resize(42, self.monitor_btn_h)
        self.btn_backlight_auto_time_1.move(self.menu_obj_pos_w + 2 + 86 + 4 + 28 + 4 + self.monitor_btn_w + 4 + 92 + 4 + 28 + 4 + 42 + 4, self.height - 4 - self.monitor_btn_h)
        self.btn_backlight_auto_time_1.setFont(self.font_s8b)
        self.btn_backlight_auto_time_1.returnPressed.connect(self.btn_backlight_auto_time_1_function)
        self.btn_backlight_auto_time_1.setStyleSheet(self.qle_menu_style)
        self.btn_backlight_auto_time_1.setAlignment(Qt.AlignCenter)
        print('-- [App.__init__] created:', self.btn_backlight_auto_time_1)
        self.btn_backlight_auto_time_1.setToolTip('Automatic Backlight Time Off\n\nAccepts only 24h Format.\n\nExample 1: 0000\nExample 2: 0030\nExample 3: 0900')
        self.object_interaction_readonly.append(self.btn_backlight_auto_time_1)
        ui_object_complete.append(self.btn_backlight_auto_time_1)
        ui_object_font_list_s8b.append(self.btn_backlight_auto_time_1)

        self.lbl_media_display = QPushButton(self)
        self.lbl_media_display.move(self.menu_obj_pos_w + 2, self.height - (4 * 4) - (self.monitor_btn_h * 4))
        self.lbl_media_display.resize(126, self.monitor_btn_h)
        self.lbl_media_display.setFont(self.font_s8b)
        self.lbl_media_display.setText('Media Display')
        self.lbl_media_display.setStyleSheet(self.btn_menu_style)
        self.lbl_media_display.clicked.connect(self.btn_media_display_function)
        print('-- [App.__init__] created:', self.lbl_media_display)
        ui_object_complete.append(self.lbl_media_display)
        ui_object_font_list_s8b.append(self.lbl_media_display)
        self.lbl_media_display.setToolTip('Media Display\n\nEnables/Disables Media Display.\n\nDisplays media states from any application that utilizes the global media player controller.')

        self.btn_media_display = QPushButton(self)
        self.btn_media_display.move(self.menu_obj_pos_w + 2 + 4 + 126, self.height - (4 * 4) - (self.monitor_btn_h * 4))
        self.btn_media_display.resize(28, 28)
        self.btn_media_display.setStyleSheet(self.btn_menu_style)
        self.btn_media_display.setIconSize(self.tog_switch_ico_sz)
        self.btn_media_display.clicked.connect(self.btn_media_display_function)
        print('-- [App.__init__] created:', self.btn_media_display)
        self.object_interaction_enabled.append(self.btn_media_display)
        ui_object_complete.append(self.btn_media_display)
        self.btn_media_display.setToolTip('Media Display\n\nEnables/Disables Media Display.')

        self.lbl_fahrenheit = QPushButton(self)
        self.lbl_fahrenheit.move(self.menu_obj_pos_w + 2, self.height - (4 * 3) - (self.monitor_btn_h * 3))
        self.lbl_fahrenheit.resize(126, self.monitor_btn_h)
        self.lbl_fahrenheit.setFont(self.font_s8b)
        self.lbl_fahrenheit.setText('Fahrenheit')
        self.lbl_fahrenheit.setStyleSheet(self.btn_menu_style)
        self.lbl_fahrenheit.clicked.connect(self.btn_fahrenheit_function)
        print('-- [App.__init__] created:', self.lbl_fahrenheit)
        ui_object_complete.append(self.lbl_fahrenheit)
        ui_object_font_list_s8b.append(self.lbl_fahrenheit)
        # self.lbl_fahrenheit.setToolTip('Media Display\n\nEnables/Disables Media Display.\n\nDisplays media states from any application that utilizes the global media player controller.')

        self.btn_fahrenheit = QPushButton(self)
        self.btn_fahrenheit.move(self.menu_obj_pos_w + 2 + 4 + 126, self.height - (4 * 3) - (self.monitor_btn_h * 3))
        self.btn_fahrenheit.resize(28, 28)
        self.btn_fahrenheit.setStyleSheet(self.btn_menu_style)
        self.btn_fahrenheit.setIconSize(self.tog_switch_ico_sz)
        self.btn_fahrenheit.clicked.connect(self.btn_fahrenheit_function)
        print('-- [App.__init__] created:', self.btn_fahrenheit)
        self.object_interaction_enabled.append(self.btn_fahrenheit)
        ui_object_complete.append(self.btn_fahrenheit)
        # self.btn_fahrenheit.setToolTip('Media Display\n\nEnables/Disables Media Display.')

        self.lbl_power_plan = QPushButton(self)
        self.lbl_power_plan.move(self.menu_obj_pos_w + 2, self.height - (4 * 6) - (self.monitor_btn_h * 6))
        self.lbl_power_plan.resize(126, self.monitor_btn_h)
        self.lbl_power_plan.setFont(self.font_s8b)
        self.lbl_power_plan.setText('G1 Power')
        self.lbl_power_plan.setStyleSheet(self.btn_menu_style)
        self.lbl_power_plan.clicked.connect(self.btn_power_plan_function)
        print('-- [App.__init__] created:', self.lbl_power_plan)
        ui_object_complete.append(self.lbl_power_plan)
        ui_object_font_list_s8b.append(self.lbl_power_plan)
        self.lbl_power_plan.setToolTip('G1 Power\n\nEnables/Disables G1 Power Plan.\n\nG1 key LED will reflect the current power plan while a short press will change the power plan.\n\nIt is recommended to properly configure your power plan(s) to compliment this feature, reducing Processor Maximum State for Power Saver.\n\nShort Press: Cycle Power Plan\n1 Second [Yellow G1]: Hibernate/Sleep\n2 Seconds [Amber G1]: Restart\n3 Seconds [Red G1]: Shutdown\n4 Seconds [White G1]: Cancel')

        self.btn_power_plan = QPushButton(self)
        self.btn_power_plan.move(self.menu_obj_pos_w + 2 + 4 + 126, self.height - (4 * 6) - (self.monitor_btn_h * 6))
        self.btn_power_plan.resize(28, 28)
        self.btn_power_plan.setStyleSheet(self.btn_menu_style)
        self.btn_power_plan.setIconSize(self.tog_switch_ico_sz)
        self.btn_power_plan.clicked.connect(self.btn_power_plan_function)
        print('-- [App.__init__] created:', self.btn_power_plan)
        self.object_interaction_enabled.append(self.btn_power_plan)
        ui_object_complete.append(self.btn_power_plan)
        self.btn_power_plan.setToolTip('G1 Power Plan\n\nEnables/Disables G1 Power Plan.')

        self.lbl_g2_disk = QPushButton(self)
        self.lbl_g2_disk.move(self.menu_obj_pos_w + 2, self.height - (4 * 5) - (self.monitor_btn_h * 5))
        self.lbl_g2_disk.resize(126, self.monitor_btn_h)
        self.lbl_g2_disk.setFont(self.font_s8b)
        self.lbl_g2_disk.setText('G2 Disks')
        self.lbl_g2_disk.setStyleSheet(self.btn_menu_style)
        self.lbl_g2_disk.clicked.connect(self.btn_g2_disk_function)
        print('-- [App.__init__] created:', self.lbl_g2_disk)
        ui_object_complete.append(self.lbl_g2_disk)
        ui_object_font_list_s8b.append(self.lbl_g2_disk)
        self.lbl_g2_disk.setToolTip('G2 Disks\n\nEnables/Disables G2 Disks\n\nShort Press G2 Or Any Non-Alpha Key To Disarm. (ESC or Short press G2 recommended)\n1 Second Hold [Yellow G2]: Eject\n2 Seconds [Amber G2]: Mount (Only un-mounted drives can be mounted, you may not mount an ejected drive).\n3 Seconds [Red G2]: Unmount (Un-mounted drives will not be automatically mounted by Windows until next reboot.\n4 Seconds [White G2]: Cancel\n\nNote: Only drives that have been unmounted while iCUE Display has been running can be mounted.\nAny drive assigned a Disk Letter can be ejected/mounted/unmounted when the alpha keys reflect your expressed intent.\n\nWARNING: This Feature Is Experimental')

        self.btn_g2_disk = QPushButton(self)
        self.btn_g2_disk.move(self.menu_obj_pos_w + 2 + 4 + 126, self.height - (4 * 5) - (self.monitor_btn_h * 5))
        self.btn_g2_disk.resize(28, 28)
        self.btn_g2_disk.setStyleSheet(self.btn_menu_style)
        self.btn_g2_disk.setIconSize(self.tog_switch_ico_sz)
        self.btn_g2_disk.clicked.connect(self.btn_g2_disk_function)
        print('-- [App.__init__] created:', self.btn_g2_disk)
        self.object_interaction_enabled.append(self.btn_g2_disk)
        ui_object_complete.append(self.btn_g2_disk)
        self.btn_g2_disk.setToolTip('G2 Disks\n\nEnables/Disables G2 Disks.')

        """ Power Saver """
        self.lbl_power_plan_key_0 = QLabel(self)
        self.lbl_power_plan_key_0.move(self.menu_obj_pos_w + 2, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_0.resize(10, 10)
        self.lbl_power_plan_key_0.setStyleSheet("""QLabel {background-color: rgb(255, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_0)
        ui_object_complete.append(self.lbl_power_plan_key_0)

        self.lbl_power_plan_key_1 = QLabel(self)
        self.lbl_power_plan_key_1.move(self.menu_obj_pos_w + 2 + 4 + 10, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_1.resize(72, 10)
        self.lbl_power_plan_key_1.setFont(self.font_s7b)
        self.lbl_power_plan_key_1.setText('Power Saver')
        self.lbl_power_plan_key_1.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_1)
        ui_object_complete.append(self.lbl_power_plan_key_1)
        ui_object_font_list_s7b.append(self.lbl_power_plan_key_1)

        """ Balanced """
        self.lbl_power_plan_key_2 = QLabel(self)
        self.lbl_power_plan_key_2.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_2.resize(10, 10)
        self.lbl_power_plan_key_2.setStyleSheet("""QLabel {background-color: rgb(0, 255, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_2)
        ui_object_complete.append(self.lbl_power_plan_key_2)

        self.lbl_power_plan_key_3 = QLabel(self)
        self.lbl_power_plan_key_3.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 10, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_3.resize(72, 10)
        self.lbl_power_plan_key_3.setFont(self.font_s7b)
        self.lbl_power_plan_key_3.setText('Balanced')
        self.lbl_power_plan_key_3.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_3)
        ui_object_complete.append(self.lbl_power_plan_key_3)
        ui_object_font_list_s7b.append(self.lbl_power_plan_key_3)

        """ High Power """
        self.lbl_power_plan_key_4 = QLabel(self)
        self.lbl_power_plan_key_4.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 10 + 4 + 72, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_4.resize(10, 10)
        self.lbl_power_plan_key_4.setStyleSheet("""QLabel {background-color: rgb(0, 0, 255);
                                               color: rgb(150, 150, 150);
                                               border-top:2px solid rgb(10, 10, 10);
                                               border-bottom:2px solid rgb(10, 10, 10);
                                               border-right:2px solid rgb(10, 10, 10);
                                               border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_4)
        ui_object_complete.append(self.lbl_power_plan_key_4)

        self.lbl_power_plan_key_5 = QLabel(self)
        self.lbl_power_plan_key_5.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 10 + 4 + 72 + 4 + 10, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_5.resize(72, 10)
        self.lbl_power_plan_key_5.setFont(self.font_s7b)
        self.lbl_power_plan_key_5.setText('High Power')
        self.lbl_power_plan_key_5.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                               color: rgb(150, 150, 150);
                                               border-top:0px solid rgb(10, 10, 10);
                                               border-bottom:0px solid rgb(10, 10, 10);
                                               border-right:0px solid rgb(10, 10, 10);
                                               border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_5)
        ui_object_complete.append(self.lbl_power_plan_key_5)
        ui_object_font_list_s7b.append(self.lbl_power_plan_key_5)

        """ Ultimate Performance """
        self.lbl_power_plan_key_6 = QLabel(self)
        self.lbl_power_plan_key_6.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 10 + 4 + 72 + 4 + 10 + 4 + 72, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_6.resize(10, 10)
        self.lbl_power_plan_key_6.setStyleSheet("""QLabel {background-color: rgb(255, 15, 100);
                                                       color: rgb(150, 150, 150);
                                                       border-top:2px solid rgb(10, 10, 10);
                                                       border-bottom:2px solid rgb(10, 10, 10);
                                                       border-right:2px solid rgb(10, 10, 10);
                                                       border-left:2px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_6)
        ui_object_complete.append(self.lbl_power_plan_key_6)

        self.lbl_power_plan_key_7 = QLabel(self)
        self.lbl_power_plan_key_7.move(self.menu_obj_pos_w + 2 + 4 + 10 + 4 + 72 + 4 + 10 + 4 + 72 + 4 + 10 + 4 + 72 + 4 + 10, self.height - (4 * 6) - (self.monitor_btn_h * 6) - 4 - 10)
        self.lbl_power_plan_key_7.resize(100, 10)
        self.lbl_power_plan_key_7.setFont(self.font_s7b)
        self.lbl_power_plan_key_7.setText('Ultimate Performance')
        self.lbl_power_plan_key_7.setStyleSheet("""QLabel {background-color: rgb(0, 0, 0);
                                                       color: rgb(150, 150, 150);
                                                       border-top:0px solid rgb(10, 10, 10);
                                                       border-bottom:0px solid rgb(10, 10, 10);
                                                       border-right:0px solid rgb(10, 10, 10);
                                                       border-left:0px solid rgb(10, 10, 10);}""")
        print('-- [App.__init__] created:', self.lbl_power_plan_key_7)
        ui_object_complete.append(self.lbl_power_plan_key_7)
        ui_object_font_list_s7b.append(self.lbl_power_plan_key_7)

        self.lbl_powershell = QPushButton(self)
        self.lbl_powershell.move(self.menu_obj_pos_w + 2, self.height - (4 * 1) - (self.monitor_btn_h * 1))
        self.lbl_powershell.resize(126, self.monitor_btn_h)
        self.lbl_powershell.setFont(self.font_s8b)
        self.lbl_powershell.setText('G6 Powershell')
        self.lbl_powershell.setStyleSheet(self.btn_menu_style)
        self.lbl_powershell.clicked.connect(self.btn_powershell_function)
        print('-- [App.__init__] created:', self.lbl_powershell)
        ui_object_complete.append(self.lbl_powershell)
        ui_object_font_list_s8b.append(self.lbl_powershell)
        self.lbl_powershell.setToolTip('G6 Powershell\n\nEnables/Disables G6 Powershell.\n\nShort press G6 spawns administrator Powershell window if iCUE Display is running as admin.')

        self.lbl_g5_backlight = QPushButton(self)
        self.lbl_g5_backlight.move(self.menu_obj_pos_w + 2, self.height - (4 * 2) - (self.monitor_btn_h * 2))
        self.lbl_g5_backlight.resize(126, self.monitor_btn_h)
        self.lbl_g5_backlight.setFont(self.font_s8b)
        self.lbl_g5_backlight.setText('G5 Backlight')
        self.lbl_g5_backlight.setStyleSheet(self.btn_menu_style)
        self.lbl_g5_backlight.clicked.connect(self.btn_g5_backlight_function)
        print('-- [App.__init__] created:', self.lbl_g5_backlight)
        ui_object_complete.append(self.lbl_g5_backlight)
        ui_object_font_list_s8b.append(self.lbl_g5_backlight)
        self.lbl_g5_backlight.setToolTip('G5 Backlight\n\nEnables/Disables G5 Backlight.\n\nG5 will turn on/off iCUE Displays backlight feature for use in low light conditions.')

        self.btn_g5_backlight = QPushButton(self)
        self.btn_g5_backlight.move(self.menu_obj_pos_w + 2 + 4 + 126, self.height - (4 * 2) - (self.monitor_btn_h * 2))
        self.btn_g5_backlight.resize(28, 28)
        self.btn_g5_backlight.setStyleSheet(self.btn_menu_style)
        self.btn_g5_backlight.setIconSize(self.tog_switch_ico_sz)
        self.btn_g5_backlight.clicked.connect(self.btn_g5_backlight_function)
        print('-- [App.__init__] created:', self.btn_g5_backlight)
        self.object_interaction_enabled.append(self.btn_g5_backlight)
        ui_object_complete.append(self.btn_g5_backlight)
        self.btn_g5_backlight.setToolTip('G5 Backlight\n\nEnables/Disables G5 Backlight.')

        self.btn_powershell = QPushButton(self)
        self.btn_powershell.move(self.menu_obj_pos_w + 2 + 4 + 126, self.height - (4 * 1) - (self.monitor_btn_h * 1))
        self.btn_powershell.resize(28, 28)
        self.btn_powershell.setStyleSheet(self.btn_menu_style)
        self.btn_powershell.setIconSize(self.tog_switch_ico_sz)
        self.btn_powershell.clicked.connect(self.btn_powershell_function)
        print('-- [App.__init__] created:', self.btn_powershell)
        self.object_interaction_enabled.append(self.btn_powershell)
        ui_object_complete.append(self.btn_powershell)
        self.btn_powershell.setToolTip('G6 Powershell\n\nEnables/Disables G6 Powershell.')

        self.btn_cpu_mon.setToolTip('CPU Utilization Monitor\n\nEnables/Disables CPU utilization monitor.')
        self.lbl_cpu_mon.setToolTip('CPU Utilization Monitor\n\nKeypad 1:       0-25%\nKeypad 4:       25-50%\nKeypad 7:       50-75%\nNumlock:       75-100%.')
        self.qle_cpu_mon_rgb_on.setToolTip('CPU Utilization Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_cpu_led_time_on.setToolTip('CPU Utilization Monitor\n\nTime Interval:\nMinimum: 0.1 Seconds\nMaximum: 5 seconds\n\nQuality: 0.1\nPerformance: 1-5.')
        self.btn_dram_mon.setToolTip('DRAM Utilization Monitor\n\nEnables/Disables DRAM utilization monitor.')
        self.lbl_dram_mon.setToolTip('DRAM Utilization Monitor\n\nKeypad 2:                  0-25%\nKeypad 5:                  25-50%\nKeypad 8:                  50-75%\nKeypad Slash:           75-100%.')
        self.qle_dram_mon_rgb_on.setToolTip('DRAM Utilization Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_dram_led_time_on.setToolTip('DRAM Utilization Monitor\n\nTime Interval:\nMinimum: 0.1 Seconds\nMaximum: 5 seconds\n\nQuality: 0.1\nPerformance: 1-5.')
        self.btn_vram_mon.setToolTip('VRAM Utilization Monitor\n\nEnables/Disables VRAM utilization monitor.')
        self.lbl_vram_mon.setToolTip( 'VRAM Utilization Monitor\n\nKeypad 3:                     0-25%\nKeypad 6:                     25-50%\nKeypad 9:                     50-75%\nKeypad Asterisk:         75-100%.')
        self.qle_vram_mon_rgb_on.setToolTip('VRAM Utilization Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_vram_led_time_on.setToolTip('VRAM Utilization Monitor\n\nTime Interval:\nMinimum: 0.1 Seconds\nMaximum: 5 seconds\n\nQuality: 0.1\nPerformance: 1-5.')
        self.btn_hdd_mon.setToolTip('Disk Read/Write Monitor\n\nEnables/Disables read/write monitor.')
        self.lbl_hdd_write_mon.setToolTip( "Disk Write Monitor\n\nWrites to disks assigned a disk letter will be displayed on\ncorresponding letters on the keyboard.")
        self.qle_hdd_mon_rgb_on.setToolTip('Disk Write Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.qle_hdd_led_time_on.setToolTip('Disk Read/Write Monitor\n\nTime Interval:\nMinimum: 0 Seconds\nMaximum: 5 seconds\n\nQuality: 0\nPerformance: 1-5\n\n(Applies to both disk reads & disk writes).')
        self.lbl_hdd_read_mon.setToolTip("Disk Read Monitor\n\nDisks assigned a disk letter that are being read will be displayed on\ncorresponding letters on the keyboard.")
        self.qle_hdd_read_mon_rgb_on.setToolTip('Disk Read Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.btn_network_adapter.setToolTip('Network Traffic Monitor\n\nEnables/Disables network traffic monitor.')
        self.lbl_network_adapter.setToolTip('Network Traffic Monitor\n\nNetwork Bytes Sent:\nNumber of Bytes: F1 - F9\nBytes: Red\nKB: Green\nMB: Blue\nGB: Light Blue\nTB: White\nF10: Units (Red) Tens (Blue) Hundreds (Light Blue) Thousands+ (White).\n\nNetwork Bytes Received:\nNumber of Bytes: 1 - 9\nBytes: Red\nKB: Green\nMB: Blue\nGB: Light Blue\nTB: White\n10: Units (Red) Tens (Blue) Hundreds (Light Blue) Thousands+ (White).')
        self.cmb_network_adapter_name.setToolTip('Network Traffic Monitor\n\nSelect network adapter to monitor sent/received\nnetwork traffic information which will\nbe displayed on the keyboard.')
        self.btn_network_adapter_refresh.setToolTip('Network Traffic Monitor\n\nRefresh list of network adapters.')
        self.qle_network_adapter_led_time_on.setToolTip('Network Traffic Monitor\n\nTime Interval:\nMinimum: 0.0 Seconds\nMaximum: 5 seconds\n\nQuality: 0.0\nPerformance: 1-5.')
        self.btn_net_con_kb.setToolTip('Internet Connection Monitor\n\nEnables/Disables internet connection monitor on the keyboard.')
        self.btn_net_con_mouse.setToolTip('Internet Connection Monitor\n\nEnables/Disables internet connection monitor on the mouse.')
        self.lbl_net_con_mouse.setToolTip( 'Internet Connection Monitor\n\nInternet connection status is\ndisplayed on a mouse.')
        self.lbl_net_con_kb.setToolTip(  'Internet Connection Monitor\n\nInternet connection status is\ndisplayed on a keyboard.')
        self.btn_net_con_mouse_led_selected_prev.setToolTip('Internet Connection Monitor\n\nSelect Previous mouse LED in which to\ndisplay internet connection status.')
        self.btn_net_con_mouse_led_selected_next.setToolTip('Internet Connection Monitor\n\nSelect Next mouse LED in which to\ndisplay internet connection status.')
        self.lbl_net_con_mouse_led_selected.setToolTip('Internet Connection Monitor\n\nDisplays which mouse LED will display internet connection status.')
        self.lbl_exclusive_con.setToolTip('Exclusive Control\n\nThis setting when enabled gives iCUE-Display full\ncontrol of connected iCUE devices.\n\nIt is recommended to keep this option enabled unless you know what you are doing.')
        self.btn_exclusive_con.setToolTip('Exclusive Control\n\nEnables/Disables iCUE-Display exclusive control.')
        self.lbl_run_startup.setToolTip('Start Automatically\n\niCUE-Display can start automatically when you log in.')
        self.btn_run_startup.setToolTip('Start Automatically\n\nEnables/Disables iCUE-Display automatic startup.')
        self.lbl_start_minimized.setToolTip('Start Minimized\n\nWhen launching iCUE-Display, the\napplication will be minimized to taskbar.\n\nThis Feature is useful when automatic\nstartup is also enabled.')
        self.btn_start_minimized.setToolTip('Start Minimized\n\nEnables/Disables iCUE-Display window starting minimized\nwhen launched.')
        self.lbl_netshare_mon.setToolTip("Network Share Monitor\n\nPrntScr:           IPC$ Default Share\nScrLck:            ADMIN$ Default Share\nPause/Break:  Disks Default Share\nHome:            Non-Default Shares")
        self.btn_netshare_mon.setToolTip('Network Share Monitor\n\nEnables/Disables iCUE-Display Network Share Monitor.')
        self.qle_netshare_mon_rgb_on.setToolTip('Network Share Monitor\n\nSet RGB color values for when an indication\nlight is ON.')
        self.btn_bck_light.setToolTip('Backlight\n\nEnable/Disable')
        self.btn_refresh_recompile.setToolTip('Refresh\n')
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

        self.lbl_execution_policy = QLabel(self)
        self.lbl_execution_policy.move(4, 60)
        self.lbl_execution_policy.resize(self.width - 8, self.height - 100)
        self.lbl_execution_policy.setFont(self.font_s7b)
        self.lbl_execution_policy.setText('To enable all features the Execution Policy must be unrestricted.\nWould you like to change the execution policy to unrestricted?')
        self.lbl_execution_policy.setAlignment(Qt.AlignCenter)
        self.lbl_execution_policy.setStyleSheet(self.lbl_menu_style)
        print('-- [App.__init__] created:', self.lbl_execution_policy)
        ui_object_complete.append(self.lbl_execution_policy)
        ui_object_font_list_s7b.append(self.lbl_execution_policy)

        btn_execution_policy_0_pos_w = int((self.width / 2) - 54)
        self.btn_execution_policy_0 = QPushButton(self)
        self.btn_execution_policy_0.move(btn_execution_policy_0_pos_w, self.height - 4 - 40)
        self.btn_execution_policy_0.resize(52, 20)
        self.btn_execution_policy_0.setFont(self.font_s7b)
        self.btn_execution_policy_0.setText('Yes')
        self.btn_execution_policy_0.setStyleSheet(self.btn_menu_style)
        self.btn_execution_policy_0.clicked.connect(self.btn_execution_policy_0_function)
        print('-- [App.__init__] created:', self.btn_execution_policy_0)
        self.object_interaction_enabled.append(self.btn_execution_policy_0)
        ui_object_complete.append(self.btn_execution_policy_0)
        ui_object_font_list_s7b.append(self.btn_execution_policy_0)

        btn_execution_policy_1_pos_w = int((self.width / 2) + 2)
        self.btn_execution_policy_1 = QPushButton(self)
        self.btn_execution_policy_1.move(btn_execution_policy_1_pos_w, self.height - 4 - 40)
        self.btn_execution_policy_1.resize(52, 20)
        self.btn_execution_policy_1.setFont(self.font_s7b)
        self.btn_execution_policy_1.setText('No')
        self.btn_execution_policy_1.setStyleSheet(self.btn_menu_style)
        self.btn_execution_policy_1.clicked.connect(self.btn_execution_policy_1_function)
        print('-- [App.__init__] created:', self.btn_execution_policy_1)
        self.object_interaction_enabled.append(self.btn_execution_policy_1)
        ui_object_complete.append(self.btn_execution_policy_1)
        ui_object_font_list_s7b.append(self.btn_execution_policy_1)

        """ check execution policy """
        self.get_execution_policy()

        if bool_execution_policy is False:
            bool_execution_policy_show = True
            self.feature_pg_execution_policy()

        elif bool_execution_policy is True:
            bool_execution_policy_show = False
            self.feature_pg_home()

        # time.sleep(2)
        event_filter_self.append(self)
        self.filter = ObjEveFilter()
        self.installEventFilter(self.filter)

        self.initUI()

    def icuedisplay_quit_function(self):
        global thread_compile_devices, thread_keyevents, thread_exclusive_gkey_event_unmount, thread_exclusive_gkey_event_mount
        global thread_gkey_pressed, thread_sdk_event_handler, thread_test_locked

        thread_keyevents[0].stop()
        thread_exclusive_gkey_event_unmount[0].stop()
        thread_exclusive_gkey_event_mount[0].stop()
        thread_gkey_pressed[0].stop()
        thread_sdk_event_handler[0].stop()
        thread_test_locked[0].stop()
        thread_compile_devices[0].stop()

        self.QCoreApplication.instance().quit

    def btn_fahrenheit_function(self):
        print('-- [btn_fahrenheit_function]: plugged in')
        global bool_switch_fahrenheit

        self.setFocus()

        if bool_switch_fahrenheit is True:
            if self.write_engaged is False:
                print('-- [App.btn_fahrenheit_function] changing bool_switch_fahrenheit:', bool_switch_fahrenheit)
                self.write_var = 'bool_switch_fahrenheit: false'
                self.write_changes()
            self.btn_fahrenheit.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_util_key_8.setText('>70°C')
            self.lbl_util_key_6.setText('>=50°C  <70°C')
            self.lbl_util_key_4.setText('>=30°C  <50°C')
            self.lbl_util_key_2.setText('<30°C')
            bool_switch_fahrenheit = False

        elif bool_switch_fahrenheit is False:
            if self.write_engaged is False:
                print('-- [App.btn_fahrenheit_function] changing bool_switch_fahrenheit:', bool_switch_fahrenheit)
                self.write_var = 'bool_switch_fahrenheit: true'
                self.write_changes()
            self.btn_fahrenheit.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_util_key_8.setText('>158°F')
            self.lbl_util_key_6.setText('>=122°F  <158°F')
            self.lbl_util_key_4.setText('>=86°F   <122°F')
            self.lbl_util_key_2.setText('<86°F')
            bool_switch_fahrenheit = True

    def btn_g5_backlight_function(self):
        print('-- [btn_g5_backlight_function]: plugged in')
        global bool_backlight_interact

        self.setFocus()

        if bool_backlight_interact is True:
            if self.write_engaged is False:
                print('-- [App.btn_powershell_function] changing bool_backlight_interact:', bool_backlight_interact)
                self.write_var = 'bool_backlight_interact: false'
                self.write_changes()
            self.btn_g5_backlight.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            bool_backlight_interact = False

        elif bool_backlight_interact is False:
            if self.write_engaged is False:
                print('-- [App.btn_powershell_function] changing bool_backlight_interact:', bool_backlight_interact)
                self.write_var = 'bool_backlight_interact: true'
                self.write_changes()
            self.btn_g5_backlight.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            bool_backlight_interact = True

    def btn_powershell_function(self):
        print('-- [btn_powershell_function]: plugged in')
        global bool_powershell_interact

        self.setFocus()

        if bool_powershell_interact is True:
            if self.write_engaged is False:
                print('-- [App.btn_powershell_function] changing bool_powershell_interact:', bool_powershell_interact)
                self.write_var = 'bool_powershell_interact: false'
                self.write_changes()
            self.btn_powershell.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            bool_powershell_interact = False

        elif bool_powershell_interact is False:
            if self.write_engaged is False:
                print('-- [App.btn_powershell_function] changing bool_powershell_interact:', bool_powershell_interact)
                self.write_var = 'bool_powershell_interact: true'
                self.write_changes()
            self.btn_powershell.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            bool_powershell_interact = True

    def btn_power_plan_function(self):
        print('-- [btn_power_plan_function]: plugged in')
        global bool_power_plan_interact, thread_power
        self.setFocus()

        if bool_power_plan_interact is True:
            if self.write_engaged is False:
                print('-- [App.btn_power_plan_function] changing bool_power_plan_interact:', bool_power_plan_interact)
                self.write_var = 'bool_power_plan_interact: false'
                self.write_changes()
            self.btn_power_plan.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            bool_power_plan_interact = False
            thread_power[0].stop()

        elif bool_power_plan_interact is False:
            if self.write_engaged is False:
                print('-- [App.btn_power_plan_function] changing bool_power_plan_interact:', bool_power_plan_interact)
                self.write_var = 'bool_power_plan_interact: true'
                self.write_changes()
            self.btn_power_plan.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            bool_power_plan_interact = True
            thread_power[0].start()

        print('-- [btn_power_plan_function] setting bool_power_plan_interact:', bool_power_plan_interact)

    def btn_g2_disk_function(self):
        print('-- [btn_g2_disk_function]: plugged in')
        global bool_switch_g2_disks, thread_eject, thread_mount, thread_unmount
        self.setFocus()

        if bool_switch_g2_disks is True:
            if self.write_engaged is False:
                print('-- [App.btn_g2_disk_function] changing bool_switch_g2_disks:', bool_switch_g2_disks)
                self.write_var = 'bool_switch_g2_disks: false'
                self.write_changes()
            self.btn_g2_disk.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            bool_switch_g2_disks = False

        elif bool_switch_g2_disks is False:
            if self.write_engaged is False:
                print('-- [App.btn_g2_disk_function] changing bool_switch_g2_disks:', bool_switch_g2_disks)
                self.write_var = 'bool_switch_g2_disks: true'
                self.write_changes()
            self.btn_g2_disk.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            bool_switch_g2_disks = True

        print('-- [btn_power_plan_function] setting bool_switch_g2_disks:', bool_switch_g2_disks)

    def btn_execution_policy_0_function(self):
        global bool_execution_policy_show
        print('-- [btn_execution_policy_0_function] unrestricted execution policy accepted: plugged in')
        try:
            cmd = 'powershell Set-ExecutionPolicy Unrestricted'
            xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info)
        except Exception as e:
            print('-- [btn_execution_policy_0_function] Error:', e)
        bool_execution_policy_show = False
        self.feature_pg_home()

    def btn_execution_policy_1_function(self):
        global bool_execution_policy_show
        print('-- [btn_execution_policy_1_function]unrestricted execution policy declined: plugged in')
        bool_execution_policy_show = False
        self.feature_pg_home()

    def get_execution_policy(self):
        print('-- [get_execution_policy]: plugged in')
        global bool_execution_policy
        cmd_output = []
        cmd = 'powershell Get-ExecutionPolicy'
        xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, startupinfo=info)
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
            print('-- [get_execution_policy] ExecutionPolicy:', _)
            if _ != 'Unrestricted':
                bool_execution_policy = False
            elif _ == 'Unrestricted':
                bool_execution_policy = True

    def btn_media_display_function(self):
        print('-- [App.btn_media_display_function]: plugged in')
        global thread_media_display, bool_switch_startup_media_display, bool_execution_policy
        self.setFocus()
        self.get_execution_policy()

        if bool_switch_startup_media_display is True:
            thread_media_display[0].stop()
            if self.write_engaged is False:
                print('-- [App.btn_media_display_function] changing bool_switch_startup_media_display:', bool_switch_startup_media_display)
                self.write_var = 'bool_switch_startup_media_display: false'
                self.write_changes()
            self.btn_media_display.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_media_display.setStyleSheet(self.btn_menu_style_1)
            bool_switch_startup_media_display = False

        elif bool_switch_startup_media_display is False:
            self.btn_media_display.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_media_display.setStyleSheet(self.btn_menu_style)
            if bool_execution_policy is True:
                thread_media_display[0].start()
                if self.write_engaged is False:
                    print('-- [App.btn_media_display_function] changing bool_switch_startup_media_display:', bool_switch_startup_media_display)
                    self.write_var = 'bool_switch_startup_media_display: true'
                    self.write_changes()
                bool_switch_startup_media_display = True
            else:
                self.btn_media_display.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                self.lbl_media_display.setStyleSheet(self.btn_menu_style_1)

    def btn_cpu_mon_temp_function(self):
        print('-- [App.btn_cpu_mon_temp_function]: plugged in')
        global thread_temperatures
        global bool_cpu_temperature, bool_vram_temperature
        self.setFocus()
        thread_temperatures[0].stop()
        if bool_cpu_temperature is True:
            if self.write_engaged is False:
                print('-- [App.btn_cpu_mon_temp_function] changing bool_cpu_temperature:', bool_cpu_temperature)
                self.write_var = 'bool_cpu_temperature: false'
                self.write_changes()
            self.btn_cpu_mon_temp.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_cpu_mon_temp.setStyleSheet(self.btn_menu_style)
            bool_cpu_temperature = False
        elif bool_cpu_temperature is False:
            if self.write_engaged is False:
                print('-- [App.btn_cpu_mon_temp_function] changing bool_cpu_temperature:', bool_cpu_temperature)
                self.write_var = 'bool_cpu_temperature: true'
                self.write_changes()
            self.btn_cpu_mon_temp.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_cpu_mon_temp.setStyleSheet(self.btn_menu_style_1)
            bool_cpu_temperature = True
        if bool_vram_temperature is True or bool_cpu_temperature is True:
            print('-- [App.btn_cpu_mon_temp_function]: starting thread_temperatures')
            thread_temperatures[0].start()
        else:
            print('-- [App.btn_cpu_mon_temp_function]: bool_cpu_temperature, bool_vram_temperature', bool_cpu_temperature, bool_vram_temperature)

    def btn_vram_mon_temp_function(self):
        print('-- [App.btn_vram_mon_temp_function]: plugged in')
        global thread_temperatures
        global bool_vram_temperature, bool_cpu_temperature
        thread_temperatures[0].stop()
        if bool_vram_temperature is True:
            if self.write_engaged is False:
                print('-- [App.btn_vram_mon_temp_function] changing bool_vram_temperature:', bool_vram_temperature)
                self.write_var = 'bool_vram_temperature: false'
                self.write_changes()
            self.btn_vram_mon_temp.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_vram_mon_temp.setStyleSheet(self.btn_menu_style)
            bool_vram_temperature = False
        elif bool_vram_temperature is False:
            if self.write_engaged is False:
                print('-- [App.btn_vram_mon_temp_function] changing bool_vram_temperature:', bool_vram_temperature)
                self.write_var = 'bool_vram_temperature: true'
                self.write_changes()
            self.btn_vram_mon_temp.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_vram_mon_temp.setStyleSheet(self.btn_menu_style_1)
            bool_vram_temperature = True
        if bool_vram_temperature is True or bool_cpu_temperature is True:
            print('-- [App.btn_cpu_mon_temp_function]: starting thread_temperatures')
            thread_temperatures[0].start()
        else:
            print('-- [App.btn_cpu_mon_temp_function]: bool_cpu_temperature, bool_vram_temperature', bool_cpu_temperature, bool_vram_temperature)

    def btn_con_stat_kb_img_function(self):
        print('-- [App.btn_con_stat_kb_img_function]: plugged in')
        global str_path_kb_img
        self.setFocus()

        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select Keyboard Image", "", "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.btn_con_stat_kb_img_function] file selected:', fileName)
                str_path_kb_img = fileName
                if self.write_engaged is False:
                    print('-- [App.btn_con_stat_kb_img_function] changing str_path_kb_img:', str_path_kb_img)
                    self.write_var = 'str_path_kb_img: '+str_path_kb_img
                    self.write_changes()
                    self.btn_con_stat_kb_img.setIcon(QIcon(str_path_kb_img))
                    self.btn_con_stat_kb_img.setStyleSheet(self.btn_status_style)
                    self.btn_con_stat_kb_img.setText('')

    def btn_con_stat_ms_img_function(self):
        print('-- [App.btn_con_stat_ms_img_function]: plugged in')
        global str_path_ms_img
        self.setFocus()
        if len(devices_kb) > 0:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, "Select Mouse Image", "", "All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                print('-- [App.btn_con_stat_ms_img_function] file selected:', fileName)
                str_path_ms_img = fileName
                if self.write_engaged is False:
                    print('-- [App.btn_con_stat_ms_img_function] changing str_path_kb_img:', str_path_ms_img)
                    self.write_var = 'str_path_ms_img: ' + str_path_ms_img
                    self.write_changes()
                    self.btn_con_stat_ms_img.setIcon(QIcon(str_path_ms_img))
                    self.btn_con_stat_ms_img.setStyleSheet(self.btn_status_style)
                    self.btn_con_stat_ms_img.setText('')

    def recompile(self):
        print('-- [App.recompile]: plugged in')
        global thread_compile_devices, devices_previous
        print('-- [App.recompile] stopping thread: thread_compile_devices:')
        thread_compile_devices[0].stop()
        devices_previous = []
        print('-- [App.recompile] starting thread: thread_compile_devices:')
        thread_compile_devices[0].start()

    def hide_all_features(self):
        print('-- [App.hide_all_features]: plugged in')
        global ui_object_complete
        self.setFocus()
        try:
            for _ in ui_object_complete:
                _.hide()
            """ title bar """
            self.lbl_title.show()
            self.btn_minimize.show()
            self.btn_quit.show()
            self.btn_bck_light.show()
            self.btn_refresh_recompile.show()
            """ connection status """
            self.btn_con_stat_name.show()
            """ connected devices """
            if len(devices_kb) > 0:
                self.btn_con_stat_kb_img.show()
                self.lbl_con_stat_kb.show()
            if len(devices_ms) > 0:
                self.btn_con_stat_ms_img.show()
                self.lbl_con_stat_mouse.show()
            """ side menu """
            self.btn_feature_page_home.show()
            self.btn_feature_page_home.setStyleSheet(self.btn_side_menu_style_1)
            self.btn_feature_page_util.show()
            self.btn_feature_page_util.setStyleSheet(self.btn_side_menu_style_1)
            self.btn_feature_page_disks.show()
            self.btn_feature_page_disks.setStyleSheet(self.btn_side_menu_style_1)
            self.btn_feature_page_network_traffic.show()
            self.btn_feature_page_network_traffic.setStyleSheet(self.btn_side_menu_style_1)
            self.btn_feature_page_networking.show()
            self.btn_feature_page_networking.setStyleSheet(self.btn_side_menu_style_1)
            self.btn_feature_page_gkeys.show()
            self.btn_feature_page_gkeys.setStyleSheet(self.btn_side_menu_style_1)
            self.btn_feature_page_settings.show()
            self.btn_feature_page_settings.setStyleSheet(self.btn_side_menu_style_1)

        except Exception as e:
            print(e)

    def feature_page_gkeys_function(self):
        print('-- [App.feature_page_gkeys_function]: plugged in')
        self.hide_all_features()
        self.lbl_settings_bg.show()

        self.btn_feature_page_gkeys.setStyleSheet(self.btn_side_menu_style)
        self.lbl_power_plan.show()
        self.btn_power_plan.show()

        self.lbl_power_plan_key_0.show()
        self.lbl_power_plan_key_1.show()
        self.lbl_power_plan_key_2.show()
        self.lbl_power_plan_key_3.show()
        self.lbl_power_plan_key_4.show()
        self.lbl_power_plan_key_5.show()
        self.lbl_power_plan_key_6.show()
        self.lbl_power_plan_key_7.show()

        self.lbl_powershell.show()
        self.btn_powershell.show()
        self.lbl_g5_backlight.show()
        self.btn_g5_backlight.show()

        self.lbl_g2_disk.show()
        self.btn_g2_disk.show()

    def feature_pg_execution_policy(self):
        print('-- [App.feature_pg_execution_policy]: plugged in')
        self.hide_all_features()

        self.btn_bck_light.hide()
        self.btn_refresh_recompile.hide()
        """ connection status """
        self.btn_con_stat_name.hide()
        """ connected devices """
        self.btn_con_stat_kb_img.hide()
        self.lbl_con_stat_kb.hide()
        self.btn_con_stat_ms_img.hide()
        self.lbl_con_stat_mouse.hide()
        """ side menu """
        self.btn_feature_page_home.hide()
        self.btn_feature_page_util.hide()
        self.btn_feature_page_disks.hide()
        self.btn_feature_page_network_traffic.hide()
        self.btn_feature_page_networking.hide()
        self.btn_feature_page_gkeys.hide()
        self.btn_feature_page_settings.hide()

        self.lbl_execution_policy.show()
        self.btn_execution_policy_0.show()
        self.btn_execution_policy_1.show()

    def feature_pg_home(self):
        print('-- [App.feature_pg_home]: plugged in')
        self.hide_all_features()
        self.btn_feature_page_home.setStyleSheet(self.btn_side_menu_style)

    def feature_pg_util(self):
        print('-- [App.feature_pg_util]: plugged in')
        self.hide_all_features()
        self.lbl_settings_bg.show()
        self.btn_feature_page_util.setStyleSheet(self.btn_side_menu_style)
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
        self.lbl_cpu_mon_temp.show()
        self.lbl_vram_mon_temp.show()
        self.btn_cpu_mon_temp.show()
        self.btn_vram_mon_temp.show()
        self.lbl_util_key_1.show()
        self.lbl_util_key_2.show()
        self.lbl_util_key_3.show()
        self.lbl_util_key_4.show()
        self.lbl_util_key_5.show()
        self.lbl_util_key_6.show()
        self.lbl_util_key_7.show()
        self.lbl_util_key_8.show()

    def btn_feature_page_disk_util(self):
        print('-- [App.btn_feature_page_disk_util]: plugged in')
        self.hide_all_features()
        self.lbl_settings_bg.show()
        self.btn_feature_page_disks.setStyleSheet(self.btn_side_menu_style)
        self.lbl_hdd_mon_sub.show()
        self.lbl_hdd_write_mon.show()
        self.btn_hdd_mon.show()
        self.qle_hdd_mon_rgb_on.show()
        self.qle_hdd_led_time_on.show()
        self.lbl_hdd_read_mon.show()
        self.qle_hdd_read_mon_rgb_on.show()
        self.lbl_disk_key_2.show()
        self.lbl_disk_key_3.show()

    def btn_feature_page_network_traffic_function(self):
        print('-- [App.btn_feature_page_network_traffic_function]: plugged in')
        self.hide_all_features()
        self.lbl_settings_bg.show()
        self.btn_feature_page_network_traffic.setStyleSheet(self.btn_side_menu_style)
        self.lbl_network_adapter.show()
        self.cmb_network_adapter_name.show()
        self.btn_network_adapter_refresh.show()
        self.btn_network_adapter.show()
        self.qle_network_adapter_led_time_on.show()

        self.lbl_nettraffic_key_0.show()
        self.lbl_nettraffic_key_1.show()
        self.lbl_nettraffic_key_2.show()
        self.lbl_nettraffic_key_3.show()
        self.lbl_nettraffic_key_4.show()
        self.lbl_nettraffic_key_5.show()
        self.lbl_nettraffic_key_6.show()
        self.lbl_nettraffic_key_7.show()
        self.lbl_nettraffic_key_8.show()
        self.lbl_nettraffic_key_9.show()
        self.lbl_nettraffic_key_11.show()
        self.lbl_nettraffic_key_12.show()
        self.lbl_nettraffic_key_13.show()
        self.lbl_nettraffic_key_14.show()
        self.lbl_nettraffic_key_15.show()
        self.lbl_nettraffic_key_16.show()
        self.lbl_nettraffic_key_17.show()
        self.lbl_nettraffic_key_18.show()
        self.lbl_nettraffic_key_19.show()
        self.lbl_nettraffic_key_20.show()
        self.lbl_nettraffic_key_21.show()
        self.lbl_nettraffic_key_22.show()

    def btn_feature_page_networking_function(self):
        print('-- [App.btn_feature_page_networking_function]: plugged in')
        self.hide_all_features()
        self.lbl_settings_bg.show()
        self.btn_feature_page_networking.setStyleSheet(self.btn_side_menu_style)
        self.lbl_net_con_mouse.show()
        self.btn_net_con_mouse.show()
        self.btn_net_con_mouse_led_selected_prev.show()
        self.lbl_net_con_mouse_led_selected.show()
        self.btn_net_con_mouse_led_selected_next.show()
        self.lbl_net_con_kb.show()
        self.btn_net_con_kb.show()
        self.lbl_netshare_mon.show()
        self.btn_netshare_mon.show()
        self.qle_netshare_mon_rgb_on.show()
        self.lbl_net_con_mouse_key_1.show()
        self.lbl_net_con_mouse_key_2.show()
        self.lbl_net_con_mouse_key_3.show()
        self.lbl_net_con_mouse_key_4.show()
        self.lbl_net_con_mouse_key_5.show()
        self.lbl_net_con_mouse_key_6.show()

    def btn_feature_page_settings_function(self):
        print('-- [App.btn_feature_page_settings_function]: plugged in')
        self.hide_all_features()
        self.lbl_settings_bg.show()
        self.btn_feature_page_settings.setStyleSheet(self.btn_side_menu_style)
        self.lbl_exclusive_con.show()
        self.btn_exclusive_con.show()
        self.lbl_run_startup.show()
        self.btn_run_startup.show()
        self.lbl_start_minimized.show()
        self.btn_start_minimized.show()
        self.lbl_backlight_sub.show()
        self.btn_backlight_sub.show()
        self.qle_backlight_rgb_on.show()
        self.lbl_backlight_auto.show()
        self.btn_backlight_auto.show()
        self.btn_backlight_auto_time_0.show()
        self.btn_backlight_auto_time_1.show()
        self.lbl_media_display.show()
        self.btn_media_display.show()
        self.lbl_fahrenheit.show()
        self.btn_fahrenheit.show()

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
            if float(self.write_var_float) >= 0.1 and float(self.write_var_float) <= 5 and self.write_var_key != 3 and self.write_var_key != 4:
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
        global bool_power_plan_interact, bool_backlight_interact, bool_powershell_interact
        for _ in self.object_interaction_enabled:
            _.setEnabled(True)

    def isenabled_false(self):
        print('-- [App.isenabled_false]: plugged in')
        global bool_power_plan_interact
        for _ in self.object_interaction_enabled:
            _.setEnabled(False)

    def read_only_true(self):
        print('-- [App.read_only_true]: plugged in')
        for _ in self.object_interaction_readonly:
            _.setReadOnly(True)

    def read_only_false(self):
        print('-- [App.read_only_false]: plugged in')
        for _ in self.object_interaction_readonly:
            _.setReadOnly(False)

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

    def color_all_id(self):
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight, bool_switch_backlight, sdk_color_backlight_on

        global devices_kb, devices_ms
        global thread_net_connection
        global thread_media_display, bool_switch_startup_media_display
        global thread_power, bool_power_plan_interact

        zone_id = [170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188]

        if len(devices_kb) > 0:
            for _ in corsairled_id_num_kb_complete:
                if _ not in zone_id:
                    itm = [{_: sdk_color_backlight}]
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
                    except Exception as e:
                        print(e)

        if len(devices_ms) > 0:
            for _ in corsairled_id_num_ms_complete:
                itm = [{_: sdk_color_backlight}]
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], itm[0])
                except Exception as e:
                    print(e)

        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if bool_switch_startup_net_con_kb is True or bool_switch_startup_net_con_ms is True:
                thread_net_connection[0].stop()
                thread_net_connection[0].start()
            if bool_switch_startup_media_display is True:
                thread_media_display[0].stop()
                thread_media_display[0].start()
            if bool_power_plan_interact is True:
                thread_power[0].stop()
                thread_power[0].start()

    def btn_bck_light_function(self):
        print('-- [App.btn_bck_light_function]: plugged in')
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight
        global sdk_color_backlight, bool_switch_backlight, sdk_color_backlight_on
        global thread_disk_rw
        self.setFocus()
        if self.write_engaged is False:
            if bool_switch_backlight is False:
                self.write_var = 'bool_switch_backlight: true'
                self.write_changes()
                sdk_color_backlight = sdk_color_backlight_on
                bool_switch_backlight = True
                print('-- [App.btn_bck_light_function] setting bool_switch_backlight:', bool_switch_backlight)
                self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_0)
                self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style_1)
            elif bool_switch_backlight is True:
                self.write_var = 'bool_switch_backlight: false'
                self.write_changes()
                sdk_color_backlight = (0, 0, 0)
                bool_switch_backlight = False
                print('-- [App.btn_bck_light_function] setting bool_switch_backlight:', bool_switch_backlight)
                self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_1)
                self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style)
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
                        self.lbl_backlight_auto.setStyleSheet(self.btn_menu_style)
                        self.write_changes()
                    elif bool_switch_backlight_auto is False:
                        thread_backlight_auto[0].start()
                        bool_switch_backlight_auto = True
                        self.write_var = 'bool_switch_backlight_auto: true'
                        self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                        self.lbl_backlight_auto.setStyleSheet(self.btn_menu_style_1)
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
                    self.lbl_exclusive_con.setStyleSheet(self.btn_menu_style_1)
                elif bool_switch_startup_exclusive_control is True:
                    print('-- [App.btn_exclusive_con_function] exclusive access request changed: releasing control')
                    self.write_var = 'exclusive_access: false'
                    sdk.release_control()
                    bool_switch_startup_exclusive_control = False
                    self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_exclusive_con.setStyleSheet(self.btn_menu_style)
                self.write_changes()
                # self.recompile()

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
                self.lbl_run_startup.setStyleSheet(self.btn_menu_style)
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
                    self.lbl_run_startup.setStyleSheet(self.btn_menu_style_1)
                    bool_switch_startup_autorun = True
                    self.write_var = 'run_startup: true'
                    self.write_changes()
                elif not os.path.exists(shortcut_out):
                    print('-- [App.btn_run_startup_function]: shortcut file failed to be created')
                    self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_run_startup.setStyleSheet(self.btn_menu_style)

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
                self.lbl_start_minimized.setStyleSheet(self.btn_menu_style)
            elif bool_switch_startup_minimized is False:
                bool_switch_startup_minimized = True
                print('-- [App.btn_start_minimized_function] setting bool_switch_startup_minimized:', bool_switch_startup_minimized)
                self.write_var = 'start_minimized: true'
                self.write_changes()
                self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                self.lbl_start_minimized.setStyleSheet(self.btn_menu_style_1)

    def btn_cpu_mon_function(self):
        print('-- [App.btn_cpu_mon_function]: plugged in')
        global bool_switch_startup_cpu_util, thread_cpu_util
        global devices_kb, devices_ms
        self.setFocus()
        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_cpu_util is True:
                    print('-- [App.btn_cpu_mon_function] stopping thread: thread_cpu_util:')
                    thread_cpu_util[0].stop()
                    self.write_var = 'cpu_startup: false'
                    bool_switch_startup_cpu_util = False
                    self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_cpu_mon.setStyleSheet(self.btn_menu_style)
                    self.write_changes()
                elif bool_switch_startup_cpu_util is False:
                    print('-- [App.btn_cpu_mon_function] starting thread: thread_cpu_util:')
                    thread_cpu_util[0].start()
                    self.write_var = 'cpu_startup: true'
                    bool_switch_startup_cpu_util = True
                    self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_cpu_mon.setStyleSheet(self.btn_menu_style_1)
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
        global bool_switch_startup_dram_util, thread_dram_util
        global devices_kb
        self.setFocus()
        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_dram_util is True:
                    print('-- [App.btn_dram_mon_function] stopping thread: thread_dram_util:')
                    thread_dram_util[0].stop()
                    self.write_var = 'dram_startup: false'
                    bool_switch_startup_dram_util = False
                    self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_dram_mon.setStyleSheet(self.btn_menu_style)
                elif bool_switch_startup_dram_util is False:
                    print('-- [App.btn_dram_mon_function] starting thread: thread_dram_util:')
                    thread_dram_util[0].start()
                    self.write_var = 'dram_startup: true'
                    bool_switch_startup_dram_util = True
                    self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_dram_mon.setStyleSheet(self.btn_menu_style_1)
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
        global bool_switch_startup_vram_util, thread_vram_util
        global devices_kb
        self.setFocus()
        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_vram_util is True:
                    print('-- [App.btn_vram_mon_function] stopping thread: thread_vram_util:')
                    thread_vram_util[0].stop()
                    self.write_var = 'vram_startup: false'
                    bool_switch_startup_vram_util = False
                    self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_vram_mon.setStyleSheet(self.btn_menu_style)
                elif bool_switch_startup_vram_util is False:
                    print('-- [App.btn_vram_mon_function] starting thread: thread_vram_util:')
                    thread_vram_util[0].start()
                    self.write_var = 'vram_startup: true'
                    bool_switch_startup_vram_util = True
                    self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_vram_mon.setStyleSheet(self.btn_menu_style_1)
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
        global bool_switch_startup_hdd_read_write, thread_disk_rw
        global devices_kb
        self.setFocus()
        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_hdd_read_write is True:
                    print('-- [App.btn_hdd_mon_function] stopping thread: thread_disk_rw:')
                    thread_disk_rw[0].stop()
                    self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_hdd_mon_sub.setStyleSheet(self.btn_menu_style)
                    self.write_var = 'hdd_startup: false'
                    bool_switch_startup_hdd_read_write = False
                    self.write_changes()
                elif bool_switch_startup_hdd_read_write is False:
                    print('-- [App.btn_hdd_mon_function] starting thread: thread_disk_rw:')
                    thread_disk_rw[0].start()
                    self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_hdd_mon_sub.setStyleSheet(self.btn_menu_style_1)
                    self.write_var = 'hdd_startup: true'
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
        global bool_switch_startup_net_traffic, thread_net_traffic
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
                    self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_network_adapter.setStyleSheet(self.btn_menu_style)
                elif bool_switch_startup_net_traffic is False:
                    bool_switch_startup_net_traffic = True
                    print('-- [App.btn_network_adapter_function] starting thread: thread_net_traffic:')
                    thread_net_traffic[0].start()
                    self.write_var = 'network_adapter_startup: true'
                    self.write_changes()
                    self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_network_adapter.setStyleSheet(self.btn_menu_style_1)

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
        global thread_net_connection, devices_kb, devices_ms
        self.setFocus()
        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_con_ms is True:
                    bool_switch_startup_net_con_ms = False
                    print('-- [App.btn_net_con_mouse_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    self.write_var = 'bool_switch_startup_net_con_ms: false'
                    self.write_changes()
                    self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_net_con_mouse.setStyleSheet(self.btn_menu_style)
                    if bool_switch_startup_net_con_kb is False:
                        self.write_var = 'bool_switch_startup_net_con: false'
                        self.write_changes()
                        bool_switch_startup_net_con = False
                        self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                        self.lbl_net_con_mouse.setStyleSheet(self.btn_menu_style)
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
                    self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_net_con_mouse.setStyleSheet(self.btn_menu_style_1)
                    self.write_var = 'bool_switch_startup_net_con: true'
                    self.write_changes()
                    bool_switch_startup_net_con = True

    def btn_net_con_kb_function(self):
        print('-- [App.btn_net_con_kb_function]: plugged in')
        global bool_switch_startup_net_con_kb, bool_switch_startup_net_con, bool_switch_startup_net_con_ms
        global thread_net_connection, devices_ms, devices_kb
        self.setFocus()
        if len(devices_kb) > 0 or len(devices_ms) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_con_kb is True:
                    bool_switch_startup_net_con_kb = False
                    print('-- [App.btn_net_con_kb_function] stopping thread: thread_net_connection')
                    thread_net_connection[0].stop()
                    self.write_var = 'bool_switch_startup_net_con_kb: false'
                    self.write_changes()
                    self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_net_con_kb.setStyleSheet(self.btn_menu_style)
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
                    self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_net_con_kb.setStyleSheet(self.btn_menu_style_1)
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
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
                    except Exception as e:
                        print(e)
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
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
                    except Exception as e:
                        print(e)
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
        global bool_switch_startup_net_share_mon, thread_net_share
        global devices_ms, devices_kb
        self.setFocus()
        if len(devices_kb) > 0:
            if self.write_engaged is False:
                if bool_switch_startup_net_share_mon is True:
                    print('-- [App.btn_defnetshare_function] stopping: thread_net_share')
                    thread_net_share[0].stop()
                    self.write_var = 'netshare_startup: false'
                    bool_switch_startup_net_share_mon = False
                    self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                    self.lbl_netshare_mon.setStyleSheet(self.btn_menu_style)
                elif bool_switch_startup_net_share_mon is False:
                    print('-- [App.btn_defnetshare_function] starting: thread_net_share')
                    thread_net_share[0].start()
                    self.write_var = 'netshare_startup: true'
                    bool_switch_startup_net_share_mon = True
                    self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                    self.lbl_netshare_mon.setStyleSheet(self.btn_menu_style_1)
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
        global devices_kb, bool_power_plan_interact, power_plan, power_plan_index
        global notification_key
        self.setFocus()

        print('-- [App.g1_function_short]: plugged in')
        if len(devices_kb):

            if bool_power_plan_interact is True:
                print('-- [App.g1_function_short] cycling power plan')
                
                if power_plan_index < 3:
                    power_plan_index += 1
                else:
                    power_plan_index = 0

                try:
                    print('power_plan_index try:', power_plan_index)
                    print('-- [App.g1_function_short] attempting to set power plan:', power_plan[power_plan_index])
                    x = power_plan[power_plan_index]
                    x = x.split()
                    power_plan_guid = x[3].strip()
                    print('-- [App.g1_function_short] isolating GUID:', power_plan_guid)
                    cmd = 'powercfg /SETACTIVE '+power_plan_guid
                    print('running command:', cmd)
                    xcmd = subprocess.Popen(cmd, shell=True, startupinfo=info)


                except Exception as e:
                    print('-- [App.g1_function_short] Error:', e)

    def g1_function_long(self):
        print('-- [App.g1_function_long]: plugged in')
        os.system('shutdown /h')

    def g1_function_long_2sec(self):
        print('-- [App.g1_function_long_2sec]: plugged in')
        os.system('shutdown /r /t 0')

    def g1_function_long_3sec(self):
        print('-- [App.g1_function_long_3sec]: plugged in')
        os.system('shutdown /s /t 0')

    def g2_function_short(self):
        print('-- [App.g2_function_short]: plugged in')

    def g2_function_long(self):
        print('-- [App.g2_function_long]: plugged in')

    def g2_function_long_2sec(self):
        print('-- [App.g2_function_long_2sec]: plugged in')

    def g2_function_long_3sec(self):
        print('-- [App.g2_function_long_3sec]: plugged in')

    def g3_function_short(self):
        print('-- [App.g3_function_short]: plugged in')

    def g3_function_long(self):
        print('-- [App.g3_function_long]: plugged in')

    def g3_function_long_2sec(self):
        print('-- [App.g3_function_long_2sec]: plugged in')

    def g3_function_long_3sec(self):
        print('-- [App.g3_function_long_3sec]: plugged in')

    def g4_function_short(self):
        print('-- [App.g4_function_short]: plugged in')

    def g4_function_long(self):
        print('-- [App.g4_function_long]: plugged in')

    def g4_function_long_2sec(self):
        print('-- [App.g4_function_long_2sec]: plugged in')

    def g4_function_long_3sec(self):
        print('-- [App.g4_function_long_3sec]: plugged in')

    def g5_function_short(self):
        global bool_backlight_interact
        print('-- [App.g5_function_short]: plugged in')
        if len(devices_kb) >= 1:
            if bool_backlight_interact is True:
                self.btn_bck_light_function()

    def g5_function_long(self):
        print('-- [App.g5_function_long]: plugged in')

    def g5_function_long_2sec(self):
        print('-- [App.g5_function_long_2sec]: plugged in')

    def g5_function_long_3sec(self):
        print('-- [App.g5_function_long_3sec]: plugged in')

    def g6_function_short(self):
        global bool_powershell_interact
        print('-- [App.g6_function_short]: plugged in')
        if bool_powershell_interact is True:
            print('-- [App.g6_function_short]: attempting to run start powershell')
            os.startfile('powershell')

    def g6_function_long(self):
        print('-- [App.g6_function_long]: plugged in')

    def g6_function_long_2sec(self):
        print('-- [App.g6_function_long_2sec]: plugged in')

    def g6_function_long_3sec(self):
        print('-- [App.g6_function_long_3sec]: plugged in')

    def initUI(self):
        print('-- [App.initUI]: plugged in')
        global sdk
        global bool_backend_allow_display, bool_switch_startup_exclusive_control, bool_switch_startup_minimized, bool_switch_backlight
        global bool_switch_startup_cpu_util, bool_switch_startup_dram_util, bool_switch_startup_vram_util, bool_cpu_temperature, bool_vram_temperature
        global bool_switch_startup_hdd_read_write, bool_switch_startup_net_share_mon, bool_switch_startup_net_traffic
        global bool_switch_backlight_auto, backlight_time_0, backlight_time_1
        global sdk_color_cpu_on, sdk_color_dram_on, sdk_color_vram_on, sdk_color_hddwrite_on, sdk_color_hddread_on, sdk_color_netshare_on, sdk_color_backlight, sdk_color_backlight_on
        global thread_compile_devices
        global thread_disk_rw
        global thread_cpu_util
        global thread_dram_util
        global thread_vram_util
        global thread_net_traffic
        global thread_net_connection
        global thread_net_share
        global thread_sdk_event_handler
        global thread_temperatures
        global thread_backlight_auto
        global thread_media_display
        global thread_pause_loop
        global thread_power
        global thread_test_locked
        global thread_overlay
        global thread_keyevents
        global bool_switch_startup_media_display
        global str_path_kb_img, str_path_ms_img
        global bool_power_plan_interact
        global bool_powershell_interact
        global bool_backlight_interact
        global bool_switch_fahrenheit
        global thread_gkey_pressed
        global bool_switch_g2_disks
        global thread_disk_guid
        global thread_eject, thread_mount, thread_unmount
        global thread_notification
        global thread_windows_update_monitor
        global thread_dir_sz_monitor

        notification_thread = SdkNotificationClass()
        thread_notification.append(notification_thread)
        thread_notification[0].start()

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
        ping_test_thread = InternetConnectionClass()
        thread_net_connection.append(ping_test_thread)
        def_netshare_thread = NetShareClass()
        thread_net_share.append(def_netshare_thread)
        sdk_event_handler = SdkEventHandlerClass(self.g1_function_short, self.g1_function_long,
                                                        self.g2_function_short, self.g2_function_long,
                                                        self.g3_function_short, self.g3_function_long,
                                                        self.g4_function_short, self.g4_function_long,
                                                        self.g5_function_short, self.g5_function_long,
                                                        self.g6_function_short, self.g6_function_long,
                                                 self.g1_function_long_3sec, self.g2_function_long_3sec,
                                                 self.g3_function_long_3sec, self.g4_function_long_3sec,
                                                 self.g5_function_long_3sec, self.g6_function_long_3sec,
                                                 self.g1_function_long_2sec, self.g2_function_long_2sec,
                                                 self.g3_function_long_2sec, self.g4_function_long_2sec,
                                                 self.g5_function_long_2sec, self.g6_function_long_2sec
                                                 )
        thread_sdk_event_handler.append(sdk_event_handler)
        backlight_auto = BackLightClass(self.color_all_id,
                                        self.btn_bck_light,
                                        self.btn_backlight_sub,
                                        self.btn_title_bar_style_0,
                                        self.btn_title_bar_style_1,
                                        self.btn_menu_style,
                                        self.btn_menu_style_1,
                                        self.lbl_backlight_sub)
        thread_backlight_auto.append(backlight_auto)
        compile_devices_thread = CompileDevicesClass(self.btn_con_stat_name, self.lbl_con_stat_kb, self.lbl_con_stat_mouse, self.btn_con_stat_ms_img, self.btn_con_stat_kb_img,
                                                     self.btn_refresh_recompile, self.btn_title_bar_style_0, self.btn_title_bar_style_1)
        thread_compile_devices.append(compile_devices_thread)
        thread_compile_devices[0].start()
        print('thread_compile_devices.isRunning:', thread_compile_devices[0].isRunning())
        temp_thread = TemperatureClass()
        thread_temperatures.append(temp_thread)
        system_mute = MediaDisplayClass()
        thread_media_display.append(system_mute)
        pause_loop = PauseLoopClass()
        thread_pause_loop.append(pause_loop)
        power_thread = PowerClass()
        thread_power.append(power_thread)
        test_locked = IsLockedClass()
        thread_test_locked.append(test_locked)
        thread_test_locked[0].start()
        keyeventsthread = KeyEventClass()
        thread_keyevents.append(keyeventsthread)
        on_gkey_pressed_thread = OnPressClass()
        thread_gkey_pressed.append(on_gkey_pressed_thread)

        disk_guid_thread = CompileDiskGUIDDictionaryListClass()
        thread_disk_guid.append(disk_guid_thread)
        thread_disk_guid[0].start()

        eject_thread = SdkEventG2_Eject()
        thread_eject.append(eject_thread)

        mount_thread = SdkEventG2_Mount()
        thread_mount.append(mount_thread)

        unmount_thread = SdkEventG2_Unmount()
        thread_unmount.append(unmount_thread)

        sdk_instruction_thread = SdkSendInstructionClass()
        thread_sdk_instruction.append(sdk_instruction_thread)
        thread_sdk_instruction[0].start()

        windows_update_monitor_thread = WindowsUpdateMonitorClass()
        thread_windows_update_monitor.append(windows_update_monitor_thread)
        thread_windows_update_monitor[0].start()

        # dir_sz_monitor_thread = DirSZMonitorThread()
        # thread_dir_sz_monitor.append(dir_sz_monitor_thread)
        # thread_dir_sz_monitor[0].start()gg
        
        self.lbl_title.show()
        self.btn_con_stat_name.show()

        print('-- [App.initUI]: waiting to display application')
        while bool_backend_allow_display is False:
            time.sleep(0.1)
        print('-- [App.initUI]: displaying application')

        if bool_switch_g2_disks is True:
            self.btn_g2_disk.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_switch_g2_disks is False:
            self.btn_g2_disk.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_switch_fahrenheit is True:
            self.btn_fahrenheit.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_util_key_8.setText('>158°F')
            self.lbl_util_key_6.setText('>=122°F  <158°F')
            self.lbl_util_key_4.setText('>=86°F    <122°F')
            self.lbl_util_key_2.setText('<86°F')
        elif bool_switch_fahrenheit is False:
            self.btn_fahrenheit.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_backlight_interact is True:
            self.btn_g5_backlight.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_backlight_interact is False:
            self.btn_g5_backlight.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_powershell_interact is True:
            self.btn_powershell.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        elif bool_powershell_interact is False:
            self.btn_powershell.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if bool_power_plan_interact is True:
            self.btn_power_plan.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
        if bool_power_plan_interact is False:
            self.btn_power_plan.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))

        if os.path.exists(str_path_kb_img):
            self.btn_con_stat_kb_img.setIcon(QIcon(str_path_kb_img))
            self.btn_con_stat_kb_img.setStyleSheet(self.btn_status_style)
            self.btn_con_stat_kb_img.setText('')
        if os.path.exists(str_path_ms_img):
            self.btn_con_stat_ms_img.setIcon(QIcon(str_path_ms_img))
            self.btn_con_stat_ms_img.setStyleSheet(self.btn_status_style)
            self.btn_con_stat_ms_img.setText('')

        if bool_switch_backlight_auto is False:
            self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_backlight_auto.setStyleSheet(self.btn_menu_style)
        elif bool_switch_backlight_auto is True:
            self.btn_backlight_auto.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_backlight_auto.setStyleSheet(self.btn_menu_style_1)
            if len(devices_kb) > 0 or len(devices_ms) > 0:
                thread_backlight_auto[0].start()
        if bool_switch_startup_autorun is True:
            self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_run_startup.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_autorun is False:
            self.btn_run_startup.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_run_startup.setStyleSheet(self.btn_menu_style)
        if bool_switch_startup_minimized is True:
            self.showMinimized()
            self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_start_minimized.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_minimized is False:
            self.btn_start_minimized.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_start_minimized.setStyleSheet(self.btn_menu_style)

        if bool_switch_startup_cpu_util is True:
            self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_cpu_mon.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_cpu_util is False:
            self.btn_cpu_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_cpu_mon.setStyleSheet(self.btn_menu_style)
        if bool_switch_startup_dram_util is True:
            self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_dram_mon.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_dram_util is False:
            self.btn_dram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_dram_mon.setStyleSheet(self.btn_menu_style)
        if bool_switch_startup_vram_util is True:
            self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_vram_mon.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_vram_util is False:
            self.btn_vram_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_vram_mon.setStyleSheet(self.btn_menu_style)
        if bool_switch_startup_hdd_read_write is True:
            self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_hdd_mon_sub.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_hdd_read_write is False:
            self.btn_hdd_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_hdd_mon_sub.setStyleSheet(self.btn_menu_style)
        if bool_switch_startup_exclusive_control is True:
            self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_exclusive_con.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_exclusive_control is False:
            self.btn_exclusive_con.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_exclusive_con.setStyleSheet(self.btn_menu_style)
        if bool_backend_icue_connected is False:
            self.btn_con_stat_name.setIcon(QIcon("./image/icue_logo_connected_0.png"))
        elif bool_backend_icue_connected is True:
            self.btn_con_stat_name.setIcon(QIcon("./image/icue_logo_connected_1.png"))
        if bool_switch_startup_net_traffic is False:
            self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_network_adapter.setStyleSheet(self.btn_menu_style)
        elif bool_switch_startup_net_traffic is True:
            self.btn_network_adapter.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_network_adapter.setStyleSheet(self.btn_menu_style_1)
        if bool_switch_startup_net_con_ms is False:
            self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_net_con_mouse.setStyleSheet(self.btn_menu_style)
        elif bool_switch_startup_net_con_ms is True:
            self.btn_net_con_mouse.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_net_con_mouse.setStyleSheet(self.btn_menu_style_1)
        if bool_switch_startup_net_con_kb is False:
            self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_net_con_kb.setStyleSheet(self.btn_menu_style)
        elif bool_switch_startup_net_con_kb is True:
            self.btn_net_con_kb.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_net_con_kb.setStyleSheet(self.btn_menu_style_1)
        if bool_switch_startup_net_share_mon is False:
            self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_netshare_mon.setStyleSheet(self.btn_menu_style)
        elif bool_switch_startup_net_share_mon is True:
            self.btn_netshare_mon.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_netshare_mon.setStyleSheet(self.btn_menu_style_1)
        self.lbl_net_con_mouse_led_selected.setText(str(corsairled_id_num_netcon_ms))
        if bool_switch_backlight is True:
            self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_0)
            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style_1)
            self.color_all_id()
        elif bool_switch_backlight is False:
            self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_1)
            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style)

        if bool_cpu_temperature is True:
            self.btn_cpu_mon_temp.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_cpu_mon_temp.setStyleSheet(self.btn_menu_style_1)
        elif bool_cpu_temperature is False:
            self.btn_cpu_mon_temp.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_cpu_mon_temp.setStyleSheet(self.btn_menu_style)
        if bool_vram_temperature is True:
            self.btn_vram_mon_temp.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_vram_mon_temp.setStyleSheet(self.btn_menu_style_1)
        elif bool_vram_temperature is False:
            self.btn_vram_mon_temp.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_vram_mon_temp.setStyleSheet(self.btn_menu_style_1)

        if bool_switch_startup_media_display is True:
            self.btn_media_display.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
            self.lbl_media_display.setStyleSheet(self.btn_menu_style_1)
        elif bool_switch_startup_media_display is False:
            self.btn_media_display.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
            self.lbl_media_display.setStyleSheet(self.btn_menu_style)

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
        self.sanitize_passed = False

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
        try:
            delta = QPoint(event.globalPos() - self.prev_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.prev_pos = event.globalPos()
        except Exception as e:
            print('-- [App.mouseMoveEvent]: Error:', e)

    def pollCursor(self):
        # print('-- [App.pollCursor]: plugged in')
        pos = QCursor.pos()
        if pos != self.cursor:
            self.cursor = pos
            self.cursorMove.emit(pos)

    def handleCursorMove(self, pos):
        # print('-- [App.handleCursorMove]: plugged in')
        pass


class CompileDevicesClass(QThread):
    print('-- [CompileDevicesClass]: plugged in')

    def __init__(self, btn_con_stat_name, lbl_con_stat_kb, lbl_con_stat_mouse, btn_con_stat_ms_img, btn_con_stat_kb_img, btn_refresh_recompile, btn_title_bar_style_0, btn_title_bar_style_1):
        QThread.__init__(self)
        global sdk_color_hddread_on, sdk_color_backlight, sdk_color_backlight_on
        self.btn_con_stat_name = btn_con_stat_name
        self.lbl_con_stat_kb = lbl_con_stat_kb
        self.lbl_con_stat_mouse = lbl_con_stat_mouse
        self.btn_con_stat_ms_img = btn_con_stat_ms_img
        self.btn_con_stat_kb_img = btn_con_stat_kb_img
        self.btn_refresh_recompile = btn_refresh_recompile
        self.btn_title_bar_style_0 = btn_title_bar_style_0
        self.btn_title_bar_style_1 = btn_title_bar_style_1
        self.device_str = ''
        self.device_index = ()
        self.bool_backend_comprehensive_enumeration = True

    def enum_kb(self):
        global sdk
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

    def enum_ms(self):
        global sdk
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
            corsairled_id_num_ms_complete.sort()
            print('-- [CompileDevicesClass.enumerate_device]  corsairled_id_num_ms_complete:', corsairled_id_num_ms_complete)

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
        global thread_backlight_auto
        global devices_kb, devices_ms
        global thread_temperatures
        global thread_media_display
        global thread_pause_loop
        global thread_power
        global thread_keyevents
        global thread_eject, thread_mount, thread_unmount

        print('-- [CompileDevicesClass.stop_all_threads] stopping all threads:', )
        if len(devices_kb) >= 1 or len(devices_ms) >= 1:

            try:
                thread_eject[0].stop()
            except Exception as e:
                print('error stopping thread_eject:', e)

            try:
                thread_mount[0].stop()
            except Exception as e:
                print('error stopping thread_mount:', e)

            try:
                thread_unmount[0].stop()
            except Exception as e:
                print('error stopping thread_unmount:', e)

            try:
                thread_disk_rw[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_cpu_util[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_dram_util[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_vram_util[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
            try:
                thread_net_traffic[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_net_connection[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)
            try:
                thread_net_share[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_sdk_event_handler[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_backlight_auto[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_temperatures[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_media_display[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_pause_loop[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_power[0].stop()
            except Exception as e:
                print('-- [CompileDevicesClass.stop_all_threads] Error:', e)

            try:
                thread_keyevents[0].stop()
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
        global thread_temperatures, bool_cpu_temperature, bool_vram_temperature
        global thread_media_display
        global thread_power
        global thread_keyevents, thread_sdk_event_handler
        global thread_disk_rw
        global thread_cpu_util, thread_dram_util, thread_vram_util
        global thread_net_traffic
        global thread_net_share

        if len(devices_kb) > 0:
            thread_sdk_event_handler[0].start()
            thread_keyevents[0].start()
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
            if bool_cpu_temperature is True or bool_vram_temperature is True:
                thread_temperatures[0].start()
            if bool_switch_startup_media_display is True:
                thread_media_display[0].start()
            if bool_power_plan_interact is True:
                thread_power[0].start()
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
        global sdk, bool_backend_icue_connected, devices_previous, bool_backend_icue_connected_previous, devices_kb, devices_ms
        connected = sdk.connect()
        if not connected:
            bool_backend_icue_connected = False
            if bool_backend_icue_connected != bool_backend_icue_connected_previous:
                bool_backend_icue_connected_previous = bool_backend_icue_connected
                self.stop_all_threads()
            devices_previous = []
            devices_kb = []
            devices_ms = []
            self.btn_con_stat_name.setIcon(QIcon("./image/icue_logo_connected_0.png"))
            self.lbl_con_stat_mouse.hide()
            self.lbl_con_stat_kb.hide()
            self.btn_con_stat_ms_img.hide()
            self.btn_con_stat_kb_img.hide()
            time.sleep(0.1)
            self.attempt_connect()
        elif connected:
            sdk.request_control()
            bool_backend_icue_connected = True
            self.btn_con_stat_name.setIcon(QIcon("./image/icue_logo_connected_1.png"))
            self.get_devices()

    def entry_sequence(self):
        print('-- [CompileDevicesClass.entry_sequence]: plugged in')
        global sdk
        global devices_kb, devices_ms
        global devices_kb_selected, devices_ms_selected
        global corsairled_id_num_ms_complete, corsairled_id_num_kb_complete
        global sdk_color_backlight
        global sdk_color_backlight, bool_switch_backlight, sdk_color_backlight_on

        zone_id = [170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188]

        if len(devices_kb) >= 1:
            for _ in corsairled_id_num_kb_complete:
                itm = [{_: (255, 255, 255)}]
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
                except Exception as e:
                    print(e)
        if len(devices_ms) >= 1:
            for _ in corsairled_id_num_ms_complete:
                itm = [{_: (255, 255, 255)}]
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], itm[0])
                except Exception as e:
                    print(e)
        time.sleep(1)
        if len(devices_kb) >= 1:
            for _ in corsairled_id_num_kb_complete:
                if _ not in zone_id:
                    itm = [{_: sdk_color_backlight}]
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
                    except Exception as e:
                        print(e)
                else:
                    itm = [{_: (0, 0, 0)}]
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], itm[0])
                    except Exception as e:
                        print(e)
        if len(devices_ms) >= 1:
            for _ in corsairled_id_num_ms_complete:
                itm = [{_: sdk_color_backlight}]
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], itm[0])
                except Exception as e:
                    print(e)

    def get_devices(self):
        # print('-- [CompileDevicesClass.get_devices]: plugged in')
        global sdk, devices_previous, devices_kb, devices_ms, devices_kb_name, bool_execution_policy_show
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
                    try:
                        self.enum_kb()
                    except Exception as e:
                        print(e)
                    try:
                        self.enum_ms()
                    except Exception as e:
                        print(e)
                    time.sleep(0.5)
                device_i += 1

            if fresh_start is True:
                print('-- [CompileDevicesClass.get_devices] fresh start: True')
                if len(devices_kb) > 0:
                    self.lbl_con_stat_kb.setText(str(devices_kb_name[0]))
                    if bool_execution_policy_show is False:
                        self.lbl_con_stat_kb.show()
                        self.btn_con_stat_kb_img.show()
                elif len(devices_kb) < 1:
                    self.lbl_con_stat_kb.setText('')
                    self.lbl_con_stat_kb.hide()
                    self.btn_con_stat_kb_img.hide()
                if len(devices_ms) > 0:
                    self.lbl_con_stat_mouse.setText(str(devices_ms_name[0]))
                    if bool_execution_policy_show is False:
                        self.lbl_con_stat_mouse.show()
                        self.btn_con_stat_ms_img.show()
                elif len(devices_ms) < 1:
                    self.lbl_con_stat_mouse.setText('')
                    self.lbl_con_stat_mouse.hide()
                    self.btn_con_stat_ms_img.hide()
                if len(devices_kb) >= 1 or len(devices_ms) >= 1:
                    self.entry_sequence()
                    devices_previous = device
                    self.stop_all_threads()
                    # time.sleep(2)
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
        global bool_cpu_temperature, bool_vram_temperature
        global str_path_kb_img, str_path_ms_img
        global bool_switch_startup_media_display
        global bool_power_plan_interact
        global bool_powershell_interact
        global bool_backlight_interact
        global bool_switch_fahrenheit
        global bool_switch_g2_disks

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
                if line == 'bool_cpu_temperature: false':
                    bool_cpu_temperature = False
                elif line == 'bool_cpu_temperature: true':
                    bool_cpu_temperature = True
                if line == 'bool_vram_temperature: false':
                    bool_vram_temperature = False
                elif line == 'bool_vram_temperature: true':
                    bool_vram_temperature = True
                if line.startswith('str_path_kb_img: '):
                    var = line.replace('str_path_kb_img: ', '')
                    if os.path.exists(var):
                        str_path_kb_img = var
                if line.startswith('str_path_ms_img: '):
                    var = line.replace('str_path_ms_img: ', '')
                    if os.path.exists(var):
                        str_path_ms_img = var
                if line == 'bool_switch_startup_media_display: false':
                    bool_switch_startup_media_display = False
                elif line == 'bool_switch_startup_media_display: true':
                    bool_switch_startup_media_display = True
                if line == 'bool_power_plan_interact: true':
                    bool_power_plan_interact = True
                elif line == 'bool_power_plan_interact: false':
                    bool_power_plan_interact = False
                if line == 'bool_powershell_interact: true':
                    bool_powershell_interact = True
                if line == 'bool_powershell_interact: false':
                    bool_powershell_interact = False

                if line == 'bool_backlight_interact: true':
                    bool_backlight_interact = True
                if line == 'bool_backlight_interact: false':
                    bool_backlight_interact = False

                if line == 'bool_switch_fahrenheit: true':
                    bool_switch_fahrenheit = True
                if line == 'bool_switch_fahrenheit: false':
                    bool_switch_fahrenheit = False

                if line == 'bool_switch_g2_disks: true':
                    bool_switch_g2_disks = True
                if line == 'bool_switch_g2_disks: false':
                    bool_switch_g2_disks = False


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
        print('-- [ConfigCompile.read_config] bool_cpu_temperature:', bool_cpu_temperature)
        print('-- [ConfigCompile.read_config] bool_vram_temperature:', bool_vram_temperature)
        bool_backend_config_read_complete = True

    def run(self):
        print('-- [CompileDevicesClass.run]: plugged in')
        global bool_backend_allow_display, bool_backend_icue_connected, bool_backend_config_read_complete, devices_kb, devices_ms
        bool_backend_config_read_complete = False
        bool_backend_allow_display = False
        self.btn_refresh_recompile.setStyleSheet(self.btn_title_bar_style_0)
        self.lbl_con_stat_mouse.hide()
        self.lbl_con_stat_kb.hide()
        self.btn_con_stat_ms_img.hide()
        self.btn_con_stat_kb_img.hide()
        self.btn_con_stat_name.setIcon(QIcon('./image/icue_logo_connected_0.png'))
        devices_kb = []
        devices_ms = []
        while True:

            if bool_backend_config_read_complete is False:

                try:
                    self.read_config()
                except Exception as e:
                    print('[-- [CompileDevicesClass.run] Error running read_config:', e)

            elif bool_backend_config_read_complete is True:
                bool_backend_allow_display = True

                try:
                    self.btn_refresh_recompile.setStyleSheet(self.btn_title_bar_style_1)
                    self.attempt_connect()
                except Exception as e:
                    print('[-- [CompileDevicesClass.run] Error running attempt_connect:', e)

            time.sleep(1)

    def stop(self):
        print('-- [CompileDevicesClass.stop]: plugged in')
        self.stop_all_threads()
        print('-- [CompileDevicesClass.stop] terminating')
        self.terminate()


class SdkNotificationClass(QThread):
    print('-- [SdkNotificationClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def notification_off(self):
        time.sleep(1)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (0, 0, 0)}))
        except Exception as e:
            print('-- [SdkNotificationClass.run] Error:', e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (0, 0, 0)}))
        except Exception as e:
            print('-- [SdkNotificationClass.run] Error:', e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (0, 0, 0)}))
        except Exception as e:
            print('-- [SdkNotificationClass.run] Error:', e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (0, 0, 0)}))
        except Exception as e:
            print('-- [SdkNotificationClass.run] Error:', e)

    def run(self):
        print('-- [SdkNotificationClass.run]: plugged in')
        global notification_key

        while True:

            if notification_key == 1:
                notification_key = 0
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (0, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (0, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (0, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (0, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)

                self.notification_off()

            elif notification_key == 2:
                notification_key = 0
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)

                self.notification_off()

            elif notification_key == 3:
                notification_key = 0
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)

                self.notification_off()

            elif notification_key == 4:
                notification_key = 0
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (100, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (100, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (100, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (100, 255, 0)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)

                self.notification_off()

            elif notification_key == 5:
                notification_key = 0
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (0, 255, 255)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (0, 255, 255)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (0, 255, 255)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (0, 255, 255)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)

                self.notification_off()

            elif notification_key == 6:
                notification_key = 0
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({177: (255, 15, 100)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({178: (255, 15, 100)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({179: (255, 15, 100)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({180: (255, 15, 100)}))
                except Exception as e:
                    print('-- [SdkNotificationClass.run] Error:', e)

                self.notification_off()
            
            time.sleep(0.5)

    def stop(self):
        print('-- [SdkNotificationClass.stop]: plugged in')


class SdkSendInstructionClass(QThread):
    print('-- [SdkSendInstructionClass]: plugged in')

    # SdkSendInstructionClass sets LEDs procedurally for special cases where instructions use same LEDs

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-- [SdkSendInstructionClass.run]: plugged in')

        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight

        global corsairled_id_num_hddreadwrite

        global bool_instruction_eject, bool_instruction_eject_end, bool_instruction_mount, bool_instruction_mount_end, bool_instruction_unmount, bool_instruction_unmount_end

        while True:

            if bool_instruction_eject is True:
                bool_instruction_eject = False
                try:
                    """ arm """
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 255, 0)}))
                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

                g2_function_long_i = 0
                for _ in corsairled_id_num_hddreadwrite:
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[g2_function_long_i]: (255, 255, 0)}))
                    except Exception as e:
                        print('-- [SdkEventG2_Eject.run] Error:', e)
                    g2_function_long_i += 1

            elif bool_instruction_eject_end is True:
                bool_instruction_eject_end = False
                g2_function_long_i = 0
                for _ in corsairled_id_num_hddreadwrite:
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[g2_function_long_i]: sdk_color_backlight}))
                    except Exception as e:
                        print('-- [SdkEventG2_Eject.run] Error:', e)
                    g2_function_long_i += 1

                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))
                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

            elif bool_instruction_mount is True:
                bool_instruction_mount = False
                try:
                    """ arm """
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 100, 0)}))
                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

                g2_function_long_i = 0
                for _ in corsairled_id_num_hddreadwrite:
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[g2_function_long_i]: (255, 100, 0)}))
                    except Exception as e:
                        print('-- [SdkEventG2_Eject.run] Error:', e)
                    g2_function_long_i += 1

            elif bool_instruction_mount_end is True:
                bool_instruction_mount_end = False
                g2_function_long_i = 0
                for _ in corsairled_id_num_hddreadwrite:
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[g2_function_long_i]: sdk_color_backlight}))
                    except Exception as e:
                        print('-- [SdkEventG2_Eject.run] Error:', e)
                    g2_function_long_i += 1

                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))
                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

            elif bool_instruction_unmount is True:
                bool_instruction_unmount = False
                try:
                    """ arm """
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 0, 0)}))
                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

                g2_function_long_i = 0
                for _ in corsairled_id_num_hddreadwrite:
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[g2_function_long_i]: (255, 0, 0)}))
                    except Exception as e:
                        print('-- [SdkEventG2_Eject.run] Error:', e)
                    g2_function_long_i += 1

            elif bool_instruction_unmount_end is True:
                bool_instruction_unmount_end = False
                g2_function_long_i = 0
                for _ in corsairled_id_num_hddreadwrite:
                    try:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[g2_function_long_i]: sdk_color_backlight}))
                    except Exception as e:
                        print('-- [SdkEventG2_Eject.run] Error:', e)
                    g2_function_long_i += 1

                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))
                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

            try:
                sdk.set_led_colors_flush_buffer()
            except Exception as e:
                print(e)

            # time.sleep(0.01)

    def stop(self):
        print('-- [SdkSendInstructionClass.stop]: plugged in')


class SdkEventG2_Eject(QThread):
    print('-- [SdkEventG2_Eject]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.kb_event = ''

    def run(self):
        print('-- [SdkEventG2_Eject.run]: plugged in')

        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, corsairled_id_num_hddreadwrite
        global disk_guid
        global bool_alpha_stage_engaged
        global bool_g2_input, kb_event
        global bool_instruction_eject, bool_instruction_eject_end
        global notification_key

        bool_alpha_stage_engaged = True

        bool_instruction_eject = True

        print('-- [SdkEventG2_Eject.run]: armed')

        kb_event = ''
        bool_g2_input = True
        while bool_g2_input is True:
            time.sleep(0)

        print('-- [SdkEventG2_Eject.run] kb_event:', kb_event)

        kb_event = str(kb_event).strip()
        bool_success = False

        if len(kb_event) == 1:
            print('-- [SdkEventG2_Eject.run] kb_event: length correct')
            if kb_event in alpha_str:
                print('-- [SdkEventG2_Eject.run] kb_event: in alpha_str')
                try:
                    eject_alpha = kb_event
                    eject_alpha = eject_alpha + ':'
                    if os.path.exists(eject_alpha):
                        print('-- [SdkEventG2_Eject.run] ejecting:', eject_alpha)
                        cmd_0 = "powershell "+"$Eject = New-Object -comObject Shell.Application; $Eject.NameSpace(17).ParseName("
                        cmd_1 = "'"+eject_alpha+"'"
                        cmd_2 = cmd_0 + cmd_1+").InvokeVerb('Eject')"
                        os.system(cmd_2)

                        if not os.path.exists(eject_alpha):
                            notification_key = 1
                            bool_success = True
                    else:
                        print('-- [SdkEventG2_Eject.run] kb_event: path does not exist')

                except Exception as e:
                    print('-- [SdkEventG2_Eject.run] Error:', e)

        print('-- [SdkEventG2_Eject.run]: disarmed')

        if bool_success is False:
            notification_key = 2

        bool_instruction_eject_end = True

        bool_alpha_stage_engaged = False

    def stop(self):
        print('-- [SdkEventG2_Eject.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, bool_alpha_stage_engaged, bool_g2_input
        global bool_instruction_eject_end, notification_key
        bool_g2_input = False

        bool_instruction_eject_end = True

        bool_alpha_stage_engaged = False

        notification_key = 2

        self.terminate()


class SdkEventG2_Mount(QThread):
    print('-- [SdkEventG2_Mount]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-- [SdkEventG2_Mount.run]: plugged in')

        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, corsairled_id_num_hddreadwrite
        global disk_guid
        global bool_alpha_stage_engaged, bool_g2_input, kb_event, bool_instruction_mount, bool_instruction_mount_end
        global notification_key

        bool_alpha_stage_engaged = True

        bool_instruction_mount = True

        print('-- [SdkEventG2_Mount.run]: armed')

        kb_event = ''
        bool_g2_input = True
        while bool_g2_input is True:
            time.sleep(0)

        print('-- [SdkEventG2_Mount.run] kb_event:', )

        kb_event = str(kb_event).strip()
        bool_success = False

        if len(kb_event) == 1:
            print('-- [SdkEventG2_Mount.run] kb_event: length correct')
            if kb_event in alpha_str:
                print('-- [SdkEventG2_Mount.run] kb_event: in alpha_str')
                mount_alpha = kb_event + ':\\'
                print('-- [SdkEventG2_Mount.run] mount:', mount_alpha)
                i = 0
                for _ in disk_guid:
                    try:
                        dict_str = str(_)
                        dict_str = dict_str.replace("{'", "")
                        dict_str = dict_str[:1]
                        dict_str = dict_str + ':\\'
                        # print('dict key:', dict_str)
                        # print('mount_alpha:', mount_alpha)
                        if canonical_caseless(dict_str) == canonical_caseless(mount_alpha):
                            print('target:', _)
                            guid = disk_guid[i][dict_str]
                            print('guid:', guid)
                            dict_str = dict_str.replace('\\', '')
                            cmd = str("powershell mountvol " + dict_str + " '" + guid + "'")
                            print('cmd:', cmd)
                            print('-- [SdkEventG2_Mount.run] running command:', cmd)
                            os.system(cmd)

                            if os.path.exists(dict_str):
                                notification_key = 1
                                bool_success = True

                    except Exception as e:
                        print('-- [SdkEventG2_Mount.run] Error:', e)
                        pass
                    i += 1

        print('-- [SdkEventG2_Mount.run]: disarmed')

        if bool_success is False:
            notification_key = 2

        bool_instruction_mount_end = True

        bool_alpha_stage_engaged = False

    def stop(self):
        print('-- [SdkEventG2_Mount.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, bool_alpha_stage_engaged, bool_g2_input, bool_instruction_mount_end
        global notification_key

        bool_g2_input = False

        bool_instruction_mount_end = True

        bool_alpha_stage_engaged = False

        notification_key = 2

        self.terminate()


class SdkEventG2_Unmount(QThread):
    print('-- [SdkEventG2_Unmount]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-- [SdkEventG2_Unmount.run]: plugged in')

        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, corsairled_id_num_hddreadwrite
        global disk_guid
        global bool_alpha_stage_engaged, bool_g2_input, kb_event, bool_instruction_unmount, bool_instruction_unmount_end
        global notification_key

        bool_alpha_stage_engaged = True

        bool_instruction_unmount = True

        print('-- [SdkEventG2_Unmount.run]: armed')

        kb_event = ''
        bool_g2_input = True
        while bool_g2_input is True:
            time.sleep(0)

        print('-- [SdkEventG2_Unmount.run] kb_event:', kb_event)

        kb_event = str(kb_event).strip()
        bool_success = False

        if len(kb_event) == 1:
            print('-- [SdkEventG2_Unmount.run] kb_event: length correct')
            if kb_event in alpha_str:
                print('-- [SdkEventG2_Unmount.run] kb_event: in alpha_str')
                try:
                    umount_alpha = kb_event
                    umount_path = umount_alpha + ':'
                    print('-- [SdkEventG2_Unmount.run] umount:', umount_alpha)
                    if os.path.exists(umount_path):
                        cmd = 'mountvol ' + umount_path + ' /D'
                        os.system(cmd)

                        if not os.path.exists(umount_path):
                            notification_key = 1
                            bool_success = True

                except Exception as e:
                    print('-- [SdkEventG2_Unmount.run] Error:', e)

        print('-- [SdkEventG2_Unmount.run]: disarmed')

        if bool_success is False:
            notification_key = 2

        bool_instruction_unmount_end = True

        bool_alpha_stage_engaged = False

    def stop(self):
        print('-- [SdkEventG2_Unmount.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, bool_alpha_stage_engaged, bool_g2_input, bool_instruction_unmount_end
        global notification_key

        bool_g2_input = False

        bool_instruction_unmount_end = True

        bool_alpha_stage_engaged = False

        notification_key = 2

        self.terminate()


class OnPressClass(QThread):
    print('-- [OnPressClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-- [OnPressClass.run]: plugged in')
        global g_key_pressed, time_now_press, sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        global bool_onpress_clause_g1, bool_onpress_clause_g2, bool_onpress_clause_g3
        global bool_onpress_clause_g4, bool_onpress_clause_g5, bool_onpress_clause_g6

        bool_catch_1 = False
        bool_catch_2 = False
        bool_catch_3 = False
        bool_catch_4 = False
        bool_onpress_clause_g1 = False
        bool_onpress_clause_g2 = False
        bool_onpress_clause_g3 = False
        bool_onpress_clause_g4 = False
        bool_onpress_clause_g5 = False
        bool_onpress_clause_g6 = False

        try:
            while True:
                date_time_now = str(datetime.datetime.now())
                var = date_time_now.split(' ')
                var = var[1].split(':')[2]
                time_now_press_hold = float(var)

                if time_now_press_hold > (time_now_press + 1.0) and time_now_press_hold < (time_now_press + 2.0):
                    if bool_catch_1 is False:
                        bool_catch_1 = True
                        print('-- [OnPressClass.run] hold 1:', g_key_pressed)
                        if g_key_pressed == 'CorsairKeyId.Kb_G1':
                            bool_onpress_clause_g1 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (255, 255, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G2':
                            bool_onpress_clause_g2 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 255, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G3':
                            bool_onpress_clause_g3 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: (255, 255, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G4':
                            bool_onpress_clause_g4 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: (255, 255, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G5':
                            bool_onpress_clause_g5 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: (255, 255, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G6':
                            bool_onpress_clause_g6 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: (255, 255, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)

                elif time_now_press_hold > (time_now_press + 2.0) and time_now_press_hold < (time_now_press + 3.0):
                    if bool_catch_2 is False:
                        bool_catch_2 = True
                        print('-- [OnPressClass.run] hold 2:', g_key_pressed)
                        if g_key_pressed == 'CorsairKeyId.Kb_G1':
                            bool_onpress_clause_g1 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (255, 100, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G2':
                            bool_onpress_clause_g2 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 100, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G3':
                            bool_onpress_clause_g3 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: (255, 100, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G4':
                            bool_onpress_clause_g4 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: (255, 100, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G5':
                            bool_onpress_clause_g5 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: (255, 100, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G6':
                            bool_onpress_clause_g6 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: (255, 100, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.on_press]  Error:', e)

                elif time_now_press_hold > (time_now_press + 3.0) and time_now_press_hold < (time_now_press + 4.0):
                    if bool_catch_3 is False:
                        bool_catch_3 = True
                        print('-- [OnPressClass.run] hold 3:', g_key_pressed)
                        if g_key_pressed == 'CorsairKeyId.Kb_G1':
                            bool_onpress_clause_g1 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (255, 0, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G2':
                            bool_onpress_clause_g2 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 0, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G3':
                            bool_onpress_clause_g3 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: (255, 0, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G4':
                            bool_onpress_clause_g4 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: (255, 0, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G5':
                            bool_onpress_clause_g5 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: (255, 0, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G6':
                            bool_onpress_clause_g6 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: (255, 0, 0)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)

                elif time_now_press_hold > (time_now_press + 4.0) and time_now_press_hold < (time_now_press + 5.0):
                    if bool_catch_4 is False:
                        bool_catch_4 = True
                        print('-- [OnPressClass.run] hold 4:', g_key_pressed)
                        if g_key_pressed == 'CorsairKeyId.Kb_G1':
                            bool_onpress_clause_g1 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (255, 255, 255)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G2':
                            bool_onpress_clause_g2 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: (255, 255, 255)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G3':
                            bool_onpress_clause_g3 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: (255, 255, 255)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G4':
                            bool_onpress_clause_g4 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: (255, 255, 255)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G5':
                            bool_onpress_clause_g5 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: (255, 255, 255)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)
                        elif g_key_pressed == 'CorsairKeyId.Kb_G6':
                            bool_onpress_clause_g6 = True
                            try:
                                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: (255, 255, 255)}))
                            except Exception as e:
                                print('-- [OnPressClass.run]  Error:', e)

        except Exception as e:
            print('-- [OnPressClass.run] Error:', e)

        g_key_pressed = ''
        if bool_onpress_clause_g1 is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: sdk_color_backlight}))
            except Exception as e:
                print('-- [OnPressClass.run]  Error:', e)
        elif bool_onpress_clause_g2 is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))
            except Exception as e:
                print('-- [OnPressClass.run]  Error:', e)
        elif bool_onpress_clause_g3 is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: sdk_color_backlight}))
            except Exception as e:
                print('-- [OnPressClass.run]  Error:', e)
        elif bool_onpress_clause_g4 is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: sdk_color_backlight}))
            except Exception as e:
                print('-- [OnPressClass.run]  Error:', e)
        elif bool_onpress_clause_g5 is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: sdk_color_backlight}))
            except Exception as e:
                print('-- [OnPressClass.run]  Error:', e)
        elif bool_onpress_clause_g6 is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: sdk_color_backlight}))
            except Exception as e:
                print('-- [OnPressClass.run]  Error:', e)

        bool_onpress_clause_g1 = False
        bool_onpress_clause_g2 = False
        bool_onpress_clause_g3 = False
        bool_onpress_clause_g4 = False
        bool_onpress_clause_g5 = False
        bool_onpress_clause_g6 = False

    def stop(self):
        print('-- [OnPressClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        global g_key_pressed
        global bool_onpress_clause_g1, bool_onpress_clause_g2, bool_onpress_clause_g3
        global bool_onpress_clause_g4, bool_onpress_clause_g5, bool_onpress_clause_g6
        try:
            if bool_onpress_clause_g1 is True:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: sdk_color_backlight}))
                except Exception as e:
                    print('-- [OnPressClass.stop]  Error:', e)
            if bool_onpress_clause_g2 is True:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({122: sdk_color_backlight}))
                except Exception as e:
                    print('-- [OnPressClass.stop]  Error:', e)
            if bool_onpress_clause_g3 is True:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({123: sdk_color_backlight}))
                except Exception as e:
                    print('-- [OnPressClass.stop]  Error:', e)
            if bool_onpress_clause_g4 is True:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({124: sdk_color_backlight}))
                except Exception as e:
                    print('-- [OnPressClass.stop]  Error:', e)
            if bool_onpress_clause_g5 is True:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({125: sdk_color_backlight}))
                except Exception as e:
                    print('-- [OnPressClass.stop]  Error:', e)
            if bool_onpress_clause_g6 is True:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({126: sdk_color_backlight}))
                except Exception as e:
                    print('-- [OnPressClass.stop]  Error:', e)
        except Exception as e:
            print(e)

        bool_onpress_clause_g1 = False
        bool_onpress_clause_g2 = False
        bool_onpress_clause_g3 = False
        bool_onpress_clause_g4 = False
        bool_onpress_clause_g5 = False
        bool_onpress_clause_g6 = False
        g_key_pressed = ''

        self.terminate()


class SdkEventHandlerClass(QThread):
    print('-- [SdkEventHandlerClass]: plugged in')

    def __init__(self, g1_function_short, g1_function_long,
                 g2_function_short, g2_function_long,
                 g3_function_short, g3_function_long,
                 g4_function_short, g4_function_long,
                 g5_function_short, g5_function_long,
                 g6_function_short, g6_function_long,
                 g1_function_long_3sec, g2_function_long_3sec,
                 g3_function_long_3sec, g4_function_long_3sec,
                 g5_function_long_3sec, g6_function_long_3sec,
                 g1_function_long_2sec, g2_function_long_2sec,
                 g3_function_long_2sec, g4_function_long_2sec,
                 g5_function_long_2sec, g6_function_long_2sec):
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
        self.g1_function_long_3sec = g1_function_long_3sec
        self.g2_function_long_3sec = g2_function_long_3sec
        self.g3_function_long_3sec = g3_function_long_3sec
        self.g4_function_long_3sec = g4_function_long_3sec
        self.g5_function_long_3sec = g5_function_long_3sec
        self.g6_function_long_3sec = g6_function_long_3sec
        self.g1_function_long_2sec = g1_function_long_2sec
        self.g2_function_long_2sec = g2_function_long_2sec
        self.g3_function_long_2sec = g3_function_long_2sec
        self.g4_function_long_2sec = g4_function_long_2sec
        self.g5_function_long_2sec = g5_function_long_2sec
        self.g6_function_long_2sec = g6_function_long_2sec
        self.time_now_press = float()
        self.time_now_press_keyId = ''
        self.time_now_release = float()
        self.time_now_release_keyId = ''
        self.time_now_press_hold = float()
        self.allow_sdk_event = True

    def gkey_sub_thread_stop(self):
        global thread_eject, thread_mount, thread_unmount

        if thread_eject[0].isRunning() is True:
            thread_eject[0].stop()

        if thread_mount[0].isRunning() is True:
            thread_mount[0].stop()

        if thread_unmount[0].isRunning() is True:
            thread_unmount[0].stop()
        # try:
        #     thread_eject[0].stop()
        # except Exception as e:
        #     print('error stopping thread_eject:', e)
        # try:
        #     thread_mount[0].stop()
        # except Exception as e:
        #     print('error stopping thread_mount:', e)
        # try:
        #     thread_unmount[0].stop()
        # except Exception as e:
        #     print('error stopping thread_unmount:', e)

    def on_press(self, event_id, data):
        # print('-- [SdkEventHandlerClass.on_press]: plugged in')
        global sdk, devices_kb, devices_kb_selected, g_key_pressed, thread_gkey_pressed, time_now_press, bool_exclsuive_g2key_allow

        try:

            date_time_now = str(datetime.datetime.now())
            var = date_time_now.split(' ')
            var = var[1].split(':')[2]
            self.time_now_press = float(var)
            self.time_now_press_keyId = str(data.keyId).strip()
            print('-- [SdkEventHandlerClass.on_press] captured event: time_now_0: {0} pressed {1}'.format(self.time_now_press, data.keyId))

            g_key_pressed = str(data.keyId).strip()
            time_now_press = self.time_now_press

            if bool_exclsuive_g2key_allow is True:
                self.gkey_sub_thread_stop()

            thread_gkey_pressed[0].start()

        except Exception as e:
            print('-- [SdkEventHandlerClass.on_press] Error:', e)

    def on_release(self, event_id, data):
        global thread_gkey_pressed, thread_eject, thread_mount, thread_unmount
        global bool_switch_g2_disks
        # print('-- [SdkEventHandlerClass.on_release]: plugged in')

        try:
            thread_gkey_pressed[0].stop()
        except Exception as e:
            print('-- [SdkEventHandlerClass.on_release] Error:', e)

        try:

            date_time_now = str(datetime.datetime.now())
            var = date_time_now.split(' ')
            var = var[1].split(':')[2]
            time_now_release = float(var)
            self.time_now_release_keyId = str(data.keyId).strip()

            if self.time_now_release_keyId == 'CorsairKeyId.Kb_G1':
                if time_now_release < (self.time_now_press + 1.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                    self.g1_function_short()

                elif time_now_release >= (self.time_now_press + 1.0) and time_now_release < (self.time_now_press + 2.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 1 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g1_function_long()

                elif time_now_release >= (self.time_now_press + 2.0) and time_now_release < (self.time_now_press + 3.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 2 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g1_function_long_2sec()

                elif time_now_release >= (self.time_now_press + 3.0) and time_now_release < (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 3 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g1_function_long_3sec()

                elif time_now_release >= (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 4 seconds (ignore) {1}'.format(self.time_now_press, data.keyId))

            elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G2':
                if time_now_release < (self.time_now_press + 1.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                    # self.g2_function_short()

                elif time_now_release >= (self.time_now_press + 1.0) and time_now_release < (self.time_now_press + 2.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 1 seconds {1}'.format(self.time_now_press, data.keyId))
                    if bool_switch_g2_disks is True:
                        thread_eject[0].start()

                elif time_now_release >= (self.time_now_press + 2.0) and time_now_release < (self.time_now_press + 3.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 2 seconds {1}'.format(self.time_now_press, data.keyId))
                    if bool_switch_g2_disks is True:
                        thread_mount[0].start()

                elif time_now_release >= (self.time_now_press + 3.0) and time_now_release < (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 3 seconds {1}'.format(self.time_now_press, data.keyId))
                    if bool_switch_g2_disks is True:
                        thread_unmount[0].start()

                elif time_now_release >= (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 4 seconds (ignore) {1}'.format(self.time_now_press, data.keyId))

            elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G3':
                if time_now_release < (self.time_now_press + 1.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                    self.g3_function_short()

                elif time_now_release >= (self.time_now_press + 1.0) and time_now_release < (self.time_now_press + 2.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 1 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g3_function_long()

                elif time_now_release >= (self.time_now_press + 2.0) and time_now_release < (self.time_now_press + 3.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 2 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g3_function_long_2sec()

                elif time_now_release >= (self.time_now_press + 3.0) and time_now_release < (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 3 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g3_function_long_3sec()

                elif time_now_release >= (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 4 seconds (ignore) {1}'.format(self.time_now_press, data.keyId))

            elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G4':
                if time_now_release < (self.time_now_press + 1.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                    self.g4_function_short()

                elif time_now_release >= (self.time_now_press + 1.0) and time_now_release < (self.time_now_press + 2.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 1 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g4_function_long()

                elif time_now_release >= (self.time_now_press + 2.0) and time_now_release < (self.time_now_press + 3.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 2 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g4_function_long_2sec()

                elif time_now_release >= (self.time_now_press + 3.0) and time_now_release < (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 3 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g4_function_long_3sec()

                elif time_now_release >= (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 4 seconds (ignore) {1}'.format(self.time_now_press, data.keyId))

            elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G5':
                if time_now_release < (self.time_now_press + 1.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                    self.g5_function_short()

                elif time_now_release >= (self.time_now_press + 1.0) and time_now_release < (self.time_now_press + 2.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 1 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g5_function_long()

                elif time_now_release >= (self.time_now_press + 2.0) and time_now_release < (self.time_now_press + 3.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 2 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g5_function_long_2sec()

                elif time_now_release >= (self.time_now_press + 3.0) and time_now_release < (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 3 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g5_function_long_3sec()

                elif time_now_release >= (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 4 seconds (ignore) {1}'.format(self.time_now_press, data.keyId))

            elif self.time_now_release_keyId == 'CorsairKeyId.Kb_G6':
                if time_now_release < (self.time_now_press + 1.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} short released {1}'.format(self.time_now_press, data.keyId))
                    self.g6_function_short()

                elif time_now_release >= (self.time_now_press + 1.0) and time_now_release < (self.time_now_press + 2.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 1 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g6_function_long()

                elif time_now_release >= (self.time_now_press + 2.0) and time_now_release < (self.time_now_press + 3.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 2 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g6_function_long_2sec()

                elif time_now_release >= (self.time_now_press + 3.0) and time_now_release < (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 3 seconds {1}'.format(self.time_now_press, data.keyId))
                    self.g6_function_long_3sec()

                elif time_now_release >= (self.time_now_press + 4.0) and self.time_now_press_keyId == self.time_now_release_keyId:
                    print('-- [App.on_press] captured event: time_now_1: {0} long released 4 seconds (ignore) {1}'.format(self.time_now_press, data.keyId))

        except Exception as e:
            print('-- [SdkEventHandlerClass.on_press] Error:', e)

    def sdk_event_handler(self, event_id, data):
        try:
            if event_id == CorsairEventId.KeyEvent:
                try:
                    if data.isPressed:
                        try:
                            self.on_press(event_id, data)
                        except Exception as e:
                            print('-- [SdkEventHandlerClass.on_press] Error:', e)
                    else:
                        self.on_release(event_id, data)
                except Exception as e:
                    print('-- [SdkEventHandlerClass.on_press] Error:', e)
            elif event_id == CorsairEventId.DeviceConnectionStatusChangedEvent:
                print("-- [SdkEventHandlerClass.sdk_event_handler]: Device id: %s   Status: %s" % (data.deviceId.decode(), "connected" if data.isConnected else "disconnected"))
            else:
                print("-- [SdkEventHandlerClass.sdk_event_handler]: invalid event")

        except Exception as e:
            print('-- [SdkEventHandlerClass.on_press] Error:', e)

    def run(self):
        global sdk, devices_kb, devices_kb_name
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
        while True:
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


class CompileDiskGUIDDictionaryListClass(QThread):
    print('-- [CompileDiskGUIDDictionaryListClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        print('-- [CompileDiskGUIDDictionaryListClass.run]: plugged in')
        global disk_guid

        while True:
            # subprocess
            cmd_output = []
            xcmd = subprocess.Popen("powershell mountvol", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while True:
                output = xcmd.stdout.readline()
                if output == '' and xcmd.poll() is not None:
                    break
                if output:
                    cmd_output.append(str(output.decode("utf-8").strip()))
                else:
                    break
                rc = xcmd.poll()
            # parse subprocess output
            guid = ''
            disk_let = ''
            i_1 = 0
            for _ in cmd_output:
                # print('-- [CompileDiskGUIDDictionaryListClass.run] raw output:', _)
                if len(_) == 3:
                    if os.path.exists(_):
                        # if cmd_output[i-1].startswith('\\\\'):  # and os.path.exists(_+'\\')
                        icmd = i_1 - 1
                        guid = cmd_output[icmd]
                        disk_let = _
                        # print('-- [CompileDiskGUIDDictionaryListClass.run] raw output:', _, guid)
                        # Create a list of all values in list of dictionaries
                        list_of_all_values = [value for elem in disk_guid for value in elem.values()]
                        # add dictionary to list
                        if guid not in list_of_all_values:
                            if guid.startswith('\\\\'):
                                # print('appending:', disk_let, guid)
                                disk_guid.append({disk_let: guid})
                        # else update key value pair in list
                        elif guid in list_of_all_values:
                            # print('check')
                            iguid = 0
                            for disk_guids in disk_guid:
                                # print(disk_guid[iguid])
                                try:
                                    dict_str = str(disk_guid[iguid])
                                    dict_str = dict_str.replace("{'", "")
                                    dict_str = dict_str[:1]
                                    dict_str = dict_str+':\\'
                                    # print('dict key:', dict_str)
                                    if disk_guid[iguid][dict_str] == guid:
                                        # print('target:', disk_guid[iguid])
                                        # print('live key:', disk_let)
                                        if disk_let != dict_str:
                                            print('-- [CompileDiskGUIDDictionaryListClass.run] update key value pair:', disk_guid[iguid], '>>', disk_let, guid)
                                            try:
                                                del disk_guid[iguid]
                                                disk_guid.append({disk_let: guid})
                                            except Exception as e:
                                                print('-- [CompileDiskGUIDDictionaryListClass.run] Error:', e)

                                except Exception as e:
                                    pass
                                iguid += 1
                i_1 += 1
            time.sleep(2)

    def stop(self):
        print('-- [CompileDiskGUIDDictionaryListClass.stop]: plugged in')
        self.terminate()


class KeyEventClass(QThread):
    print('-- [KeyEventClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def capslock_state(self):
        import ctypes
        user32_dll = ctypes.WinDLL("User32.dll")
        vk_capital = 0x14
        return user32_dll.GetKeyState(vk_capital)

    def capslock_function(self):
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight

        capslock = self.capslock_state()
        if ((capslock) & 0xffff) != 0:
            # print('-- [KeyEventClass.run] capslock state: enabled')
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({37: (255, 255, 0)}))
            except Exception as e:
                print(e)
        elif ((capslock) & 0xffff) == 0:
            # print('-- [KeyEventClass.run] capslock state: disabled')
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({37: sdk_color_backlight}))
            except Exception as e:
                print(e)

    def run(self):
        print('-- [KeyEventClass.run]: plugged in')
        global bool_g2_input, kb_event
        while True:
            if bool_g2_input is True:
                kb_event = keyboard.read_key()
                bool_g2_input = False
            self.capslock_function()
            """ Example use of keyboard module
            keyboard.wait('-')
            """
            time.sleep(0.1)

    def stop(self):
        print('-- [KeyEventClass.stop]: plugged in')
        self.terminate()


class IsLockedClass(QThread):
    print('-- [IsLockedClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.locked = None
        self.locked_prev = None

    def run(self):
        print('-- [IsLockedClass.run]: plugged in')
        global thread_compile_devices, devices_previous
        while True:
            try:
                process_name = 'LogonUI.exe'
                callall = 'TASKLIST'
                outputall = subprocess.check_output(callall)
                outputstringall = str(outputall)

                if process_name in outputstringall:
                    self.locked = True
                    if self.locked != self.locked_prev:
                        self.locked_prev = True
                        print("-- [IsLockedClass]: Locked.")
                        devices_previous = []
                        thread_compile_devices[0].stop()
                else:
                    self.locked = False
                    if self.locked != self.locked_prev:
                        self.locked_prev = False
                        print("-- [IsLockedClass]: Unlocked.")
                        devices_previous = []
                        thread_compile_devices[0].start()

            except Exception as e:
                print("-- [IsLockedClass]: Error:", e)
            time.sleep(1.5)

    def stop(self):
        print('-- [IsLockedClass.stop]: plugged in')
        self.terminate()


class PowerClass(QThread):
    print('-- [PowerClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.active_pp = -1
        self.active_pp_prev = -1

    def run(self):
        print('-- [PowerClass.run]: plugged in')
        global power_plan, power_plan_index, devices_kb, devices_kb_selected, sdk, bool_onpress_clause_g1, notification_key
        while True:
            try:
                """ subprocess """
                cmd_output = []
                xcmd = subprocess.Popen("powercfg /LIST", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while True:
                    output = xcmd.stdout.readline()
                    if output == '' and xcmd.poll() is not None:
                        break
                    if output:
                        cmd_output.append(str(output.decode("utf-8").strip()))
                    else:
                        break
                    rc = xcmd.poll()
                i = 0
                for _ in cmd_output:
                    if _.endswith('*'):
                        # print('-- [PowerClass.run] active power plan:', _)
                        if 'Power saver' in _:
                            self.active_pp = 1
                            if self.active_pp != self.active_pp_prev:
                                notification_key = 3
                            power_plan_index = 0
                            # if self.active_pp != self.active_pp_prev:
                            if bool_onpress_clause_g1 is not True:
                                self.active_pp_prev = 1
                                try:
                                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (255, 0, 0)}))
                                except Exception as e:
                                    print(e)

                                """ Example Overlay Call
                                open('./system_overlay.dat', 'w').close()
                                with open('./system_overlay.dat', 'w') as fo:
                                    fo.writelines('POWER SAVER')
                                fo.close()
                                """

                        elif 'Balanced' in _:
                            self.active_pp = 2
                            if self.active_pp != self.active_pp_prev:
                                notification_key = 4
                            power_plan_index = 1
                            # if self.active_pp != self.active_pp_prev:
                            if bool_onpress_clause_g1 is not True:
                                self.active_pp_prev = 2
                                try:
                                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (0, 255, 0)}))
                                except Exception as e:
                                    print(e)

                                """ Example Overlay Call
                                open('./system_overlay.dat', 'w').close()
                                with open('./system_overlay.dat', 'w') as fo:
                                    fo.writelines('BALANCED')
                                fo.close()
                                """

                        elif 'High performance' in _:
                            self.active_pp = 3
                            if self.active_pp != self.active_pp_prev:
                                notification_key = 5
                            power_plan_index = 2
                            # if self.active_pp != self.active_pp_prev:
                            if bool_onpress_clause_g1 is not True:
                                self.active_pp_prev = 3
                                try:
                                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (0, 255, 255)}))
                                except Exception as e:
                                    print(e)

                                """ Example Overlay Call
                                open('./system_overlay.dat', 'w').close()
                                with open('./system_overlay.dat', 'w') as fo:
                                    fo.writelines('HIGH PERFORMANCE')
                                fo.close()
                                """

                        elif 'Ultimate Performance' in _:
                            self.active_pp = 4
                            if self.active_pp != self.active_pp_prev:
                                notification_key = 6
                            power_plan_index = 3
                            # if self.active_pp != self.active_pp_prev:
                            if bool_onpress_clause_g1 is not True:
                                self.active_pp_prev = 4
                                try:
                                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: (255, 15, 100)}))
                                except Exception as e:
                                    print(e)

                                """ Example Overlay Call
                                open('./system_overlay.dat', 'w').close()
                                with open('./system_overlay.dat', 'w') as fo:
                                    fo.writelines('ULTIMATE PERFORMANCE')
                                fo.close()
                                """

                    if _.startswith('Power Scheme GUID:'):

                        if canonical_caseless('Power saver') in canonical_caseless(_) and canonical_caseless('Power saver') not in power_plan:
                            power_plan[0] = _
                        if canonical_caseless('Balanced') in canonical_caseless(_) and canonical_caseless('Balanced') not in power_plan:
                            power_plan[1] = _
                        if canonical_caseless('High performance') in canonical_caseless(_) and canonical_caseless('High performance') not in power_plan:
                            power_plan[2] = _
                        if canonical_caseless('Ultimate Performance') in canonical_caseless(_) and canonical_caseless('Ultimate Performance') not in power_plan:
                            power_plan[3] = _

                        i += 1

            except Exception as e:
                print('-- [PowerClass.run] Error:', e)

            time.sleep(1)

    def stop(self):
        print('-- [PowerClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        self.active_pp = -1
        self.active_pp_prev = -1
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({121: sdk_color_backlight}))
        except Exception as e:
            print('-- [PowerClass.stop] Error:', e)
        self.terminate()


class PauseLoopClass(QThread):
    print('-- [PauseLoopClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight

        while True:
            if len(devices_kb) >= 1:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: (255, 255, 0)}))
                except Exception as e:
                    print(e)
            time.sleep(0.6)
            if len(devices_kb) >= 1:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: sdk_color_backlight}))
                except Exception as e:
                    print(e)
            time.sleep(0.6)

    def stop(self):
        print('-- [PauseLoopClass.stop]: plugged in')
        self.terminate()


class MediaDisplayClass(QThread):
    print('-- [MediaDisplayClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.bool_mute = None
        self.bool_mute_prev = None
        self.media_state = -1
        self.media_state_prev = -1

    def send_instruction_on(self):
        # print('-- [MediaDisplayClass.send_instruction_on]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        if len(devices_kb) >= 1:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({98: (0, 255, 0)}))
            except Exception as e:
                print(e)

    def send_instruction_off(self):
        # print('-- [MediaDisplayClass.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        if len(devices_kb) >= 1:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({98: (255, 0, 0)}))
            except Exception as e:
                print(e)

    def send_instruction_off_1(self):
        # print('-- [MediaDisplayClass.send_instruction_off]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_kb) >= 1:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({98: sdk_color_backlight}))
            except Exception as e:
                print(e)

    async def get_media_state(self):
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, thread_pause_loop
        sessions = await MediaManager.request_async()

        current_session = sessions.get_current_session()

        if current_session != None:

            if int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING) == current_session.get_playback_info().playback_status:
                self.media_state = 1
                if self.media_state != self.media_state_prev:
                    print('-- [MediaDisplayClass.run]: PLAYING')
                    self.media_state_prev = 1
                    thread_pause_loop[0].stop()
                    try:
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: (0, 255, 0)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: (0, 0, 255)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: (0, 0, 255)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: sdk_color_backlight}))
                    except Exception as e:
                        print(e)

            if int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.PAUSED) == current_session.get_playback_info().playback_status:
                self.media_state = 2
                if self.media_state != self.media_state_prev:
                    print('-- [MediaDisplayClass.run]: PAUSED')
                    self.media_state_prev = 2
                    thread_pause_loop[0].start()
                    try:
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: (255, 100, 0)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: (255, 100, 0)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: sdk_color_backlight}))
                    except Exception as e:
                        print(e)

            if int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.STOPPED) == current_session.get_playback_info().playback_status:
                self.media_state = 0
                if self.media_state != self.media_state_prev:
                    print('-- [MediaDisplayClass.run]: STOPPED')
                    self.media_state_prev = 0
                    thread_pause_loop[0].stop()
                    try:
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: sdk_color_backlight}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: (255, 0, 0)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: sdk_color_backlight}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: sdk_color_backlight}))
                    except Exception as e:
                        print(e)

            if int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.CLOSED) == current_session.get_playback_info().playback_status:
                self.media_state = 0
                if self.media_state != self.media_state_prev:
                    print('-- [MediaDisplayClass.run]: CLOSED')
                    self.media_state_prev = 0
                    thread_pause_loop[0].stop()
                    try:
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: sdk_color_backlight}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: (255, 0, 0)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: sdk_color_backlight}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: sdk_color_backlight}))
                    except Exception as e:
                        print(e)

            if int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus.CHANGING) == current_session.get_playback_info().playback_status:
                self.media_state = 0
                if self.media_state != self.media_state_prev:
                    print('-- [MediaDisplayClass.run]: CHANGING')
                    self.media_state_prev = 0
                    thread_pause_loop[0].stop()
                    try:
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: sdk_color_backlight}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: (255, 0, 0)}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: sdk_color_backlight}))
                        if len(devices_kb) >= 1:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: sdk_color_backlight}))
                    except Exception as e:
                        print(e)

        else:
            self.media_state = 0
            if self.media_state != self.media_state_prev:
                print('-- [MediaDisplayClass.run]: CLOSED')
                self.media_state_prev = 0
                thread_pause_loop[0].stop()
                try:
                    if len(devices_kb) >= 1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: sdk_color_backlight}))
                    if len(devices_kb) >= 1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: (255, 0, 0)}))
                    if len(devices_kb) >= 1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: sdk_color_backlight}))
                    if len(devices_kb) >= 1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: sdk_color_backlight}))
                except Exception as e:
                    print(e)

    def run(self):
        print('-- [MediaDisplayClass.run]: plugged in')
        while True:
            try:
                self.current_media_info_1 = asyncio.run(self.get_media_state())
            except Exception as e:
                print('-- [MediaDisplayClass.run] Error:', e)

            try:
                """ subprocess """
                cmd_output = []
                cmd = 'powershell ./check_mute.ps1'
                xcmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = xcmd.stdout.readline()
                if output == '' and xcmd.poll() is not None:
                    break
                if output:
                    cmd_output.append(str(output.decode("utf-8").strip()))
                else:
                    break
                rc = xcmd.poll()

                """ parse standard output """
                for _ in cmd_output:
                    # print('-- [MediaDisplayClass.run] output:', _)
                    if _ == 'False':
                        self.bool_mute = False
                        if self.bool_mute_prev is True or self.bool_mute_prev is None:
                            print('-- [MediaDisplayClass.run]: un-muted')
                            self.bool_mute_prev = False
                            self.send_instruction_on()
                    elif _ == 'True':
                        self.bool_mute = True
                        if self.bool_mute_prev is False or self.bool_mute_prev is None:
                            print('-- [MediaDisplayClass.run]: muted')
                            self.bool_mute_prev = True
                            self.send_instruction_off()

                    else:
                        self.bool_mute = None
                        self.bool_mute_prev = None
                        self.send_instruction_off_1()

            except Exception as e:
                print('-- [MediaDisplayClass.run] Error:', e)
                time.sleep(1)

            time.sleep(0.1)

    def stop(self):
        print('-- [MediaDisplayClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight
        self.bool_mute = None
        self.bool_mute_prev = None
        self.media_state = -1
        self.media_state_prev = -1
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({98: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({99: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({101: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({100: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({102: sdk_color_backlight}))
        except Exception as e:
            print('-- [MediaDisplayClass.stop] Error:', e)
        self.terminate()


class TemperatureClass(QThread):
    print('-- [TemperatureClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        global sdk_color_cpu_on, sdk_color_vram_on
        self.cpu_pack = ''
        self.gpu_core = ''
        self.stored_cpu_color = sdk_color_cpu_on
        self.stored_vram_color = sdk_color_vram_on

    def send_instruction(self):
        global sdk, devices_kb, devices_kb_selected
        global bool_cpu_temperature, bool_vram_temperature, sdk_color_cpu_on, sdk_color_vram_on
        # print('-- [TemperatureClass.send_instruction]: plugged in')
        if bool_cpu_temperature is True:
            if self.cpu_pack != '':
                cpu_pack_0 = self.cpu_pack.split()
                cpu_pack_1 = cpu_pack_0[-1]
                cpu_pack_1 = cpu_pack_1.split('.')
                cpu_pack_2 = cpu_pack_1[0]
                cpu_pack_2 = int(cpu_pack_2)
                if cpu_pack_2 < 30:
                    rgb_cpu_temp = [0, 255, 255]
                elif cpu_pack_2 >= 30 and cpu_pack_2 < 50:
                    rgb_cpu_temp = [255, 255, 0]
                elif cpu_pack_2 >= 50 and cpu_pack_2 < 70:
                    rgb_cpu_temp = [255, 100, 0]
                elif cpu_pack_2 >= 70:
                    rgb_cpu_temp = [255, 0, 0]
                sdk_color_cpu_on = rgb_cpu_temp

        if bool_vram_temperature is True:
            if self.gpu_core != '':
                gpu_core_0 = self.gpu_core.split()
                gpu_core_1 = gpu_core_0[-1]
                gpu_core_1 = gpu_core_1.split('.')
                gpu_core_2 = gpu_core_1[0]
                gpu_core_2 = int(gpu_core_2)
                if gpu_core_2 < 30:
                    rgb_gpu_temp = [0, 255, 255]
                elif gpu_core_2 >= 30 and gpu_core_2 < 50:
                    rgb_gpu_temp = [255, 255, 0]
                elif gpu_core_2 >= 50 and gpu_core_2 < 70:
                    rgb_gpu_temp = [255, 100, 0]
                elif gpu_core_2 >= 70:
                    rgb_gpu_temp = [255, 0, 0]
                sdk_color_vram_on = rgb_gpu_temp

    def run(self):
        # print('-- [TemperatureClass.run]: plugged in')
        while True:
            cmd = os.path.join(os.getcwd() + '\\py\\temp_mon.vbs')
            xcmd = subprocess.Popen(cmd, shell=True)
            if os.path.exists('./py/temp_sys.dat'):
                try:
                    with open('./py/temp_sys.dat', 'r') as fo:
                        for line in fo:
                            line = line.strip()
                            if 'CPU Package' in line:
                                self.cpu_pack = line
                            if 'GPU Core' in line:
                                self.gpu_core = line
                    fo.close()

                except Exception as e:
                    print('-- [TemperatureClass.run] Error:', e)
            self.send_instruction()
            time.sleep(1)

    def stop(self):
        print('-- [TemperatureClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_backlight, sdk_color_cpu_on, sdk_color_vram_on
        sdk_color_cpu_on = self.stored_cpu_color
        sdk_color_vram_on = self.stored_vram_color
        self.terminate()


class BackLightClass(QThread):
    print('-- [BackLightClass]: plugged in')

    def __init__(self, color_all_id, btn_bck_light, btn_backlight_sub, btn_title_bar_style_1, btn_title_bar_style_0, btn_menu_style, btn_menu_style_1, lbl_backlight_sub):
        QThread.__init__(self)
        self.color_all_id = color_all_id
        self.btn_bck_light = btn_bck_light
        self.btn_backlight_sub = btn_backlight_sub
        self.btn_title_bar_style_0 = btn_title_bar_style_0
        self.btn_title_bar_style_1 = btn_title_bar_style_1
        self.btn_menu_style = btn_menu_style
        self.btn_menu_style_1 = btn_menu_style_1
        self.lbl_backlight_sub = lbl_backlight_sub

    def run(self):
        print('-- [BackLightClass.run]: plugged in')
        global backlight_time_0, backlight_time_1, bool_switch_backlight, sdk_color_backlight, sdk_color_backlight_on

        while True:
            date_time_now = str(datetime.datetime.now())
            time_now = date_time_now.split(' ')
            time_now_str = time_now[1].replace(':', '')
            time_now_str = time_now_str[:4]
            time_now_int = int(time_now_str)
            backlight_time_0_int = int(backlight_time_0)
            backlight_time_1_int = int(backlight_time_1)
            # print('-- [BackLightClass.run] target_time_0:', backlight_time_0, '   target_time_1:', backlight_time_1,'   time_now:', time_now[1], '   time_now_str:', time_now_str)
            if backlight_time_0_int < backlight_time_1_int:
                # print('-- [BackLightClass.run] auto backlight: backlight_time_0_int < backlight_time_1_int')
                if time_now_int >= backlight_time_0_int and time_now_int < backlight_time_1_int:
                    if bool_switch_backlight is False:
                        print('-- [BackLightClass.run] auto backlight: turning on')
                        bool_switch_backlight = True
                        self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_0)
                        self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                        self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style_1)
                        sdk_color_backlight = sdk_color_backlight_on
                        self.color_all_id()
                if time_now_int < backlight_time_0_int or time_now_int >= backlight_time_1_int:
                    if bool_switch_backlight is True:
                        print('-- [BackLightClass.run] auto backlight: turning off')
                        bool_switch_backlight = False
                        self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_1)
                        self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                        self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style)
                        sdk_color_backlight = (0, 0, 0)
                        self.color_all_id()
            elif backlight_time_0_int > backlight_time_1_int:
                # print('-- [BackLightClass.run] auto backlight: backlight_time_0_int > backlight_time_1_int')
                if time_now_str.startswith('0'):
                    if time_now_int <= backlight_time_0_int and time_now_int < backlight_time_1_int:
                        if bool_switch_backlight is False:
                            print('-- [BackLightClass.run] auto backlight: turning on')
                            bool_switch_backlight = True
                            self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_0)
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                            self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style_1)
                            sdk_color_backlight = sdk_color_backlight_on
                            self.color_all_id()
                    else:
                        if bool_switch_backlight is True:
                            print('-- [BackLightClass.run] auto backlight: turning off')
                            bool_switch_backlight = False
                            self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_1)
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                            self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style)
                            sdk_color_backlight = (0, 0, 0)
                            self.color_all_id()
                else:
                    if time_now_int <= backlight_time_1_int or time_now_int >= backlight_time_0_int:
                        if bool_switch_backlight is False:
                            print('-- [BackLightClass.run] auto backlight: turning on')
                            bool_switch_backlight = True
                            self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_0)
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_enabled.png"))
                            self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style_1)
                            sdk_color_backlight = sdk_color_backlight_on
                            self.color_all_id()
                    else:
                        if bool_switch_backlight is True:
                            print('-- [BackLightClass.run] auto backlight: turning off')
                            bool_switch_backlight = False
                            self.btn_bck_light.setStyleSheet(self.btn_title_bar_style_1)
                            self.btn_backlight_sub.setIcon(QIcon("./image/img_toggle_switch_disabled.png"))
                            self.lbl_backlight_sub.setStyleSheet(self.btn_menu_style)
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
                time.sleep(1)
            else:
                time.sleep(2)

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
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[1]: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[2]: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netshare[3]: sdk_color_backlight}))
        except Exception as e:
            print('-- [NetShareClass.stop] Error:', e)
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
        # pythoncom.CoInitialize()
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
                try:
                    if self.u_type == 0:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_0}))
                    elif self.u_type == 1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_1}))
                    elif self.u_type == 2:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_2}))
                    elif self.u_type == 3:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_net_traffic_utype_3}))
                except Exception as e:
                    print(e)
                if self.b_type == 0:
                    net_set = 0
                    while net_set < self.switch_num:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_bytes}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type == 1:
                    net_set = 0
                    while net_set < self.switch_num:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_kb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type == 2:
                    net_set = 0
                    while net_set < self.switch_num:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_mb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type == 3:
                    net_set = 0
                    while net_set < self.switch_num:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_gb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type == 4:
                    net_set = 0
                    while net_set < self.switch_num:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_set]: sdk_color_net_traffic_tb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
            if self.network_adapter_display_rcv_bool[net_rcv_i] is False and self.network_adapter_display_rcv_bool_prev[net_rcv_i] != self.network_adapter_display_rcv_bool[net_rcv_i]:
                self.network_adapter_display_rcv_bool_prev[net_rcv_i] = False
                self.switch_count += 1
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_rcv_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
            if self.network_adapter_display_rcv_bool == [False, False, False, False, False, False, False, False, False]:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_backlight}))
                except Exception as e:
                    print(e)
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
                try:
                    if self.u_type_1 == 0:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_0}))
                    elif self.u_type_1 == 1:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_1}))
                    elif self.u_type_1 == 2:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_2}))
                    elif self.u_type_1 == 3:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_net_traffic_utype_3}))
                except Exception as e:
                    print(e)
                if self.b_type_1 == 0:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_bytes}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type_1 == 1:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_kb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type_1 == 2:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_mb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type_1 == 3:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_gb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
                elif self.b_type_1 == 4:
                    net_set = 0
                    while net_set < self.switch_num_1:
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_set]: sdk_color_net_traffic_tb}))
                        except Exception as e:
                            print(e)
                        net_set += 1
            if self.network_adapter_display_snt_bool[net_snd_i] is False and self.network_adapter_display_snt_bool_prev[net_snd_i] != self.network_adapter_display_snt_bool[net_snd_i]:
                self.network_adapter_display_snt_bool_prev[net_snd_i] = False
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_snd_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
            if self.network_adapter_display_snt_bool == [False, False, False, False, False, False, False, False, False]:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_backlight}))
                except Exception as e:
                    print(e)
            net_snd_i += 1

    def send_instruction(self):
        # print('-- [NetworkMonClass.send_instruction]: plugged in')
        self.get_stat()
        try:
            self.snd_ins_netr()
            self.snd_ins_nets()
        except Exception as e:
            print('-- [NetworkMonClass.send_instruction] Error:', e)

    def get_stat(self):
        # print('-- [NetworkMonClass.get_stat]: plugged in')
        global devices_network_adapter_name
        network_adapter_exists_bool = False
        try:
            self.network_adapter_display_rcv_bool = [False, False, False, False, False, False, False, False, False]
            self.network_adapter_display_snt_bool = [False, False, False, False, False, False, False, False, False]
            rec_item = ''
            sen_item = ''
            # print('-- [NetworkMonClass.send_instruction] testing wmi call: 1')
            try:
                pythoncom.CoInitialize()
                wmis = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            except Exception as e:
                print(e)
                self.get_stat()
            # print('-- [NetworkMonClass.send_instruction] testing wmi call: 2')
            try:
                wbems = wmis.ConnectServer(".", "root\\cimv2")
            except Exception as e:
                print(e)
                self.get_stat()
            # print('-- [NetworkMonClass.send_instruction] testing wmi call: 3')
            try:
                col_items = wbems.ExecQuery('SELECT * FROM Win32_PerfFormattedData_Tcpip_NetworkAdapter')
            except Exception as e:
                print(e)
                self.get_stat()
            # print('-- [NetworkMonClass.send_instruction] testing wmi call: 4')
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
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv[net_rcv_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
                net_rcv_i += 1
        except Exception as e:
            print('-- [NetworkMonClass.stop] Error:', e)
            pass
        try:
            net_rcv_i = 0
            for _ in corsairled_id_num_netsnt:
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt[net_rcv_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
                net_rcv_i += 1
        except Exception as e:
            print('-- [NetworkMonClass.stop] Error:', e)
            pass
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netrcv_utype: sdk_color_backlight}))
        except Exception as e:
            print(e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_netsnt_utype: sdk_color_backlight}))
        except Exception as e:
            print(e)
            pass
        print('-- [NetworkMonClass.stop] terminating')
        self.terminate()


class InternetConnectionClass(QThread):
    print('-- [InternetConnectionClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.ping_key = int()
        self.ping_bool_prev = None
        self.ping_fail_i = 0
        self.rgb_key = ()

    def run(self):
        print('-- [InternetConnectionClass.run]: plugged in')
        global devices_kb
        while True:
            try:
                if len(devices_kb) >= 1 or len(devices_ms) >= 1:
                    self.ping_fail_i = 0
                    self.ping()
                    self.send_instruction()
                    time.sleep(1)
                else:
                    time.sleep(2)
            except Exception as e:
                print('-- [InternetConnectionClass.stop] Error:', e)

    def send_instruction_on(self):
        # print('-- [InternetConnectionClass.send_instruction_on]: plugged in')
        global devices_ms, bool_switch_startup_net_con_ms, corsairled_id_num_netcon_ms, corsairled_id_num_ms_complete, devices_ms_selected, devices_kb, bool_switch_startup_net_con_kb, devices_kb_selected, sdk_color_backlight
        if len(devices_ms) >= 1 and bool_switch_startup_net_con_ms is True:
            if corsairled_id_num_netcon_ms < len(corsairled_id_num_ms_complete):
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: (self.rgb_key)}))
                except Exception as e:
                    print(e)
        if len(devices_kb) >= 1 and bool_switch_startup_net_con_kb is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({170: (self.rgb_key)}))
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({188: (self.rgb_key)}))
            except Exception as e:
                print(e)

    def send_instruction_off(self):
        # print('-- [InternetConnectionClass.send_instruction_off]: plugged in')
        global devices_ms, bool_switch_startup_net_con_ms, corsairled_id_num_netcon_ms, corsairled_id_num_ms_complete, devices_ms_selected, devices_kb, bool_switch_startup_net_con_kb, devices_kb_selected
        if len(devices_ms) >= 1 and bool_switch_startup_net_con_ms is True:
            if corsairled_id_num_netcon_ms < len(corsairled_id_num_ms_complete):
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
        if len(devices_kb) >= 1 and bool_switch_startup_net_con_kb is True:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({170: sdk_color_backlight}))
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({188: sdk_color_backlight}))
            except Exception as e:
                print(e)

    def send_instruction(self):
        # print('-- [InternetConnectionClass.send_instruction]: plugged in')
        global sdk, devices_ms, devices_ms_selected, corsairled_id_num_ms_complete, ping_test_key_id, corsairled_id_num_netcon_kb
        global corsairled_id_num_netcon_ms, bool_switch_startup_net_con_ms, bool_switch_startup_net_con_kb, devices_kb, devices_kb_selected
        global bool_switch_startup_net_traffic

        if self.ping_key == 1 and self.ping_key != self.ping_bool_prev:
            # print('-- [1] (0% loss)')
            self.rgb_key = (100, 255, 0)
            self.send_instruction_on()
            self.ping_bool_prev = 1
        if self.ping_key == 2 and self.ping_key != self.ping_bool_prev:
            # print('-- [1] intermittent')
            self.rgb_key = (255, 75, 0)
            self.send_instruction_on()
            time.sleep(2)
            self.ping_bool_prev = 2
        elif self.ping_key == 0 and self.ping_key != self.ping_bool_prev:
            # print('-- [1] Destination host unreachable')
            self.rgb_key = (255, 0, 0)
            self.send_instruction_on()
            self.ping_bool_prev = 0

    def ping(self):
        # print('-- [InternetConnectionClass.ping]: plugged in')
        self.ping_key = 0
        cmd = 'ping -n 2 -l 1 8.8.8.8'  # Google
        try:
            foocheck = False
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            stdout, stderror = p.communicate()
            output = stdout.decode('UTF-8')
            lines = output.split(os.linesep)
            for _ in lines:
                if 'Packets: Sent = 2, Received = 2, Lost = 0 (0% loss)' in _:
                    for liness in lines:
                        if 'Destination host unreachable.' in liness:
                            foocheck = True
                            break
                    if foocheck is False:
                        # print('-- [0] (0% loss)')
                        self.ping_key = 1
                elif 'Packets: Sent = 2, Received = 1, Lost = 1 (50% loss)' in _:
                    for liness in lines:
                        if 'Destination host unreachable.' in liness:
                            foocheck = True
                            break
                    if foocheck is False:
                        # print('-- [0] (50% loss)')
                        self.ping_key = 2
                elif 'Destination host unreachable.' in _ or 'PING: transmit failed. General failure.' in _:
                    # print('-- [0] Destination host unreachable')
                    self.ping_key = 0
        except Exception as e:
            print('-- [InternetConnectionClass.ping] Error:', e)

    def stop(self):
        print('-- [InternetConnectionClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, corsairled_id_num_ms_complete, corsairled_id_num_netcon_ms
        self.ping_bool_prev = None
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_ms[devices_ms_selected], ({corsairled_id_num_ms_complete[corsairled_id_num_netcon_ms]: sdk_color_backlight}))
        except Exception as e:
            print('-- [InternetConnectionClass.stop] Error:', e)
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({170: sdk_color_backlight}))
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({188: sdk_color_backlight}))
        except Exception as e:
            print('-- [InternetConnectionClass.stop] Error:', e)
        print('-- [InternetConnectionClass.stop] terminating')
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
        # pythoncom.CoInitialize()
        global sdk, devices_kb

        self.i_w = int()
        self.i_r = int()
        self.b_type_key = ()
        self.bool_dwps_greater = False
        self.dwps = ()
        self.drps = ()
        self.disk_letter_complete = []
        self.i_umount = int()

        while True:
            try:
                if len(devices_kb) >= 1:
                    try:
                        self.get_stat()
                    except Exception as e:
                        print('-- [HddMonClass.run] Error:', e)
                    time.sleep(timing_hdd_util)
                else:
                    time.sleep(1)
            except Exception as e:
                print('-- [HddMonClass.run] Error:', e)
                time.sleep(1)

    def send_write_instruction(self):
        # print('-- [HddMonClass.send_write_instruction]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddwrite_on
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_w]: sdk_color_hddwrite_on}))
        except Exception as e:
            print('-- [HddMonClass.send_write_instruction] Error:', e)

    def send_read_instruction(self):
        # print('-- [HddMonClass.send_read_instruction]: plugged in')
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddread_on
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_r]: sdk_color_hddread_on}))
        except Exception as e:
            print('-- [HddMonClass.send_read_instruction] Error:', e)

    def send_write_instruction_1(self):
        # print('-- [HddMonClass.send_write_instruction_1]: plugged in')
        global bool_switch_display_disk_mount
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddwrite_on, sdk_color_backlight
        try:
            if bool_switch_display_disk_mount is True:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_w]: (0, 0, 255)}))
            else:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_w]: sdk_color_backlight}))
        except Exception as e:
            print('-- [HddMonClass.send_write_instruction_1] Error:', e)

    def send_read_instruction_1(self):
        # print('-- [HddMonClass.send_read_instruction_1]: plugged in')
        global bool_switch_display_disk_mount
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddread_on, sdk_color_backlight
        try:
            if bool_switch_display_disk_mount is True:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_r]: (0, 0, 255)}))
            else:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_r]: sdk_color_backlight}))
        except Exception as e:
            print('-- [HddMonClass.send_read_instruction_1] Error:', e)

    def send_instruction_umounted(self):
        # print('-- [HddMonClass.send_instruction_umounted]: plugged in')
        global bool_switch_display_disk_mount
        global sdk, devices_kb, devices_kb_selected
        global corsairled_id_num_hddreadwrite, sdk_color_hddread_on, sdk_color_backlight
        try:
            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[self.i_umount]: sdk_color_backlight}))
        except Exception as e:
            print('-- [HddMonClass.send_instruction_umounted] Error:', e)

    def get_stat(self):
        # print('-- [HddMonClass.get_stat]: plugged in')
        global alpha_str, hdd_bytes_type_w, hdd_bytes_type_r, hdd_bytes_str, bool_alpha_stage_engaged
        get_stat_allow = False
        try:
            self.disk_letter_complete = []
            try:
                try:
                    pythoncom.CoInitialize()
                    hdd_wmis = win32com.client.Dispatch("WbemScripting.SWbemLocator")
                except Exception as e:
                    print(e)
                    self.get_stat()
                try:
                    hdd_wbems = hdd_wmis.ConnectServer(".", "root\\cimv2")
                except Exception as e:
                    print(e)
                    self.get_stat()
                try:
                    hdd_col_items = hdd_wbems.ExecQuery("SELECT * FROM Win32_PerfFormattedData_PerfDisk_PhysicalDisk")
                except Exception as e:
                    print(e)
                    self.get_stat()
                get_stat_allow = True
            except Exception as e:
                print(e)
                get_stat_allow = False
            if get_stat_allow is True:
                for objItem in hdd_col_items:
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
                                    if self.dwps == 0 or self.drps == 0:
                                        self.i_w = 0
                                        for _ in alpha_str:
                                            if canonical_caseless(disk_letter_0) == canonical_caseless(alpha_str[self.i_w]):
                                                if bool_alpha_stage_engaged is False:
                                                    self.send_write_instruction_1()
                                            self.i_w += 1
                                    elif self.dwps > 0 or self.drps > 0:
                                        if self.dwps >= self.drps:
                                            self.bool_dwps_greater = True
                                            self.i_w = 0
                                            for _ in alpha_str:
                                                if canonical_caseless(disk_letter_0) == canonical_caseless(alpha_str[self.i_w]):
                                                    if bool_alpha_stage_engaged is False:
                                                        self.send_write_instruction()
                                                self.i_w += 1
                                        elif self.dwps < self.drps:
                                            self.bool_dwps_greater = False
                                            self.i_r = 0
                                            for _ in alpha_str:
                                                if canonical_caseless(disk_letter_0) == canonical_caseless(alpha_str[self.i_r]):
                                                    if bool_alpha_stage_engaged is False:
                                                        self.send_read_instruction()
                                                self.i_r += 1
                self.i_umount = 0
                for _ in alpha_str:
                    if _.upper() not in self.disk_letter_complete:
                        if bool_alpha_stage_engaged is False:
                            self.send_instruction_umounted()
                    self.i_umount += 1
        except Exception as e:
            print('-- [HddMonClass.get_stat] Error:', e)

    def stop(self):
        print('-- [HddMonClass.stop]: plugged in')
        global sdk, devices_kb, devices_kb_selected, sdk_color_hddread_on, sdk_color_hddwrite_on, sdk_color_backlight, corsairled_id_num_hddreadwrite

        hdd_i = 0
        for _ in corsairled_id_num_hddreadwrite:
            try:
                sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_hddreadwrite[hdd_i]: sdk_color_backlight}))
            except Exception as e:
                print('-- [HddMonClass.stop] Error:', e)

            hdd_i += 1
            
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
                try:
                    if self.cpu_key[cpu_i] is True:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_cpu[cpu_i]: sdk_color_cpu_on}))
                        self.cpu_key_prev[cpu_i] = True
                    elif self.cpu_key[cpu_i] is False:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_cpu[cpu_i]: sdk_color_backlight}))
                        self.cpu_key_prev[cpu_i] = False
                except Exception as e:
                    print(e)
                cpu_i += 1
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
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_cpu[cpu_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
                cpu_i += 1
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
                try:
                    if self.dram_key[dram_i] is True:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_dram[dram_i]: sdk_color_dram_on}))
                        self.dram_key_prev[dram_i] = True
                    elif self.dram_key[dram_i] is False:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_dram[dram_i]: sdk_color_backlight}))
                        self.dram_key_prev[dram_i] = False
                except Exception as e:
                    print(e)
                dram_i += 1
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
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_dram[dram_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
                dram_i += 1
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
                try:
                    if self.vram_key[vram_i] is True:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_vram[vram_i]: sdk_color_vram_on}))
                        self.vram_key_prev[vram_i] = True
                    elif self.vram_key[vram_i] is False:
                        sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_vram[vram_i]: sdk_color_backlight}))
                        self.vram_key_prev[vram_i] = False
                except Exception as e:
                    print(e)
                vram_i += 1
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
                try:
                    sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({corsairled_id_num_vram[vram_i]: sdk_color_backlight}))
                except Exception as e:
                    print(e)
                vram_i += 1
        except Exception as e:
            print('-- [VramMonClass.stop] Error:', e)
            pass
        print('-- [VramMonClass.stop] terminating')
        self.terminate()


class WindowsUpdateMonitorClass(QThread):
    print('-- [WindowsUpdateMonitorClass]: plugged in')

    def __init__(self):
        QThread.__init__(self)
        self.win_update_dir_sz_prev = 0

    def run(self):
        print('-- [WindowsUpdateMonitorClass.run]: plugged in')

        global sdk, devices_kb, devices_kb_selected

        windows_update_dir_default = 'C:\\Windows\\SoftwareDistribution'

        while True:
            dl_prog = False
            if os.path.exists(windows_update_dir_default):
                win_update_dir_sz = sum(file.stat().st_size for file in Path(windows_update_dir_default).rglob('*'))

                if win_update_dir_sz > self.win_update_dir_sz_prev:
                    # print('-- [WindowsUpdateMonitorClass.run]: download update may be in progress')
                    self.win_update_dir_sz_prev = win_update_dir_sz

                    if len(devices_kb) > 0:
                        dl_prog = True
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({171: (100, 255, 0)}))
                            time.sleep(0.5)
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({171: (0, 0, 0)}))
                            time.sleep(0.5)
                        except Exception as e:
                            print('-- [WindowsUpdateMonitorClass.run] Error:', e)

                elif win_update_dir_sz < self.win_update_dir_sz_prev:
                    # print('-- [WindowsUpdateMonitorClass.run]: download update may be in progress')
                    self.win_update_dir_sz_prev = win_update_dir_sz

                    if len(devices_kb) > 0:
                        dl_prog = True
                        try:
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({171: (255, 0, 0)}))
                            time.sleep(0.5)
                            sdk.set_led_colors_buffer_by_device_index(devices_kb[devices_kb_selected], ({171: (0, 0, 0)}))
                            time.sleep(0.5)
                        except Exception as e:
                            print('-- [WindowsUpdateMonitorClass.run] Error:', e)

            if dl_prog is False:
                time.sleep(1)

    def stop(self):
        print('-- [WindowsUpdateMonitorClass.stop]: plugged in')
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
