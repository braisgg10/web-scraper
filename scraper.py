from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v138.fed_cm import click_dialog_button
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time, requests

#Funciones
def entrar_wallapop():
    #print("Iniciando el navegador Chrome...")
    servicio = Service(ChromeDriverManager().install())

    opciones = Options()
    opciones.add_argument("--start-maximized")  # Inicia maximizado
    #opciones.add_argument("--headless") # Para ejecutarlo sin abrir ventana

    # Aquí es donde realmente se abre la ventana de Chrome
    driver = webdriver.Chrome(service=servicio, options=opciones)
    #print(f"Abriendo la URL: {"https://es.wallapop.com/"}")

    # El navegador va a la URL
    driver.get("https://es.wallapop.com/")

    #print("Esperando 5 segundos a que cargue la página...")
    time.sleep(5)

    # Obtenemos el HTML
    html = driver.page_source
    return driver

def aceptar_cookies_wallapop(driver):
    boton_aceptar = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    #print(boton_aceptar)
    boton_aceptar.click()

def filtro_wallapop(driver):
    boton_coche = driver.find_element(By.XPATH, "//div[@data-testid='desktop-category-navigation']//nav/a[1]")
    #print("coche=", boton_coche)
    boton_coche.click()
    time.sleep(3)
    ubi_cambiar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='sidebar-filter-layout_SidebarFilter__container__Kj4cV']//button[@class='location-sidebar-filter_LocationFilter__openButton__a8Fqv pt-3']")))
    #print("ubi=", ubi_cambiar)
    ubi_cambiar.click()
    time.sleep(3)

    lupa = driver.find_element(By.XPATH, "//walla-dialog/div/walla-search-input/div")
    lupa.click()
    texto = driver.find_element(By.XPATH, "//walla-dialog/div/walla-search-input/div/input")
    texto.send_keys("Madrid")
    time.sleep(3)

    seleccion = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//walla-dialog/div/div[1]/walla-list/walla-list-item[1]")))
    seleccion.click()
    time.sleep(2)

    aceptar = driver.find_element(By.XPATH, "//walla-dialog/div/div[3]/walla-button[2]")
    aceptar.click()
    time.sleep(3)

def buscar_wallapop_audi(driver):
    wait = WebDriverWait(driver, 10)
    audi = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='Audi']")))
    #print("audi=", audi)
    driver.execute_script("arguments[0].click();", audi)
    #print("audi clickado")
    time.sleep(5)
    
    # Modelos Audi
    lmodelos =['//*[@id="A1"]', '//*[@id="A3"]', '//*[@id="Q3"]', '//*[@id="Q5"]']
    #print(lmodelos)

    # Columnas Audi
    precios = []
    kilometros = []
    años = []
    potencias = []
    marcas = []
    modelos = []
    main_tab = driver.current_window_handle
    for i in range(4):
        lmodelo = driver.find_element(By.XPATH, lmodelos[i])
        driver.execute_script("arguments[0].click();", lmodelo)
        time.sleep(3)
        coches = ['//div/a[1]/div[2]/div/div/strong',
                  '//div/a[2]/div[2]/div/div/strong',
                  '//div/a[3]/div[2]/div/div/strong',
                  '//div/a[4]/div[2]/div/div/strong']
        time.sleep(3)
        # print(coches)
        for j in range(4):
            coche = driver.find_element(By.XPATH, coches[j])
            driver.execute_script("arguments[0].click();", coche)
            time.sleep(3)
            all_tabs = driver.window_handles
            driver.switch_to.window(all_tabs[-1])
            precio = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/aside/section[1]/div[2]/div[1]/div/div/span')
            precios.append(precio.text)
            #print(precio.text)
            kilometro = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[4]/span[2]')
            kilometros.append(kilometro.text + " km")
            #print(kilometro.text + " km")
            año = driver.find_element(By.XPATH,
                                      '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[3]/span[2]')
            años.append(año.text)
            #print(año.text)
            texto = driver.find_element(By.XPATH,
                                           '//div[walla-icon[@icon="piston"]]//span')
            potencia = texto.text.split(" ")[0]
            potencias.append(potencia + " cv")
            #print(potencia + " cv")
            marca = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[1]/a/span')
            marcas.append(marca.text)
            #print(marca.text)
            modelo = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/section/section/section[5]/div/div/div[2]/a/span')
            modelos.append(modelo.text)
            #print(modelo.text)
            # clave = j + 1 + 4 * i
            #print("coche numero", clave)
            driver.close()
            driver.switch_to.window(main_tab)
    return precios, kilometros, años, potencias, marcas, modelos

