from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import time
import re

"""
driver = webdriver.Chrome()

driver.get("http://127.0.0.1:5000/login") 



driver.find_element(By.ID, "password").send_keys("elPepe2025#")
driver.find_element(By.ID, "login").click()

time.sleep(2)

saldo_texto = driver.find_element(By.ID,"saldo_usuario").text 
saldo_inicial = float(saldo_texto.split(":")[-1].strip())

driver.find_element(By.ID, "deposit_button").click()

time.sleep(2)

driver.find_element(By.ID, "balance").send_keys("100")
driver.find_element(By.ID, "deposit").click()

time.sleep(2)

saldo_texto_final = driver.find_element(By.ID, "saldo_usuario").text
saldo_final = float(saldo_texto_final.split(":")[-1].strip())

assert saldo_final == saldo_inicial + 100,f"Error: Saldo esperado {saldo_inicial +100}; Saldo obtenido {saldo_texto_final}"

time.sleep(2)
driver.quit()
"""

# Test feliz

driver = webdriver.Chrome()

driver.get("http://127.0.0.1:5000/login") 

driver.find_element(By.ID, "password").send_keys("elPepe2025#")
driver.find_element(By.ID, "login").click()

time.sleep(2)

saldo_texto = driver.find_element(By.ID,"saldo_usuario").text 
saldo_inicial = float(saldo_texto.split(":")[-1].strip())


driver.find_element(By.ID, "Withdraw_button").click()

time.sleep(2)

driver.find_element(By.ID, "balance").send_keys("10")
driver.find_element(By.ID, "password").send_keys("elPepe2025#")
driver.find_element(By.ID, "withdraw_button").click()

time.sleep(2)

saldo_texto_final = driver.find_element(By.ID, "saldo_usuario").text
saldo_final = float(saldo_texto_final.split(":")[-1].strip())

assert saldo_final == saldo_inicial - 10, f"Error: Saldo esperado {saldo_inicial - 10}; Saldo obtenido {saldo_final}"

driver.quit()

# Test no feliz

driver = webdriver.Chrome()

driver.get("http://127.0.0.1:5000/login") 

driver.find_element(By.ID, "email").send_keys("el.pepe@urosario.edu.co")
driver.find_element(By.ID, "password").send_keys("lamala")
driver.find_element(By.ID, "login").click()

time.sleep(2)

error_login = driver.find_element(By.ID, "error_login").text
assert "Credenciales inválidas" in error_login, f"Error esperado no encontrado. Mensaje obtenido: {error_login}"

driver.quit()
