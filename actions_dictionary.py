import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from helpers import *
from message_colors import color_message

remembered = {}

def string_input(driver, step, arguments):
  xpath = str_apply_arguments(step['xpath'], arguments) if 'xpath' in step else None
  value = str_apply_arguments(step['value'], arguments) if 'value' in step else None
  if value == None or xpath == None:
    print(color_message('String input action must have value and xpath')['warn'])
    return False
  element = select_element(driver, xpath, EC.element_to_be_clickable((By.XPATH, xpath)))
  if element == None: return False
  element.send_keys(value)
  return True

def click(driver, step, arguments):
  xpath = str_apply_arguments(step['xpath'], arguments) if 'xpath' in step else None
  if xpath == None:
    print(color_message('Click action must have xpath')['warn'])
    return False
  element = select_element(driver, xpath, EC.element_to_be_clickable((By.XPATH, xpath)))
  if element == None:
    return False
  element.click()
  return True

def drag_drop(driver, step, arguments):
  drag_xpath = str_apply_arguments(step['drag_xpath'], arguments) if 'drag_xpath' in step else None
  drop_xpath = str_apply_arguments(step['drop_xpath'], arguments) if 'drop_xpath' in step else None
  if drag_xpath == None or drop_xpath == None:
    print(color_message('Drag and drop action must have drag_xpath and drop_xpath'))

  drag = select_element(driver, drag_xpath, EC.element_to_be_clickable((By.XPATH, drag_xpath)))
  drop = select_element(driver, drop_xpath, EC.element_to_be_clickable((By.XPATH, drop_xpath)))
  if drag == None or drop == None: return False

  ActionChains(driver).drag_and_drop(drag, drop).perform()

  return True

def remember(driver, step, arguments):
  xpath = str_apply_arguments(step['xpath'], arguments) if 'xpath' in step else None
  rememberKey = str_apply_arguments(step['rememberKey'], arguments) if 'rememberKey' in step else None

  if xpath == None or rememberKey == None:
    print(color_message('Remember action must have xpath, and rememberKey')['warn'])
    return False

  element = select_element(driver, xpath, EC.element_to_be_clickable((By.XPATH, xpath)))
  if element == None: return False

  remembered[rememberKey] = element.text

  return True

def forget(driver, step, arguments):
  rememberKey = str_apply_arguments(step['rememberKey'], arguments) if 'rememberKey' in step else None

  if rememberKey == None:
    print(color_message('Forget action must have a rememberKey')['warn'])
    return False

  if rememberKey in remembered:
    del remembered[rememberKey]
  
  return True


#### Checks ####

def check_exists(driver, step, arguments):
  xpath = str_apply_arguments(step['xpath'], arguments) if 'xpath' in step else None
  if xpath == None:
    print(color_message('Check exists action must have xpath')['warn'])
    return False
  element = select_element(driver, xpath, EC.visibility_of_element_located((By.XPATH, xpath)))
  return element != None

def check_value(driver, step, arguments):
  xpath = str_apply_arguments(step['xpath'], arguments) if 'xpath' in step else None
  value = str_apply_arguments(step['value'], arguments) if 'value' in step else None
  if value == None or xpath == None:
    print(color_message('Check value action must have value and xpath')['warn'])
    return False
  element = select_element(driver, xpath, EC.element_attribute_to_include((By.XPATH, xpath), 'value'))
  if element == None: return False

  v = element.get_attribute('value')
  if v != value:
    print(color_message(f'Fail: Element {xpath} value is {v} not {value}')['red'])
    return False
  
  return True

def check_text_is_remembered(driver, step, arguments):
  xpath = str_apply_arguments(step['xpath'], arguments) if 'xpath' in step else None
  rememberKey = str_apply_arguments(step['rememberKey'], arguments) if 'rememberKey' in step else None
  if xpath == None or rememberKey == None:
    print(color_message('Check remembered action must have xpath and rememberKey')['warn'])
    return False
  element = select_element(driver, xpath, EC.element_to_be_clickable((By.XPATH, xpath)))
  if element == None: return False

  if element.text != remembered[rememberKey]:
    colored_fail = color_message('Fail:')['red']
    colored_text = color_message(element.text)['red']
    colored_remembered = color_message(remembered[rememberKey])['red']
    print(f'{colored_fail} Element {xpath} value is {colored_text} not {colored_remembered}')
    return False
  
  return True

actions = {
  'string input': string_input,
  'click': click,
  'drag and drop': drag_drop,
  'remember': remember,
  'check exists': check_exists,
  'check value': check_value,
  'check remembered': check_text_is_remembered,
  'forget': forget,
}