from scipy.io import loadmat


def get_data_from_julek() -> [list, list]:
    # Load the .mat file
    data = loadmat('C:/Users/norbert/repositories/fbg_compression/python/data/od_julka.mat')

    # Extract the first set of x and y data
    volt_N = data['volt_N']
    y_N = data['y_N']

    x = [i for i in volt_N[0]]
    y_all = [s for s in y_N]

    return x, y_all
