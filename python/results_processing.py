from math import nan
import numpy as np
from matplotlib import pyplot as plt

from Common.data import FbgData, DataFromJulek

data = {
    'multiple peaks': [{'data set': 'raw',
                        'entropy': 5.977875151550401,
                        'mse': nan,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 8.624420324109426,
                                    'sprintz': 10.016329305196983}},
                       {'data set': 'noiseless',
                        'entropy': 4.536279157564378,
                        'mse': 13236.597721496995,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 6.544641406979141,
                                    'sprintz': 5.197311814923902}},
                       {'data set': 'peaks stream',
                        'entropy': 6.648519993772593,
                        'mse': nan,
                        'original bitwidth': 12,
                        'results': {'arithmetic': 9.59185360094451,
                                    'sprintz': 4.681345926800472}},
                       {'data set': 'raw parallel',
                        'entropy': 5.165420541212975,
                        'mse': nan,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 7.453433208489389,
                                    'sprintz': 9.352559300873908}},
                       {'data set': 'noiseless parallel',
                        'entropy': 4.523956317599315,
                        'mse': 182584.2424469413,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 6.526841448189762,
                                    'sprintz': 7.307116104868913}},
                       {'data set': 'raw parallel noiseless',
                        'entropy': 4.425737586143162,
                        'mse': 182584.2424469413,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 6.3865168539325845,
                                    'sprintz': 5.069912609238452}},
                       {'data set': 'noise floor',
                        'entropy': 0.5715887236005829,
                        'mse': 175720.19205544042,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 0.8248698027142446,
                                    'sprintz': 0.6899508704733969}}],
    'single peak': [{'data set': 'raw',
                     'entropy': 5.48630268996592,
                     'mse': nan,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 7.916655654128618,
                                 'sprintz': 10.174298214224255}},
                    {'data set': 'noiseless',
                     'entropy': 4.107150057001681,
                     'mse': 454448.841720896,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 5.9269589611475935,
                                 'sprintz': 5.621125462039771}},
                    {'data set': 'peaks stream',
                     'entropy': 4.090807295619112,
                     'mse': nan,
                     'original bitwidth': 12,
                     'results': {'arithmetic': 5.901832407328433,
                                 'sprintz': 3.6604870740888718}},
                    {'data set': 'raw parallel',
                     'entropy': 5.452328074898036,
                     'mse': nan,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 7.8667528142628,
                                 'sprintz': 9.60594772527099}},
                    {'data set': 'noiseless parallel',
                     'entropy': 4.272593181222412,
                     'mse': 91556.35810940909,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.1642052744871565,
                                 'sprintz': 7.155972053641458}},
                    {'data set': 'raw parallel noiseless',
                     'entropy': 4.357639678294283,
                     'mse': 91556.35810940909,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.287573454123806,
                                 'sprintz': 5.111697402989776}},
                    {'data set': 'noise floor',
                     'entropy': 0.16318698472011645,
                     'mse': 171261.52315929063,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 0.2370218378094061,
                                 'sprintz': 0.8184013709067056}}]}


def get_raw_dataset(results: list):
    for val in results:
        if val['data set'] == 'raw':
            return val
    return None


def get_peaks_dataset(results: list):
    for val in results:
        if val['data set'] == 'peaks stream':
            return val
    return None


def fig_raw_data_results(figure_name: str, res: dict):
    labels = list(res.keys())
    index = np.arange(len(labels))
    bar_width = 0.2
    fig, axs = plt.subplots(1, 1)
    axs.bar(index, [get_raw_dataset(entry)['entropy'] for entry in res.values()], bar_width, label='Entropy')
    algorithms = res[list(res.keys())[0]][0]['results'].keys()
    for idx, alg in enumerate(algorithms):
        values = []
        for ds in res.values():
            values.append(get_raw_dataset(ds)['results'][alg])
        axs.bar(index + (idx + 1) * bar_width, values, bar_width, label=alg)
    axs.set_xlabel('Zbiór danych')
    axs.set_ylabel('Bity na próbkę')
    axs.set_title('Wyniki kompresji surowych danych')
    axs.set_xticks(index + bar_width / 2)
    axs.set_xticklabels(labels, rotation=45)
    axs.legend()
    plt.savefig(figure_name, bbox_inches='tight')


def fig_peaks_data_results(figure_name: str, res: dict):
    labels = list(res.keys())
    index = np.arange(len(labels))
    bar_width = 0.2
    fig, axs = plt.subplots(1, 1)
    axs.bar(index, [get_peaks_dataset(entry)['entropy'] for entry in res.values()], bar_width, label='Entropy')
    algorithms = res[list(res.keys())[0]][0]['results'].keys()
    for idx, alg in enumerate(algorithms):
        values = []
        for ds in res.values():
            values.append(get_peaks_dataset(ds)['results'][alg])
        axs.bar(index + (idx + 1) * bar_width, values, bar_width, label=alg)
    axs.set_xlabel('Zbiór danych')
    axs.set_ylabel('Bity na próbkę')
    axs.set_title('Wyniki kompresji danych o wierzchołkach')
    axs.set_xticks(index + bar_width / 2)
    axs.set_xticklabels(labels, rotation=45)
    axs.legend()
    plt.savefig(figure_name, bbox_inches='tight')


def fig_dataset_results(figure_name: str, res: list):
    labels = [entry['data set'] for entry in res]
    index = np.arange(len(labels))
    bar_width = 0.2
    fig, axs = plt.subplots(1, 1)
    axs.bar(index, [entry['entropy'] for entry in res], bar_width, label='Entropy')
    algorithms = res[0]['results'].keys()
    for idx, alg in enumerate(algorithms):
        values = [val['results'][alg] for val in res]
        axs.bar(index + (idx + 1) * bar_width, values, bar_width, label=alg)
    axs.set_xlabel('Transformacja danych')
    axs.set_ylabel('Bity na próbkę')
    axs.set_title('Wyniki kompresji danych')
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


def fig_example_oscyllogram(figure_name: str, figure_title: str, data: list):
    fig, ax = plt.subplots(1, 1)
    ax.plot(data)
    ax.set_xlabel('Numer próbki')
    ax.set_ylabel('Znormalizowana moc optyczna')
    ax.set_title(figure_title)
    plt.savefig(figure_name, bbox_inches='tight')


fig_raw_data_results("Figures/results_raw.png", data)
fig_mean_square_error("Figures/mse.png", data)

target_datasets = ['noiseless', 'raw parallel', 'noiseless parallel',
                   'raw parallel noiseless', 'noise floor']
fig_dataset_results("Figures/results_wide_lossy.png", [entry for entry in data['multiple peaks'] if entry['data set'] in target_datasets])
fig_dataset_results("Figures/results_thin_lossy.png", [entry for entry in data['single peak'] if entry['data set'] in target_datasets])

fig_peaks_data_results("Figures/results_peaks.png", data)

wide_data = FbgData("C:/Users/norbert/PycharmProjects/data", 10000)
data = wide_data.get_sample_with_index(wide_data.get_number_of_samples() // 2)
fig_example_oscyllogram("Figures/wide_data_example.png", "Przykład oscylogramu z szerokiego zbioru danych", data)

thin_data = DataFromJulek(1000)
data = thin_data.get_sample_with_index(thin_data.get_number_of_samples() // 2)
fig_example_oscyllogram("Figures/thin_data_example.png", "Przykład oscylogramu z wąskiego zbioru danych", data)
