# Modulos
# Scraping
from bs4 import BeautifulSoup
import requests
# Sistema
import os
import sys
import threading
import argparse
# Archivos
import csv
import json
# fecha
from datetime import datetime
#log
import logging

# Scraper de mercadolibre

# Start log
def start_log(filename_log_debug, filename_log_info):
	logging.basicConfig(level=logging.DEBUG, filename=filename_log_debug, filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
	logger_info = logging.getLogger("INFO")
	logger_info.setLevel(logging.INFO)
	filehandler_info = logging.FileHandler(filename_log_info, "w")
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	filehandler_info.setFormatter(formatter)
	logger_info.addHandler(filehandler_info)
	return logger_info

# Scraping product details
def scraping_product_details(product_soup):
	date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	# Diccionario de informacion del producto
	product_dict = {
		"fecha_hora" : date_now,
		"producto": "",
		"precio": "",
		"moneda" : "ARS",
		"url_producto": "",
		"url_img_producto" : "",
		"reviews": "",
		"id_publicacion": "",
		"estado": "",
		"vendidos": ""
	}
	### Busqueda en la pagina de productos
	# Titulo
	title_product = product_soup.find('h2','ui-search-item__title').string
	product_dict["producto"] = "\"" + title_product + "\""
	# Url
	url_product = product_soup.find("a", "ui-search-link").get("href")
	product_dict["url_producto"] = url_product
	logger_info.info(f"Scrapeando producto actual de la pagina {url_product}")
	# Imagen
	img_product = product_soup.find('img','ui-search-result-image__element')
	product_dict["url_img_producto"] = img_product.get('data-src')
	### Busqueda en el link individual
	product_soup_details = BeautifulSoup(requests.get(url_product).text,'html.parser')
	# Reviews
	try:
		reviews = product_soup_details.find('span','ui-pdp-review__amount').string
		reviews = reviews.replace("(", "")
		reviews = reviews.replace(")", "")
		product_dict["reviews"] = reviews
	except:
		product_dict["reviews"] = "0"
	# Id Publicacion
	try:
		id_publish = product_soup_details.findAll('span','ui-pdp-color--BLACK ui-pdp-family--SEMIBOLD')[-1].string
		id_publish = id_publish.replace("#", "")
		id_publish = id_publish.strip()
		product_dict["id_publicacion"] = id_publish
	except:
		pass
	# Unidades Vendidas / Estado
	try:
		subtext_status = product_soup_details.find("span", "ui-pdp-subtitle").string.split("|")
		status = subtext_status[0].strip()
		if len(subtext_status) == 2:
			count_selled = subtext_status[1].replace("vendido", "").replace("s", "").strip()
		else:
			count_selled = "0"
		product_dict["estado"] = status
		product_dict["vendidos"] = count_selled
	except:
		pass
	# Precio
	try:
		price = product_soup_details.find('span','andes-money-amount__fraction').string.replace(".", "")
		product_dict["precio"] = price
	except:
		logger_info.info("No se logro encontrar el precio, se dejara en -")
		product_dict["precio"] = "-"
	# Fin de registro
	products.append(product_dict)


# Fecha de ejecucion
date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Parametros de entrada
parser = argparse.ArgumentParser()
parser.add_argument("--busqueda", help="Producto a buscar en ML")
parser.add_argument("--paginas", help="Cantidad de paginas a buscar (Default: 1)")
args = parser.parse_args()

# Parametro busqueda
if args.busqueda:
	product_find = args.busqueda.replace(" ", "-")
else:
	print("Error: No se ingreso un producto a buscar")
	sys.exit(1)

# Log
filename_log_info = os.path.join("log", "busqueda_" + product_find + "_ml_INFO_" + date_now.split(" ")[0] + ".log")
filename_log_debug = os.path.join("log", "busqueda_" + product_find + "_ml_DEBUG_" + date_now.split(" ")[0] + ".log")
logger_info = start_log(filename_log_debug, filename_log_info)

# Parametro paginas
if args.paginas:
	try:
		count_pages = int(args.paginas)
	except BaseException as err:
		logger_info.error("Error en la cantidad de paginas, el parametro ingresado no es un numero o es negativo")
		print("Error: el parametro ingresado no es un numero")
		sys.exit(1)
	if count_pages < 1:
		logger_info.error("Error en la cantidad de paginas, el parametro ingresado no es un numero o es negativo")
		print("Error: Las paginas no pueden ser menor a 1")
		sys.exit(1)
	else:
		print(f"Se ingresaron {count_pages} paginas")
else:
	print(f"No se ingreso cantidad de paginas, por defecto sera 1")
	count_pages = 1

# Armado del url mercado libre 
url = "https://listado.mercadolibre.com.ar/"
url += product_find + "_OrderId_PRICE"

logger_info.info(f"Inicio del scraping en mercadolibre al producto {product_find}")
print("Url: ", url)

# Scraping meli
# Global
products = []
for i in range(0, count_pages):
	try:
		response = requests.get(url)
	except requests.RequestException as err:
		logger_info.error(f"Error al intentar buscar la siguiente pagina({i}), la pagina no responde a la peticion")
		print("Error al realizar la peticion de la pagina, posiblemente esta caida o no exista " + err)
		sys.exit(1)
	try:
		soup = BeautifulSoup(response.text,'html.parser')
		title_url = soup.title.string
		print (title_url + " | Pagina " + str(i+1))
	except Exception as err:
		print(err)
	thread_list = []
	for product_soup in soup.find_all('li','ui-search-layout__item'):
		thread_scraping = threading.Thread(target=scraping_product_details, args=(product_soup,))
		thread_list.append(thread_scraping)
		thread_scraping.start()
	for thread in thread_list:
		thread.join()
	try:
		if i < count_pages - 1:
			link_next = (soup.find('li','andes-pagination__button andes-pagination__button--next')).find('a','andes-pagination__link')
			url = link_next.get('href')
			logger_info.info(f"Se ira a la siguiente pagina del producto {url}")
	except Exception as err:
		# Salgo del for debido a que no se encontro otro link de pagina
		logger_info.error(f"Error al encontrar el siguiente link. " + str(err))
		print("Error al encontrar el siguiente link, se terminaron las paginas")
		print(err)
		if len(products) == 0:
			print("No se encontraron productos")
			sys.exit(1)
		break

# Armado del archivo con los datos encontrados
logger_info.info(f"Se guardaran los productos encontrados en el archivo " + os.path.join("output", "busqueda_" + product_find + "_ml_" + date_now.split(" ")[0] + ".csv"))

# Armado del Header en el archivo
filename = open(os.path.join("output", "busqueda_" + product_find + "_ml_" + date_now.split(" ")[0] + ".csv"), "w", encoding="utf-8-sig")
filename.write("fecha_hora|producto|precio|moneda|url_producto|url_img_producto|reviews|id_publicacion|estado|vendidos\n")
# Escritura de los datos
for product in products:
	filename.write(product["fecha_hora"] + "|")
	filename.write(product["producto"] + "|")
	filename.write(product["precio"] + "|")
	filename.write(product["moneda"] + "|")
	filename.write(product["url_producto"] + "|")
	filename.write(product["url_img_producto"] + "|")
	filename.write(product["reviews"] + "|")
	filename.write(product["id_publicacion"] + "|")
	filename.write(product["estado"] + "|")
	filename.write(product["vendidos"] + "\n")
filename.close()

# Fin del programa
logger_info.info(f"El scraping del producto {product_find} se ha completado.")
logger_info.info("Total de productos encontrados: " + str(len(products)))
print("Total de productos encontrados: ", len(products))
print("Fin del proceso")
sys.exit(0)