def buscar_wallapop_bmw(driver):
    wait = WebDriverWait(driver, 10)
    bmw = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='BMW']")))
    #print("bmw=", bmw)
    driver.execute_script("arguments[0].click();", bmw)
    #print("bmw clickado")
    time.sleep(5)

    # Modelos BMW
    lmodelos = ['//*[@id="Serie 8"]', '//*[@id="X1"]', '//*[@id="Serie 3"]', '//*[@id="i3"]']
    # print(lmodelos)

    # Columnas BMW
    precios = []
    kilometros = []
    años = []
    potencias = []
    marcas = []
    modelos = []
    main_tab = driver.current_window_handle
    for i in range(4):
        lmodelo = driver.find_element(By.XPATH, lmodelos[i])
        driver.execute_script("arguments[0].click();", lmodelo)
        time.sleep(3)
        coches = ['//div/a[1]/div[2]/div/div/strong',
                  '//div/a[2]/div[2]/div/div/strong',
                  '//div/a[3]/div[2]/div/div/strong',
                  '//div/a[4]/div[2]/div/div/strong']
        time.sleep(3)
        # print(coches)
        for j in range(4):
            coche = driver.find_element(By.XPATH, coches[j])
            driver.execute_script("arguments[0].click();", coche)
            time.sleep(3)
            all_tabs = driver.window_handles
            driver.switch_to.window(all_tabs[-1])
            precio = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/aside/section[1]/div[2]/div[1]/div/div/span')
            precios.append(precio.text)
            #print(precio.text)
            kilometro = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[4]/span[2]')
            kilometros.append(kilometro.text + " km")
            #print(kilometro.text + " km")
            año = driver.find_element(By.XPATH,
                                      '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[3]/span[2]')
            años.append(año.text)
            #print(año.text)
            texto = driver.find_element(By.XPATH, '//div[walla-icon[@icon="piston"]]//span')
            potencia = texto.text.split(" ")[0]
            potencias.append(potencia +  " cv")
            #print(potencia +  " cv")
            marca = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[1]/a/span')
            marcas.append(marca.text)
            #print(marca.text)
            modelo = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/section/section/section[5]/div/div/div[2]/a/span')
            modelos.append(modelo.text)
            #print(modelo.text)
            # clave = j + 1 + 4 * i
            #print("coche numero", clave)
            driver.close()
            driver.switch_to.window(main_tab)
    return precios, kilometros, años, potencias, marcas, modelos

def buscar_wallapop_porsche(driver):
    wait = WebDriverWait(driver, 10)
    porsche = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='Porsche']")))
    #print("porsche=", porsche)
    driver.execute_script("arguments[0].click();", porsche)
    #print("porsche clickado")
    time.sleep(5)

    # Modelos Porsche
    lmodelos = ['//*[@id="Macan"]', '//*[@id="Panamera"]', '//*[@id="Boxster"]', '//*[@id="Cayenne"]']
    # print(lmodelos)

    # Columnas Porsche
    precios = []
    kilometros = []
    años = []
    potencias = []
    marcas = []
    modelos = []
    main_tab = driver.current_window_handle
    for i in range(4):
        lmodelo = driver.find_element(By.XPATH, lmodelos[i])
        driver.execute_script("arguments[0].click();", lmodelo)
        time.sleep(3)
        coches = ['//div/a[1]/div[2]/div/div/strong',
                  '//div/a[2]/div[2]/div/div/strong',
                  '//div/a[3]/div[2]/div/div/strong',
                  '//div/a[4]/div[2]/div/div/strong']
        time.sleep(3)
        #print(coches)
        for j in range(4):
            coche = driver.find_element(By.XPATH, coches[j])
            driver.execute_script("arguments[0].click();", coche)
            time.sleep(3)
            all_tabs = driver.window_handles
            driver.switch_to.window(all_tabs[-1])
            precio = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/aside/section[1]/div[2]/div[1]/div/div/span')
            precios.append(precio.text)
            #print(precio.text)
            kilometro = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[4]/span[2]')
            kilometros.append(kilometro.text + " km")
            #print(kilometro.text + " km")
            año = driver.find_element(By.XPATH,
                                      '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[3]/span[2]')
            años.append(año.text)
            #print(año.text)
            texto = driver.find_element(By.XPATH,
                                           '//div[walla-icon[@icon="piston"]]//span')
            potencia = texto.text.split(" ")[0]
            potencias.append(potencia + " cv")
            #print(potencia + " cv")
            marca = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/main/div/div[2]/div[2]/div/section/section/section[5]/div/div/div[1]/a/span')
            marcas.append(marca.text)
            #print(marca.text)
            modelo = driver.find_element(By.XPATH,
                                         '//*[@id="__next"]/main/div/div[2]/div[2]/div[1]/section/section/section[5]/div/div/div[2]/a/span')
            modelos.append(modelo.text)
            #print(modelo.text)
            # clave = j + 1 + 4 * i
            #print("coche numero", clave)
            driver.close()
            driver.switch_to.window(main_tab)
    return precios, kilometros, años, potencias, marcas, modelos

