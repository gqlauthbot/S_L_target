import logging
class log():
    def __init__(self,name,debbug=False) -> None:
        
        # create logger with name as a param
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG) 
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
        fh=logging.FileHandler("LOG.txt",'a')
        fh.setFormatter(formatter)
        fh.setLevel(logging.DEBUG)
        self.logger.addHandler(fh)
        if debbug:
            # create console handler and set level to debug
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            # add formatter to ch
            ch.setFormatter(formatter)
            # add ch to logger
            self.logger.addHandler(ch)
            self.logger.removeHandler(fh)

    def get_logger(self)->logging.Logger:
        return self.logger