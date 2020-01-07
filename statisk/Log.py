from termcolor import colored, cprint

ascii_title = """ ▄▄▄· ▄· ▄▌.▄▄ · ▄▄▄▄▄ ▄▄▄· ▄▄▄▄▄▪  .▄▄ · ▄ •▄ 
▐█ ▄█▐█▪██▌▐█ ▀. •██  ▐█ ▀█ •██  ██ ▐█ ▀. █▌▄▌▪
 ██▀·▐█▌▐█▪▄▀▀▀█▄ ▐█.▪▄█▀▀█  ▐█.▪▐█·▄▀▀▀█▄▐▀▀▄·
▐█▪·• ▐█▀·.▐█▄▪▐█ ▐█▌·▐█ ▪▐▌ ▐█▌·▐█▌▐█▄▪▐█▐█.█▌
.▀     ▀ •  ▀▀▀▀  ▀▀▀  ▀  ▀  ▀▀▀ ▀▀▀ ▀▀▀▀ ·▀  ▀"""


# https://pypi.org/project/termcolor/
def title():
    line_break()
    green(ascii_title)
    line_break()


def error(message):
    cprint('Error: %s' % message, 'red')


def fatal_error(message):
    line_break()
    cprint('Fatal Error: %s' % message, 'red')
    line_break()
    exit(-1)


def red(message):
    print(colored(message, 'red'))


def salmon(message):
    print('\033[91m' + message + '\033[0m')


def purple(message):
    print('\033[95m' + message + '\033[0m')


def blue(message):
    print('\033[94m' + message + '\033[0m')


def green(message):
    cprint(message, 'green')


def grey(message):
    cprint(message, 'grey')


def line_break():
    print("")

