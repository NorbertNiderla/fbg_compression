import socketserver, struct, logging, threading, math, time

def prioritizer_thread(udp_queue_priority, udp_queue):
    packet_no=0
    while True:
        if udp_queue_priority.qsize() > 0:
            data = udp_queue_priority.get()
            if (packet_no +1)%256 < data[0]:
                logging.warning("packet skipped: {} != {}".format(packet_no, data[0]))
            if (packet_no +1)%256 > data[0]:
                logging.warning("packet wrong order: {} != {}".format(packet_no, data[0]))
            packet_no = data[0]#priority
            udp_queue.put(data[1])#data without priority
        else:
            time.sleep(0.1)

class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.srvqueue = server.srvqueue
        socketserver.StreamRequestHandler.__init__(self, request, client_address, server)
    def handle(self):
        self.data = self.request[0]
        current_thread = threading.current_thread()
        logging.debug("{}: client: {}, length: {}".format(current_thread.name, self.client_address, len(self.data)))

        unpacked={}
        unpacked["type"] = self.data[0] & 0xE0
        if unpacked["type"] == 64:#TODO: fix this
            unpacked["no"] = self.data[1]
            unpckd = struct.unpack('<'+'H'*math.floor(len(self.data)/2-1), self.data[2:])
            unpacked["data"] = unpckd[1:]
            unpacked["temperature"] = unpckd[0]
        elif unpacked["type"] == 32:           
            unpacked["grtit"] = self.data[0] & 0x1F
            unpacked["no"] = self.data[2]
            unpacked["data"] = struct.unpack('<'+'f'*364, self.data[2:])#NLEN

        #with open('data'+str('\\')+str(time.time())+".ftbinlol", "w") as f:
            #f.write(str(unpacked))
            #f.write('\n'.join(str(v) for v in unpacked["data"]))

        self.srvqueue.put((unpacked["no"],unpacked))
        self.finish()

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True,srvqueue=None):
        self.srvqueue = srvqueue
        socketserver.UDPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=bind_and_activate)

class ServerManager():
    def __init__(self, srvqueue):
        self.HOST, self.PORT = "0.0.0.0", 57070#randomize port
        self.server = ThreadedUDPServer((self.HOST, self.PORT), ThreadedUDPRequestHandler, srvqueue=srvqueue)
        self.server.max_packet_size = 8192*4
    def start(self):             
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()     
        logging.info("udp_srv started at {} port {}".format(self.HOST, self.PORT))  
    def stop(self):
        self.server.shutdown()
        self.server.server_close()