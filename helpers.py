from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

def select_element(driver, xpath, waitUntilCondition):
  try:
    ignored_exceptions = (
      # StaleElementReferenceException,
      # NoSuchElementException
    )
    element = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(waitUntilCondition)
    return element
  except TimeoutException:
    print(f'Fail: Element {xpath} does not exist.')
  except ElementNotInteractableException:
    print(f'Fail: Element {xpath} is not interactable.')
  except InvalidSelectorException:
    print(f'Invalid Selector in {xpath}.')

def str_apply_arguments(str, arguments):
  res = str
  for key, value in arguments.items():
    if f'^{key}^' in str:
      res = str.replace(f'^{key}^', value)
      break
  return res