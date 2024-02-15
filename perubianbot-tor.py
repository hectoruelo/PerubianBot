import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime
import warnings
import requests
import json
import colorama
from colorama import Fore, Style
from consolemenu import *
from consolemenu.items import *
import signal
import sys
#warnings.filterwarnings("ignore", category=DeprecationWarning) 
import time
import os
from os import system

version = 'Beta 2.0'
service = 0
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# Desactiva todos los mensajes de log.
#logging.getLogger().setLevel(100)  # Un nivel superior a CRITICAL.
global debug
debug = 0

system("title " 'PerubianBot '+version)

global perubian
perubian = Fore.MAGENTA + Style.BRIGHT + r"""
______               _     _               _____  _____ 
| ___ \             | |   (_)             / __  \|  _  |
| |_/ /__ _ __ _   _| |__  _  __ _ _ __   `' / /'| |/' |
|  __/ _ \ '__| | | | '_ \| |/ _` | '_ \    / /  |  /| |
| | |  __/ |  | |_| | |_) | | (_| | | | | ./ /___\ |_/ /
\_|  \___|_|   \__,_|_.__/|_|\__,_|_| |_| \_____(_)___/ 
""" + Style.RESET_ALL

menu = ConsoleMenu(Fore.YELLOW + perubian, "Seleccione un modo"+ Style.RESET_ALL)

#Firefox Configuration
def firefoxsetup():
    global binary, options, PATH_TO_DEV_NULL 
    if os.name == 'nt':  # Windows
        binary = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        PATH_TO_DEV_NULL = 'nul'
    elif os.uname().sysname == 'Darwin':  # macOS
        binary = '/Applications/Firefox.app/Contents/MacOS/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    else:
        binary = '/usr/bin/firefox'
        PATH_TO_DEV_NULL = '/dev/null'
    
    options = Options()
    options.add_argument("--headless")
    options.set_preference("media.autoplay.default", 0)
    options.accept_untrusted_certs = True
    options.set_preference("media.volume_scale", "0.0")
    
    # Configuración para usar Tor como proxy SOCKS
    options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
    options.set_preference("network.proxy.socks", "127.0.0.1")  # Dirección IP del proxy SOCKS (Tor)
    options.set_preference("network.proxy.socks_port", 9050)  # Puerto del proxy SOCKS (Tor)
    options.set_preference("network.proxy.socks_version", 5)  # Versión SOCKS (Tor usa SOCKS5)
    options.set_preference("network.proxy.socks_remote_dns", True)  # Para que las solicitudes DNS pasen también por Tor
    

#Limpiar Consola
def clear_console():
    print()
   # os.system('cls' if os.name == 'nt' else 'clear')

#Formulario Datos
def pregunta_estilizada(prompt, datos_previos='', email='', validacion=None):
    clear_console()
    print(perubian)
    # Imprimir los datos previos antes de hacer la nueva pregunta
    if datos_previos:
        print(datos_previos)
    print(Fore.YELLOW + Style.BRIGHT + prompt)
    
    while True:
        try:
            respuesta = input(Fore.GREEN + Style.BRIGHT + ">>> " + Style.RESET_ALL)
            # Si se proporciona una función de validación y la respuesta es válida, romper el bucle
            if not validacion or validacion(respuesta):
                break
            else:
                print(Fore.RED + "Entrada inválida, por favor intente de nuevo." + Style.RESET_ALL)
        except EOFError:
            clear_console()
            exit(0)
    
    # Agregar el correo electrónico a datos_previos si se proporciona
    if email:
        datos_previos += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL
    
    return respuesta

def validacion_no_vacia(input_str):
    return input_str.strip() != ''

