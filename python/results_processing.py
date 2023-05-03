from math import nan
import numpy as np
from matplotlib import pyplot as plt

data = {
    'multiple peaks': [{'data set': 'raw',
                            'entropy': 5.970030927869522,
                            'mse': nan,
                            'original bitwidth': 14,
                            'results': {'arithmetic': 8.613098705501617,
                                        'sprintz': 10.021545307443366,
                                        'sprintz delta': 10.078058252427185}},
                           {'data set': 'noiseless',
                            'entropy': 4.528444898262379,
                            'mse': 13168.21703074434,
                            'original bitwidth': 14,
                            'results': {'arithmetic': 6.533317152103559,
                                        'sprintz': 5.193559870550162,
                                        'sprintz delta': 5.246893203883494}},
                           {'data set': 'peaks stream',
                            'entropy': 5.765295739852721,
                            'mse': nan,
                            'original bitwidth': 12,
                            'results': {'arithmetic': 8.319148936170214,
                                        'sprintz': 6.949709864603482,
                                        'sprintz delta': 6.949709864603482}},
                           {'data set': 'raw parallel',
                            'entropy': 2.8934591868379536,
                            'mse': nan,
                            'original bitwidth': 14,
                            'results': {'arithmetic': 4.25,
                                        'sprintz': 15.15,
                                        'sprintz delta': 14.77}},
                           {'data set': 'noiseless parallel',
                            'entropy': 2.718473401330013,
                            'mse': 1547473.66,
                            'original bitwidth': 14,
                            'results': {'arithmetic': 4.0,
                                        'sprintz': 15.15,
                                        'sprintz delta': 15.15}},
                           {'data set': 'raw parallel noiseless',
                            'entropy': 0.0,
                            'mse': 1547473.66,
                            'original bitwidth': 14,
                            'results': {'arithmetic': 0.1,
                                        'sprintz': 2.8,
                                        'sprintz delta': 2.8}},
                           {'data set': 'noise floor',
                            'entropy': 0.5548245980268753,
                            'mse': 175559.34618122975,
                            'original bitwidth': 14,
                            'results': {'arithmetic': 0.8006796116504855,
                                        'sprintz': 0.6744822006472492,
                                        'sprintz delta': 0.6709546925566343}}],
        'single peak': [{'data set': 'raw',
                         'entropy': 5.485106867237306,
                         'mse': nan,
                         'original bitwidth': 14,
                         'results': {'arithmetic': 7.9149763431048985,
                                     'sprintz': 10.162262188548683,
                                     'sprintz delta': 10.207974977853574}},
                        {'data set': 'noiseless',
                         'entropy': 4.107341366588825,
                         'mse': 449051.03247729753,
                         'original bitwidth': 14,
                         'results': {'arithmetic': 5.9272730971100485,
                                     'sprintz': 5.620611073888856,
                                     'sprintz delta': 5.581502666063434}},
                        {'data set': 'peaks stream',
                         'entropy': 3.6496641042312836,
                         'mse': nan,
                         'original bitwidth': 12,
                         'results': {'arithmetic': 5.266243146419446,
                                     'sprintz': 4.939474727111638,
                                     'sprintz delta': 4.924990719869634}},
                        {'data set': 'raw parallel',
                         'entropy': 3.851970823205285,
                         'mse': nan,
                         'original bitwidth': 14,
                         'results': {'arithmetic': 5.597636815920398,
                                     'sprintz': 12.577487562189054,
                                     'sprintz delta': 12.498930348258707}},
                        {'data set': 'noiseless parallel',
                         'entropy': 3.298925011597541,
                         'mse': 774020.8135820895,
                         'original bitwidth': 14,
                         'results': {'arithmetic': 4.800995024875622,
                                     'sprintz': 11.224253731343286,
                                     'sprintz delta': 11.224253731343286}},
                        {'data set': 'raw parallel noiseless',
                         'entropy': 1.8971033077103474,
                         'mse': 774020.8135820895,
                         'original bitwidth': 14,
                         'results': {'arithmetic': 2.789303482587065,
                                     'sprintz': 3.958706467661691,
                                     'sprintz delta': 3.958706467661691}},
                        {'data set': 'noise floor',
                         'entropy': 0.16303920318586979,
                         'mse': 170985.8813799198,
                         'original bitwidth': 14,
                         'results': {'arithmetic': 0.2367802590836178,
                                     'sprintz': 0.8124139258740506,
                                     'sprintz delta': 0.8210706526816732}}]}


def fig_algorithms_w_entropy_results(figure_name: str, res: list):
    labels = [entry['data set'] for entry in res]
    entropy_values = [entry['entropy'] for entry in res]
    index = np.arange(len(labels))
    bar_width = 0.2
    algs = res[0]['results'].keys()
    fig, axs = plt.subplots(1, 1)
    axs.bar(index, entropy_values, bar_width, label='Entropy')
    for idx, alg in enumerate(algs):
        values = [val['results'][alg] for val in res]
        axs.bar(index + (idx + 1) * bar_width, values, bar_width, label=alg)
    axs.set_xlabel('Data Set')
    axs.set_ylabel('Results')
    axs.set_title('Results for Multiple Peaks')
    axs.set_xticks(index + bar_width / 2)
    axs.set_xticklabels(labels, rotation=45)
    axs.legend()
    plt.savefig(figure_name, bbox_inches='tight')


fig_algorithms_w_entropy_results("results_multiple_peaks.png", data['multiple peaks'])
fig_algorithms_w_entropy_results("results_single_peak.png", data['single peak'])
