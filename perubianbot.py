import logging # Permite hacer seguimiento de eventos en tu aplicación, facilitando la depuración y el diagnóstico de problemas.
from selenium import webdriver # Proporciona herramientas para automatizar la interacción con navegadores web.
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary # Permite especificar la ubicación del binario de Firefox para Selenium.
from datetime import datetime # Proporciona funciones para trabajar con fechas y horas.
import warnings # Ofrece una forma de advertir al desarrollador sobre situaciones que no son necesariamente excepciones.
import requests # Permite enviar solicitudes HTTP/1.1 de manera fácil.
import json # Facilita la codificación y decodificación de datos en formato JSON.
import colorama # Hace posible que la salida de la terminal contenga colores en diferentes plataformas.
from colorama import Fore, Style # Fore permite cambiar el color del texto, y Style ajusta el estilo del texto (como negrita).
from consolemenu import * # Proporciona funcionalidades para crear menús de consola interactivos.
from consolemenu.items import * # Incluye elementos específicos que se pueden agregar a los menús de consola, como FuncItem para funciones.
import signal # Proporciona herramientas para manejar señales de UNIX, permitiendo la interacción con el sistema operativo.
import sys # Ofrece acceso a algunas variables y funciones que interactúan con el intérprete de Python.
warnings.filterwarnings("ignore", category=DeprecationWarning)  # Configura los avisos para ignorar los avisos de obsolescencia.
import time # Ofrece funciones para trabajar con el tiempo, como esperas.
import os # Proporciona una forma de usar funcionalidades dependientes del sistema operativo, como manejar archivos y directorios.
from os import system # Permite ejecutar comandos del sistema desde Python.
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

version = 'Beta 2.0'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
global debug
debug = 1

#VARIABLES
global perubian
perubian = Fore.MAGENTA + Style.BRIGHT + r"""
""" + Style.RESET_ALL
menu = ConsoleMenu(Fore.YELLOW + perubian, "Seleccione un modo"+ Style.RESET_ALL)

#Verificar conexion con Tor
def verificar_conexion_tor():
    try:
        # Hacer una petición a la API para obtener la dirección IP actual

        response = requests.get('https://api.ipify.org', proxies=dict(http='socks5://127.0.0.1:9050', https='socks5://127.0.0.1:9050'))
        ip_actual = response.text
        print(Fore.YELLOW + "IP actual a través de Tor: " + ip_actual + Style.RESET_ALL)
        # Aquí puedes añadir una comprobación adicional para asegurarte de que la IP es una de Tor
        # Por simplicidad, asumimos que cualquier respuesta exitosa implica que Tor está configurado correctamente
        return True
    except Exception as e:
        print(Fore.RED + "Error al verificar la conexión con Tor: " + str(e) + Style.RESET_ALL)
        return False

#Firefox Configuration
def firefoxsetup():
    path_to_geckodriver = '/usr/bin/geckodriver'
    global options
    options = Options()
    # options.add_argument("--headless")  # Ejecutar Firefox en modo headless
    options.accept_insecure_certs = True  # Aceptar certificados inseguros directamente en las Options
    
    # Configurar preferencias directamente en las Options
    #options.set_preference("media.autoplay.default", 0)
    #options.set_preference("media.volume_scale", "0.0")
    #options.set_preference("permissions.default.image", 2)  # Desactivar la carga de imágenes
    #options.set_preference("dom.popup_maximum", 0)  # Bloquear los pop-ups
    #options.set_preference("datareporting.healthreport.uploadEnabled", False)  # Desactivar la telemetría
    #options.set_preference("datareporting.policy.dataSubmissionEnabled", False)  # Desactivar la telemetría
    #options.set_preference("dom.webnotifications.enabled", False)  # Desactivar las notificaciones

    # Configuración del proxy SOCKS para usar con Tor
    options.set_preference("network.proxy.type", 1)  # Manual proxy configuration
    options.set_preference("network.proxy.socks", "127.0.0.1")  # Dirección IP del proxy SOCKS (Tor por defecto)
    options.set_preference("network.proxy.socks_port", 9050)  # Puerto del proxy SOCKS (Tor por defecto)
    options.set_preference("network.proxy.socks_version", 5)  # Versión del proxy SOCKS (Tor utiliza la versión 5)
    options.set_preference("network.proxy.socks_remote_dns", True)  # DNS queries a través de Tor
     
    global service
    service = Service(executable_path=path_to_geckodriver)
    global browser
    browser = webdriver.Firefox(service=service, options=options)

