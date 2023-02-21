import logging, numpy, math
from scipy import interpolate

def calculate_temperature(adcdata):
    beta=3864.10
    adc_vref = 2.5
    voltmeas = adcdata*adc_vref/65535.0
    r_up = 10e3
    ntc_res=(3.3-voltmeas)*r_up/voltmeas
    ntc_temp=beta/(math.log(ntc_res/10000.0)+beta/298.15)- 273.15
    return ntc_temp

def calculate_wavelengths(temp,length):
    a=-0.0293
    b=-0.03
    lmbd=1550.5
    c=0.200
    upper_v = 0
    lower_v = 18
    volts=numpy.linspace(lower_v,upper_v,length)
    wavlens=  a*volts*volts + b*volts + c*(temp-25) + lmbd
    return wavlens

def filter_waveform(data):
    # Filter the data
    
    return data

def find_extrema(yaxis, xaxis, span,threshold):
    maxind = 0
    extremas = []
    for i in range(len(yaxis)):
        if (yaxis[i] > yaxis[maxind]):
            maxind = i
        if ((i - maxind) > 2 * span and yaxis[maxind] > threshold):
            mass = 0
            central = 0
            for j in range(maxind - span, maxind + span):
                if yaxis[j] > yaxis[maxind]/2:
                    central += yaxis[j] * xaxis[j]
                    mass += yaxis[j]
            extremas.append(central / mass)
            maxind = i
    return extremas

def equdistant_vector(nonequdistant_vector):
    step = numpy.diff(nonequdistant_vector).min()*10
    nums=(nonequdistant_vector.max()-nonequdistant_vector.min())/step
    eqdst_vector = numpy.linspace(nonequdistant_vector.min(), nonequdistant_vector.max(), math.floor(nums))
    return (eqdst_vector,step)

def interpolate_data(nonuniform_xaxis, yaxis, desired_xaxis):
    fcubic = interpolate.interp1d(nonuniform_xaxis, yaxis, kind='cubic')
    ycubic = fcubic(desired_xaxis)
    return ycubic

def dsp_process(udp_queue, plot_queue):
    while True:
        if udp_queue.qsize() > 0:
            unpacked = udp_queue.get()
            qitem={}
            if unpacked["type"] == 32:
                qitem["peaks"] = [[],[]]
                qitem["peaks"].insert(unpacked["grtit"],unpacked["data"])
                #qitem["wavelens"]
            if unpacked["type"] == 64:
                qitem["VCSEL_t"] = calculate_temperature(unpacked["temperature"])
                wavelens_nu = calculate_wavelengths(qitem["VCSEL_t"],4095)#wavelens non_uniform
                qitem["wavelens"], wavelength_step = equdistant_vector(wavelens_nu)
                spectrum_raw = numpy.array(unpacked["data"][0:4095]) #1100 todo: make this dynamic
                qitem["spectrum"] = interpolate_data(wavelens_nu, spectrum_raw, qitem["wavelens"])
                qitem["spectrum_filt"] = filter_waveform(qitem["spectrum"])
                grating_width= math.floor(1/wavelength_step)
                qitem["peaks"] = find_extrema(qitem["spectrum_filt"], qitem["wavelens"], span=grating_width, threshold=3000)
                logging.debug("peaks: {}".format(qitem["peaks"]))
                logging.debug("grating_width: {} wavelength_step: {}".format(grating_width, wavelength_step))
            plot_queue.put(qitem)
        else:
            #logging.warning("dsp has nothing to do")
            #time.sleep(1/60)# dodać automatyczne korekcje stepu
            pass