def aceptar_cookies_auto(driver):
    time.sleep(3)
    try:
        boton_cookies = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="didomi-notice-agree-button"]')))
        # Si llega aquí, es porque lo encontró: haz clic
        boton_cookies.click()
        #print("Banner de cookies encontrado y aceptado.")
    except TimeoutException:
        pass

def buscar_auto_audi(driver):
    driver.get("https://www.autocasion.com")
    aceptar_cookies_auto(driver)
    time.sleep(2)
    desplegable = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/p')))
    desplegable.click()
    time.sleep(1)
    audi = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[7]')))
    #print("audi=", audi)
    driver.execute_script("arguments[0].click();", audi)
    #print("audi clickado")
    time.sleep(1)
    boton_continuar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/button')))
    boton_continuar.click()
    time.sleep(2)

    # Modelos Audi
    desplegable2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="filter2"]/p')))
    desplegable2.click()
    lmodelos =['//*[@id="family-list"]/li[3]/label/a','//*[@id="family-list"]/li[7]/label/a',
               '//*[@id="family-list"]/li[22]/label/a', '//*[@id="family-list"]/li[25]/label/a']
    desplegable2.click()
    # Columnas Audi
    precios = []
    kilometros = []
    años = []
    potencias = []
    marcas = []
    modelos = []
    for i in range(4):
        desplegable2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filter2"]/p')))
        desplegable2.click()
        time.sleep(1)
        mod = driver.find_element(By.XPATH, lmodelos[i])
        driver.execute_script("arguments[0].click();", mod)
        time.sleep(3)
        coches = ['//*[@id="results-html"]/article[1]/a/div[2]', '//*[@id="results-html"]/article[2]/a/div[2]',
                  '//*[@id="results-html"]/article[3]/a/div[2]', '//*[@id="results-html"]/article[4]/a/div[2]']
        time.sleep(3)
        for j in range(4):
            coche = driver.find_element(By.XPATH, coches[j])
            driver.execute_script("arguments[0].click();", coche)
            time.sleep(3)
            texto = driver.find_element(By.XPATH, "/ html / body / div[3] / section[1] / div[2] // div[@class = 'precio']")                       #   '/html/body/div[3]/section[1]/div[2]/div[@class = "precio"]')
            precio = texto.text.split("\n")[-1]
            precios.append(precio)
            #print(precio)
            kilometro = driver.find_element(By.XPATH,
                                            '/html/body/div[3]/section[1]/div[6]/ul/li[2]')
            kilometros.append(kilometro.text)
            #print(kilometro.text)
            texto = driver.find_element(By.XPATH,
                                      '/html/body/div[3]/section[1]/div[6]/ul/li[1]')
            año = texto.text.split("/")[-1]
            años.append(año)
            #print(año)
            potencia = driver.find_element(By.XPATH,
                                           "//li[span[contains(@class, 'icon icon-motor')]]")
            potencias.append(potencia.text)
            #print(potencia.text)
            marca_modelo = driver.find_element(By.XPATH,
                                        '/html/body/div[3]/section[1]/div[6]/h2')
            texto = marca_modelo.text.split(" ")
            marca = texto[1]
            marcas.append(marca)
            #print(marca)
            modelo = texto[2]
            modelos.append(modelo)
            #print(modelo)
            # clave = j + 1 + 4 * i
            #print("coche numero", clave)
            driver.back()
            time.sleep(4)
    return precios, kilometros, años, potencias, marcas, modelos

