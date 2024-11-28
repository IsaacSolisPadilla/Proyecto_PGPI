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

class TestComprarContraReembolso():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_comprarContraReembolso(self):
    self.driver.get("http://localhost:8000/")
    self.driver.set_window_size(1510, 697)
    self.driver.find_element(By.NAME, "cantidad").send_keys("2")
    self.driver.find_element(By.NAME, "cantidad").click()
    self.driver.find_element(By.NAME, "cantidad").send_keys("3")
    self.driver.find_element(By.NAME, "cantidad").click()
    element = self.driver.find_element(By.NAME, "cantidad")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.NAME, "cantidad").send_keys("4")
    self.driver.find_element(By.NAME, "cantidad").click()
    self.driver.find_element(By.NAME, "cantidad").send_keys("5")
    self.driver.find_element(By.NAME, "cantidad").click()
    element = self.driver.find_element(By.NAME, "cantidad")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.NAME, "cantidad").send_keys("6")
    self.driver.find_element(By.NAME, "cantidad").click()
    self.driver.find_element(By.NAME, "cantidad").send_keys("7")
    self.driver.find_element(By.NAME, "cantidad").click()
    element = self.driver.find_element(By.NAME, "cantidad")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.NAME, "cantidad").send_keys("8")
    self.driver.find_element(By.NAME, "cantidad").click()
    self.driver.find_element(By.NAME, "cantidad").send_keys("9")
    self.driver.find_element(By.NAME, "cantidad").click()
    element = self.driver.find_element(By.NAME, "cantidad")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.NAME, "cantidad").send_keys("10")
    self.driver.find_element(By.NAME, "cantidad").click()
    self.driver.find_element(By.NAME, "cantidad").send_keys("11")
    self.driver.find_element(By.NAME, "cantidad").click()
    element = self.driver.find_element(By.NAME, "cantidad")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.NAME, "cantidad").send_keys("12")
    self.driver.find_element(By.NAME, "cantidad").click()
    self.driver.find_element(By.NAME, "cantidad").send_keys("13")
    self.driver.find_element(By.NAME, "cantidad").click()
    element = self.driver.find_element(By.NAME, "cantidad")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(2) .add-to-cart-button").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(3) .fas").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").send_keys("2")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").send_keys("3")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").send_keys("4")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").send_keys("5")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").click()
    element = self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").send_keys("6")
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) div > input").click()
    self.driver.find_element(By.CSS_SELECTOR, ".product:nth-child(5) .fas").click()
    self.driver.find_element(By.CSS_SELECTOR, ".fa-shopping-cart").click()
    self.driver.find_element(By.ID, "confirmar").click()
    self.driver.find_element(By.ID, "id_nombre").click()
    self.driver.find_element(By.ID, "id_nombre").send_keys("Isaac")
    self.driver.find_element(By.ID, "id_apellidos").send_keys("Solis")
    self.driver.find_element(By.ID, "id_direccion").send_keys("Tarfia")
    self.driver.find_element(By.ID, "id_email").send_keys("isaacsolis@gmail.com")
    self.driver.find_element(By.ID, "id_metodo_de_pago").click()
    self.driver.find_element(By.CSS_SELECTOR, "#id_metodo_de_pago > option:nth-child(1)").click()
    self.driver.find_element(By.ID, "id_forma_entrega").click()
    self.driver.find_element(By.CSS_SELECTOR, "#id_forma_entrega > option:nth-child(1)").click()
    self.driver.find_element(By.CSS_SELECTOR, "div > button:nth-child(1)").click()
  
