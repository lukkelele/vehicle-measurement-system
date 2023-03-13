class PicoLogger:

    def info(self, message):
        print('[INFO] ', message)

    def warn(self, message):
        print('[WARN] ', message)

    def trace(self, message):
        print('[TRACE] ', message)

    def error(self, message):
        print('[ERROR] ', message)

    def critical(self, message):
        print('[CRITICAL] ', message)
