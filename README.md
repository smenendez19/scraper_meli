# scraper_mercadolibre_cli.py

## Descripcion

Script que scrapea paginas web de busquedas de mercadolibre y parsea los items buscados a un archivo csv para poder analizarlo o insertarlo en alguna tabla.  
Utiliza beautifulsoup y requests para el scraping.
El script fue realizado usando Python 3.7.2

## Funcionamiento

El programa funciona de la siguiente manera:

1) Se reciben por parametro el producto a buscar y la cantidad de paginas para visitar en mercadolibre. Por defecto 1.  
2) Por cada producto de la busqueda se toman los siguientes datos:
    - fecha_hora
    - producto
    - precio
    - moneda
    - url_producto
    - url_img_producto
    - reviews
    - id_publicacion
    - estado
    -vendidos
3) Una vez buscado todos los datos se guarda en un archivo csv con el formato "busqueda_{producto}_{fecha}ml.csv" en la carpeta output del script.
    - producto : Nombre de producto
    - fecha : Fecha de ejecucion en formato YYYY-MM-DD
4) Se guarda un log con el formato "busqueda_{producto}_{fecha}ml.log" en la carpeta log del script.

## Parametros

El script de consola recibe los siguientes parametros:

**--busqueda** : Producto de ml a buscar  
**--paginas** (opcional) : Cantidad de paginas a buscar, por defecto 1.

**Ejemplo:**

    python scraping_mercadolibre_cli.py --busqueda "placas de video nvidia" --paginas 5

## Requerimientos

Necesitan tener los siguientes modulos instalados:  

- **requests**
- **bs4 (BeautifulSoup4)**  

Para poder instalarlo tienen que abrir su consola cmd/shell y escribir: "pip install requests --user" y "pip install bs4 --user".
