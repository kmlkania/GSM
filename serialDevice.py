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
        self.conn = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=8, timeout=2,
                                  stopbits=serial.STOPBITS_ONE)

    def close_connection(self):
        self.conn.close()

    def send_text_data(self, data):
        if self.conn.isOpen():
            self.conn.write("{}{}".format(data, "\n").encode())

    def receive_data(self):
        if self.conn.isOpen():
            return [line.decode().replace('\r\n', '') for line in self.conn.readlines()]


if __name__ == "__main__":
    # devices = list(port_list.comports())
    # print([dev.__str__() for dev in devices])
    # for dev in devices:
    #     print("baud rate: {}".format(dev.device))
    ser = SerialGSMConnection('COM3')
    ser.establish_connection()
    import time
    time.sleep(3)
    ser.send_text_data('AT')
    time.sleep(3)
    print(ser.receive_data())
    # time.sleep(3)
    ser.send_text_data('AT+CPIN')
    time.sleep(3)
    print(ser.receive_data())
    time.sleep(3)
    print(ser.receive_data())
