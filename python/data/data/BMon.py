import concurrent.futures, logging, queue, multiprocessing
import threading
import bmserver, bmdsp, bmplot, bmlogger, bmuart


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging_e = threading.Event()

    udp_queue_priority = queue.PriorityQueue()
    udp_queue = multiprocessing.Queue()
    plot_queue = multiprocessing.Queue()

    plot_proc = multiprocessing.Process(target=bmplot.plot_process, args=(plot_queue,))
    dsp_proc = multiprocessing.Process(target=bmdsp.dsp_process, args=(udp_queue, plot_queue,))
    
    servermgr = bmserver.ServerManager(udp_queue_priority)
    try:
        plot_proc.start()
        dsp_proc.start()
        servermgr.start() 
    except (KeyboardInterrupt, SystemExit):
        servermgr.stop()
        exit()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(bmlogger.logging_thread, udp_queue, udp_queue_priority, plot_queue)
        executor.submit(bmserver.prioritizer_thread, udp_queue_priority, udp_queue)
        executor.submit(bmuart.uart_thread)