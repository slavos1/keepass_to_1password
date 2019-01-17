import os

import twiggy

def make_logger(name):
    return twiggy.log.name(name).fields(pid=os.getpid())

