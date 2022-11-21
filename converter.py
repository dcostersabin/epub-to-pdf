from executor_manager import Executor
from uuid import uuid5
from uuid import NAMESPACE_DNS
from datetime import datetime
from random import getrandbits


class Converter(Executor):

    def __init__(self, filename, output_dir):
        self.filename = filename
        self.output_dir = output_dir
        self.status = False
        super(Converter, self).__init__()

    @property
    def _get_name(self):
        return f"{uuid5(NAMESPACE_DNS, str(datetime.now().strftime('%s')) + str(getrandbits(20)))}.pdf"

    def commands(self):
        return [f'ebook-convert {self.filename} {self.output_dir}/{self._get_name}']

    def post_execution(self):
        self.status = True

    def process_error(self, e: Exception):
        self.status = False
