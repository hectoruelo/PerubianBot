import \
    logging  # Permite hacer seguimiento de eventos en tu aplicación, facilitando la depuración y el diagnóstico de problemas.
from selenium import webdriver  # Proporciona herramientas para automatizar la interacción con navegadores web.
from selenium.webdriver.firefox.firefox_binary import \
    FirefoxBinary  # Permite especificar la ubicación del binario de Firefox para Selenium.
from datetime import datetime  # Proporciona funciones para trabajar con fechas y horas.
import \
    warnings  # Ofrece una forma de advertir al desarrollador sobre situaciones que no son necesariamente excepciones.
import requests  # Permite enviar solicitudes HTTP/1.1 de manera fácil.
import json  # Facilita la codificación y decodificación de datos en formato JSON.
import colorama  # Hace posible que la salida de la terminal contenga colores en diferentes plataformas.
from colorama import Fore, \
    Style  # Fore permite cambiar el color del texto, y Style ajusta el estilo del texto (como negrita).
from consolemenu import *  # Proporciona funcionalidades para crear menús de consola interactivos.
from consolemenu.items import *  # Incluye elementos específicos que se pueden agregar a los menús de consola, como FuncItem para funciones.
import \
    signal  # Proporciona herramientas para manejar señales de UNIX, permitiendo la interacción con el sistema operativo.
import sys  # Ofrece acceso a algunas variables y funciones que interactúan con el intérprete de Python.

warnings.filterwarnings("ignore",
                        category=DeprecationWarning)  # Configura los avisos para ignorar los avisos de obsolescencia.
import time  # Ofrece funciones para trabajar con el tiempo, como esperas.
import \
    os  # Proporciona una forma de usar funcionalidades dependientes del sistema operativo, como manejar archivos y directorios.
from os import system  # Permite ejecutar comandos del sistema desde Python.
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import selenium

print(selenium.__version__)

version = '1'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
global debug
debug = 1
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
start = '10:40:00'
end = '22:00:00'

# VARIABLES
global perubian
perubian = Fore.MAGENTA + Style.BRIGHT + r"""
""" + Style.RESET_ALL
menu = ConsoleMenu(Fore.YELLOW + perubian, "Seleccione un modo" + Style.RESET_ALL)


# Verificar conexion con Tor
def verificar_conexion_tor():
    try:
        # Hacer una petición a la API para obtener la dirección IP actual

        response = requests.get('https://api.ipify.org',
                                proxies=dict(http='socks5://127.0.0.1:9050', https='socks5://127.0.0.1:9050'))
        ip_actual = response.text
        print(Fore.GREEN + "IP actual a través de Tor: " + ip_actual + Style.RESET_ALL)
        # Aquí puedes añadir una comprobación adicional para asegurarte de que la IP es una de Tor
        # Por simplicidad, asumimos que cualquier respuesta exitosa implica que Tor está configurado correctamente
        return True
    except Exception as e:
        print(Fore.RED + "Error al verificar la conexión con Tor: " + str(e) + Style.RESET_ALL)
        return False


