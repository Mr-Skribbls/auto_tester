# helpful selenium video - https://www.youtube.com/watch?v=SPM1tm2ZdK4

# argument 1 - site url to test
# argument 2 to end - tests to run

import sys
import json
import time
from message_colors import color_message
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from actions_dictionary import actions

def run_step(step, arguments, driver, actions):
  time.sleep(1)

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
  
  return res

def run_steps(steps, arguments, driver, actions):
  if arguments == None:
    arguments = {}

  res = True

  for step in steps:
    res = run_step(step, arguments, driver, actions)
    if not res:
      break

  return res

def run_procedure(p, arguments, driver, actions):
  res = True
  with open(p['path']) as f:
    procedure = json.load(f)
    res = run_steps(procedure['steps'], arguments, driver, actions)
  
  if not res:
    name = procedure['name']
    msg = f'Procedure Failed: {name}'
    print(color_message(msg)['red'])

  return res

def run_procedures(procedures, driver, actions):
  test_pass = True
  for procedure in procedures:
    if 'path' in procedure and 'steps' not in procedure:
      arguments = procedure['arguments'] if 'arguments' in procedure else None
      test_pass = run_procedure(procedure, arguments, driver, actions)
    elif 'steps' in procedure and 'path' not in procedure:
      steps = procedure['steps']
      test_pass = run_steps(steps, None, driver, actions)
    else:
      msg = 'Test procedure must include either a path or steps, but not both'
      print(color_message(msg)['red'])
      test_pass = False
    
    if not test_pass:
      break
  return test_pass

def run_test(t, driver, actions):
  with open(f'tests/{t}.json') as f:
    test = json.load(f)
    name = test['name']
    print(color_message(f'----- Starting Test: {name} -----')['blue'])
    test_pass = run_procedures(test['procedures'], driver, actions)
    teardown_pass = run_procedures(test['teardownProcedures'], driver, actions)

    test_res = color_message(f'{name} - Passes')['green'] if test_pass else color_message(f'{name} - Failed')['red']
    teardown_res = color_message(f'{name} - Teardown Passes')['green'] if teardown_pass else color_message(f'{name} - Teardown Failed')['red']

    print(test_res)
    print(teardown_res)
    print(color_message(f'----- Completed Testing For: {name} -----')['blue'])

options = Options()
# options.add_experimental_option('detach', True)

driver = webdriver.Chrome(
  service=Service(ChromeDriverManager().install()),
  options=options
)

driver.get(sys.argv[1])
driver.maximize_window()

for i in range(2, len(sys.argv)):
  if not run_test(sys.argv[i], driver, actions):
    break