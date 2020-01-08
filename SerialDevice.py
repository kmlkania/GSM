import serial
import serial.tools.list_ports as port_list


def getSerialDevices():
    return list(port_list.comports())


class SerialGSMConnection:
    def __init__(self, port, baudrate=115200):
        self.conn = None
        self.port = port
        self.baudrate = baudrate

    def establish_connection(self):
        try:
            self.conn = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=8, timeout=0.2,
                                      stopbits=serial.STOPBITS_ONE)
            return 1, None
        except serial.SerialException as e:
            return 0, e.__str__()

    def close_connection(self):
        self.conn.close()

    def send_text_data(self, data):
        if self.conn.isOpen():
            self.conn.write("{}{}".format(data, "\n").encode())

    def receive_data(self):
        if self.conn.isOpen():
            return [line.decode().replace('\r\n', '') for line in self.conn.readlines()]
