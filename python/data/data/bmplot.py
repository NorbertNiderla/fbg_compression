import time
from matplotlib import pyplot as plt

def plot_process(queue):

    data = queue.get()
        
    fig = plt.figure()
    #mngr = plt.get_current_fig_manager()
    #mngr.full_screen_toggle()

    spectrum_sp = fig.add_subplot(2, 2, (1,2))
    firstgrating_sp = fig.add_subplot(2, 2, 3)
    secondtgrating_sp = fig.add_subplot(2, 2, 4)

    spectrum_ln, = spectrum_sp.plot([],'b-')
    spectrum_filt_ln, = spectrum_sp.plot([],'r--')
    firstextr_ln = spectrum_sp.axvline(color='k')
    secondextr_ln = spectrum_sp.axvline(color='k')

    firstgrating_ln, = firstgrating_sp.plot([],'b-')
    secondgrating_ln, = secondtgrating_sp.plot([],'b-')

    spectrum_sp.set_xlim(data["wavelens"].min(), data["wavelens"].max())
    spectrum_sp.set_ylim([data["spectrum"].min()-100, data["spectrum"].max()+500])
    spectrum_sp.set_xlabel("Wavelength (nm)")
    spectrum_sp.set_ylabel("Intensity")
    spectrum_sp.set_title("Spectrum")

    if len(data["peaks"]) > 0:
        firstgrating_sp.set_xlim(0,100)
        firstgrating_sp.set_ylim(data["peaks"][0]-0.2, data["peaks"][0]+0.2)
    if len(data["peaks"]) > 1:
        secondtgrating_sp.set_xlim(0,100)
        secondtgrating_sp.set_ylim(data["peaks"][1]-0.2, data["peaks"][1]+0.2)

    fig.canvas.draw()

    spectrum_bg = fig.canvas.copy_from_bbox(spectrum_sp.bbox)
    firstgrating_bg = fig.canvas.copy_from_bbox(firstgrating_sp.bbox)
    secondtgrating_bg = fig.canvas.copy_from_bbox(secondtgrating_sp.bbox)

    plt.show(block=False)

    t_start = time.time()-1/60
    t_last = t_start
    i = 0

    grt1 = []
    grt2 = []
    while True:
        while queue.qsize() > 0 or (len(grt1) < 100 and len(data["peaks"])> 0):
            data = queue.get()
            if len(data["peaks"]) > 0:
                grt1.append(data["peaks"][0])
            if len(data["peaks"]) > 1:
                grt2.append(data["peaks"][1])

        grt1 = grt1[-100:]
        grt2 = grt2[-100:]

        spectrum_ln.set_data(data["wavelens"], data["spectrum"])
        #spectrum_filt_ln.set_data(data["wavelens"], data["spectrum_filt"])
        if len(data["peaks"]) > 0:
            firstextr_ln.set_xdata(data["peaks"][0])          
            firstgrating_ln.set_data(range(100),grt1)
        if len(data["peaks"]) > 1:
            secondextr_ln.set_xdata(data["peaks"][1])
            secondgrating_ln.set_data(range(100),grt2)

        spectrum_sp.set_title('FPS: {fps:.1f} VCSEL_T: {vcselt:.3f}'.format(fps= ((i+1) / (time.time() - t_start)), vcselt=data["VCSEL_t"]))

        fig.canvas.restore_region(spectrum_bg)

        spectrum_sp.draw_artist(spectrum_ln)
        spectrum_sp.draw_artist(spectrum_filt_ln)

        if len(data["peaks"]) > 0:
            spectrum_sp.draw_artist(firstextr_ln)
            fig.canvas.restore_region(firstgrating_bg)
            firstgrating_sp.draw_artist(firstgrating_ln)
            fig.canvas.blit(firstgrating_sp.bbox)
        if len(data["peaks"]) > 0:
            spectrum_sp.draw_artist(secondextr_ln)    
            fig.canvas.restore_region(secondtgrating_bg)
            secondtgrating_sp.draw_artist(secondgrating_ln)
            fig.canvas.blit(secondtgrating_sp.bbox)
        
        fig.canvas.blit(spectrum_sp.bbox)
        #if len(data["peaks"]) > 0:
            #firstgrating_sp.set_ylim(min(grt1)-0.02, max(grt1)+0.02)
            #secondtgrating_sp.set_ylim(min(grt2)-0.02, max(grt2)+0.02)
        fig.canvas.flush_events()

        i=i+1
        continue
        cur_time= time.time()
        if cur_time - t_last < 1/60:
            time.sleep(1/60)
        t_last = cur_time