from colorama import init
init()
from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

from colorama import init
from termcolor import colored
# use Colorama to make Termcolor work on Windows too
init()
# then use Termcolor for all colored text output
print(colored('Hello, World!', 'green', 'on_red'))
print(colored("Hello, World!", "green"))

from colorama import init, Fore
init(autoreset=True)
print(Fore.RED + 'some red text')
print('automatically back to default color again')