#Limpiar Consola
def clear_console():
    print()
   # os.system('cls' if os.name == 'nt' else 'clear')

#Formulario Datos
def pregunta_estilizada(prompt, datos_previos='', email='', validacion=None):
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
                exit(0)
    
    # Agregar el correo electrónico a datos_previos si se proporciona
    if email:
        datos_previos += Fore.WHITE + Style.BRIGHT + f"Correo: {email}\n" + Style.RESET_ALL
    
    return respuesta

def validacion_no_vacia(input_str):
    return input_str.strip() != ''

#Formulario
def formulario():
    global email,  number, name, surname
    datos_persona = ''
    prefijos = ('6', '8', '7', '9')
    if debug == 1:
        logging.debug("Modo debug activado.")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        number, name, surname, email = '666666666', 'Piter', 'Grifin', 'uhieor43@gmail.com'
    else:
        logging.disable(logging.CRITICAL + 1)
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
    print(datos_persona)

interrupted = False
def handle_interrupt(browser):
    global interrupted
    interrupted = True
    browser.quit()
    print("Navegador cerrado. Volviendo al menú principal...")

def main():
    print ("Entro al main")
    global interrupted
    if not verificar_conexion_tor():
        print(Fore.RED + "Conexión a Tor fallida. Interrumpiendo ejecución." + Style.RESET_ALL)
        sys.exit(1)
    
    #Limite hora
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    start = '10:40:00'
    end = '22:00:00'

    repeat = input('Modo repetición [S/N]: ').lower()
    if repeat in ('y', 'yes', 's', 'si'):
        repeat = 1
        
    while not interrupted:
        firefoxsetup()
        if getattr(sys, 'frozen', False):
            geckodriver_path = os.path.join(sys._MEIPASS, 'geckodriver')
        else:
            geckodriver_path = 'geckodriver'
        
        #SECURITAS DIRECT
        print(Fore.YELLOW + "SECURITAS DIRECT" + Style.RESET_ALL)

        if interrupted:
            break
        try:
            browser.get('https://www.securitasdirect.es/')
            time.sleep(5)
            browser.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]').click() #Cookies
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="edit-telefono1"]').send_keys(number)

            time.sleep(150) #EVITA EL ENVIO

            browser.find_element_by_xpath('//*[@id="edit-submit"]').click()
            time.sleep(1)
            if(browser.current_url == 'https://www.securitasdirect.es/error-envio'):
                print(Fore.RED + "Securitas Direct: Skipeado (Limite Excedido)" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Securitas Direct: OK'" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + "Securitas Direct: Skipeado (ERROR)" + Style.RESET_ALL)

        #Vodafone
        print(Fore.YELLOW + "VODAFONE" + Style.RESET_ALL)

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
            print(Fore.GREEN + "Vodafone: OK'" + Style.RESET_ALL)

        except:
            print(Fore.RED + "Vodafone: Skipeado (ERROR)" + Style.RESET_ALL)
            

        #euroinnova
        print(Fore.YELLOW + "EUROINNOVA" + Style.RESET_ALL)

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
            print(Fore.GREEN + "Euroinnova: OK" + Style.RESET_ALL)            
        except:
            print(Fore.RED + "Euroinnova: Skipeado (ERROR)" + Style.RESET_ALL)

        #GENESIS
        print(Fore.YELLOW + "GENESIS" + Style.RESET_ALL)

        try:
            if current_time > start and current_time < end:
                browser.get('https://www.genesis.es/modal/c2c')
                time.sleep(3)
                try:
                    browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
                except:
                    pass
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/article/div/div/div/div/div/form/section/div/div[2]/div/select/option[3]').click()
                browser.find_element_by_xpath('//*[@id="edit-por-quien-preguntamos-"]').send_keys(name)
                browser.find_element_by_xpath('//*[@id="edit-phone"]').send_keys(number)
                browser.find_element_by_xpath('//*[@id="edit-phone-confirmation"]').send_keys(number)

                browser.find_element_by_xpath('//*[@id="edit-actions-submit"]').click()
                time.sleep(1)
                print(Fore.GREEN + "Genesis: OK'" + Style.RESET_ALL)
            else:
                print('Genesis: Skipeado (Fuera de Horario)')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Genesis: (ERROR)" + Style.RESET_ALL)

        #Racctel+
        print(Fore.YELLOW + "RACCTEL" + Style.RESET_ALL)

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
            print(Fore.GREEN + "Racctel+: OK'" + Style.RESET_ALL)         
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Racctel+: (ERROR)" + Style.RESET_ALL)

        #JAZZTEL
        print(Fore.YELLOW + "JAZZTEL" + Style.RESET_ALL)        
        try:
            browser.get('https://llamamegratis.es/jazztel/v2/webphone.html?lang=es-ES&isLandingLander=1&typeOrigin=wphFollow&widget=3294&wphUrl#https://www.telefonojazztel.es/')
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="phoneNumber"]').send_keys(number)
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="env"]').click()
            time.sleep(3)
            print(Fore.GREEN + "Jazztel: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Jazztel: (ERROR)" + Style.RESET_ALL)

        #Euskaltel
        print(Fore.YELLOW + "EUSKALTEL" + Style.RESET_ALL) 
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
                print(Fore.GREEN + "Euskaltel: OK'" + Style.RESET_ALL)
            else:   
                print(Fore.RED + "Euskltel: Skipeado (ERROR)" + Style.RESET_ALL)

        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Euskaltel Skipeado: ERROR')

        #ITEP
        print(Fore.YELLOW + "ITEP" + Style.RESET_ALL) 
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
            print(Fore.GREEN + "ITEP: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "ITEP: Skipeado (ERROR)" + Style.RESET_ALL)

        #Prosegur
        print(Fore.YELLOW + "PROSEGUR" + Style.RESET_ALL) 
        try:
            browser.get('https://www.prosegur.es/esp/alarmahogar/sem')
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[2]/div/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[3]/div/fieldset/label/span').click()
            browser.find_element_by_xpath('/html/body/section[2]/div/div/div/div[2]/section/div/div/div/div/div[1]/div[2]/form/div[2]/div[4]/div/div/div/button/span').click()
            time.sleep(3)
            print(Fore.GREEN + "Prosegur: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Prosegur: (ERROR)" + Style.RESET_ALL)

        #LineaDirecta
        print(Fore.YELLOW + "LINEA DIRECTA" + Style.RESET_ALL) 
        try:
            browser.get('https://www.lineadirecta.com/te-llamamos-gratis.html?idServicio=http0036&from=B009975&indVehiculo=C')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//button[@id="didomi-notice-agree-button"]').click()
            except:
                pass
            browser.find_element_by_xpath('//*[@id="telefono"]').send_keys(number)
            time.sleep(2)
            try:
                browser.find_element_by_xpath('/html/body/div[1]/section/section/form/div[2]/div/div[2]/a').click() # Buttom 1
            except:
                browser.find_element_by_xpath('/html/body/div[3]/section/section/form/div[2]/div/div[2]/a').click() # Buttom 2
            time.sleep(3)
            print(Fore.GREEN + "Linea Directa: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Linea Directa: (ERROR)" + Style.RESET_ALL)


        #Telecable
        print(Fore.YELLOW + "TELECABLE" + Style.RESET_ALL) 
        try:
            browser.get('http://marcador-c2c.alisys.net/telecablec2c_v2/c2c.php')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="numero"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/button').click()
            time.sleep(3)
            print(Fore.GREEN + "Telecable: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Telecable: (ERROR)" + Style.RESET_ALL)

        #Mapfre
        print(Fore.YELLOW + "MAPFRE" + Style.RESET_ALL) 
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
            print(Fore.GREEN + "Mapfre: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Mapfre: (ERROR)" + Style.RESET_ALL)

        #Orange
        print(Fore.YELLOW + "ORANGE" + Style.RESET_ALL) 
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
            print(Fore.GREEN + "Orange: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Orange: (ERROR)" + Style.RESET_ALL)

        #Selectra
        print(Fore.YELLOW + "SELECTRA" + Style.RESET_ALL) 
        try:
            browser.get('https://ww.selectra.es/contact-internet')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/input').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/label/span[1]').click()
            browser.find_element_by_xpath('/html/body/div[2]/div/div/form/input[3]').click()
            time.sleep(3)
            print(Fore.GREEN + "Selectra: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Selectra: (ERROR)" + Style.RESET_ALL)

        #Iberdrola
        print(Fore.YELLOW + "IBERDROLA" + Style.RESET_ALL) 
        try:
            browser.get('https://www.iberdrola.es/')
            time.sleep(4)
            browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click() #Cookies
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="telf-lc-header"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/section[1]/div[2]/div/div/div[2]/form/div[2]/label').click()
            browser.find_element_by_xpath('/html/body/div[1]/main/div[2]/section[1]/div[2]/div/div/div[2]/div/button/span').click()
            time.sleep(3)
            print(Fore.GREEN + "Iberdrola: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Iberdrola: (ERROR)" + Style.RESET_ALL)

        #proyectosyseguros
        print(Fore.YELLOW + "PROYECTOS Y SEGUROS" + Style.RESET_ALL) 
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
            print(Fore.GREEN + "Proyectos y Seguros: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "Proyectos y Seguros: (ERROR)" + Style.RESET_ALL)

        #urologiaclinicabilbao
        print(Fore.YELLOW + "UROLOGIA BILBAO" + Style.RESET_ALL) 
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
            print(Fore.GREEN + "urologiaclinicaBilbao: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "urologiaclinicaBilbao: (ERROR)" + Style.RESET_ALL)

        #emagister
        print(Fore.YELLOW + "EMAGISTER" + Style.RESET_ALL) 
        try:
            browser.get('https://www.emagister.com/')
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/header/div[2]/div/div[3]/div/nav/div[1]/div/div/section[2]/button').click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="callMe-phone"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/p/label/span[2]').click()
            browser.find_element_by_xpath('/html/body/table[2]/tbody/tr[2]/td[2]/div/div[2]/form/button').click()
            time.sleep(3)
            print(Fore.GREEN + "emagister: OK'" + Style.RESET_ALL)
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print(Fore.RED + "emagister: (ERROR)" + Style.RESET_ALL)

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

        #clinicaboccio
        try:
            browser.get('https://www.clinicaboccio.com/pide-cita/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('/html/body/div[1]/div/div[6]/button[1]').click() #Cokies
            except:
                pass
            browser.find_element_by_xpath('//*[@id="input_5_1"]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="input_5_4"]').send_keys(number)
            browser.find_element_by_xpath('//*[@id="input_5_5_1"]').click()
            browser.find_element_by_xpath('//*[@id="gform_submit_button_5"]').click()
            time.sleep(2)
            print('Clinica Boccio: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Clinica Boccio: Skipeado (ERROR)')

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

        #centrodermatologicoestetico
        try:
            browser.get('https://www.centrodermatologicoestetico.com/te-llamamos/')
            time.sleep(3)
            try:
                browser.find_element_by_xpath('//*[@id="cookie_action_close_header"]').click() #Cookies
            except:
                pass
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[5]').send_keys(name)
            browser.find_element_by_xpath('//*[@id="international_PhoneNumber_countrycode"]').send_keys(number)
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/input[7]').send_keys(email)
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/div/div/div/input').click()
            browser.find_element_by_xpath('/html/body/main/div/div[1]/section/div[2]/div[1]/div/div[4]/div/form/button').click()
            time.sleep(2)
            print('centrodermatologicoestetico: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('centrodermatologicoestetico: Skipeado (ERROR)')

        #generali
        try:
            browser.get('https://www.generali.es/blog/tuasesorsalud/solicitar-informacion/')
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
            time.sleep(2)
            browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[1]/div[2]/label').click()
            browser.find_element_by_xpath('//*[contains(@id,"email")]').send_keys(email)
            browser.find_element_by_xpath('//*[contains(@id,"firstname")]').send_keys(name)
            browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div/form/div[3]/div[1]/div/select/option[2]').click()
            browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div/form/div[3]/div[2]/div/select/option[2]').click()
            browser.find_element_by_xpath('//*[contains(@id,"phone")]').send_keys(number)
            browser.find_element_by_xpath('//*[contains(@id,"autorizacion_ofertas_comerciales")]').send_keys(number)
            browser.find_element_by_xpath('/html/body/div[3]/div[2]/section[1]/div/section[2]/div/main/div/div/div/div/form/div[1]/div[3]/div[2]/div/form/div[16]/div[2]/input').click()
            time.sleep(5)
            print('Generali: OK')
        except KeyboardInterrupt:
            browser.close()
            quit()
        except:
            print('Generali: Skipeado (ERROR)')

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
    menu.show()     
