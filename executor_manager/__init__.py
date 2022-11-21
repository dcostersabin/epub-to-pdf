import subprocess
from abc import ABC, abstractmethod


class Executor(ABC):

    def __init__(self, cwd=None):
        self.cwd = cwd
        self.output = None
        self.return_code = None
        self.error = None
        self.process = None
        self._timeout = 60 * 120

    def start(self):
        self._run()

    def _run(self):
        self._start_subprocess()

    @abstractmethod
    def commands(self):
        pass

    @abstractmethod
    def post_execution(self):
        pass

    @abstractmethod
    def process_error(self, e: Exception):
        pass

    def _start_subprocess(self):
        try:
            self.process = subprocess.Popen(
                self.commands(),
                stdout=subprocess.PIPE,
                shell=True,
                cwd=self.cwd
            )

            self.output = self.process.communicate(timeout=self._timeout)[0].decode('utf-8')
            self.error = self.process.stderr
            self.return_code = self.process.wait(self._timeout * 5)
            self.post_execution()
        except Exception as e:
            self.process_error(e)
        finally:
            if not self.process:
                self.process.kill()