def buscar_auto_bmw(driver):
    driver.get("https://www.autocasion.com")
    aceptar_cookies_auto(driver)
    time.sleep(2)
    desplegable = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/p')))
    desplegable.click()
    time.sleep(1)
    bmw = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[11]')))
    #print("bmw=", bmw)
    driver.execute_script("arguments[0].click();", bmw)
    #print("bmw clickado")
    time.sleep(1)
    boton_continuar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/button')))
    boton_continuar.click()
    time.sleep(2)

    # Modelos Bmw
    desplegable2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="filter2"]/p')))
    desplegable2.click()
    lmodelos =['//*[@id="family-list"]/li[36]/label/a', '//*[@id="family-list"]/li[38]/label/a',
               '//*[@id="family-list"]/li[31]/label/a', '//*[@id="family-list"]/li[13]/label/a']
    desplegable2.click()
    # Columnas Bmw
    precios = []
    kilometros = []
    años = []
    potencias = []
    marcas = []
    modelos = []
    for i in range(4):
        desplegable2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filter2"]/p')))
        desplegable2.click()
        time.sleep(1)
        mod = driver.find_element(By.XPATH, lmodelos[i])
        driver.execute_script("arguments[0].click();", mod)
        time.sleep(3)
        coches = ['//*[@id="results-html"]/article[1]/a/div[2]', '//*[@id="results-html"]/article[2]/a/div[2]',
                  '//*[@id="results-html"]/article[3]/a/div[2]', '//*[@id="results-html"]/article[4]/a/div[2]']
        time.sleep(3)
        for j in range(4):
            coche = driver.find_element(By.XPATH, coches[j])
            driver.execute_script("arguments[0].click();", coche)
            time.sleep(3)
            texto = driver.find_element(By.XPATH, "/ html / body / div[3] / section[1] / div[2] // div[@class = 'precio']")                       #   '/html/body/div[3]/section[1]/div[2]/div[@class = "precio"]')
            precio = texto.text.split("\n")[-1]
            precios.append(precio)
            #print(precio)
            kilometro = driver.find_element(By.XPATH,
                                            '/html/body/div[3]/section[1]/div[6]/ul/li[2]')
            kilometros.append(kilometro.text)
            #print(kilometro.text)
            texto = driver.find_element(By.XPATH,
                                      '/html/body/div[3]/section[1]/div[6]/ul/li[1]')
            año = texto.text.split("/")[-1]
            años.append(año)
            #print(año)
            potencia = driver.find_element(By.XPATH,
                                           "//li[span[contains(@class, 'icon icon-motor')]]")
            if "-" in potencia.text:
                potencia = "0 cv"
                potencias.append(potencia)
                #print(potencia)
            else:
                potencias.append(potencia.text)
                #print(potencia.text)
            marca_modelo = driver.find_element(By.XPATH,
                                        '/html/body/div[3]/section[1]/div[6]/h2')
            texto = marca_modelo.text.split(" ")
            marca = texto[1]
            marcas.append(marca)
            #print(marca)
            if i == 0 or i == 2:
                modelo = texto[2] + " " + texto[3]
            else:
                modelo = texto[2]
            modelos.append(modelo)
            #print(modelo)
            # clave = j + 1 + 4 * i
            #print("coche numero", clave)
            driver.back()
            time.sleep(4)
    return precios, kilometros, años, potencias, marcas, modelos

def buscar_auto_porsche(driver):
    driver.get("https://www.autocasion.com")
    aceptar_cookies_auto(driver)
    time.sleep(2)
    desplegable = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/p')))
    desplegable.click()
    time.sleep(1)
    porsche = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/div[1]/div/ul/li[88]')))
    #print("porsche=", porsche)
    driver.execute_script("arguments[0].click();", porsche)
    #print("porsche clickado")
    time.sleep(1)
    boton_continuar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div[1]/button')))
    boton_continuar.click()
    time.sleep(2)

    # Modelos porsche
    desplegable2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="filter2"]/p')))
    desplegable2.click()
    lmodelos =['//*[@id="family-list"]/li[18]/label/a', '//*[@id="family-list"]/li[19]/label/a',
               '//*[@id="family-list"]/li[13]/label/a', '//*[@id="family-list"]/li[15]/label/a']
    desplegable2.click()
    # Columnas porsche
    precios = []
    kilometros = []
    años = []
    potencias = []
    marcas = []
    modelos = []
    for i in range(4):
        desplegable2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="filter2"]/p')))
        desplegable2.click()
        time.sleep(1)
        mod = driver.find_element(By.XPATH, lmodelos[i])
        driver.execute_script("arguments[0].click();", mod)
        time.sleep(3)
        coches = ['//*[@id="results-html"]/article[1]/a/div[2]', '//*[@id="results-html"]/article[2]/a/div[2]',
                  '//*[@id="results-html"]/article[3]/a/div[2]', '//*[@id="results-html"]/article[4]/a/div[2]']
        time.sleep(3)
        for j in range(4):
            coche = driver.find_element(By.XPATH, coches[j])
            driver.execute_script("arguments[0].click();", coche)
            time.sleep(3)
            texto = driver.find_element(By.XPATH, "/ html / body / div[3] / section[1] / div[2] // div[@class = 'precio']")
            #   '/html/body/div[3]/section[1]/div[2]/div[@class = "precio"]')
            precio = texto.text.split("\n")[-1]
            precios.append(precio)
            #print(precio)
            kilometro = driver.find_element(By.XPATH,
                                            '/html/body/div[3]/section[1]/div[6]/ul/li[2]')
            kilometros.append(kilometro.text)
            #print(kilometro.text)
            texto = driver.find_element(By.XPATH,
                                      '/html/body/div[3]/section[1]/div[6]/ul/li[1]')
            año = texto.text.split("/")[-1]
            años.append(año)
            #print(año)
            potencia = driver.find_element(By.XPATH,
                                           "//li[span[contains(@class, 'icon icon-motor')]]")
            potencias.append(potencia.text)
            #print(potencia.text)
            marca_modelo = driver.find_element(By.XPATH,
                                        '/html/body/div[3]/section[1]/div[6]/h2')
            texto = marca_modelo.text.split(" ")
            marca = texto[1]
            marcas.append(marca)
            #print(marca)
            modelo = texto[2]
            modelos.append(modelo)
            #print(modelo)
            # clave = j + 1 + 4 * i
            #print("coche numero", clave)
            driver.back()
            time.sleep(4)
    return precios, kilometros, años, potencias, marcas, modelos

