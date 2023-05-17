from math import nan
from statistics import median
import numpy as np
from matplotlib import pyplot as plt
from Common.data import FbgData, DataFromJulek
from denoise_data import denoise_data

data = {
    'multiple peaks': [{'data set': 'raw',
                        'entropy': 5.977535351924411,
                        'mse': nan,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 8.623932586344967,
                                    'sprintz': 10.016995766362303}},
                       {'data set': 'noiseless',
                        'entropy': 4.535898454428314,
                        'mse': 13233.245042131886,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 6.544090256036792,
                                    'sprintz': 5.196011026719808}},
                       {'data set': 'peaks stream',
                        'entropy': 6.678212082205621,
                        'mse': nan,
                        'original bitwidth': 12,
                        'results': {'arithmetic': 9.634654546527758,
                                    'sprintz': 4.44420505858395}},
                       {'data set': 'raw parallel',
                        'entropy': 5.367215667258702,
                        'mse': nan,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 7.743579290664492,
                                    'sprintz': 9.088055442315532}},
                       {'data set': 'noiseless parallel',
                        'entropy': 4.6401340470620385,
                        'mse': 120704.99331430902,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 6.695067264573991,
                                    'sprintz': 7.193232776192417}},
                       {'data set': 'raw parallel noiseless',
                        'entropy': 4.611895650364981,
                        'mse': 120704.99331430902,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 6.653974724826743,
                                    'sprintz': 4.8927028128821854}},
                       {'data set': 'noise floor',
                        'entropy': 0.5699333445339994,
                        'mse': 175700.10332272615,
                        'original bitwidth': 14,
                        'results': {'arithmetic': 0.8224784525124113,
                                    'sprintz': 0.6886814507564213}}],
    'single peak': [{'data set': 'raw',
                     'entropy': 5.47560112104185,
                     'mse': nan,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 7.901240111650406,
                                 'sprintz': 10.177583264924674}},
                    {'data set': 'noiseless',
                     'entropy': 4.691933745341393,
                     'mse': 79680.29503935747,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.770647817742003,
                                 'sprintz': 7.432328792946276}},
                    {'data set': 'peaks stream',
                     'entropy': 4.1056533398356265,
                     'mse': nan,
                     'original bitwidth': 12,
                     'results': {'arithmetic': 5.9232328801200556,
                                 'sprintz': 3.5419166399806103}},
                    {'data set': 'raw parallel',
                     'entropy': 5.5671664963802865,
                     'mse': nan,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 8.031904920846761,
                                 'sprintz': 9.473555755438653}},
                    {'data set': 'noiseless parallel',
                     'entropy': 4.710701869022074,
                     'mse': 61419.63561243244,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.796501584486886,
                                 'sprintz': 7.621433818236833}},
                    {'data set': 'raw parallel noiseless',
                     'entropy': 4.84141802012826,
                     'mse': 61419.63561243244,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 6.984914817299002,
                                 'sprintz': 6.029760181865077}},
                    {'data set': 'noise floor',
                     'entropy': 0.1545529801093907,
                     'mse': 171142.8291533023,
                     'original bitwidth': 14,
                     'results': {'arithmetic': 0.22459358490147174,
                                 'sprintz': 0.821371374336872}}]}


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


def save_figure(figure_name: str):
    plt.savefig(figure_name, bbox_inches='tight', format=figure_name.split(sep=".")[1])


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
    save_figure(figure_name)


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
    save_figure(figure_name)


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
    save_figure(figure_name)


def fig_mean_square_error(figure_name: str, res: dict):
    real_data = res.copy()
    for key, value in real_data.items():
        real_data[key] = [x for x in value if x['data set'] != "raw" and x['data set'] != "peaks stream" and x['data set'] != "raw parallel"]
    labels = [entry['data set'] for entry in real_data[list(real_data.keys())[0]]]
    index = np.arange(len(labels))
    bar_width = 0.2
    datasets = list(real_data.keys())

    fig, axs = plt.subplots(1, 1)
    for idx, d in enumerate(datasets):
        values = []
        if d == "multiple peaks":
            values = [val['mse']/6000 for val in real_data[d]]
        elif d == "single peak":
            values = [val["mse"]/600 for val in real_data[d]]
        axs.bar(index + idx * bar_width, values, bar_width, label=d)
    axs.set_xlabel('Rodzaj transformacji')
    axs.set_ylabel('Znormalizowany błąd')
    plt.yscale('log')
    axs.set_title('Błąd transformacji danych')
    axs.set_xticks(index + bar_width / 2)
    axs.set_xticklabels(labels, rotation=45)
    axs.legend()
    save_figure(figure_name)


