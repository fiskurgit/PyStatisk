from termcolor import colored, cprint

ascii_title = """ ▄▄▄· ▄· ▄▌.▄▄ · ▄▄▄▄▄ ▄▄▄· ▄▄▄▄▄▪  .▄▄ · ▄ •▄ 
▐█ ▄█▐█▪██▌▐█ ▀. •██  ▐█ ▀█ •██  ██ ▐█ ▀. █▌▄▌▪
 ██▀·▐█▌▐█▪▄▀▀▀█▄ ▐█.▪▄█▀▀█  ▐█.▪▐█·▄▀▀▀█▄▐▀▀▄·
▐█▪·• ▐█▀·.▐█▄▪▐█ ▐█▌·▐█ ▪▐▌ ▐█▌·▐█▌▐█▄▪▐█▐█.█▌
.▀     ▀ •  ▀▀▀▀  ▀▀▀  ▀  ▀  ▀▀▀ ▀▀▀ ▀▀▀▀ ·▀  ▀"""


# https://pypi.org/project/termcolor/
def title():
    line_break()
    salmon(ascii_title)
    line_break()


def error(message):
    cprint('Error: %s' % message, 'yellow', 'on_red')


def fatal_error(message):
    cprint('Fatal Error: %s' % message, 'yellow', 'on_red')
    exit(-1)


def red(message):
    print(colored(message, 'red'))


def salmon(message):
    print('\033[91m' + message + '\033[0m')


def purple(message):
    print('\033[95m' + message + '\033[0m')


def blue(message):
    print('\033[94m' + message + '\033[0m')


def line_break():
    print("")