# Firefox Configuration
def firefoxsetup():
    global binary, profile, PATH_TO_DEV_NULL
    global options
    options = Options()

    if os.name == 'nt':  # Windows
        binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        PATH_TO_DEV_NULL = 'nul'
        path_to_geckodriver = 'C:\\Users\\Hector\\Desktop\\scripts\\PerubianBot\\geckodriver.exe'
        path_to_log = 'C:\\Users\\Hector\\Desktop\\scripts\\PerubianBot\\geckodriver.log'
        tor = 0
    elif os.uname().sysname == 'Darwin':  # macOS
        binary = '/Applications/Firefox.app/Contents/MacOS/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    else:
        binary = '/usr/bin/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
        path_to_geckodriver = '/usr/bin/geckodriver'
        path_to_log = '/tmp/geckodriver.log'
        options.add_argument("--headless")  # Ejecutar Firefox en modo headless (LINUX)
        tor = 1

    options.accept_insecure_certs = True  # Aceptar certificados inseguros directamente en las Options
    options.binary_location = binary
    # Configurar preferencias directamente en las Options
    # options.set_preference("media.autoplay.default", 0)
    # options.set_preference("media.volume_scale", "0.0")
    # options.set_preference("permissions.default.image", 2)  # Desactivar la carga de imágenes
    options.set_preference("dom.popup_maximum", 0)  # Bloquear los pop-ups
    # options.set_preference("datareporting.healthreport.uploadEnabled", False)  # Desactivar la telemetría
    # options.set_preference("datareporting.policy.dataSubmissionEnabled", False)  # Desactivar la telemetría
    # options.set_preference("dom.webnotifications.enabled", False)  # Desactivar las notificaciones

    if tor == 1:
        # Configuración del proxy SOCKS para usar con Tor
        options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
        options.set_preference("network.proxy.socks", "127.0.0.1")  # Dirección IP del proxy SOCKS (Tor por defecto)
        options.set_preference("network.proxy.socks_port", 9050)  # Puerto del proxy SOCKS (Tor por defecto)
        options.set_preference("network.proxy.socks_version", 5)  # Versión del proxy SOCKS (Tor utiliza la versión 5)
        options.set_preference("network.proxy.socks_remote_dns", True)  # DNS queries a través de Tor

        verificar_conexion_tor()

    global service
    service = Service(executable_path=path_to_geckodriver, service_log_path=path_to_log)
    global browser
    browser = webdriver.Firefox(service=service, options=options)


# Formulario
def formulario():
    global email, number, name, surname
    if debug == 1:
        logging.debug("Modo debug activado.")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        number, name, surname, email = '868030340', 'Mario', 'Roman', 'uhieor43@gmail.com'
    else:
        logging.disable(logging.CRITICAL + 1)
        number = print('Nº de Teléfono: ')
        name = print('Nombre de la persona: ')
        surname = print('Apellido: ')
        email = print('email : ')
        if not email:
            email = 'pepi@gmail.com'


interrupted = False


def handle_interrupt(browser):
    global interrupted
    interrupted = True
    browser.quit()
    print("Navegador cerrado. Volviendo al menú principal...")