def fig_example_oscyllogram(figure_name: str, figure_title: str, data: list):
    fig, ax = plt.subplots(1, 1)
    ax.plot(data)
    ax.set_xlabel('Numer próbki')
    ax.set_ylabel('Znormalizowana moc optyczna')
    ax.set_title(figure_title)
    save_figure(figure_name)


def fig_denoising_process_example(figure_name: str, figure_title: str, data: list, denoised_data: list):
    fig, ax = plt.subplots(1, 1)
    ax.plot(data, label="Surowe dane")
    ax.plot(denoised_data, label="Dane odszumione")
    ax.legend()
    ax.set_xlabel('Numer próbki')
    ax.set_ylabel('Znormalizowana moc optyczna')
    ax.set_title(figure_title)
    save_figure(figure_name)


def fig_noise_floor_process_example(figure_name: str, figure_title: str, data: list, denoised_data: list):
    fig, ax = plt.subplots(1, 1)
    ax.plot(data, label="Surowe dane")
    ax.plot(denoised_data, label="Dane po trasformacji")
    ax.legend()
    ax.set_xlabel('Numer próbki')
    ax.set_ylabel('Znormalizowana moc optyczna')
    ax.set_title(figure_title)
    save_figure(figure_name)


# Raw data results
fig_raw_data_results("Figures/results_raw.pdf", data)

# Mean square error values
fig_mean_square_error("Figures/mse.pdf", data)

# Lossy results for both datasets
target_datasets = ['noiseless', 'raw parallel', 'noiseless parallel',
                   'raw parallel noiseless', 'noise floor']
fig_dataset_results("Figures/results_wide_lossy.pdf",
                    [entry for entry in data['multiple peaks'] if entry['data set'] in target_datasets])
fig_dataset_results("Figures/results_thin_lossy.pdf",
                    [entry for entry in data['single peak'] if entry['data set'] in target_datasets])

# Results for peaks dataset
fig_peaks_data_results("Figures/results_peaks.pdf", data)

# Example oscillogram for wide dataset
wide_data = FbgData("C:/Users/norbert/PycharmProjects/data", 10000)
data = wide_data.get_sample_with_index(wide_data.get_number_of_samples() // 2)
fig_example_oscyllogram("Figures/wide_data_example.pdf", "Przykład oscylogramu z szerokiego zbioru danych", data)

# Example escillogram for thin dataset
thin_data = DataFromJulek(1000)
data = thin_data.get_sample_with_index(thin_data.get_number_of_samples() // 2)
fig_example_oscyllogram("Figures/thin_data_example.pdf", "Przykład oscylogramu z wąskiego zbioru danych", data)

# Example of denoising process for thin dataset
data_source = DataFromJulek(1000)
data = data_source.get_sample_with_index(data_source.get_number_of_samples() // 2)
denoised_data = denoise_data(data, 7)
fig_denoising_process_example("Figures/thin_data_denoising.pdf", "Przykład procesu odszumania wąskiego zbioru danych",
                              data, denoised_data)

# Example of noise floor method for thin dataset
noise_level = int(median(data) * 1.2)
data_noise_floor = data.copy()
for x in range(len(data_noise_floor)):
    if data_noise_floor[x] < noise_level:
        data_noise_floor[x] = noise_level
fig_noise_floor_process_example("Figures/thin_data_noise_floor.pdf",
                                "Przykład procesu ustalenia poziomu tła dla wąskiego zbioru danych",
                                data, data_noise_floor)

# Example of denoising process for wide dataset
data = wide_data.get_sample_with_index(wide_data.get_number_of_samples() // 2)
denoised_data = denoise_data(data, 30)
fig_denoising_process_example("Figures/wide_data_denoising.pdf", "Przykład procesu odszumania szerokiego zbioru danych",
                              data, denoised_data)

# Example of noise floor method for wide dataset
noise_level = int(median(data) * 1.2)
data_noise_floor = data.copy()
for x in range(len(data_noise_floor)):
    if data_noise_floor[x] < noise_level:
        data_noise_floor[x] = noise_level
fig_noise_floor_process_example("Figures/wide_data_noise_floor.pdf",
                                "Przykład procesu ustalenia poziomu tła dla szerokiego zbioru danych",
                                data, data_noise_floor)
