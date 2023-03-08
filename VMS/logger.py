from os import environ
import logging as log

LOGGING_LEVEL = log.DEBUG

try:
    import coloredlogs # pyright: ignore
    environ["COLOREDLOGS_LOG_FORMAT"] = f'%(asctime)s - %(levelname)3s - %(filename)4s:%(lineno)s | %(message)s '
    environ["COLOREDLOGS_DATE_FORMAT"] = '%H:%M:%S'
    coloredlogs.install()
except:
    print("Coloredlogs could not be initialized, running basic log.configuration instead")

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'TRACE': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

class ColorFormatter(log.Formatter):
    def __init__(self, msg, use_color = True):
        log.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return log.Formatter.format(self, record)


class Logger(log.Logger):
    log.basicConfig(level=LOGGING_LEVEL,
                         format='{asctime} {levelname} {filename:<4s}:{lineno} | {message}', 
                         datefmt='%H:%M:%S',
                         style='{')

    FORMAT = "[$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name):
        log.Logger.__init__(self, name, LOGGING_LEVEL)
        color_formatter = ColorFormatter(self.COLOR_FORMAT)
        console = log.StreamHandler()
        console.setFormatter(color_formatter)
        self.addHandler(console)
        log.Handler.setLevel(log.NOTSET)
        return
