import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from datetime import datetime


class TestSauceDemo(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument('start-maximized')
        preferences = {
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True
        }
        options.add_experimental_option("prefs", preferences)

        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(options=options, service=service)
        self.wait = WebDriverWait(self.driver, 20)

    def guardar_captura(self, prefijo="screenshot"):
        os.makedirs("img", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join("img", f"{prefijo}_{timestamp}.png")
        self.driver.save_screenshot(file_path)
        print(f"Captura guardada en: {file_path}")

    def test_compra_saucedemo(self):
        try:
            print("Paso 1: Abriendo SauceDemo...")
            self.driver.get("https://www.saucedemo.com/")
            login_btn = self.wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
            self.assertTrue(login_btn.is_displayed(), "No cargó el botón de inicio de sesión")

            print("Paso 2: Iniciando sesión...")
            self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
            self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
            login_btn.click()

            titulo = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title"))).text
            self.assertEqual(titulo, "Products", "El título de la página no coincide con 'Products'")

            print("Paso 3: Agregando producto al carrito...")
            self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
            carrito_num = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
            ).text
            self.assertEqual(carrito_num, "1", "Se esperaba '1' producto en el carrito")

            print("Paso 4: Abriendo carrito...")
            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))).click()
            self.wait.until(EC.url_contains("cart.html"))
            producto = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
            ).text
            self.assertEqual(producto, "Sauce Labs Backpack", "El producto en el carrito no coincide")

            print("Paso 5: Llenando datos de envío...")
            self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()
            self.wait.until(EC.url_contains("checkout-step-one.html"))

            first_name = self.wait.until(EC.element_to_be_clickable((By.ID, "first-name")))
            first_name.clear()
            first_name.send_keys("Ana")

            last_name = self.wait.until(EC.element_to_be_clickable((By.ID, "last-name")))
            last_name.clear()
            last_name.send_keys("Luquez")

            postal_code = self.wait.until(EC.element_to_be_clickable((By.ID, "postal-code")))
            postal_code.clear()
            postal_code.send_keys("20301")

            self.wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()
            self.wait.until(EC.url_contains("checkout-step-two.html"))

            print("Paso 6: Finalizando compra...")
            finish_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "finish")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", finish_btn)
            finish_btn.click()

            self.wait.until(EC.url_contains("checkout-complete.html"))
            mensaje_final = self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
            ).text
            print(f"Mensaje final: {mensaje_final}")
            self.assertEqual(
                mensaje_final,
                "Thank you for your order!",
                "El mensaje de confirmación no coincide con el esperado"
            )

            print("Paso 7: Guardando captura final...")
            self.guardar_captura("screenshot")

        except Exception as e:
            print(f"FALLO DETECTADO: {type(e).__name__} -> {e}")
            self.guardar_captura("error")
            raise

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="reporthtmlrunner"))