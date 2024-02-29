def black(msg):
  return f'\033[90m{msg}\033[0m'

def red(msg):
  return f'\033[91m{msg}\033[0m'

def green(msg):
  return f'\033[92m{msg}\033[0m'

def yellow(msg):
  return f'\033[93m{msg}\033[0m'

def blue(msg):
  return f'\033[94m{msg}\033[0m'

def magenta(msg):
  return f'\033[95m{msg}\033[0m'

def cyan(msg):
  return f'\033[96m{msg}\033[0m'

def white(msg):
  return f'\033[97m{msg}\033[0m'

def color_message(msg):
  return {
    'black': black(msg),
    'red': red(msg),
    'green': green(msg),
    'yellow': yellow(msg),
    'blue': blue(msg),
    'magenta': magenta(msg),
    'cyan': cyan(msg),
    'white': white(msg),
  }