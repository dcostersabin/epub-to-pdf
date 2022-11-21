import os
import argparse
from converter import Converter
from multiprocessing import Pool
from multiprocessing import cpu_count

parser = argparse.ArgumentParser(description='Epub Converter')

parser.add_argument('--input-dir', help='Path To Input Directory', required=True)
parser.add_argument('--output-dir', help='Path To Output Directory', required=True)

ar = parser.parse_args()


class ConvertEpub:

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self._files = []

    def start(self):
        self._get_files()
        self._process_pipeline()

    @staticmethod
    def _convert(filename, output_dir):
        obj = Converter(filename=filename, output_dir=output_dir)
        obj.start()
        msg = f"Converted {filename} To PDF" if obj.status else f"Failed To Convert {filename} To PDF"
        return msg

    def _get_files(self):
        file_list = os.listdir(self.input_dir)
        self._files += [f'{self.input_dir}/{i}' for i in file_list if i.endswith('.epub')]

    def _process_pipeline(self):
        with Pool(processes=cpu_count()) as p:
            multi_process = [p.apply_async(self._convert, (i, self.output_dir)) for i in self._files]
            statuses = [res.get(timeout=60 * 3) for res in multi_process]
            _ = [print(status) for status in statuses]


if __name__ == "__main__":
    obj = ConvertEpub(input_dir=ar.input_dir, output_dir=ar.output_dir)
    obj.start()
