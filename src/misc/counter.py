import logging

class Counter:
    def __init__(self, len, info_func=None) -> None:
        self.len = len
        self.step = self.len/10000
        self.cur = 0
        self.last_block = 0
        self.logger = logging.getLogger(f"Counter")
        self.info_func=info_func
        pass

    def next(self):
        self.cur = self.cur+1
        self.last_block = self.last_block + 1
        if self.last_block >= self.step:
            cur_progress = self.cur*10000//self.len/100
            self.logger.debug(f"Progress: {cur_progress}%")
            if self.info_func is not None:
                self.info_func(cur_progress)
            self.last_block = 0

