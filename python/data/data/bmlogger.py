import logging, time, multiprocessing, threading
def logging_thread(udp_queue, udp_queue_priority, plot_queue):
    while True :
        time.sleep(10)
        logging.info("udp_queue size: %d", udp_queue.qsize())
        logging.info("udp_queue_priority size: %d", udp_queue_priority.qsize())
        logging.info("plot_queue size: %d", plot_queue.qsize())
        logging.info("active threads: {}".format(threading.active_count()))
        #logging.info("threads: {}".format(threading.enumerate()))
        #logging.info("processes: {}".format(multiprocessing.enumerate()))
        #logging.info("processes: {}".format(multiprocessing.current_process()))
        logging.info("processes count: {}".format(multiprocessing.active_children()))