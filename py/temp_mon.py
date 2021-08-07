# Requires only OpenHardwareMonitorLib.dll and if necessary right click the dll, properties, general, unblock.

import os
import time
import clr
from System import String
from System.Collections import *
import psutil

print('-- pluggeed in: script')

openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
cputhermometer_hwtypes = ['Mainboard','SuperIO','CPU','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData']
cputhermometer_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level']

dat_file = ''
keep_alive = True


def checkIfProcessRunning():
    global keep_alive

    proc_item = []

    for proc in psutil.process_iter():
        try:
            proc_item.append(proc.name().lower())
            print('-- [checkIfProcessRunning]:', proc.name().lower())
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if 'icuedisplay.exe'.lower() not in proc_item:
        print('-- process not found: icuedisplay.exe')
        print('-- [checkIfProcessRunning]: false')
        keep_alive = False


def config():
    global dat_file
    app_data_path = os.path.join(os.path.expanduser('~'), 'AppData\\Local\\iCUEDisplay\\icue_display_py_config.dat')
    print('-- [config]: plugged in')
    if os.path.exists(app_data_path):   # here
        print('-- [config]: exists')
        with open(app_data_path, 'r') as fo:
            for line in fo:
                line = line.strip()
                print('-- [config]: raw config data:', line)
                if line.startswith('PATH: '):
                    print('-- [config]: found PATH:', line)
                    line = line.replace('PATH: ', '')
                    print('-- [config]: PATH exists:', line)
                    dat_file = line
    else:
        print('-- [config]: cannot be found')


def initialize_openhardwaremonitor():
    clr.AddReference(".\\bin\\OpenHardwareMonitorLib")

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)


def parse_sensor(sensor):
    global dat_file
    if sensor.Value is not None:
        if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
            sensortypes = openhardwaremonitor_sensortypes
            hardwaretypes = openhardwaremonitor_hwtypes
        else:
            return

        if sensor.SensorType == sensortypes.index('Temperature'):
            # print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))
            line_str = str(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))
            print(line_str)
            with open(dat_file, 'a', encoding="utf-8") as fo:
                fo.writelines(line_str+'\n')
            fo.close()


if __name__ == "__main__":
    config()
    time.sleep(1)
    HardwareHandle = initialize_openhardwaremonitor()
    while keep_alive is True:
        try:
            checkIfProcessRunning()
            try:
                open(dat_file, 'w').close()
                time.sleep(1)
                fetch_stats(HardwareHandle)
            except:
                time.sleep(3)
                pass
        except Exception as e:
            print(e)
        time.sleep(3)