#Formulario
def formulario():
    global email 
    datos_persona = ''
    prefijos = ('6', '8', '7', '9')
    if debug == 1:
        logging.debug("Modo debug activado.")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        print(perubian)
        global number, name, surname
        number, name, surname, email = '666666666', 'Piter', 'Grifin', 'uhieor43@gmail.com'
    else:
        datos_persona = ''
        number = pregunta_estilizada('Nº de Teléfono: ')
        while len(number) != 9 or not number.isdigit() or number[0] not in prefijos:
            number = pregunta_estilizada('Número incorrecto. Ingrese Nº de Teléfono nuevamente: ')
        datos_persona += Fore.WHITE + Style.BRIGHT + f"Nº de Teléfono: {number}\n" + Style.RESET_ALL

        name = pregunta_estilizada('Nombre de la persona: ', datos_previos=datos_persona, validacion=validacion_no_vacia)
        surname = pregunta_estilizada('Apellido: ', datos_previos=datos_persona, validacion=validacion_no_vacia)
        nombre_completo = Fore.WHITE + Style.BRIGHT + f"Nombre: {name} {surname}\n" + Style.RESET_ALL
        datos_persona += nombre_completo

        email = pregunta_estilizada('Si no indicas email se va a introducir: ' + name.lower() + surname.lower() + '@gmail.com' + '\nCorreo: ', datos_persona)
        if not email:
            email = f'{name.lower()}.{surname.lower()}@gmail.com'
        datos_persona += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL

    # Después de recopilar toda la información, puedes mostrar datos_persona
    clear_console()
    print(perubian)
    print(datos_persona)

interrupted = False

def handle_interrupt(browser):
    global interrupted
    interrupted = True
    browser.quit()
    print("Navegador cerrado. Volviendo al menú principal...")