# Funciones de Scraping
def SECURITAS_DIRECT(browser, number):
    if interrupted:
        return "0"
    try:
        print(Fore.YELLOW + "SECURITAS DIRECT" + Style.RESET_ALL)

        browser.get('https://www.securitasdirect.es/')
        # browser.find_element(By.XPATH,'//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').clickk() #Cookies
        element = browser.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
        element.click()

        # Para enviar un número al campo de teléfono
        element_telefono = browser.find_element(By.XPATH, '//*[@id="edit-telefono1"]')
        element_telefono.send_keys(number)

        # Para hacer click en el botón de enviar
        element_submit = browser.find_element(By.XPATH, '//*[@id="edit-submit"]')
        element_submit.click()

        if (browser.current_url == 'https://www.securitasdirect.es/error-envio'):
            print(Fore.RED + "Securitas Direct: Error " + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Securitas Direct: OK'" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Securitas Direct: Skipeado (Limite Excedido)" + str(e) + Style.RESET_ALL)


def VODAFONE(browser, name, surname, number, email):
    print(Fore.YELLOW + "VODAFONE" + Style.RESET_ALL)

    if interrupted:
        return "0"
    try:
        browser.get('https://www.vodafone.es/c/empresas/pymes/es/conectividad/red-infinity/')
        time.sleep(3)

        element = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        element.click()

        time.sleep(2)

        element = browser.find_element(By.XPATH, '//*[@id="RedInfinity-smart"]/section[1]/div/div/button')
        actions = ActionChains(browser)
        actions.move_to_element(element).click().perform()

        time.sleep(2)
        element = browser.find_element(By.XPATH, '//*[@id="facade-phoneNumber"]')
        element.send_keys(number)

        element = browser.find_element(By.XPATH, '//*[@id="facade-firstName"]')
        element.send_keys(name)

        element = browser.find_element(By.XPATH, '//*[@id="facade-lastName"]')
        element.send_keys(surname)

        element = browser.find_element(By.XPATH, '//*[@id="facade-email"]')
        element.send_keys(email)

        element = browser.find_element(By.XPATH, '//*[@id="facade-entreprise"]')
        element.send_keys(email)

        # ESTO NO HACE NI CASO

        boton_clausula = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Cláusula de protección de datos')]"))
        )
        boton_clausula = browser.find_element(By.XPATH, "//a[contains(text(), 'Cláusula de protección de datos')]")
        browser.execute_script("arguments[0].click();", boton_clausula)

        browser.find_element(By.XPATH,
                             '/html/body/div[2]/main/div[4]/div/div/span/div/div/div/div/div[4]/section/div[1]/button').click()

        browser.find_element(By.XPATH,
                             '/html/body/div[2]/main/div[4]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[10]/button').click()

        time.sleep(50)

        browser.find_element(By.XPATH,
                             '/html/body/div[2]/main/div[4]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[9]/div[2]/label').click()

        browser.find_element(By.XPATH,
                             '/html/body/div[2]/main/div[4]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[9]/div[2]/label').click()

        time.sleep(10)
        element = browser.find_element(By.XPATH, '//*[@id="X-modal-form"]/div[2]/form[1]/div/div[10]/button')
        # element.click

        print(Fore.GREEN + "Vodafone: OK'" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Vodafone: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def EUROINNOVA(browser, name, surname, number, email):
    print(Fore.YELLOW + "EUROINNOVA" + Style.RESET_ALL)
    if interrupted:
        return 1
    try:
        element = browser.get('https://www.euroinnova.edu.es/cursos#formulario')
        time.sleep(3)
        element = browser.find_element(By.XPATH, '//*[@id="accept-cookies"]')
        element.click()
        time.sleep(2)
        element = browser.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/button')
        element.click()
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="name"]').send_keys(name)
        browser.find_element(By.XPATH, '//*[@id="mail"]').send_keys(email)
        browser.find_element(By.XPATH, '//*[@id="tel"]').send_keys(number)
        time.sleep(1)
        element = browser.find_element(By.XPATH, '//*[@id="privacidad"]')
        element.click()
        time.sleep(1)
        element = browser.find_element(By.XPATH, '//*[@id="btn_enviar"]')
        element.click()
        time.sleep(3)
        print(Fore.GREEN + "Euroinnova: OK" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + "Euroinnova : Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def GENESIS(browser, name, number):
    print(Fore.YELLOW + "GENESIS" + Style.RESET_ALL)
    try:
        if current_time > start and current_time < end:
            element = browser.get('https://www.genesis.es/modal/c2c')
            time.sleep(3)
            try:
                element = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
                element.click()
            except:
                pass
            time.sleep(1)
            element = browser.find_element(By.XPATH,
                                           '/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/div/form/section/div/div[2]/div/select/option[3]')
            element.click()
            element = browser.find_element(By.XPATH, '//*[@id="edit-por-quien-preguntamos-"]')
            element.send_keys(name)
            element = browser.find_element(By.XPATH, '//*[@id="edit-phone"]')
            element.send_keys(number)
            element = browser.find_element(By.XPATH, '//*[@id="edit-phone-confirmation"]')
            element.send_keys(number)
            element = browser.find_element(By.XPATH, '//*[@id="edit-actions-submit"]')
            element.click()
            time.sleep(1)
            print(Fore.GREEN + "Genesis: OK'" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Genesis: Skipeado (Fuera de Horario)" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Genesis: (ERROR)" + str(e) + Style.RESET_ALL)


def RACCTEL(browser, number):
    print(Fore.YELLOW + "RACCTEL" + Style.RESET_ALL)
    try:
        url = "https://eshop.prod.k8s.masmovil.com/catalog/api/c2c/racctel"
        payload = {
            "NumeroTelefonoCliente": number,
            "Ambito": 4,
            "EsCliente": 0,
            "TipoCliente": -1,
            "Idioma": 3,
            "Medio": "",
            "Ruta": "https:"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'x-brand': 'RACCTEL',
            'x-locale': 'es-ES',
            'Cache-Control': 'public, s-maxage=180, stale-while-revalidate=60',
            'Origin': 'https://www.racctelplus.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.racctelplus.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'TE': 'trailers'}
        requests.post(url, headers=headers, json=payload)
        print(Fore.GREEN + "Racctel+: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Racctel+: (ERROR)" + str(e) + Style.RESET_ALL)


def JAZZTEL(broser, number):
    print(Fore.YELLOW + "JAZZTEL" + Style.RESET_ALL)
    try:
        browser.get(
            'https://llamamegratis.es/jazztel/v2/webphone.html?lang=es-ES&isLandingLander=1&typeOrigin=wphFollow&widget=3294&wphUrl#https://www.telefonojazztel.es/')
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="phoneNumber"]').send_keys(number)
        time.sleep(1)
        browser.find_element(By.XPATH,'//*[@id="env"]').click()
        time.sleep(3)
        print(Fore.GREEN + "Jazztel: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Jazztel: (ERROR)" + str(e) + Style.RESET_ALL)


# FALTA EUSCASTEL QUE PA LUEGO
def ITEP(browser, email, number):
    print(Fore.YELLOW + "ITEP" + Style.RESET_ALL)
    try:
        browser.get('https://www.itep.es/')
        time.sleep(3)
        try:
            element = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/button[1]')
            element.click()  # Cookies
            time.sleep(1)
        except:
            pass
        element = browser.find_element(By.XPATH, '/html/body/header/div/div[5]/div/p/button')
        element.click()  # Solicitar Informacion
        time.sleep(1)
        element = browser.find_element(By.XPATH, '//*[@id="edit-email--2"]')
        element.send_keys(email)
        element = browser.find_element(By.XPATH, '//*[@id="edit-phone--2"]')
        element.send_keys(number)
        element = browser.find_element(By.XPATH, '//*[@id="edit-cp--2"]')
        element.send_keys("08002")
        element = browser.find_element(By.XPATH,
                                       '/html/body/div[4]/div/div[2]/div/div/form/div[4]/select/optgroup[1]/option[2]')
        element.click()
        elemento_select = browser.find_element(By.ID, 'edit-city--_0PgxR5lD9s')
        # Crea una instancia de Select utilizando el elemento encontrado
        select = Select(elemento_select)
        # Selecciona la opción "Sevilla" por su valor
        select.select_by_value('1730')

        element = browser.find_element(By.XPATH, '//*[@id="edit-city--2"]/option[3]')
        time.sleep(5)
        element.click()
        time.sleep(30)

        element = browser.find_element(By.XPATH, '//*[@id="lead-form-header-web-solicita-info-general-2"]/div[5]')
        element.click()

        print(Fore.GREEN + "ITEP: OK" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "ITEP: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def PROSEGUR(browser, number):  # HAY QUE REVISARLO
    print(Fore.YELLOW + "PROSEGUR" + Style.RESET_ALL)
    try:
        browser.get('https://www.prosegur.es/esp/alarmahogar/sem')
        time.sleep(3)
        element = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/button')
        element.click()
        time.sleep(3)
        element = browser.find_element(By.XPATH, '//*[@id="form-hero"]/div[2]/div[2]/div/input')
        element.send_keys(number)
        element = browser.find_element(By.XPATH, '//*[@id="form-hero"]/div[2]/div[3]/div/fieldset/label/p/span')
        element.click()
        element = browser.find_element(By.XPATH,
                                       '/html/body/section[1]/div/div/div/div[2]/section[2]/div/div/div/div/div[4]/div/div/div/button/span')
        element.click()
        time.sleep(3)
        print(Fore.GREEN + "Prosegur : OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Prosegur (ERROR):" + str(e) + Style.RESET_ALL)


def LINEADIRECTA(browser, number):
    print(Fore.YELLOW + "LINEA DIRECTA" + Style.RESET_ALL)
    try:
        browser.get(
            'https://www.lineadirecta.com/te-llamamos-gratis.html?idServicio=http0036&from=B009975&indVehiculo=C')
        time.sleep(3)
        try:
            element = browser.find_element(By.XPATH, '//button[@id="didomi-notice-agree-button"]')
            element.click()
        except:
            pass
        element = browser.find_element(By.XPATH, '/html/body/div/div/section/div[2]/div[2]/div/form/div[3]/div/input')
        element.send_keys(number)
        time.sleep(2)
        try:
            element = browser.find_element(By.XPATH, '/html/body/div/div/section/div[2]/div[2]/div/form/div[5]/a')
            element.click() # Buttom 1
        except:
            element = browser.find_element(By.XPATH, '/html/body/div[3]/section/section/form/div[2]/div/div[2]/a')
            element.click() # Buttom 2
        time.sleep(3)
        print(Fore.GREEN + "Linea Directa: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Linea Directa: (ERROR)" + str(e) + Style.RESET_ALL)


def TELECABLE(browser, name, surname, number):
    print(Fore.YELLOW + "TELECABLE" + Style.RESET_ALL)
    try:
        browser.get('http://marcador-c2c.alisys.net/telecablec2c_v2/c2c.php')
        time.sleep(3)
        selection = browser.find_element(By.XPATH, '//*[@id="numero"]')
        selection.send_keys(number)
        selection = browser.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/button')
        selection.click()
        time.sleep(3)
        print(Fore.GREEN + "Telecable: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Telecable: (ERROR)" + str(e) + Style.RESET_ALL)


def MAPFRE(browster, name, surname, number):
    print(Fore.YELLOW + "MAPFRE" + Style.RESET_ALL)
    try:
        browser.get('https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos')
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        selection.click()
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '//*[@id="nombre"]')
        selection.send_keys(name)
        selection = browser.find_element(By.XPATH, '//*[@id="primer_apellido"]')
        selection.send_keys(surname)
        selection = browser.find_element(By.XPATH, '//*[@id="codigo_postal"]')
        selection.send_keys("08002")
        selection = browser.find_element(By.XPATH, '//*[@id="tlfn"]')
        selection.send_keys(number)
        selection = browser.find_element(By.XPATH, '//*[@id="politicaprivacidad"]')
        selection.click()
        selection = browser.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input')
        selection.click()
        time.sleep(3)
        print(Fore.GREEN + "Mapfre: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Mapfre: (ERROR)" + str(e) + Style.RESET_ALL)


def ORANGE(browser, number):  # HAY QUE REVISARLO
    print(Fore.YELLOW + "ORANGE" + Style.RESET_ALL)
    try:
        browser.get('https://selectra.es/internet-telefono/companias/orange/telefono')
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/button[1]')
        selection.click()  # Cookies
        time.sleep(1)
        selection = browser.find_element(By.XPATH, '//*[@id="block-0lateralorangetelefono-area"]/div/div/div[1]/a[2]')
        selection.click()  # Cookies
        time.sleep(1)
        selection = browser.find_element(By.XPATH, '//*[@id="callback-modal__phone"]')
        selection.send_keys(number)
        time.sleep(1)
        selection = browser.find_element(By.XPATH,
                                         '//*[@id="block-groupeth-system-main"]/section/div[3]/form/div[3]/label/span[1]')
        selection.click()
        selection = browser.find_element(By.XPATH, '//*[@id="callback-modal__submit"]')
        selection.click()
        time.sleep(3)
        print(Fore.GREEN + "Orange: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Orange: (ERROR)" + str(e) + Style.RESET_ALL)


def SELECTRA(browser, number):
    print(Fore.YELLOW + "SELECTRA" + Style.RESET_ALL)
    try:
        browser.get('https://ww.selectra.es/contact-internet')
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[1]/input')
        selection.send_keys(number)
        selection = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/form/label/span[1]')
        selection.click()
        selection = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/form/input[3]')
        selection.click()
        time.sleep(3)
        print(Fore.GREEN + "Selectra: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except:
        print(Fore.RED + "Selectra: (ERROR)" + Style.RESET_ALL)


def IBERDROLA(browser, number):
    print(Fore.YELLOW + "IBERDROLA" + Style.RESET_ALL)
    try:
        browser.get('https://www.iberdrola.es/')
        time.sleep(4)
        selection = browser.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
        selection.click()  # Cookies
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '//*[@id="telf-lc-header"]')
        selection.send_keys(number)
        selection = browser.find_element(By.XPATH, '//*[@id="cmb-form-header"]/div[2]/label/p')
        selection.click()
        selection = browser.find_element(By.XPATH, '//*[@id="btn-click-to-call-luz"]/span')
        selection.click()
        time.sleep(3)
        print(Fore.GREEN + "Iberdrola: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Iberdrola: (ERROR)" + str(e) + Style.RESET_ALL)


def PROYECTOSYSEGUROS(browser, name, number):
    print(Fore.YELLOW + "PROYECTOS Y SEGUROS" + Style.RESET_ALL)
    try:
        browser.get('https://www.proyectosyseguros.com/te-llamamos/')
        time.sleep(3)
        browser.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
        browser.find_element(By.XPATH,
                             '/html/body/div[4]/div/div/div/div/form/div[3]/div[2]/select/optgroup[1]/option[7]').click()
        browser.find_element(By.XPATH, '//*[@id="llamada-nombre"]').send_keys(name)
        browser.find_element(By.XPATH, '//*[@id="llamada-telefono"]').send_keys(number)
        browser.find_element(By.XPATH, '//*[@id="llamada-lopd"]').click()
        selection = browser.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input')
        browser.find_element(By.XPATH, '//*[@id="llamada-enviar"]').click()
        time.sleep(3)
        print(Fore.GREEN + "Proyectos y Seguros: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Proyectos y Seguros: (ERROR)" + str(e) + Style.RESET_ALL)


def UROLOGIACLINICABILBAO(browser, name, surname, number):
    print(Fore.YELLOW + "UROLOGIA BILBAO" + Style.RESET_ALL)
    try:
        browser.get('https://www.urologiaclinicabilbao.com/te-llamamos.php')
        time.sleep(2)
        browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div/div[1]/button[1]/span').click()
        time.sleep(1)
        browser.find_element(By.XPATH,
                             '/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[1]/input').send_keys(
            number)
        browser.find_element(By.XPATH,
                             '/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[2]/input').send_keys(
            surname)
        browser.find_element(By.XPATH,
                             '/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[3]/input').send_keys(
            name)
        selection = browser.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input')
        browser.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[2]/input').click()
        time.sleep(3)
        print(Fore.GREEN + "urologiaclinicaBilbao: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "urologiaclinicaBilbao: (ERROR)" + str(e) + Style.RESET_ALL)


def EMAGISTER(broser, number):
    print(Fore.YELLOW + "EMAGISTER" + Style.RESET_ALL)
    try:
        browser.get('https://www.emagister.com/')
        time.sleep(2)
        browser.find_element(By.XPATH,
                             '/html/body/header/div[2]/div/div[3]/div/nav/div[1]/div/div/section[2]/button').click()
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="callMe-phone"]').send_keys(number)
        browser.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/p/label/span[2]').click()
        selection = browser.find_element(By.XPATH,'/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input')
        browser.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/button').click()
        time.sleep(3)
        print(Fore.GREEN + "emagister: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "emagister: (ERROR)" + str(e) + Style.RESET_ALL)


def MFOLLARANAORTODONCIA(browser, name, number, email):
    print(Fore.YELLOW + "MFOLLARANAORTODONCIA" + Style.RESET_ALL)

    try:
        browser.get('https://www.mfollanaortodoncia.com/contactar/')
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/button[2]')
        selection.click()
        time.sleep(2)
        selection = browser.find_element(By.XPATH, '//*[@id="input_2_1"]')
        selection.send_keys(name)
        time.sleep(2)

        selection = browser.find_element(By.XPATH, '//*[@id="input_2_4"]')
        selection.send_keys(number)
        time.sleep(2)

        selection = browser.find_element(By.XPATH, '//*[@id="input_2_6"]')
        selection.send_keys(email)
        selection = browser.find_element(By.XPATH, '//*[@id="input_2_5_1"]')
        selection.click()
        time.sleep(2)

        selection = browser.find_element(By.XPATH, '//*[@id="gform_submit_button_2"]')
        selection.click()
        print(Fore.GREEN + "MFOLLARANAORTODONCIA: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "mfollanaortodoncia: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def CLINICABOCCIO(browser, name, number):
    print(Fore.YELLOW + "CLINICA BOCCIO" + Style.RESET_ALL)
    try:
        browser.get('https://www.clinicaboccio.com/pide-cita/')
        time.sleep(3)
        try:
            browser.find_element(By.XPATH, '/html/body/div[1]/div/div[6]/button[1]').click()  # Cokies
        except:
            pass
        browser.find_element(By.XPATH, '//*[@id="input_5_1"]').send_keys(name)
        browser.find_element(By.XPATH, '//*[@id="input_5_4"]').send_keys(number)
        browser.find_element(By.XPATH, '//*[@id="input_5_5_1"]').click()
        browser.find_element(By.XPATH,'//*[@id="gform_submit_button_5"]').click()
        time.sleep(2)
        print(Fore.GREEN + "Clinica boccio: OK'" + Style.RESET_ALL)

    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "Clinica Boccio: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def PONTGRUP(browser, name, number):
    print(Fore.YELLOW + "PONTGRUP" + Style.RESET_ALL)
    try:
        browser.get('https://www.pontgrup.com/contacto/')
        time.sleep(3)
        try:
            browser.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()  # Cookies
        except:
            pass
        browser.find_element(By.XPATH, '//*[@id="btn_call"]/div/a').click()
        time.sleep(1)
        browser.find_element(By.XPATH, '//*[@id="nombre-popup"]').send_keys(name)
        browser.find_element(By.XPATH, '//*[@id="telefono-popup"]').send_keys(number)
        browser.find_element(By.XPATH, '//*[@id="terminos-popup"]').click()
        browser.find_element(By.XPATH,'//*[@id="btn-submit-contacto"]').click()
        time.sleep(2)
        print(Fore.GREEN + "PontGrup: OK" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "PontGrup: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def ELPASO2000(browser, number):
    print(Fore.YELLOW + "ELPASO 2000" + Style.RESET_ALL)
    try:
        browser.get('https://www.elpaso2000.com/te-llamamos/')
        time.sleep(3)
        try:
            browser.find_element(By.XPATH, '//*[@id="CybotCookiebotDialogBodyButtonDecline"]').click()  # Cookies
        except:
            pass
        browser.find_element(By.XPATH,
                             '/html/body/div/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(
            number)
        browser.find_element(By.XPATH,
                             '//*[@id="gatsby-focus-wrapper"]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/label/span').click()
        time.sleep(1)
        browser.find_element(By.XPATH,'//*[@id="gatsby-focus-wrapper"]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[3]/button/span').click()
        time.sleep(2)
        print(Fore.GREEN + "ElPaso2000: OK'" + Style.RESET_ALL)

    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "ElPaso2000: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def CENTRODERMATOLOGICOESTETICO(browser, name, number, email, ):
    print(Fore.YELLOW + "CENTRO DERMATOLOGICO ESTETICO" + Style.RESET_ALL)
    try:
        browser.get('https://www.centrodermatologicoestetico.com/te-llamamos/')
        time.sleep(3)
        try:
            browser.find_element(By.XPATH, '//*[@id="cookie_action_close_header"]').click()  # Cookies
        except:
            pass
        browser.find_element(By.XPATH,
                             '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[5]').send_keys(
            name)
        browser.find_element(By.XPATH, '//*[@id="international_PhoneNumber_countrycode"]').send_keys(number)
        browser.find_element(By.XPATH,
                             '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[7]').send_keys(
            email)
        browser.find_element(By.XPATH,
                             '/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/div/div/div/input').click()
        browser.find_element(By.XPATH,'/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/button').click()
        time.sleep(2)
        print(Fore.GREEN + "centrodermatologicoestetico: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + "centrodermatologicoestetico: Skipeado (ERROR)" + str(e) + Style.RESET_ALL)


def GENERALI(browser, email, name, number):
    print(Fore.YELLOW + "GENERALI" + Style.RESET_ALL)
    try:
        browser.get('https://www.generali.es/blog/tuasesorsalud/solicitar-informacion/')
        time.sleep(3)
        browser.find_element(By.XPATH, '//*[@id="onetrust-reject-all-handler"]').click()
        time.sleep(2)
        browser.find_element(By.XPATH, '//*[@id="email-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').send_keys(email)
        browser.find_element(By.XPATH, '//*[@id="firstname-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').send_keys(name)
        browser.find_element(By.XPATH,
                             '//*[@id="eres_cliente_de_generali_-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').click()
        browser.find_element(By.XPATH,
                             '/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/form/div[3]/div/div/select/option[3]').click()
        browser.find_element(By.XPATH,
                             '//*[@id="que_seguro_tienes_ahora_-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').click()
        browser.find_element(By.XPATH,
                             '/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/form/div[3]/div[2]/div/select/option[10]').click()
        browser.find_element(By.XPATH, '//*[@id="phone-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').send_keys(number)
        browser.find_element(By.XPATH, '//*[@id="agendar_llamada-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').click()
        browser.find_element(By.XPATH,
                             '/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/form/div[5]/div/select/option[2]').click()
        time.sleep(4)
        browser.find_element(By.XPATH,
                             '//*[@id="autorizacion_ofertas_comerciales-c1a9e7d9-fef2-4f6a-8251-2ed4fac8c3df"]').click()
        browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/form/div[15]/div[2]/input').click()

        time.sleep(5)
        print(Fore.GREEN + "Generali: OK'" + Style.RESET_ALL)

    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print('Generali: Skipeado (ERROR)')


def REGAL(browser, number):
    print(Fore.YELLOW + "REGAL" + Style.RESET_ALL)
    try:
        browser.get('https://te-llamamos.regal.es/user-details')
        time.sleep(3)
        browser.find_element(By.XPATH, "//input[@placeholder='Teléfono']").send_keys(number)
        browser.find_element(By.XPATH, "//input[@placeholder='Confirmar teléfono']").send_keys(number)
        # browser.find_element(By.XPATH,'//*[@id="continueButton"]').click()
        time.sleep(3)
        print(Fore.GREEN + "Regal: OK'" + Style.RESET_ALL)
    except KeyboardInterrupt:
        browser.close()
        quit()
    except Exception as e:
        print(Fore.RED + 'Regal: Skipeado (ERROR)' + str(e) + Style.RESET_ALL)

def HOMESERVE (browser, name, surname, number):
        print(Fore.YELLOW + "HOMESERVE" + Style.RESET_ALL)
        try:
            browser.get('https://www.homeserve.es/servicios-reparaciones/fontaneros')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[3]/div/button').click() #Cookies
            except:
                pass
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[2]/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input[1]').send_keys(name)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[5]/input[2]').send_keys(surname)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/input[1]').send_keys(number)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[6]/input[2]').send_keys(email)
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[7]/input').click()
            browser.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[2]/div[1]/div[1]/form/div[9]/button').click()
            time.sleep(1)
            print(Fore.GREEN + "homeserve: OK'" + Style.RESET_ALL)

        except KeyboardInterrupt:
            browser.close()
            quit()
        except Exception as e:
            print(Fore.RED + "homeserve: Skipeado (ERROR)" + Style.RESET_ALL)


def main():
    debug = 1

    if debug == 1:
        number, name, surname, email = '686010340', 'Piter', 'Grifin', 'uhieor43@gmail.com'
    else:
        name = input("Nombre :")
        number = input("Teléfono :")
        surname = "Garcia"
        email = "mistergarcy@gmail.com"

    repeat = 0
    global interrupted
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start = '10:40:00'
    end = '22:00:00'

    while not interrupted:
        firefoxsetup()
        if getattr(sys, 'frozen', False):
            geckodriver_path = os.path.join(sys._MEIPASS, 'geckodriver')
        else:
            geckodriver_path = 'geckodriver'
        if interrupted:
            break
        try:
                    SECURITAS_DIRECT(browser, number)
                    VODAFONE(browser, name, surname, number, email) #ESTE ME CASCA POR EL == $0
                    EUROINNOVA(browser, name, surname, number, email)
                    GENESIS (browser, name, number)
                    RACCTEL(browser, number)
                    JAZZTEL(browser, number)
                    ITEP(browser, email, number) #NO TIRA
                    PROSEGUR(browser, number)
                    LINEADIRECTA (browser , number)
                    TELECABLE (browser, name , surname, number) #OK
                    MAPFRE (browser, name, surname, number) #OK
                    ORANGE (browser, number)
                    SELECTRA(browser, number) #OK
                    IBERDROLA (browser, number)
                    MFOLLARANAORTODONCIA(browser, name, number, email)
                    HOMESERVE (browser, name, surname, number) #OK
                    CLINICABOCCIO (browser, name, number) #OK
                    PONTGRUP(browser, name, number)
                    ELPASO2000(browser, number)
                    CENTRODERMATOLOGICOESTETICO (browser, name, number, email)
                    REGAL (browser , number)
                    GENERALI (browser, email, name, number)

        except Exception as e:
            print(Fore.RED + "Securitas Direct: Skipeado (ERROR):" + str(e) + Style.RESET_ALL)
            interrupted = True

        if repeat == 1:
            browser.close()
            print('Repeat ON')
        else:
            browser.quit()
            break


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda sig, frame: handle_interrupt(browser))

    main()
