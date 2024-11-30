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

class TestCrearCategoria():
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_crearCategoria(self):
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1510, 697)
        self.driver.find_element(By.CSS_SELECTOR, ".cta > span").click()
        self.driver.find_element(By.CSS_SELECTOR, "label:nth-child(3) > span").click()
        self.driver.find_element(By.NAME, "email").send_keys("grupo17@gmail.com")
        self.driver.find_element(By.NAME, "password").send_keys("1234")
        self.driver.find_element(By.CSS_SELECTOR, ".submit").click()

        # Espera y maneja el pop-up (alerta) que aparece después de iniciar sesión
        WebDriverWait(self.driver, 10).until(
            expected_conditions.alert_is_present()
        )
        alert = self.driver.switch_to.alert
        alert.accept()  # Hace clic en "OK" en el pop-up

        # Continúa con las acciones después del login
        self.driver.find_element(By.LINK_TEXT, "Crear nueva categoría").click()
        self.driver.find_element(By.NAME, "nombre").click()
        self.driver.find_element(By.NAME, "nombre").send_keys("Prueba")
        self.driver.find_element(By.NAME, "descripcion").send_keys("Prueba de creacion de categoria")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        self.driver.find_element(By.LINK_TEXT, "Editar").click()
        self.driver.find_element(By.ID, "descripcion").click()
        self.driver.find_element(By.ID, "descripcion").send_keys("Velas aromáticas para meditación y relajación. Esto es una prueba de edicion de categoria")
        self.driver.find_element(By.CSS_SELECTOR, ".submit-button").click()
        self.driver.find_element(By.CSS_SELECTOR, ".category-item:nth-child(4) .delete-button").click()
        self.driver.switch_to.alert.accept()