def main():
    #Limite hora
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start = '10:40:00'
    end = '22:00:00'

    repeat = input('Modo repetición [S/N]: ').lower()
    if repeat in ('y', 'yes', 's', 'si'):
        repeat = 1
        
    global interrupted
    while not interrupted:
        firefoxsetup()
        global browser , service
        if getattr(sys, 'frozen', False):
            geckodriver_path = os.path.join(sys._MEIPASS, 'geckodriver')
            service = FirefoxService(executable_path=geckodriver_path, log_path=PATH_TO_DEV_NULL)
        else:
            geckodriver_path = 'geckodriver'
            browser = webdriver.Firefox(options=options, service=service)
            service = FirefoxService(executable_path=geckodriver_path, log_path=PATH_TO_DEV_NULL)

        # Visita la página de verificación de Tor
        browser.get("https://check.torproject.org")

        # Busca el mensaje de confirmación
        status = browser.find_element_by_css_selector('body > div > h1').text
        print(status)  # Imprime el mensaje de estado, por ejemplo, "Congratulations. This browser is configured to use Tor."

        # Opcional: Extrae y muestra la IP detectada por la página
        ip_address = browser.find_element_by_css_selector('body > div > p').text
        print(ip_address)  # Imprime tu dirección IP según lo detectado por la página

        #Vodafone
        if interrupted:
            break    
        try:
            browser.get('https://www.vodafone.es/c/empresas/pymes/es/conectividad/red-infinity/')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[2]/div/div/div/div/span/div/div/section/div[2]/div[2]/div[2]/div/div/div/div[2]/form/div/div[1]/div/div/div[2]/div[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[6]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[1]/div[2]/label').click()
            browser.find_element_by_xpath('//*[@id="facade-firstName"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="facade-lastName"]').send_keys(surname)
            browser.find_element_by_xpath('//*[@id="facade-entreprise"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="facade-phoneNumber"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="facade-email"]').send_keys(email)
            time.sleep(1)
            checkbox = browser.find_element_by_xpath("//input[@id='facade-legal']")
            browser.execute_script("arguments[0].click();", checkbox)
            checkbox = browser.find_element_by_xpath('//input[@id="facade-newsletter"]')
            browser.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/main/div[6]/div/div/span/div/div/div/div/div[1]/div[1]/div[2]/form[1]/div/div[10]/button/span[1]').click()
            time.sleep(8)
            print(Fore.GREEN+  'Vodafone: OK' + Style.RESET_ALL)
        except:
            print(Fore.RED +  'Vodafone: Skipeado (ERROR)' + Style.RESET_ALL) 

        #euroinnova
        if interrupted:
            break
        try:
            browser.get('https://www.euroinnova.edu.es/cursos#formulario')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="accept-cookies"]').click() #Cookies
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/button').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="name"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="mail"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="tel"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="privacidad"]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="btn_enviar"]').click()
            time.sleep(3)
            print('Euroinnova: OK')
        except:
            print('Euroinnova: Skipeado (ERROR)')

        #Racctel+
        try:
            url = "https://eshop.prod.k8s.masmovil.com/catalog/api/c2c/racctel"
            payload = {
            "NumeroTelefonoCliente": "642177882",
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
            print('Racctel+: Ok')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Racctel+: Skipeado (ERROR)')

        #Euskaltel
        try:
            url = "https://www.euskaltel.com/CanalOnline/zonas/clicktocall/callmenow_ajax.jsp"

            payload = 'ambito=1&idioma=0&cliente=1&telefono='+number+'&contratar=1&urlActual=%2FCanalOnline%2Fzonas%2Fclicktocall%2Fpopup_callmenow_embed.jsp&medio=undefined&urlPadre=ofertas%2Fpara-ti'
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.euskaltel.com',
            'Alt-Used': 'www.euskaltel.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.euskaltel.com/CanalOnline/zonas/clicktocall/popup_callmenow_embed.jsp?callmenow_idioma=0&callmenow_cliente=1&callmenow_telefono='+number+'&callmenow_email_cliente=-1&callmenow_medio=undefined',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
            'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=LFLCBFHHMCDDGCOBKDNBPIIMEMIDCGLBPLICDHNOEOBAFEDOOBIENKMPBLPKIFNKMLEDEECAPCPIOCCCPNOAGJALCHGBENALMHKAOHODGADLEGBLLBBJLOINKIHCNEPP; JSESSIONID=bzNgsethFpiIXEUljvS8VT8B.node22; BIGipServer~Euskaltel~pool_webpubpro_80=rd3o00000000000000000000ffffac12cf08o80; ektAnonimo=20231227195242906; esClienteEktIp=0'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                print('Euskaltel: OK')
            else:   
                print('Euskaltel Skipeado: ERROR')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Euskaltel Skipeado: ERROR')

        #ITEP
        try:
            browser.get('https://www.itep.es/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() # Cookies
                time.sleep(1)
            except:
                pass
            browser.find_element_by_xpath('/html/body/header/div/div[5]/div/p/button').click() # Solicitar Informacion
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="edit-email--2"]').send_keys(email)
            browser.find_element_by_xpath('//*[@id="edit-phone--2"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="edit-cp--2"]').send_keys("08002")
            browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/form/div[4]/select/optgroup[1]/option[2]').click()
            browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/form/div[5]/select/option[2]').click()
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-conditions--')]").click()
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-educa-consent--')]").click()
            time.sleep(1)
            browser.find_element_by_xpath("//*[starts-with(@id, 'edit-submit-lead-form-header-web-solicita-info-general-2--')]").click()
            time.sleep(3)
            print('ITEP: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('ITEP Skipeado: ERROR')

        #Prosegur
        try:
            browser.get('https://www.prosegur.es/esp/alarmahogar/sem')
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[2]/div/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[3]/div/fieldset/label/span').click()
            browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[4]/div/div/div/button/span').click()
            time.sleep(3)
            print('Prosegur: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Prosegur: Skipeado (ERROR)')

        #Telecable
        try:
            browser.get('http://marcador-c2c.alisys.net/telecablec2c_v2/c2c.php')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="numero"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/button').click()
            time.sleep(3)
            print('Telecable: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Telecable: Skipeado (ERROR)')

        #Mapfre
        try:
            browser.get('https://www.mapfre.es/boi/inicio.do?origen=autos_portalmapfre&destino=sgc_new&producto=autos')
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="nombre"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="primer_apellido"]').send_keys(surname)
            browser.find_element_by_xpath('//*[@id="codigo_postal"]').send_keys("08002")
            browser.find_element_by_xpath('//*[@id="tlfn"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="politicaprivacidad"]').click()
            browser.find_element_by_xpath('/html/body/div[1]/main/div/div/div[2]/form/fieldset/div[10]/input').click()
            time.sleep(3)
            print('Mapfre: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Mapfre: Skipeado (ERROR)')

        #Orange
        try:
            browser.get('https://selectra.es/internet-telefono/companias/orange/telefono')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/button[1]').click() #Cookies
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div/main/div[2]/div[1]/article/div/div[1]/p/a[2]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="callback-modal__phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/section/div[3]/form/div[3]/label/span[1]').click()
            browser.find_element_by_xpath('//*[@id="callback-modal__submit"]').click()
            time.sleep(3)
            print('Orange: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Orange: Skipeado (ERROR)')

        #Selectra
        try:
            browser.get('https://ww.selectra.es/contact-internet')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/label/span[1]').click()
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/input[3]').click()
            time.sleep(3)
            print('Selectra: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Selectra: Skipeado (ERROR)')

        #proyectosyseguros
        try:
            browser.get('https://www.proyectosyseguros.com/te-llamamos/')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click()
            browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/form/div[3]/div[2]/select/optgroup[1]/option[7]').click()
            browser.find_element_by_xpath('//*[@id="llamada-nombre"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="llamada-telefono"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="llamada-lopd"]').click()
            browser.find_element_by_xpath('//*[@id="llamada-enviar"]').click()
            time.sleep(3)
            print('Proyectos y Seguros: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Proyectos y Seguros: Skipeado (ERROR)')

        #urologiaclinicabilbao
        try:
            browser.get('https://www.urologiaclinicabilbao.com/te-llamamos.php')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[1]/button[1]/span').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[2]/input').send_keys(surname)
            browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[1]/div[3]/input').send_keys(name)
            browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div/div[1]/div[2]/form/div[2]/input').click()
            time.sleep(3)
            print('urologiaclinicaBilbao: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('urologiaclinicaBilbao: Skipeado (ERROR)')

        #emagister
        try:
            browser.get('https://www.emagister.com/')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/header/div[2]/div/div[3]/div/nav/div[1]/div/div/section[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="callMe-phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/p/label/span[2]').click()
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/button').click()
            time.sleep(3)
            print('emagister: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('emagister: Skipeado (ERROR)')

        #mfollanaortodoncia
        try:
            browser.get('https://www.mfollanaortodoncia.com/contactar/')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[1]/div[5]/a[1]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="input_1_1"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="input_1_4"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[2]/div[2]/main/div/section/div/div/div[2]/div/div/div/div[2]/form/div[1]/ul/li[3]/div/div/select/option[1]').click()
            browser.find_element_by_xpath('//*[@id="input_1_5_1"]').click()
            browser.find_element_by_xpath('//*[@id="gform_submit_button_1"]').click()
            print('mfollanaortodoncia: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('mfollanaortodoncia: Skipeado (ERROR)')

        #homeserve
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
            print('homeserve: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('homeserve: Skipeado (ERROR)')

        #pontgrup
        try:
            browser.get('https://www.pontgrup.com/contacto/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('/html/body/div[3]/div[2]/button[2]').click() #Cookies
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/section[2]/div/div/div/div[1]/div/div/div/div/a/span/span[2]').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="nombre-contacto"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="telefono-contacto"]]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="terminos-contacto"]').click()
            browser.find_element_by_xpath('//*[@id="btn-submit-contacto"]').click()
            time.sleep(2)
            print('PontGrup: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('PontGrup: Skipeado (ERROR)')

        #ElPaso2000
        try:
            browser.get('https://www.elpaso2000.com/te-llamamos/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="elpaso-button-accept"]').click() #Cookies
            except:
                pass
            browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/label/span').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/main/div/div[1]/div[1]/div[1]/div[2]/form/div[3]/button/span').click()
            time.sleep(2)
            print('ElPaso2000: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('ElPaso2000: Skipeado (ERROR)')

        #regal
        try:
            browser.get('https://te-llamamos.regal.es/user-details')
            time.sleep(3)
            browser.find_element_by_xpath('//input[@id="primaryPhoneInput"][1]').send_keys(number)
            browser.find_element_by_xpath('//input[@id="primaryPhoneInput"][2]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="continueButton"]')
            time.sleep(5)
            print('Regal: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Regal: Skipeado (ERROR)')

        if repeat == 1:
            browser.close()
            print('Repeat ON')
        else:
            browser.quit()
            break

#Menu
def modo_automatico():
    print('Activando Modo automatico...')
    time.sleep(1)
    formulario()
    main()

def modo_porculero():
    print("MODO NO DISPONIBLE")
    time.sleep(2)

def modo_nocturno():
    print("MODO NO DISPONIBLE")
    time.sleep(2)


submenu_selection_menu = SelectionMenu(["subitem1", "subitem2", "subitem3"], title="Modo Contrareembolso")
submenu_item = SubmenuItem("Modo Contrareembolso", submenu=submenu_selection_menu, menu=menu)

# Crear los ítems del menú
item1 = FunctionItem("Modo Automático", modo_automatico)
item2 = FunctionItem("Modo Porculero", modo_porculero)
item3 = FunctionItem("Modo Nocturno", modo_nocturno)

# Añadir los ítems al menú
menu.append_item(item1)
menu.append_item(item2)
menu.append_item(item3)
menu.append_item(submenu_item)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda sig, frame: handle_interrupt(browser))
