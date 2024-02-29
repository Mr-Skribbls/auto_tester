from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from message_colors import color_message

def select_element(driver, xpath, waitUntilCondition):
  try:
    ignored_exceptions = (
      StaleElementReferenceException,
      NoSuchElementException
    )
    element = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(waitUntilCondition)
    return element
  except TimeoutException:
    print(color_message(f'Fail: Element {xpath} does not exist.')['red'])
  except ElementNotInteractableException:
    print(color_message(f'Fail: Element {xpath} is not interactable.')['red'])
  except InvalidSelectorException:
    print(color_message(f'Invalid Selector in {xpath}.')['red'])

def str_apply_arguments(str, arguments):
  res = str
  for key, value in arguments.items():
    if f'^{key}^' in str:
      res = str.replace(f'^{key}^', value)
      break
  return res