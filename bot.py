
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import login
import time
import pandas as pd
from selenium.common.exceptions import TimeoutException


browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()


browser.get("https://www.linkedin.com/login")

input_email = browser.find_element_by_id("username")
input_email.send_keys('guilherme.hlalbuquerque@gmail.com')

input_senha = browser.find_element_by_id("password")
input_senha.send_keys('Guilherme03')

btn_login = browser.find_element_by_xpath("//button[@type='submit']")
btn_login.click()


find = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Pesquisar']"))
)


busca = browser.find_element_by_xpath("//input[@placeholder='Pesquisar']")
busca.send_keys("Python")
busca.send_keys(Keys.RETURN)


filtro_vagas = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Vagas']")))
filtro_vagas.click()

elementos_vagas = WebDriverWait(browser, 50).until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'job-card-container')]")))

titulos = []
empresas = []
localizacoes = []

for vaga in elementos_vagas:
    titulo = vaga.find_element_by_xpath(".//h3[contains(@class, 'job-card-title')]").text
    empresa = vaga.find_element_by_xpath(".//h4[contains(@class, 'job-card-company')]").text
    localizacao = vaga.find_element_by_xpath(".//span[contains(@class, 'job-card-location')]").text

    titulos.append(titulo)
    empresas.append(empresa)
    localizacoes.append(localizacao)

browser.quit()

dados = {'Título': titulos, 'Empresa': empresas, 'Localização': localizacoes}
df = pd.DataFrame(data=dados)
df.to_csv('vagas_linkedin.csv', index=False)

try:
    filtro_vagas = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Vagas']")))
except TimeoutException:
    print('Elemento não encontrado. Continuando a execução.')
