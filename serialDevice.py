import serial.tools.list_ports as port_list

# print([dev.__str__() for dev in list(port_list.comports())])

def getSerialDevices():
    return list(port_list.comports())
