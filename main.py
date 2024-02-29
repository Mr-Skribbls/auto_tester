# helpful selenium video - https://www.youtube.com/watch?v=SPM1tm2ZdK4

# argument 1 - site url to test
# argument 2 to end - tests to run

import sys
import json
import time
import argparse
from message_colors import color_message
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from actions_dictionary import actions

def run_step(step, arguments, driver, actions, **kwargs):
  show_steps = kwargs['show_steps'] if 'show_steps' in kwargs else False

  if show_steps:
    print(color_message(step['description'])['cyan'])

  if 'waitBefore' in step:
    time.sleep(step['waitBefore'])

  res = True

  action = step['action']
  if action not in actions:
    msg = f'Action: {action} is not currently supported'
    print(color_message(msg)['red'])
    res = False
  
  if res:
    res = actions[action](driver, step, arguments)

  if not res:
    description = step['description']
    msg = f'Step Failed: {description}'
    print(color_message(msg)['red'])
  
  if 'waitAfter' in step:
    time.sleep(step['waitAfter'])

  return res

def run_steps(steps, arguments, driver, actions, **kwargs):
  if arguments == None:
    arguments = {}

  res = True

  show_steps = kwargs['show_steps'] if 'show_steps' in kwargs else False

  for step in steps:
    res = run_step(step, arguments, driver, actions, show_steps=show_steps)
    if not res:
      break

  return res

def run_procedure(p, arguments, driver, actions, **kwargs):
  res = True

  show_steps = kwargs['show_steps'] if 'show_steps' in kwargs else False

  with open(p['path']) as f:
    procedure = json.load(f)
    if show_steps:
      print(color_message(procedure['name'])['magenta'])
    res = run_steps(procedure['steps'], arguments, driver, actions, show_steps=show_steps)
  
  if not res:
    name = procedure['name']
    msg = f'Procedure Failed: {name}'
    print(color_message(msg)['red'])

  return res

def run_procedures(procedures, driver, actions, **kwargs):
  test_pass = True

  show_steps = kwargs['show_steps'] if 'show_steps' in kwargs else False

  for procedure in procedures:
    if 'path' in procedure and 'steps' not in procedure:
      arguments = procedure['arguments'] if 'arguments' in procedure else None
      test_pass = run_procedure(procedure, arguments, driver, actions, show_steps=show_steps)
    elif 'steps' in procedure and 'path' not in procedure:
      steps = procedure['steps']
      if show_steps:
        print(color_message(procedure['name'])['magenta'])
      test_pass = run_steps(steps, None, driver, actions, show_steps=show_steps)
    else:
      msg = 'Test procedure must include either a path or steps, but not both'
      print(color_message(msg)['red'])
      test_pass = False
    
    if ('continue_on_fail' not in kwargs or not kwargs['continue_on_fail']) and not test_pass:
      break

  return test_pass

def run_test(t, driver, actions, show_steps):
  with open(f'tests/{t}.json') as f:
    test = json.load(f)
    name = test['name']
    print(color_message(f'----- Starting Test: {name} -----')['blue'])
    test_pass = run_procedures(test['procedures'], driver, actions, show_steps=show_steps)
    teardown_pass = run_procedures(test['teardownProcedures'], driver, actions, show_steps=show_steps, continue_on_fail=True)

    test_res = color_message(f'{name} - Passes')['green'] if test_pass else color_message(f'{name} - Failed')['red']
    teardown_res = color_message(f'{name} - Teardown Passes')['green'] if teardown_pass else color_message(f'{name} - Teardown Failed')['red']

    print(test_res)
    print(teardown_res)
    print(color_message(f'----- Completed Testing For: {name} -----')['blue'])

parser = argparse.ArgumentParser(description='Web Automated Testing')
parser.add_argument('url', type=str, help='URL of the website to test')
parser.add_argument('tests', type=str, nargs='+', help='Tests to run. Must be provided in the tests directory.')
parser.add_argument('-s', '--show-steps', action='store_true', help='Shows procedure names and step descriptions in the terminal.')
args = parser.parse_args()

options = Options()
# options.add_experimental_option('detach', True)

driver = webdriver.Chrome(
  service=Service(ChromeDriverManager().install()),
  options=options
)

driver.get(args.url)
driver.maximize_window()

for t in args.tests:
  if not run_test(t, driver, actions, show_steps=args.show_steps):
    break