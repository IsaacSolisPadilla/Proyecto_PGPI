# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestEliminarProductoEnCarrito():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_eliminarProductoEnCarrito(self):
    self.driver.get("http://localhost:8000/")
    self.driver.set_window_size(1510, 697)
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").send_keys("2")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").send_keys("3")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").send_keys("4")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").send_keys("5")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").send_keys("6")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").send_keys("7")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) .fas").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(4) .add-to-cart-button").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").send_keys("2")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").send_keys("3")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").send_keys("4")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").send_keys("5")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").send_keys("6")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(8) .fas").click()
    self.driver.find_element(By.CSS_SELECTOR, ".fa-shopping-cart").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(3) > td:nth-child(6) input:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > td:nth-child(6) input:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, "td:nth-child(6) input:nth-child(1)").click()
    self.driver.find_element(By.ID, "volver").click()
  
