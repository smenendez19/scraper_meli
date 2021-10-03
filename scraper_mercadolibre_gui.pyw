# Cosas a agregar
# 3) Frontend mas bonito (icono, fuentes, colores)
# 4) Centrado de las ventanas

# Modulos

# GUI
import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from tkinter.filedialog import askopenfilename

# Scraping
from bs4 import BeautifulSoup
import requests
# Sistema
import os
import sys
import threading
# Archivos
import csv
import json
# fecha
from datetime import datetime
#log
import logging

# Clases

# Clase Interfaz scraping
class scraping_ml_gui:
    def __init__(self):
        ### Root
        self.root = tkinter.Tk()
        self.root.title("Scraper Web MercadoLibre")
        self.root.resizable(0, 0)
        self.root.configure(background="black")
        self.root.iconphoto(True, tkinter.PhotoImage(file=os.path.join(os.path.dirname(sys.argv[0]), "static", "icon.png")))

        ### Frames
        self.top_frame = tkinter.Frame(self.root, bg="black", width=300, height=300)
        self.form_frame = tkinter.Frame(self.root, bg="black", width=300, height=300)
        self.scraping_list_frame = tkinter.Frame(self.root, bg="black", width=300, height=300)
        self.buttoms_frame = tkinter.Frame(self.form_frame, bg="black")

        ### Grid frames
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="")
        self.form_frame.grid(row=1, column=0, sticky="")
        self.scraping_list_frame.grid(row=1, column=1, sticky="")
        self.buttoms_frame.grid(row=2, column=0, columnspan=2, sticky="")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=2)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_columnconfigure(2, weight=2)

        ### Variables de inputs
        self.producto_busqueda = tkinter.StringVar()
        self.cant_paginas = tkinter.StringVar()

        ### Otras variables
        self.scraping_process = 0

        ### Fuente de texto
        font = tkinter.font.Font(family="Arial", size=15, weight="bold")

        ### Labels
        self.label_titulo = tkinter.Label(self.top_frame, text="Scraper Web mercado libre", font=font)
        self.label_titulo.configure(background="black", foreground="white", anchor="center")

        self.label_info_ingreso_busqueda = tkinter.Label(self.form_frame, text="Ingresa el producto a buscar: ", font=("Arial", 15))
        self.label_info_ingreso_busqueda.configure(background="black", foreground="white")

        self.label_info_cant_paginas = tkinter.Label(self.form_frame, text="Ingresa la cantidad de paginas: ", font=("Arial", 15))
        self.label_info_cant_paginas.configure(background="black", foreground="white")

        ### Entries
        self.entry_product_ml = tkinter.Entry(self.form_frame, textvariable=self.producto_busqueda, font=("Arial", 15))
        self.entry_product_ml.configure(background="black", foreground="white", insertbackground="white")

        self.entry_cant_paginas = tkinter.Entry(self.form_frame, textvariable=self.cant_paginas, font=("Arial", 15))
        self.entry_cant_paginas.configure(background="black", foreground="white", insertbackground="white")

        ### Botones
        # Boton de comenzar a scrapear
        self.boton_start_scraping = tkinter.Button(self.buttoms_frame, text="Comenzar",command=self.start_scraping, font=("Arial", 15))
        self.boton_start_scraping.configure(background="black", foreground="white")

        # Boton de testing
        self.boton_view_file = tkinter.Button(self.buttoms_frame, text="Ver archivo",command=lambda : self.select_file_output(), font=("Arial", 15))
        self.boton_view_file.configure(background="black", foreground="white")

        self.boton_delete_list = tkinter.Button(self.buttoms_frame, text="Borrar Lista",command=lambda : self.delete_list(), font=("Arial", 15))
        self.boton_delete_list.configure(background="black", foreground="white")

        self.boton_help = tkinter.Button(self.buttoms_frame, text="Ayuda",command=lambda : print, font=("Arial", 15))
        self.boton_help.configure(background="black", foreground="white")

        # Treeviews
        columns_scraping = ["Ejecucion", "Pagina", "Elementos", "Estado"]
        self.tv_scraping_runs = ttk.Treeview(self.scraping_list_frame, columns=columns_scraping, show="headings")
        for col in columns_scraping:
            self.tv_scraping_runs.heading(col, text=col)
            self.tv_scraping_runs.column(col, minwidth=50, stretch=1, anchor=tkinter.W)

        # Separadores
        self.separator_frames = ttk.Separator(self.form_frame, orient=tkinter.HORIZONTAL)

        ### Menu
        self.menubar = tkinter.Menu(self.root)
        self.root.configure(menu=self.menubar)

        file_menu = tkinter.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Abrir archivo", command=lambda : self.select_file_output())
        file_menu.add_command(label="Salir", command=self.exit_question)
        self.menubar.add_cascade(label="Archivo", menu=file_menu)

        list_menu = tkinter.Menu(self.menubar, tearoff=0)
        list_menu.add_command(label="Exportar Lista", command=lambda : self.export_list())
        list_menu.add_command(label="Borrar Lista", command=lambda : self.delete_list())
        self.menubar.add_cascade(label="Lista Ejecuciones", menu=list_menu)

        help_menu = tkinter.Menu(self.menubar, tearoff=0)
        #help_menu.add_command(label="Leer readme", command=lambda : print)
        help_menu.add_command(label="Acerca de", command=lambda : self.about_message())
        self.menubar.add_cascade(label="Ayuda", menu=help_menu)
        
        ### Styles
        style_tv = ttk.Style(self.scraping_list_frame)
        style_tv.theme_use("clam")
        style_tv.configure("Treeview", background="black", fieldbackground="black", foreground="white")
        style_tv.configure("Separator", background="white")

        ### Grid
        self.label_titulo.grid(row=0, column=0, sticky="")

        self.label_info_ingreso_busqueda.grid(row=0,column=0, sticky="")
        self.entry_product_ml.grid(row=0,column=1, sticky="")
        self.label_info_cant_paginas.grid(row=1,column=0, sticky="")
        self.entry_cant_paginas.grid(row=1,column=1, sticky="")
        self.separator_frames.grid(row=0, column=2, rowspan=3, sticky="NS", padx=20, ipady=110)

        self.boton_start_scraping.grid(row=1,column=0)
        self.boton_view_file.grid(row=1,column=1)
        self.boton_delete_list.grid(row=1,column=2)
        self.boton_help.grid(row=1,column=3)

        self.tv_scraping_runs.grid(row=2, column=0)

        ### Protocolos
        self.root.protocol("WM_DELETE_WINDOW", self.exit_question)
        
        ### Solo para testing
        #self.insert_test_values()

        ### Start
        self.root.mainloop()

    # SOLO PARA TESTING
    def insert_test_values(self):
        self.tv_scraping_runs.insert("", tkinter.END, values=("Maquina afeitadora", "1", "0", "EJECUTANDO"))
        self.tv_scraping_runs.insert("", tkinter.END, values=("Pelota futbol", "1", "0", "ERROR - Producto"))
        self.tv_scraping_runs.insert("", tkinter.END, values=("Placa de video AMD", "1", "0", "ERROR - Pagina"))
        self.tv_scraping_runs.insert("", tkinter.END, values=("MacBook Air", "1", "0", "TERMINADO"))
        return

    # Acerca de
    def about_message(self):
        tkinter.messagebox.showinfo("Acerca de", "Scraper de productos de Mercado Libre\nVersion 2.0\nCreado por santimenendez19")

    # Borrado de la lista de progresos scraping (TERMINADOS y ERRORES)
    def delete_list(self):
        for child in self.tv_scraping_runs.get_children():
            if self.tv_scraping_runs.item(child)['values'][3] != "EJECUTANDO":
                self.tv_scraping_runs.delete(child)
        return

    # Exportar lista de scraping a json
    def export_list(self):
        json_list = []
        for child in self.tv_scraping_runs.get_children():
            if self.tv_scraping_runs.item(child)['values'][3] != "EJECUTANDO":
                json_dict = {
                    "Producto" : self.tv_scraping_runs.item(child)["values"][0],
                    "Paginas" : self.tv_scraping_runs.item(child)["values"][1],
                    "Cantidad" : self.tv_scraping_runs.item(child)["values"][2],
                    "Estado" : self.tv_scraping_runs.item(child)["values"][3]
                }
                json_list.append(json_dict)
        # Valido que hayan elementos en la lista
        if len(json_list) == 0:
            messagebox.showerror("Error", "No hay elementos en la lista")
            return
        date_now = datetime.now().strftime("%Y-%m-%d")
        try:
            with open(os.path.join(os.path.dirname(sys.argv[0]), "log", f"lista_ejecuciones_{date_now}.json"), "w") as json_file:
                json.dump(json_list, json_file)
            tkinter.messagebox.showinfo("Exportar Lista", "Se exportaron las ejecuciones correctamente en el archivo " + os.path.join(os.path.dirname(sys.argv[0]), "log", f"lista_ejecuciones_{date_now}.json"))
        except Exception as err:
            messagebox.showerror("Error", f"Error al exportar la lista: {err}")
            return

    # Salida del programa
    def exit_question(self):
        valor = tkinter.messagebox.askokcancel("Salir", "¿Desea salir de la aplicacion?")
        if(valor):
            self.root.destroy()
            os._exit(0)
            return

    # Seleccionar archivo para observar
    def select_file_output(self):
        filename = askopenfilename(initialdir=os.path.join(os.path.dirname(sys.argv[0]), "output"))
        if filename:
            with open(filename, "rt", encoding="utf-8") as f_csv:
                header = next(f_csv).split("|")
                if len(header) == 10:
                    view_file_ml(self.root, filename)
                else:
                    tkinter.messagebox.showerror("Error al abrir archivo",f"Error al abrir el archivo:\n{filename}.\nNo coincide la cabezera con las armadas por el proceso")
        return

    # Informacion scraping completado
    def scraping_completed(self, filename):
        valor = tkinter.messagebox.askokcancel("Ver productos", "¿Desea abrir el visualizador de productos scrapeados?")
        if(valor):
            view_file_ml(self.root, filename)
        return

    # Actualizacion de progreso del scraping
    def update_progress(self, scraping_product, type_update, value=None):
        for child in self.tv_scraping_runs.get_children():
            if scraping_product.lower() == self.tv_scraping_runs.item(child)['values'][0].lower():
                row = self.tv_scraping_runs.item(child)['values']
                page = int(row[1])
                elements = int(row[2])
                if type_update == "new_element":
                    elements = elements + 1
                    self.tv_scraping_runs.item(child, values=(scraping_product, page, elements, "EJECUTANDO"))
                elif type_update == "next_page":
                    page = page + 1
                    self.tv_scraping_runs.item(child, values=(scraping_product, page, elements, "EJECUTANDO"))
                elif type_update == "finished":
                    self.tv_scraping_runs.item(child, values=(scraping_product, page, elements, "TERMINADO"))
                elif type_update == "error":
                    self.tv_scraping_runs.item(child, values=(scraping_product, page, elements, f"ERROR - {value}"))
                break
        return
    
    # Start log
    def start_log(self, filename_log_debug, filename_log_info):
        logging.basicConfig(level=logging.DEBUG, filename=filename_log_debug, filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
        logger_info = logging.getLogger("INFO")
        logger_info.setLevel(logging.INFO)
        filehandler_info = logging.FileHandler(filename_log_info, "w")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehandler_info.setFormatter(formatter)
        logger_info.addHandler(filehandler_info)
        return logger_info

    # Inicio de scraping
    def start_scraping(self):
        # Logging
        date = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(os.path.dirname(sys.argv[0]), "output", "busqueda_" + self.producto_busqueda.get().strip().replace(" ", "-") + "_ml_" + date + ".csv")
        filename_log_debug = os.path.join(os.path.dirname(sys.argv[0]), "log", "busqueda_" + self.producto_busqueda.get().strip().replace(" ", "-") + "_ml_DEBUG_" + date + ".log")
        filename_log_info = os.path.join(os.path.dirname(sys.argv[0]), "log", "busqueda_" + self.producto_busqueda.get().strip().replace(" ", "-") + "_ml_INFO_" + date + ".log")
        logger_info = self.start_log(filename_log_debug, filename_log_info)
        # Scraping a MercadoLibre
        url = "https://listado.mercadolibre.com.ar/"
        if self.producto_busqueda.get() == "":
            self.tv_scraping_runs.insert("", tkinter.END, values=(self.producto_busqueda.get(), "-", "0", "ERROR - Producto"))
            logger_info.error("Error en el campo producto, no se ingreso el producto a buscar")
            tkinter.messagebox.showerror("Error campo producto", "No se ingreso el producto a buscar")
            return 1
        # Verificar si el producto ya fue buscado recientemente
        for child in self.tv_scraping_runs.get_children():
            if self.producto_busqueda.get().lower() == self.tv_scraping_runs.item(child)['values'][0].lower():
                # Preguntar si desea buscar de nuevo
                logger_info.info(f"El producto {self.producto_busqueda.get()} ya fue buscado anteriormente")
                if tkinter.messagebox.askyesno("Producto ya buscado", f"El producto {self.producto_busqueda.get()} ya fue buscado recientemente, desea buscarlo de nuevo?"):
                    self.tv_scraping_runs.delete(child)
                else:
                    return 0
        url += self.producto_busqueda.get().strip().replace(" ", "-") + "_OrderId_PRICE"
        if self.cant_paginas.get() == "":
            self.cant_paginas.set(1)
        try:
            pag = int(self.cant_paginas.get())
            if pag < 1:
                raise Exception("Error en la cantidad de paginas")
        except BaseException as err:
            self.tv_scraping_runs.insert("", tkinter.END, values=(self.producto_busqueda.get(), "-", "0", f"ERROR - {err}"))
            logger_info.error("Error en la cantidad de paginas, el parametro ingresado no es un numero o es negativo")
            tkinter.messagebox.showerror("Error paginas", "El parametro ingresado no es un numero o es negativo")
            return 1
        logger_info.info(f"Inicio del scraping en mercadolibre al producto {self.producto_busqueda.get()}")
        self.tv_scraping_runs.insert("", tkinter.END, values=(self.producto_busqueda.get(), "1", "0", "EJECUTANDO"))
        t1 = threading.Thread(target=self.scraping_ml, args=(url, self.producto_busqueda.get(), int(self.cant_paginas.get()), filename, logger_info))
        t1.start()
        return 0

    # Scraping a ml
    def scraping_ml(self, url, scraping_product, pages, filename, logger_info):
        count_products = 0
        self.scraping_process += 1
        products = []
        for i in range (0, int(pages)):
            try:
                logger_info.info(f"Buscando la pagina {i+1} del producto")
                response = requests.get(url)
            except requests.RequestException as err:
                self.update_progress(scraping_product, "error", err)
                logger_info.error(f"Error al intentar buscar la siguiente pagina({i}), la pagina no responde a la peticion")
                tkinter.messagebox.showerror(f"ERROR {scraping_product}", f"Error al intentar buscar la siguiente pagina({i}), la pagina no responde a la peticion")
                self.exit_question()
                error_code = 1
                self.scraping_process -= 1
                return 1
            soup = BeautifulSoup(response.text,'html.parser')
            #title_url = soup.title.string
            date_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for product_soup in soup.find_all('li', 'ui-search-layout__item'):
                # Diccionario de informacion del producto
                product_dict = {
                    "fecha_hora" : date_actual,
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
                title_product = product_soup.find('h2', 'ui-search-item__title').string
                product_dict["producto"] = "\"" + title_product + "\""
                # Url
                url_product = product_soup.find("a", "ui-search-link").get("href")
                product_dict["url_producto"] = url_product
                logger_info.info(f"Scrapeando producto actual de la pagina {url_product}")
                # Imagen
                img_product = product_soup.find('img','ui-search-result-image__element')
                product_dict["url_img_producto"] = img_product.get('data-src')
                ### Busqueda en el link individual
                try:
                    product_soup_details = BeautifulSoup(requests.get(url_product).text,'html.parser')
                except requests.RequestException as err:
                    self.update_progress(scraping_product, "error", err)
                    tkinter.messagebox.showerror(f"ERROR {scraping_product}", f"Error al intentar buscar el siguiente producto ({url_product}), la pagina no responde a la peticion")
                    logger_info.error(f"Error al intentar buscar el siguiente producto ({url_product}), la pagina no responde a la peticion")
                    if tkinter.messagebox.askyesno("Continuar", "¿Desea continuar con el scraping?"):
                        continue
                    else:
                        error_code = 1
                        self.scraping_process -= 1
                        return 1
                # Reviews
                try:
                    reviews = product_soup_details.find('span','ui-pdp-review__amount').string
                    reviews = reviews.split(" ")[0]
                    if reviews == "":
                        reviews = "0"
                    product_dict["reviews"] = reviews
                except:
                    logger_info.info("No se encontraron reviews, se dejara en 0")
                    product_dict["reviews"] = "0"
                # Id Publicacion
                try:
                    id_publish = product_soup_details.findAll('span','ui-pdp-color--BLACK ui-pdp-family--SEMIBOLD')[-1].string
                    product_dict["id_publicacion"] = id_publish
                except:
                    logger_info.info("No se logro encontrar ID de publicacion, se dejara en NULL")
                    product_dict["id_publicacion"] = "NULL"
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
                    price = product_soup_details.find('span','price-tag-fraction').string.replace(".", "")
                    product_dict["precio"] = price
                except:
                    logger_info.info("No se logro encontrar el precio, se dejara en -")
                    product_dict["precio"] = "-"
                # Fin de registro
                products.append(product_dict)
                count_products += 1
                self.update_progress(scraping_product, "new_element", None)
            try:
                link_next = (soup.find('li','andes-pagination__button andes-pagination__button--next')).find('a','andes-pagination__link')
                url = link_next.get('href')
                logger_info.info(f"Se ira a la siguiente pagina del producto {url}")
                self.update_progress(scraping_product, "next_page", None)
            except Exception as err:
                self.update_progress(scraping_product, "error", "Fin de pagina")
                logger_info.error(f"Error al encontrar el siguiente link. " + str(err))
                tkinter.messagebox.showerror("Error url",f"Error al intentar buscar la siguiente pagina ({i}), se acabaron las busquedas")
                error_code = 0
                self.scraping_process -= 1
                self.end_scraping(error_code, scraping_product, filename, products, logger_info)
                return 1
        logger_info.info(f"Se terminaron de encontrar todos los productos disponibles, se han encontrado {count_products} productos")
        error_code = 0
        self.scraping_process -= 1
        self.end_scraping(error_code, scraping_product, filename, products, logger_info)
        return 0

    # Finalizacion de scraping y escritura en archivo
    def end_scraping(self, error_code, scraping_product, filename, products, logger_info):
        logger_info.info(f"Se guardaran los productos encontrados en el archivo {filename}")
        # Armado del Header en el archivo
        file = open(filename, "w", encoding="utf-8-sig")
        file.write("fecha_hora|producto|precio|moneda|url_producto|url_img_producto|reviews|id_publicacion|estado|vendidos\n")
        # Escritura de los datos
        for product in products:
            file.write(product["fecha_hora"] + "|")
            file.write(product["producto"] + "|")
            file.write(product["precio"] + "|")
            file.write(product["moneda"] + "|")
            file.write(product["url_producto"] + "|")
            file.write(product["url_img_producto"] + "|")
            file.write(product["reviews"] + "|")
            file.write(product["id_publicacion"] + "|")
            file.write(product["estado"] + "|")
            file.write(product["vendidos"] + "\n")
        file.close()
        if error_code == 0:
            self.update_progress(scraping_product, "finished", None)
            tkinter.messagebox.showinfo("Scraping completado", f"El scraping del producto {scraping_product} se ha completado.")
            logger_info.info(f"El scraping del producto {scraping_product} se ha completado.")
            self.scraping_completed(filename)
        else:
            logger_info.error("Ocurrio un error al guardar los productos encontrados, revisar el log DEBUG")
            self.update_progress(scraping_product, "error", "Scraping")
        return 0

# Clase vista archivo
class view_file_ml:
    def __init__(self, master, filename):
        # Variables
        self.columns = ("Fecha_Hora", "Producto", "Precio", "Moneda", "Url_Producto", "URL_Imagen_Producto", "Reviews", "ID_publicacion", "Estado", "Cantidad_Vendidos")
        self.filename = filename
        # Root
        self.root = tkinter.Toplevel(master)
        # Estilos
        self.style_lista_productos = ttk.Style()
        # Treeview
        self.lista_productos = ttk.Treeview(self.root, columns=self.columns, show="headings")
        self.refresh_button = tkinter.Button(self.root, text="Refresh", command=self.load_treeview)
        self.quit_button = tkinter.Button(self.root, text="Quit", command=print)
        # Carga configuracion
        self.config_root()
        self.load_treeview()
        self.load_styles()
        self.load_scroll_bars()
        self.load_binds()
        # Ejecucion
        self.root.mainloop()

    # Salida del programa
    def salida_question(self):
        valor = tkinter.messagebox.askokcancel("Salir", "¿Desea salir del view?")
        if(valor):
            self.root.destroy()

    def config_root(self):
        self.root.title("Lista de productos")
        self.root.configure(background="#FFFFFF")
        self.root.geometry("1220x600")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
    
    # Cambio de tipo de datos en el treeview
    def transform_fields(self):
        rows = []
        with open(self.filename, "rt", encoding="utf-8") as f_csv:
            csv_reader = csv.reader(f_csv, delimiter="|")
            next(csv_reader)
            for row in csv_reader:
                rows.append(row)
            if rows[-1] == "":
                del rows[-1]
        return rows

    # Carga el treeview (vista de productos)
    def load_treeview(self):
        rows = self.transform_fields()
        if len(self.lista_productos.get_children()) > 0:
            self.lista_productos.delete(*self.lista_productos.get_children())
        self.lista_productos.grid(row=0, column=0, sticky='nsew')
        for col in self.columns:    
            self.lista_productos.heading(col, text=col, command=lambda _col=col : self.treeview_sort_column(_col, False))
            self.lista_productos.column(col, minwidth=100, stretch=1, anchor=tkinter.W)
        for row in rows:
            self.lista_productos.insert("", tkinter.END, values=tuple(row))
        self.refresh_button.grid(row=2, column=0, sticky='nsew')
        self.quit_button.grid(row=2, column=1, sticky='nsew')

    # Ordenamiento de columnas
    def treeview_sort_column(self, col, reverse):
        if col in ["Precio", "Reviews", "Cantidad_Vendidos"]:
            set_rows = [(int(self.lista_productos.set(key, col)), key) for key in self.lista_productos.get_children('')]
        else:
            set_rows = [(self.lista_productos.set(key, col), key) for key in self.lista_productos.get_children('')]
        set_rows.sort(reverse=reverse)
        for index, (_, k) in enumerate(set_rows):
            self.lista_productos.move(k, '', index)
        self.lista_productos.heading(col, command=lambda _col=col : self.treeview_sort_column(_col, not reverse))

    # Carga de estilos de texto
    def load_styles(self):
        self.style_lista_productos.configure("Frame", foreground="#FFFFFF",background="#222222")
        self.style_lista_productos.configure("Treeview", foreground="#FFFFFF", background="#222222")

    # Binds
    def load_binds(self):
        self.lista_productos.bind('<ButtonRelease-1>', self.tree_click_function)

    # ScrollBar
    def load_scroll_bars(self):
        self.scroll_bar_ver = tkinter.Scrollbar(self.root, orient=tkinter.VERTICAL, command=self.lista_productos.yview, width=20)
        self.scroll_bar_ver.grid(row=0, column=1, sticky='ns')
        self.lista_productos.config(yscrollcommand=self.scroll_bar_ver.set)
        self.scroll_bar_hor = tkinter.Scrollbar(self.root, orient=tkinter.HORIZONTAL, command=self.lista_productos.xview, width=20)
        self.scroll_bar_hor.grid(row=1, column=0, sticky='we')
        self.lista_productos.config(xscrollcommand=self.scroll_bar_hor.set)

    # Funciones
    def tree_click_function(self, event):
        current_item = self.lista_productos.item(self.lista_productos.focus())
        column = self.lista_productos.identify_column(event.x)
        self.root.clipboard_clear()
        if current_item["values"] != "":
            copied_element = current_item['values'][int(column.replace("#", "")) - 1]
            self.root.clipboard_append(copied_element)
            self.root.title(f"Lista de productos | Elemento copiado: {copied_element}")

if __name__ == "__main__":
    scraping_ml_gui()