# Obtener los datos
driver=entrar_wallapop()
aceptar_cookies_wallapop(driver)
filtro_wallapop(driver)
wpreciosaudi, wkilometrosaudi, wañosaudi, wpotenciasaudi, wmarcasaudi, wmodelosaudi = buscar_wallapop_audi(driver)
wpreciosbmw, wkilometrosbmw, wañosbmw, wpotenciasbmw, wmarcasbmw, wmodelosbmw = buscar_wallapop_bmw(driver)
wpreciosporsche, wkilometrosporsche, wañosporsche, wpotenciasporsche, wmarcasporsche, wmodelosporsche = buscar_wallapop_porsche(driver)
apreciosaudi, akilometrosaudi, aañosaudi, apotenciasaudi, amarcasaudi, amodelosaudi = buscar_auto_audi(driver)
apreciosbmw, akilometrosbmw, aañosbmw, apotenciasbmw, amarcasbmw, amodelosbmw = buscar_auto_bmw(driver)
apreciosporsche, akilometrosporsche, aañosporsche, apotenciasporsche, amarcasporsche, amodelosporsche = buscar_auto_porsche(driver)

#CSV
import csv
def escribir_csv_desde_lista_mod(nombre_archivo, lista):
    with open(nombre_archivo, "w", newline="\n", encoding="utf-8-sig") as csvfile:
        csvtool = csv.writer(csvfile, delimiter=";")
        for elem in lista:
            csvtool.writerow(elem)
    #print(f"Se escribieron los datos en el archivo '{nombre_archivo}' desde una lista.")

def generar_csv_coche(filename, marcas, modelos, precios, kms, anios, potencias):
    """
    Función genérica que crea la lista de datos y llama a la función de escritura.
    """
    #print(f"Generando archivo {filename}...")
    header = [["Marca", "Modelo", "Precio", "Kilometros", "Año", "Potencia"]]
    datos_combinados = list(zip(marcas, modelos, precios, kms, anios, potencias))
    datos_finales = header + datos_combinados
    escribir_csv_desde_lista_mod(filename, datos_finales)
    #print(f"Archivo {filename} generado correctamente.")

generar_csv_coche("Wallapop_audi.csv", wmarcasaudi, wmodelosaudi, wpreciosaudi, wkilometrosaudi, wañosaudi, wpotenciasaudi)
generar_csv_coche("Wallapop_bmw.csv", wmarcasbmw, wmodelosbmw, wpreciosbmw, wkilometrosbmw, wañosbmw, wpotenciasbmw)
generar_csv_coche("Wallapop_porsche.csv", wmarcasporsche, wmodelosporsche, wpreciosporsche, wkilometrosporsche, wañosporsche, wpotenciasporsche)
generar_csv_coche("Autocasion_audi.csv", amarcasaudi, amodelosaudi, apreciosaudi, akilometrosaudi, aañosaudi, apotenciasaudi)
generar_csv_coche("Autocasion_bmw.csv", amarcasbmw, amodelosbmw, apreciosbmw, akilometrosbmw, aañosbmw, apotenciasbmw)
generar_csv_coche("Autocasion_porsche.csv", amarcasporsche, amodelosporsche, apreciosporsche, akilometrosporsche, aañosporsche, apotenciasporsche)
