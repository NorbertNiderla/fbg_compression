from os import listdir
from os.path import join

DATA_LIMIT = 0.19


class FbgData:
    def __init__(self, data_folder, step):
        self.dir = data_folder
        self.files = listdir(data_folder)
        original_len = len(self.files)
        self.files = [val for idx, val in enumerate(self.files) if
                      ((idx % step == 0) and (idx < DATA_LIMIT * original_len))]
        self.idx = 0
        self.size = len(self.files)

    def get_number_of_files(self):
        return self.size

    def get_data(self) -> [list, bool]:
        data = []
        last_file = False
        with open(join(self.dir, self.files[self.idx])) as datafile:
            data = eval(datafile.read())["data"]
        self.idx += 1
        if self.idx == self.size:
            self.idx = 0
            last_file = True

        return list(data), last_file

    def get_data_with_index(self, index):
        assert(index < len(self.files))
        with open(join(self.dir, self.files[index])) as datafile:
            data = eval(datafile.read())["data"]
            return data
