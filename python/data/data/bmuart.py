import logging, serial, time


#def handle_data(data):
    #print(data)

def uart_thread():
    port = 'COM7'
    baud = 115200
    mode=b"full-spectrum"
    UDP_IP = "192.168.88.254"
    UDP_PORT = 57070

    recv_str=""
    #conf_str=b"Mode: "+mode+b" Address: "+UDP_IP.encode("utf-8")+b" Port: "+str(UDP_PORT).encode("utf-8")+ b" Voltage: 0 to 4095 Rampfall: 409 to 420 GratesN: 2 GSpan: 15"
    conf_str=b"Mode: "+mode+b" Address: "+UDP_IP.encode("utf-8")+b" Port: "+str(UDP_PORT).encode("utf-8")+ b" Voltage: 0 to 4095 Rampfall: 4096 to 6180 GratesN: 2 GSpan: 150"
    #uint8_t uartrx[128] = ":Mode full-spectrum Address: 10.10.10.246 Port: 57070 Voltage: 0 to 4095 Rampfall: 1100 to 1120 GratesN: 2 GSpan: 30\n";
    #uint8_t  = "Mode: central-wavelength Address: 10.10.10.246 Port: 57070 Voltage: 0 to 4096 Rampfall: 4096 to 4200 GratesN: 2 GSpan: 15\n";

    serial_port = serial.Serial(port, baud, timeout=0)
    while len(conf_str) < 128:
        conf_str = conf_str + b"\n"

    while True:
        while serial_port.in_waiting > 0:
            recv_str = serial_port.readline()
            try:
                print(recv_str.decode("Ascii"))
                if recv_str == conf_str:
                    logging.info("configured properly")
                    continue
                else:
                    serial_port.write(conf_str)
            except:
                pass
    #while not connected:
        #serin = ser.read()
    #    connected = True

    #    while True:
    #       print("test")
    #       reading = ser.readline().decode()
     #     handle_data(reading)

