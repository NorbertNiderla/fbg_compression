from math import nan

import numpy as np
from matplotlib import pyplot as plt

data = {'multiple peaks': [{'data set': 'raw',
                            'entropy': 5.974817644440901,
                            'mse': nan,
                            'original bitwidth': 14,
                            'results': [['sprintz', 10.013065570053387],
                                        ['sprintz delta', 10.079345742378331]]},
                           {'data set': 'noiseless',
                            'entropy': 4.5336990489232845,
                            'mse': 13183.036641724897,
                            'original bitwidth': 14,
                            'results': [['sprintz', 5.195169336054253],
                                        ['sprintz delta', 5.23830828849999]]},
                           {'data set': 'peaks stream',
                            'entropy': 6.474695665695363,
                            'mse': nan,
                            'original bitwidth': 12,
                            'results': [['sprintz', 5.17962870045158],
                                        ['sprintz delta', 5.1073758153537385]]},
                           {'data set': 'raw parallel',
                            'entropy': 4.458495623956762,
                            'mse': nan,
                            'original bitwidth': 14,
                            'results': [['sprintz', 10.31464968152866],
                                        ['sprintz delta', 10.385987261146497]]},
                           {'data set': 'noiseless parallel',
                            'entropy': 4.103054350129071,
                            'mse': 335569.11592356686,
                            'original bitwidth': 14,
                            'results': [['sprintz', 8.54140127388535],
                                        ['sprintz delta', 8.54140127388535]]},
                           {'data set': 'raw parallel noiseless',
                            'entropy': 3.819986437631907,
                            'mse': 335569.11592356686,
                            'original bitwidth': 14,
                            'results': [['sprintz', 6.778343949044586],
                                        ['sprintz delta', 6.742675159235668]]},
                           {'data set': 'noise floor',
                            'entropy': 0.5669652299939721,
                            'mse': 175664.1974779956,
                            'original bitwidth': 14,
                            'results': [['sprintz', 0.684510337435327],
                                        ['sprintz delta', 0.68454847154371]]}]}

MSE_SCALE = 40000

labels = [entry['data set'] for entry in data['multiple peaks']]
sprintz_values = [entry['results'][0][1] for entry in data['multiple peaks']]
sprintz_delta_values = [entry['results'][1][1] for entry in data['multiple peaks']]
mse_values = [entry['mse'] / MSE_SCALE for entry in data['multiple peaks']]

index = np.arange(len(labels))
bar_width = 0.2

fig, axs = plt.subplots(1, 2)

axs[0].bar(index, sprintz_values, bar_width, label='Sprintz')
axs[0].bar(index + bar_width, sprintz_delta_values, bar_width, label='Sprintz Delta')
axs[0].set_xlabel('Data Set')
axs[0].set_ylabel('Results')
axs[0].set_title('Results for Multiple Peaks')
axs[0].set_xticks(index + bar_width / 2)
axs[0].set_xticklabels(labels, rotation=45)
axs[0].legend()

axs[1].bar(index, mse_values, bar_width, label='Normalized MSE')
axs[1].set_xlabel('Data Set')
axs[1].set_ylabel('Normalized MSE')
axs[1].set_title('Results for Multiple Peaks')
axs[1].set_xticks(index)
axs[1].set_xticklabels(labels, rotation=45)

plt.tight_layout()
plt.show()
