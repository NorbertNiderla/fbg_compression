from math import nan
import numpy as np
from matplotlib import pyplot as plt

data = {
    'multiple peaks': [{'data set': 'raw',
                     'entropy': 5.977875151550401,
                     'mse': nan,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 8.624420324109426,
                                 'sprintz': 10.016329305196983,
                                 'sprintz delta': 10.082279028237357}},
                    {'data set': 'noiseless',
                     'entropy': 4.536279157564378,
                     'mse': 13236.597721496995,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.544641406979141,
                                 'sprintz': 5.197311814923902,
                                 'sprintz delta': 5.244217584007045}},
                    {'data set': 'peaks stream',
                     'entropy': 6.648519993772593,
                     'mse': nan,
                     'original bitwidth': 12,
                     'results': {'arithmetic': 9.59185360094451,
                                 'sprintz': 4.681345926800472,
                                 'sprintz delta': 4.696458087367178}},
                    {'data set': 'raw parallel',
                     'entropy': 5.165420541212975,
                     'mse': nan,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 7.453433208489389,
                                 'sprintz': 9.352559300873908,
                                 'sprintz delta': 9.440449438202247}},
                    {'data set': 'noiseless parallel',
                     'entropy': 4.523956317599315,
                     'mse': 182584.2424469413,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.526841448189762,
                                 'sprintz': 7.307116104868913,
                                 'sprintz delta': 7.426966292134831}},
                    {'data set': 'raw parallel noiseless',
                     'entropy': 4.425737586143162,
                     'mse': 182584.2424469413,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.3865168539325845,
                                 'sprintz': 5.069912609238452,
                                 'sprintz delta': 5.0059925093632955}},
                    {'data set': 'noise floor',
                     'entropy': 0.5715887236005829,
                     'mse': 175720.19205544042,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 0.8248698027142446,
                                 'sprintz': 0.6899508704733969,
                                 'sprintz delta': 0.6904892347348984}}],
 'single peak': [{'data set': 'raw',
                  'entropy': 5.48630268996592,
                  'mse': nan,
                  'original bitwidth': 14,
                  'results': {'arithmetic': 7.916655654128618,
                              'sprintz': 10.174298214224255,
                              'sprintz delta': 10.213349773272526}},
                 {'data set': 'noiseless',
                  'entropy': 4.107150057001681,
                  'mse': 454448.841720896,
                  'original bitwidth': 14,
                  'results': {'arithmetic': 5.9269589611475935,
                              'sprintz': 5.621125462039771,
                              'sprintz delta': 5.580728325666768}},
                 {'data set': 'peaks stream',
                  'entropy': 4.090807295619112,
                  'mse': nan,
                  'original bitwidth': 12,
                  'results': {'arithmetic': 5.901832407328433,
                              'sprintz': 3.6604870740888718,
                              'sprintz delta': 3.6641050772402313}},
                 {'data set': 'raw parallel',
                  'entropy': 5.452328074898036,
                  'mse': nan,
                  'original bitwidth': 14,
                  'results': {'arithmetic': 7.8667528142628,
                              'sprintz': 9.60594772527099,
                              'sprintz delta': 9.749494483736006}},
                 {'data set': 'noiseless parallel',
                  'entropy': 4.272593181222412,
                  'mse': 91556.35810940909,
                  'original bitwidth': 14,
                  'results': {'arithmetic': 6.1642052744871565,
                              'sprintz': 7.155972053641458,
                              'sprintz delta': 7.291213984932836}},
                 {'data set': 'raw parallel noiseless',
                  'entropy': 4.357639678294283,
                  'mse': 91556.35810940909,
                  'original bitwidth': 14,
                  'results': {'arithmetic': 6.287573454123806,
                              'sprintz': 5.111697402989776,
                              'sprintz delta': 5.077033671700358}},
                 {'data set': 'noise floor',
                  'entropy': 0.16318698472011645,
                  'mse': 171261.52315929063,
                  'original bitwidth': 14,
                  'results': {'arithmetic': 0.2370218378094061,
                              'sprintz': 0.8184013709067056,
                              'sprintz delta': 0.8270496263212763}}]}


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


def fig_mean_square_error(figure_name: str, res: dict):
    labels = [entry['data set'] for entry in res[list(res.keys())[0]]]
    index = np.arange(len(labels))
    bar_width = 0.2
    datasets = list(res.keys())
    fig, axs = plt.subplots(1, 1)
    for idx, d in enumerate(datasets):
        values = [val['mse'] for val in res[d]]
        axs.bar(index + idx * bar_width, values, bar_width, label=d)
    axs.set_xlabel('Data Set')
    axs.set_ylabel('Mean Square Error')
    axs.set_title('Transformations MSE in comparison to raw data')
    axs.set_xticks(index + bar_width / 2)
    axs.set_xticklabels(labels, rotation=45)
    axs.legend()
    plt.savefig(figure_name, bbox_inches='tight')


fig_algorithms_w_entropy_results("Figures/results_multiple_peaks.png", data['multiple peaks'])
fig_algorithms_w_entropy_results("Figures/results_single_peak.png", data['single peak'])
fig_mean_square_error("Figures/mse.png", data)
