def green(msg):
  return f'\033[92m{msg}\033[0m'

def red(msg):
  return f'\033[91m{msg}\033[0m'

def cyan(msg):
  return f'\033[96m{msg}\033[0m'

def blue(msg):
  return f'\033[94m{msg}\033[0m'

def warn(msg):
  return f'\033[93m{msg}\033[0m'

def color_message(msg):
  return {
    'red': red(msg),
    'green': green(msg),
    'blue': blue(msg),
    'cyan': cyan(msg),
    'warn': warn(msg),
  }