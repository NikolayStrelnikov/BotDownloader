import logging
from logging import handlers


# Автоматическая настройка логов
def logger():
    log_file = './log/bot.log'
    log_level = logging.INFO
    log_format = '%(asctime)s - %(levelname)s:%(name)s:%(message)s'
    log_handler = [handlers.RotatingFileHandler(filename=log_file,
                                                maxBytes=10 * 1024 * 1024,
                                                backupCount=5,
                                                encoding='utf-8')]
    logging.basicConfig(level=log_level, format=log_format, handlers=log_handler)


# DEBUG: наименее серьезный уровень. Обычно используется для диагностики
# INFO: используется для подтверждения того, что все работает как ожидалось
# WARNING: указывает на то, что произошло что-то необычное, или на возможную проблему в будущем
# ERROR: указывает на более серьезную проблему, которая не позволила программе выполнить что-то
# CRITICAL: наиболее серьезный уровень. Индицирует очень серьезную проблему


def read_last_log(filename='log/bot.log', lines=10):
    with open(filename, 'r', encoding='utf-8') as f:
        return ''.join(f.readlines()[-lines:])
