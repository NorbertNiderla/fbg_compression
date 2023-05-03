from abc import ABC, abstractmethod
from os import listdir
from os.path import join

from data.parse_od_julka import get_data_from_julek


class Data(ABC):
    @abstractmethod
    def get_number_of_samples(self) -> int:
        pass

    @abstractmethod
    def get_next_sample(self) -> list:
        pass

    @abstractmethod
    def get_sample_with_index(self, index: int) -> list:
        pass


class FbgData(Data):
    def __init__(self, data_folder, step):
        self.DATA_LIMIT = 0.19
        self.dir = data_folder
        self.files = listdir(data_folder)
        original_len = len(self.files)
        self.files = [val for idx, val in enumerate(self.files) if
                      ((idx % step == 0) and (idx < self.DATA_LIMIT * original_len))]
        self.idx = 0
        self.size = len(self.files)

    def get_number_of_samples(self) -> int:
        return self.size

    def get_next_sample(self) -> list:
        with open(join(self.dir, self.files[self.idx])) as datafile:
            data = eval(datafile.read())["data"]
        self.idx += 1
        if self.idx == self.size:
            self.idx = 0

        return list(data)

    def get_sample_with_index(self, index):
        assert (index < len(self.files))
        with open(join(self.dir, self.files[index])) as datafile:
            data = list(eval(datafile.read())["data"])
            return data


class DataFromJulek(Data):
    def __init__(self, file_step: int):
        self.x, self.y = get_data_from_julek(file_step)
        self.size = len(self.y)
        self.idx = 0

    def get_number_of_samples(self) -> int:
        return self.size

    def get_next_sample(self) -> list:
        data = self.get_sample_with_index(self.idx)
        self.idx += 1
        if self.idx == self.size:
            self.idx = 0
        return data

    def get_sample_with_index(self, index: int) -> list:
        return self.y[index].tolist()
