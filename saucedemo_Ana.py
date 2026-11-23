import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Abrir la pagina y validar pantalla de login
        driver.get("https://www.saucedemo.com/")
        login_btn = wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
        assert login_btn.is_displayed(), "No cargo el boton de login"

        # 2. Iniciar sesion y validar que entra al catalogo
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        login_btn.click()

        titulo = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title"))).text
        assert titulo == "Products", f"Se esperaba 'Products' y llego '{titulo}'"

        # 3. Agregar 'Sauce Labs Backpack' al carrito y validar el contador en 1
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        carrito_num = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        ).text
        assert carrito_num == "1", f"Se esperaba '1' en el carrito y llego '{carrito_num}'"

        # 4. Abrir el carrito y validar que aparezca 'Sauce Labs Backpack'
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        producto = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        ).text
        assert producto == "Sauce Labs Backpack", "El producto en el carrito no coincide"

        # 5. Hacer clic en Checkout, llenar datos y continuar
        driver.find_element(By.ID, "checkout").click()
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Ana")
        driver.find_element(By.ID, "last-name").send_keys("Luquez")
        driver.find_element(By.ID, "postal-code").send_keys("20301")
        driver.find_element(By.ID, "continue").click()

        # 6. Finalizar compra y validar mensaje de confirmacion
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        mensaje = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text
        assert mensaje == "Thank you for your order!", f"Mensaje inesperado: '{mensaje}'"

        print("Prueba automatizada exitosa en https://www.saucedemo.com/")

    finally:
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()