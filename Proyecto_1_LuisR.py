#Importación de librerías 

import tkinter as tk
from tkinter import messagebox
import csv
from tkinter import *
from PIL import Image, ImageTk  # Usamos Pillow para cargar imágenes JPG
import os 
from tkinter import Toplevel, Canvas, NO
import random 
 
# Evita que se presenten problemas al cargar las imagenes 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Guarda las imagenes en memoría para que no se borren 
referencias_imagenes = []

#Lista que guardará los personajes seleccionados por el usuario 
personajes_seleccionados = []

#Lista que guardará el avatar seleccionado por el usuario 
avatar_seleccionado = []

# Lista que guardará los 3 personajes escogidos originalmente en parametrización
    #Al iniciar una batalla en diferentes reinos se utilizarán solos los 3 personajes esccogidos en la parametrización 
        # Se crea esa lista vacía para guardar esa información 
personajes_base = []

###########################################
#Creación de pantalla principal 
pantalla_principal = Tk()

# Título de pantalla principal 
pantalla_principal.title("Epic Adventure")

# Se deshabilita el redimensionamiento de la ventana
pantalla_principal.resizable(False, False) 

#Ajuste la ventana al máximo tamaño de la pantalla 
#pantalla_principal.state('zoomed')


# Se ajustael tamaño para dejar visible la barra de tareas
ancho_pantalla = pantalla_principal.winfo_screenwidth()
alto_pantalla = pantalla_principal.winfo_screenheight()

# Se resta unos píxeles al alto (80 px deja ver la barra de tareas)
pantalla_principal.geometry(f"{ancho_pantalla}x{alto_pantalla - 80}+0+0")

# Se define las dimesiones de la ventana "largoxancho" + posición eje "x" y posición eje "y"
#pantalla_principal.geometry("950x600+300+100")
        
# A la pantalla principal se le asigna un canvas para que pueda colocarse botones o menús
canvas_pantalla_principal = Canvas(pantalla_principal, bg="white")

#Se extiende el canvas al tamaño total de la ventana principal
canvas_pantalla_principal.pack(fill=tk.BOTH, expand=True)

# Se inicializa la música desde que se muestra la pantalla principal 
#pantalla_principal.after(100, lambda: reproducir_musica(True))

###########################################

#Función que carga la imagen de la pantalla principal 
def carga_imagen_pantalla_principal(imagen_nombre):
    canvas_pantalla_principal.update_idletasks()

#Se obtiene el ancho y alto de la pantalla principal donde se colocará la imagen 
    ancho = canvas_pantalla_principal.winfo_width()
    alto = canvas_pantalla_principal.winfo_height()

    ruta = os.path.join('Imagenes', imagen_nombre)
    imagen = Image.open(ruta)

#Se ajusta la imagen al tamaño de la ventana
    imagen_ajustada = imagen.resize((ancho, alto), Image.LANCZOS)
    imagen_tk = ImageTk.PhotoImage(imagen_ajustada)
        
#Mantiene la imagen de fondo y evita que se borre 
    canvas_pantalla_principal.imagen_fondo = imagen_tk
    #imagen_fondo = imagen_tk 
    canvas_pantalla_principal.create_image(0, 0, image=canvas_pantalla_principal.imagen_fondo, anchor=tk.NW)

# Se llama a la función que mostrará la imagen de fondo al canvas de la pantalla principal 
pantalla_principal.after(200, lambda: carga_imagen_pantalla_principal("Fondo1.png"))



###########################################
#Función que carga la imagen de fondo que tendrá el botón jugar 

def cargar_imagen_boton_jugar(nombre_imagen):
    
    # Se define la ruta de la imagen del botón
    ruta = os.path.join(BASE_DIR, 'Imagenes',nombre_imagen)
    
    # Se abre la ruta donde esta la imagén de fondo del botón 
    imagen = Image.open(ruta)

    # Se define el tamaño (alto y largo) máximo permitido para el botón
    max_ancho, max_alto = 350, 140

    # Se obtiene el tamaño original de la imagen
    ancho_original, alto_original = imagen.size

    # Se calcula la proporción para no deformar la imagen
    proporcion = min(max_ancho / ancho_original, max_alto / alto_original)

    # Se calculan las nuevas dimensiones manteniendo proporción
    nuevo_ancho = int(ancho_original * proporcion)
    nuevo_alto = int(alto_original * proporcion)

    # Se redimensiona la imagen con alta calidad
    imagen = imagen.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)

    # Se convierte la imagen a formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se retorna la imagen lista para usarse en el botón
    return imagen_tk

###########################################

# Función que carga la imagen de los personajes 
def cargar_imagen_personaje(ruta):
    
    # Se abre la ruta de la imagen
    imagen = Image.open(ruta)
    
    # Se ajusta el tamaño de la imagen
    imagen = imagen.resize((100, 100), Image.LANCZOS)
    
    # Se convierte la imagen a formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)
    
    # Se retorna la imagen
    return imagen_tk

###########################################

#Función que evita que se seleccione otra vez el mismo personaje 
def personaje_seleccionado(lista, indice, pos):

    # si el personaje no ha sido seleccionado de los 15 disponibles devuelve False 
    if pos >= len(lista):
        return False

    # Si el personaje ya fue seleccionado y esta en la lista devuelve True
    if lista[pos] == indice:
        return True

    # Se continua con la revisión de la lista e incrementa el indice 
    return personaje_seleccionado(lista, indice, pos + 1)

###########################################
def seleccionar_personaje(indice, boton,ventana):

    # Se llama la función que valida si el personaje ya fue escogido por el usuario 
    resultado_busqueda = personaje_seleccionado(personajes_seleccionados, indice, 0)

    #Se limpia la pantalla que muestra los mensajes de advertencia (personaje seleccionado o cantidad seleccionada)
    ventana.label_mensaje.config(text="")

    # Si el personaje ya fue seleccionado, no hace nada
    if resultado_busqueda == True:
        #Se muestra el mensaje de que el personaje ya fue seleccionado 
        ventana.label_mensaje.config(text="Este personaje ya fue seleccionado")
        return

    # Si todavía no se han seleccionado 3 personajes
    if len(personajes_seleccionados) < 3:
        
        # Se agrega el personaje a la lista de seleccionados
        personajes_seleccionados.append(indice)

        # Se cambia el borde del botón para marcarlo como seleccionado
        boton.config(highlightbackground="yellow", highlightthickness=3)

        # Se muestra en consola cuáles personajes van seleccionados
        print("Personajes seleccionados:", personajes_seleccionados)
        
        #Se muestra la cantidad de guerreros seleccionados por el usuario 
        ventana.label_mensaje.config(
            text=f"Personajes seleccionados: {len(personajes_seleccionados)}/3"
        )

    else:
        
        # se muestra un mensaje de advertencia
        ventana.label_mensaje.config(text="Ya seleccionaste 3 personajes. No puedes elegir más")
        return 

###########################################

# Función que coloca los personajes en pantalla de parametrización 
def mostrar_personajes(indice, fila, columna, rutas, frame,ventana):

    # Si ya no hay más imágenes no se hace nada 
    if indice >= len(rutas):
        return  

    # Se carga la imagen 
    imagen = cargar_imagen_personaje(rutas[indice])

    # Se guarda la referencia para evitar que la imagen desaparezca
    referencias_imagenes.append(imagen)

    # Se crea un botón con cada  imagen
    boton = Button(
                    frame,
                    image=imagen,
                    bg="black",
                    relief="flat",
                    highlightthickness=1,
                    highlightbackground="white"
                )

    # Acción cuando el usuario hace clic
    boton.config(command=lambda: seleccionar_personaje(indice, boton, ventana))
    
    # Se coloca el botón en la posición (fila, columna)
    boton.grid(row=fila, column=columna, padx=5, pady=5)

    # Se incrementa la cantidad de columnas 
    columna = columna + 1

    # Si ya hay 5 columnas, se baja a la siguiente fila (queda 3 filas con 5 personajes cada uno)
    if columna == 5:
        columna = 0
        fila = fila + 1

    # Se llama la función para mostrar el siguiente personaje
    mostrar_personajes(indice + 1, fila, columna, rutas, frame,ventana)

###########################################

#Función que carga las imagenes de los 15 personajes en la pantalla de parametrización 
def crea_personajes(ventana):
    
    #Espacio o frame que contendra las imagenes 
    frame_personajes = Frame(ventana, bg="royalblue4")
    #posición del cuadro donde se colocan los personajes en el eje x, eje y y ancho 
    frame_personajes.place(x=120, y=130, width=590, height=350)
    
    #Se define la ruta de las imagenes de los personajes 
    rutas_personajes = [
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero1_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero2_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero3_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero4_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero5_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero6_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero7_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero8_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero9_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero10_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero11_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero12_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero13_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero14_frente.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Guerrero15_frente.png')
    ]
                       #indice, columna, fila, rutas_personajes, frame_personajes
    mostrar_personajes(0, 0, 0, rutas_personajes, frame_personajes,ventana)

###########################################

# Función que valida si ya hay un avatar seleccionado
def validar_avatar_seleccionado(lista, pos):

    # Si la lista está vacía, no se ha seleccionado un  avatar
    if pos >= len(lista):
        return False
    
    # Si encuentra el id, significa que el avatar ya fue seleccionado
    else: 
        return True
    
###########################################

# Función que permite seleccionar un avatar
def seleccionar_avatar(indice, boton, ventana):

    # Limpia el mensaje anterior en que ya no se puede seleccionar otro avatar 
    ventana.label_mensaje_avatar.config(text="")

    # llama a la función avatar_seleccionado y Se revisa si ya había un avatar seleccionado
    resultado_avatar = validar_avatar_seleccionado(avatar_seleccionado, 0)

    # Si todavía no se ha seleccionado un avatar
    if resultado_avatar == False:

        # Se guarda el índice del avatar seleccionado
        avatar_seleccionado.append(indice)

        # Se marca visualmente el botón del avatar seleccionado 
        boton.config(highlightbackground="yellow", highlightthickness=3)

        # Se muestra en consola
        print("Avatar seleccionado:", avatar_seleccionado)

        # Mensaje en pantalla
        ventana.label_mensaje_avatar.config(text="Avatar seleccionado correctamente")

    else:
        ventana.label_mensaje_avatar.config(text="Ya seleccionaste un avatar. No puedes elegir otro")
        return
###########################################

# Función que coloca los avatars en pantalla de parametrización
def mostrar_avatars(indice, columna, rutas, frame, ventana):

    # Si ya no hay más imágenes, termina
    if indice >= len(rutas):
        return

    # Se carga la imagen
    imagen = cargar_imagen_personaje(rutas[indice])

    # Se guarda la referencia para evitar que desaparezca
    referencias_imagenes.append(imagen)

    # Se crea el botón con la imagen
    boton = Button(
                    frame,
                    image=imagen,
                    bg="RoyalBlue4",
                    relief="solid",
                    bd=2,
                    highlightthickness=1,
                    highlightbackground="black"
                )

    # Acción cuando el usuario hace clic
    boton.config(command=lambda: seleccionar_avatar(indice, boton, ventana))

    # Se coloca en una sola fila los 3 avatares
    boton.grid(row=0, column=columna, padx=3, pady=3)

    # En la llamada recursiva se incrementa el indice y la columna 
    mostrar_avatars(indice + 1, columna + 1, rutas, frame, ventana)

###########################################


# Función que carga las imágenes de los 3 avatars
def crea_avatars(ventana):

    # Frame donde se colocarán los avatares
    frame_avatars = Frame(ventana, bg="white")

    # Posición del frame
    frame_avatars.place(x=130, y=555, width=340, height=110)

    # Rutas de las imagenes donde están ubicados los avatares
    rutas_avatars = [
        os.path.join(BASE_DIR, 'Imagenes', 'Avatar1.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Avatar2.png'),
        os.path.join(BASE_DIR, 'Imagenes', 'Avatar3.png')
    ]

    #              (indice, columna,rutas_avatars, frame_avatars, ventana )
    mostrar_avatars(0,         0,   rutas_avatars, frame_avatars, ventana)

###########################################
# Función que permite iniciar el registro del juego  Coloca los label, cuadro de texto y botón sobre el canvas     
def boton_inicio():
    
    #Se vacía la lista de los personajes seleccionados por el usuario si este se sale de la pantalla 
    personajes_seleccionados.clear()

    #Se vacía la lista global que almacena los personajes que fueron elegidos al inicio, cuando se pierde se debe volver a escoger los personajes 
    personajes_base.clear() 

    #Se vacía la lista del avatar seleccionado por el usuario si este se sale de la pantalla 
    avatar_seleccionado.clear()
    
    #Toplevel: permite abrir una ventana secundaria sobre la ventana principal (para escribir el nombre del usuario) 
    ventana_boton_inicio = Toplevel(pantalla_principal)
    ventana_boton_inicio.title("Parametrización") # Da el nombre a la ventana del nombre del jugador 
    ventana_boton_inicio.geometry("800x690+410+80") # Se define el tamaño  de la ventana para que el usuario ingrese su nombre  + posición eje x + posición eje  y
    ventana_boton_inicio.resizable(False, False) # Evita que se pueda aumentar o disminuir el tamaño de la ventana 
    
    # mantiene la ventana del botón jugar siempre al frente
    ventana_boton_inicio.attributes('-topmost', True)
    
    # Se coloca una imagen a la pantalla  de parametrización
    ruta_imagen_fondo = os.path.join(BASE_DIR, 'Imagenes', 'Fondo5.png')  # Ruta donde esta ubicada la imagen 
    print(f"Ruta de la imagen: {ruta_imagen_fondo}") 
    imagen_fondo = Image.open(ruta_imagen_fondo) # Abre la carpeta donde esta colocada la imagen 
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo.resize((800, 750), Image.LANCZOS))  # Redimensiona la imagen 

##### 
    # Se dibuja la imagen del botón de play sobre el canvas de la pantalla de parametrización 
    canvas_param = Canvas(ventana_boton_inicio, width=800, height=690, highlightthickness=0, bd=0)
    canvas_param.place(x=0, y=0)

    # Se dibuja la imagen de fondo del canvas en la pantalla de parametrización 
    canvas_param.create_image(400, 345, image=imagen_fondo_tk)

    # Guarda la imagen del fondo de la pantalla de parametrización en memoria 
    canvas_param.imagen_fondo = imagen_fondo_tk

#####    
    #Creación del label para indicarle al jugador que digite su nombre 
    label_nombre_jugador = Label(ventana_boton_inicio, text="Ingrese su nombre de jugador:", bg="RoyalBlue4", fg="white")  # Etiqueta para indicar que debe digitar su nombre de jugador 
    label_nombre_jugador.pack(pady=10)

#####    
    #Creación de cuadro de texto para que el jugador digite su nombre 
    cuadro_texto_nombre=Entry(ventana_boton_inicio,width=27,bg="white")# crea la caja de texto para digitar el nombre de jugador
    cuadro_texto_nombre.pack(pady=10)

#####
 #Creación del label para indicarle al jugador que seleccione los personales
    label_nombre_personajes = Label(ventana_boton_inicio, text="Seleccione 3 personajes:", bg="RoyalBlue4", fg="white")  # Etiqueta para indicar que se escoja los personaje por usar 
    label_nombre_personajes.pack(pady=12)

#####
 #Creación del label para indicarle al jugador que seleccione su avatar
    label_nombre_avatar = Label(ventana_boton_inicio, text="Seleccione su avatar:",bg="RoyalBlue4",fg="white")
    label_nombre_avatar.place(x=320, y=520)

#####
# Se llama a la función que crea los personajes 
    crea_personajes(ventana_boton_inicio)

# Se llama a la función que crea los avatars
    crea_avatars(ventana_boton_inicio)

#####
    #Creación de label que mostrará el mensaje de advertencia de no seleccionar más de 3 personajes 
    label_mensaje = Label(ventana_boton_inicio,
                          text="", 
                          bg="black", 
                          fg="yellow", 
                          font=("Arial", 12))
    label_mensaje.place(x=290, y=480)

    # Se guarda la referencia en la ventana
    ventana_boton_inicio.label_mensaje = label_mensaje

#####  
    #Creación de label que mostrará el mensaje de advertencia de no seleccionar un avatar o escoger más de 1 avatar    
    label_mensaje_avatar = Label(
                                    ventana_boton_inicio,
                                    text="",
                                    bg="black",
                                    fg="cyan",
                                    font=("Arial", 12)
                                    )
    label_mensaje_avatar.place(x=250, y=660)

    # Se guarda la referencia del label mensaje de advertencia avatar en la ventana
    ventana_boton_inicio.label_mensaje_avatar = label_mensaje_avatar

#####  
    imagen_boton_jugar_param = cargar_imagen_boton_jugar("Fondo2.png")

    # Se dibuja el botón sobre el canvas de la pantalla de parametrización 
    id_boton_jugar = canvas_param.create_image(595, 610, image=imagen_boton_jugar_param)

    # Se guarda la imagen del botón en memoria 
    canvas_param.imagen_boton = imagen_boton_jugar_param

    # Evento clic del botón iniciar juego (play)
        #tag_bind: sirve para detectar eventos en el canvas 
    canvas_param.tag_bind(
                            id_boton_jugar,
                            #button-1 se acciona cuando se da clic izquierdo con el mouse
                            "<Button-1>",
                            lambda event: valida_inicio_juego(cuadro_texto_nombre, ventana_boton_inicio)
                         )

###########################################

# Función que crea y muestra el botón de inicio en la pantalla principal
def crear_boton_inicio():
    
    # Se obtiene la imagen del botón llamando a la función de carga
    imagen_boton = cargar_imagen_boton_jugar("Fondo4.png")

      # se dibuja directamente la imagen sobre el canvas (se le da una ubicación al botón)

    id_boton = canvas_pantalla_principal.create_image(800, 320, image=imagen_boton)

    # Se guarda la referencia de la imagen para evitar que se borre
    canvas_pantalla_principal.imagen_boton = imagen_boton

    # Función que detecta el clic sobre la imagen
    def click_boton(event):
        boton_inicio()

    # Se enlaza el clic izquierdo del mouse con la imagen del botón
    canvas_pantalla_principal.tag_bind(id_boton, "<Button-1>", click_boton)


# Se crea el botón después de que el fondo ya fue dibujado
pantalla_principal.after(300, crear_boton_inicio)

###########################################

# Función que abre la ventana del juego y muestra el mapa 
def abrir_ventana_juego():

    #Se crea una ventana encima de la pantalla principal 
    ventana_juego = Toplevel(pantalla_principal)
    
    #Se da un nombre a la pantalla del mapa
    ventana_juego.title("Epic Adventure")
    
    #Se define el tamaño de la ventana (tamaño de la ventana, posición eje "x", posición eje "y")
    ventana_juego.geometry("900x600+300+100")
    
    #Se bloquea la opción de aumentar o disminuir el tamaño de la ventana
    ventana_juego.resizable(False, False)

    canvas_juego = colocar_fondo_mapa(ventana_juego)

    #Se llama a la función que crea las 5 ubicaciones sobre el mapa 
    crear_ubicaciones_mapa(canvas_juego)

    # Se dibuja sobre la imagen el texto "Mapa del juego"
    canvas_juego.create_text(
                                450, 50,
                                text="Mapa del juego",
                                fill="white",
                                font=("Arial", 24, "bold")
                            )
###########################################

# Función que valida los datos antes de iniciar el juego
def valida_inicio_juego(cuadro_texto_nombre, ventana):

    # Se obtiene el nombre escrito por el usuario
    nombre_jugador = cuadro_texto_nombre.get()

    # Limpia mensajes anteriores
    ventana.label_mensaje.config(text="")
    ventana.label_mensaje_avatar.config(text="")

    # Si el nombre está vacío
    if nombre_jugador == "":
        ventana.label_mensaje.config(text="Debe escribir su nombre de jugador")
        return

    # Si no ha seleccionado 3 personajes
    if len(personajes_seleccionados) != 3:
        ventana.label_mensaje.config(text="Debe seleccionar 3 personajes")
        return

    # Si no ha seleccionado avatar
    if len(avatar_seleccionado) != 1:
        ventana.label_mensaje_avatar.config(text="Debe seleccionar 1 avatar")
        return
    
    # Se cierra la ventana de parametrización 
    ventana.destroy()

    #Se guarda los 3 personajes escogidos en la parametrización para que una vez que se gane una partida el siguiente reino use los mismos personajes 
    personajes_base.clear() 
    personajes_base.append(personajes_seleccionados[0]) 
    personajes_base.append(personajes_seleccionados[1]) 
    personajes_base.append(personajes_seleccionados[2])
    
    # Si todo está correcto, se abre la ventana del juego
    abrir_ventana_juego()

###########################################
#Función que coloca el fondo a la pantalla de juego 
def colocar_fondo_mapa(ventana):

    # Ruta de la imagen del mapa
    ruta_mapa = os.path.join(BASE_DIR, 'Imagenes', 'Fondo6.png')

    # Se abre la ruta donde se encuentra la imagen 
    imagen_mapa = Image.open(ruta_mapa)

    # Se ajusta el tamaño de la imagen al tamaño de la ventana del juego 
    imagen_mapa = imagen_mapa.resize((900, 600), Image.LANCZOS)

    # Se convierte la imangen al formato que pueda usar tkinter
    imagen_mapa_tk = ImageTk.PhotoImage(imagen_mapa)

    # Creación del canvas que contendrá el mapa 
    canvas_mapa = Canvas(ventana, width=900, height=600, highlightthickness=0, bd=0)
    canvas_mapa.place(x=0, y=0)

    # Dibujar la imagen en el centro del canvas
    canvas_mapa.create_image(450, 300, image=imagen_mapa_tk)

    # Guardar referencia para que no desaparezca
    canvas_mapa.imagen_fondo = imagen_mapa_tk

    return canvas_mapa

###########################################

# Basado en:
# Python Software Foundation. (s.f.). Módulo csv.
# https://docs.python.org/3/library/csv.html
# Adaptado a recursividad para este proyecto
# Apoyo de la IA chatgpt

#Función que cargar los personajes del archivo CSV 
def cargar_personajes_csv():

    #Se abre la ruta que contiene el archivo csv que 
    ruta = os.path.join(BASE_DIR, "Personajes.csv")
    
    #Lista que guardará todos los personajes 
    personajes = []

    #Se abre el archivos CSV
    with open(ruta, newline='', encoding='utf-8') as archivo:

        #Convierte cada filas del CSV en un diccionario 
        lector = csv.DictReader(archivo)
    
        """   {
            "nombre": "Maga del bosque",
            "imagen": "Guerrero1_frente.png",
            "vida": "78",
            "ataque": "82",
            "defensa": "58"
            } """

        return leer_csv(lector, personajes)

#############

# Función que va leyendo una a una las filas del archivo CSV
def leer_csv(lector, personajes):

    try:
        # Obtiene la siguiente fila del CSV
        fila = next(lector)

        #Convierte la fila en un objeto 
        personaje = {
            "nombre": fila["nombre"],
            "imagen": fila["imagen"],
            "vida": int(fila["vida"]),
            "ataque": int(fila["ataque"]),
            "defensa": int(fila["defensa"])
        }
        #Se agrega el personaje a la lista 
        personajes.append(personaje)

        # Llamada recursiva
        return leer_csv(lector, personajes)
    
    #Se detiene la lectura del CSV cuando ya no hay másfilas 
    except StopIteration:
        return personajes

#Se llama a la función que lee el archivo SCV y guarda el resultado en la variable "personajes"  
    # cargar los datos del CSV y los guarda en memoria {'nombre': 'Maga del bosque', 'ataque': 82, ...}  
personajes = cargar_personajes_csv()

###########################################
###########################################
#Función que carga los hollows del archivo CSV
def cargar_hollows_csv():

    #Se abre la ruta que contiene el archivo CSV de los hollows
    ruta = os.path.join(BASE_DIR, "Hollows.csv")

    #Lista que guardará todos los hollows
    hollows = []

    #Se abre el archivo CSV
    with open(ruta, newline='', encoding='utf-8') as archivo:

        #Convierte cada fila del CSV en un diccionario
        lector = csv.DictReader(archivo)

        return leer_hollows_csv(lector, hollows)

###########################################

#Función que va leyendo una a una las filas del archivo CSV de hollows
def leer_hollows_csv(lector, hollows):

    try:
        #Obtiene la siguiente fila del CSV
        fila = next(lector)

        #Convierte la fila en un objeto
        hollow = {
            "ubicacion": int(fila["ubicacion"]),
            "nombre": fila["nombre"],
            "imagen": fila["imagen"],
            "vida": int(fila["vida"]),
            "ataque": int(fila["ataque"]),
            "defensa": int(fila["defensa"])
        }

        #Se agrega el hollow a la lista
        hollows.append(hollow)

        #Llamada recursiva
        return leer_hollows_csv(lector, hollows)

    #Se detiene la lectura del CSV cuando ya no hay más filas
    except StopIteration:
        return hollows

###########################################

#Se llama a la función que lee el archivo CSV de hollows
hollows = cargar_hollows_csv()

###########################################

# Función que valida si la siguiente ubicación esta disponible o esta bloqueada 
def seleccionar_ubicacion_mapa(indice, canvas_mapa):

    # Se valida que el jugador solo pueda acceder a la siguiente ubicación disponible
    if indice == canvas_mapa.ubicacion_actual[0] + 1:


        print("Ingresando a la ubicación:", indice + 1)

        # Se borra cualquier mensaje anterior del mapa
        canvas_mapa.delete("mensaje_mapa")  

        # Mensaje que indica a qué ubicación avanzó
        canvas_mapa.create_text(
                            450, 560,
                            text=f"Ingresando a la ubicación {indice + 1}",
                            fill="white",
                            font=("Arial", 16, "bold"),
                            tags="mensaje_mapa"  
                          )

        # Se llama a la función que abre la pantalla de batalla, pero todavía no se actualiza la ubicación 
            #Ingresar a la batalla no significa que se ganó esta (en caso de que el usuario abra y cierra la ventana )
        iniciar_ventana_batalla(indice, canvas_mapa)
        return  

    # Si la ubicación ya fue superada o todavía no está disponible, se bloquea
    canvas_mapa.delete("mensaje_mapa") 

    canvas_mapa.create_text(
                        450, 560,
                        text="Ubicación bloqueada",
                        fill="red",
                        font=("Arial", 16, "bold"),
                        tags="mensaje_mapa"  
                      )        

###########################################
# Función que coloca las 5 ubicaciones en el mapa
def crear_ubicaciones_mapa(canvas):

    canvas.ubicacion_actual = [-1]
    # Lista que contiene la ubicación y el nombre de cada zona de juego(x,y,nombre)
    ubicaciones = [
                    (120, 420, "Desierto","Desierto.png"),
                    (780, 460, "Castillo","Castillo.png"),
                    (300, 250, "Selva","Selva.png"),
                    (30, 180, "Nieve", "Nieve.png"),
                     (490, 110, "Volcán", "Volcan.png"),
                    
                    ]

    mostrar_ubicaciones_mapa(0, ubicaciones, canvas)

###########################################

# Función que valida si una ubicación del mapa puede ser seleccionada
    #Será utilizada en la función mostrar_ubicaciones_mapa()
def clic_ubicacion_mapa(indice, canvas):

    # Solo permite ingresar a la siguiente ubicación disponible que sea mayor a la actual
     #Si esta en la primera ubicación "desierto" solo podrá acceder a la ubicación #2 "Selva"
        #Es decir no se podrá retroceder o avanzar a otras ubicaciones superiores que no sea la correcta
    if indice == canvas.ubicacion_actual[0] + 1: 
        seleccionar_ubicacion_mapa(indice, canvas)  
        return 

    # Si la ubicación ya fue superada o aún no está disponible, se bloquea
        #Se muestra el mensaje de que la ubicación esta bloqueada 
    canvas.delete("mensaje_mapa")  
    canvas.create_text(
                        450, 560,
                        text="Ubicación bloqueada",
                        fill="white",
                        font=("Arial", 16, "bold"),
                        tags="mensaje_mapa"
                      )
###########################################



# Función que dibuja las ubicaciones del mapa
def mostrar_ubicaciones_mapa(indice, ubicaciones, canvas):

    # si ya se recorrió toda la lista de ubicaciones, se detiene
    if indice >= len(ubicaciones):
        return
   
    ubicacion = ubicaciones[indice]

    # Cada ubicación tiene: (posición eje x, posición eje y, nombre de la ubicación , imagen)
    x = ubicacion[0]
    y = ubicacion[1]
    nombre = ubicacion[2]

    # Si se esta en la primera ubicación "Desierto" se coloca la imagen de este 
    if indice == 0:
        imagen_ubicacion = "Desierto.png"

    # Si se esta en la segunda ubicación "Castillo" se coloca la imagen de este 
    elif indice == 1:
        imagen_ubicacion = "Castillo.png"

    # Si se esta en la tercera ubicación "Selva" se coloca la imagen de este 
    elif indice == 2:
        imagen_ubicacion = "Selva.png"

    # Si se esta en la cuarta ubicación "Nieve" se coloca la imagen de este 
    elif indice == 3:
        imagen_ubicacion = "Nieve.png"

    # Si se esta en la primera ubicación "Volcan" se coloca la imagen de este 
    elif indice == 4:
        imagen_ubicacion = "Volcan.png"

    #Se accede a la ruta donde esta las imagenes de las locaciones 
    ruta_imagen = os.path.join(BASE_DIR, 'Imagenes', imagen_ubicacion)

    # Se carga y ajusta la imagen
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((65, 65), Image.LANCZOS)
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda la referencia de las imágenes para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Se dibuja la imagen en el mapa
    icono = canvas.create_image(x, y, image=imagen_tk)

    # Dibuja el nombre de la ubicación debajo de la imagen
    texto = canvas.create_text(
                                x,
                                y + 45,
                                text=nombre,
                                fill="white",
                                font=("Arial", 10, "bold")
                            )

    # Se asigna el clic al icono de la ubicación
        # Se llama a la función clic_ubicacion_mapa para validar si la ubicación esta bloquead o no 
            # canvas.tag_bind: es una función en tkinter que sirve para detectar eventos con el clic
    canvas.tag_bind(
                        icono,
                        "<Button-1>", #clic izquierdo
                        lambda event, i=indice: clic_ubicacion_mapa(i, canvas) 
                    )

    # Se asigna la posibilidad de acceder a la ubicación si se da  clic al texto
        # Se llama a la función clic_ubicacion_mapa para validar si la ubicación esta bloquead o no 
            # canvas.tag_bind: es una función en tkinter que sirve para detectar eventos con el clic 
    canvas.tag_bind(
                        texto,
                        "<Button-1>", #clic izquierdo 
                        lambda event, i=indice: clic_ubicacion_mapa(i, canvas)  
                    )

    

    # Llamada recursiva para la siguiente ubicación
    mostrar_ubicaciones_mapa(indice + 1, ubicaciones, canvas)

###########################################

#Función que crea la pantalla para iniciar la batalla del juego 
def iniciar_ventana_batalla(indice, canvas_mapa):

#######
    #Se crea la ventana de batalla  
    ventana_batalla = Toplevel(pantalla_principal)

    #Se da el nombre a la ventana de btallas 
    ventana_batalla.title("Batalla contra Hollow")

    #Se define el tamaño que tiene la pantalla de batallas 
    ventana_batalla.geometry("700x500+385+150")

    #Se impide ampliar el tamaño de la pantalla de batallas 
    ventana_batalla.resizable(False, False)

#######
    #Se define los fondos de pantalla que tendrá cada escenario de lucha 
    if indice == 0:
        fondo_batalla = "FondoBatallaDesierto.png"
    elif indice == 1:
        fondo_batalla = "FondoBatallaCastillo.png"
    elif indice == 2:
        fondo_batalla = "FondoBatallaSelva.png"
    elif indice == 3:
        fondo_batalla = "FondoBatallaNieve.png"
    elif indice == 4:
        fondo_batalla = "FondoBatallaVolcan.png"
    else:
        fondo_batalla = "FondoBatallaDesierto.png"

#######
    # Se crea el canvas donde se colocará la imagen de fondo de la pantalla de batallas 
    canvas_batalla = Canvas(ventana_batalla, width=700, height=500, highlightthickness=0)
    canvas_batalla.place(x=0, y=0)

#######
    # Se guarda referencia al canvas del mapa para actualizar progreso solo si gana
        # Viene de la función seleccionar_ubicacion_mapa(...)
    canvas_batalla.canvas_mapa = canvas_mapa 

#######
    # Se guarda cuál es la ubicación que se está peleando (desierto, selva, etc)
        # Viene de la función seleccionar_ubicacion_mapa(indice, canvas)
        # donde la ubicación "desierto" es el indice =0, ubicación "castillo", es el indice 1, etc.
    canvas_batalla.indice_ubicacion = indice 

#######
    #Variable que inicializa la vida del enemigo con 100 puntos de vida (cada vez que se ingresa a la pantalla de batalla se inicializa con 100) 
    canvas_batalla.vida_enemigo = 100

#######
    # Se define la ruta donde se encuentra las imagenes de fondo de la pantalla de batalla 
    ruta_fondo = os.path.join(BASE_DIR, 'Imagenes', fondo_batalla)

    # Se abre la ruta donde se encuentra la imagen de fondo de la pantalla de batalla 
    imagen_fondo = Image.open(ruta_fondo)

    # Se ajusta la imagen de fondo de la pantalla de batalla  al mismo tamaño de la ventana 
    imagen_fondo = imagen_fondo.resize((700, 500), Image.LANCZOS)

    #Se convierte la imagen en un formato que tkinter pueda usar 
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)

    # Se dibuja la imagen sobre el canvas 
    canvas_batalla.create_image(350, 250, image=imagen_fondo_tk)

    # Se evita que la imagen de la pantalla de batalla desaparezca 
    canvas_batalla.imagen_fondo = imagen_fondo_tk

#######    
    # Se llama a la función que carga la imagenes de los guerrero en la pantalla de juego 
    mostrar_avatar_batalla(canvas_batalla)

#######
    # Se crea la lista vacía donde se guardará el ID de los personajes guerreros
    canvas_batalla.ids_guerreros = []

#######
    # Se crea la lista vacía donde se almacenará la posición de los guerreros 
    canvas_batalla.posiciones_guerreros = []

#######
#Se guarda la vida de los personajes 

    # Se define una lista vacía donde se guardarán las vidas
    canvas_batalla.vidas_guerreros = []

    # ===== PERSONAJE 1 =====

    # AL indice 1 se le asigna al primer personaje seleccionado en la pantalla de parametrización  
    indice1 = personajes_seleccionados[0]             
    personaje1 = personajes[indice1]
    #Se obtiene la vida del personaje del CSV                
    vida1 = personaje1["vida"]           
    # Se guarda la vida del personaje 
    canvas_batalla.vidas_guerreros.append(vida1)     

    # ===== PERSONAJE 2 =====
    # AL indice 1 se le asigna al primer personaje seleccionado en la pantalla de parametrización 
    indice2 = personajes_seleccionados[1]
    personaje2 = personajes[indice2]
    #Se obtiene la vida del personaje del CSV 
    vida2 = personaje2["vida"]
    # Se guarda la vida del personaje 
    canvas_batalla.vidas_guerreros.append(vida2)

    # ===== PERSONAJE 3 =====

    # AL indice 1 se le asigna al primer personaje seleccionado en la pantalla de parametrización 
    indice3 = personajes_seleccionados[2]
    personaje3 = personajes[indice3]
    #Se obtiene la vida del personaje del CSV 
    vida3 = personaje3["vida"]
    # Se guarda la vida del personaje 
    canvas_batalla.vidas_guerreros.append(vida3)
#######

    # Se llama a la función que carga la imagen del avatar en la pantalla de juego 
    mostrar_personajes_batalla(0, canvas_batalla)

#######
    #Se llama a la función que muestra el botón de fight 
    mostrar_boton_fight(canvas_batalla)

#######
    #Vida del jugador 
        #Se crea la variable de vida del jugador que se irá restanto conforme ataque el Hollow
    canvas_batalla.vida_jugador = 100
        #Se crea vida máxima del jugador que servirá como referencia porcentual de cuanta vida le queda al jugador 
            # Por ejemplo 30 / 100 = 0.3 → 30% de la barra de vida es lo que le queda al jugador 
    canvas_batalla.vida_maxima_jugador = 100

#######

    # Se inicializa la cantidad de acompañantes (función obtener_acompanantes_hollows) que tendrán los hollows en una lista vacía 
    canvas_batalla.acompanantes = obtener_acompanantes_hollows(2, [])

#######
    # Se obtiene el hollow correspondiente a la ubicación seleccionada del mapa
    hollow_actual = hollows[indice]

    # Se guardan los atributos del hollow dentro del canvas de batalla
    canvas_batalla.hollow_actual = hollow_actual
    canvas_batalla.vida_hollow = hollow_actual["vida"]
    canvas_batalla.ataque_hollow = hollow_actual["ataque"]
    canvas_batalla.defensa_hollow = hollow_actual["defensa"]

#######
    #Lista vacía que contendrá a los enemigos (acompañantes de los hollows)
    canvas_batalla.enemigos = []

    # # Se agrega el hollow como enemigo principal dentro de la lista de batalla,
    # copiando sus atributos desde el CSV para integrarlo al sistema de combate
    canvas_batalla.enemigos.append({
                                    "tipo": "hollow",
                                    "nombre": hollow_actual["nombre"],
                                    "vida": hollow_actual["vida"],
                                    "vida_maxima": hollow_actual["vida"],
                                    "ataque": hollow_actual["ataque"],
                                    "defensa": hollow_actual["defensa"],
                                    "imagen": hollow_actual["imagen"]
                                }) 
    
    #Se llama a la función que agrega los enemigos con sus atributos 
    enemigos(0, canvas_batalla)

    # Se inicializa el enemigo actual en la posición 0
        # La posición 0 corresponde al Hollow principal
    canvas_batalla.enemigo_actual = 0 

#######

    #Se llama a la función que dibuja la barra de vida el hollow
    barra_vida_hollow(canvas_batalla)

######
    #Se llama a la función que coloca la imagen del hollow en la pantalla de batallas 
    imagen_hollow_batalla(canvas_batalla)

######
    
    #Lista que guardará los IDs de las imágenes de los acompañantes enemigos
        # Viene de la función iniciar_ventana_batalla(indice)
        # Se utiliza para almacenar los identificadores (IDs) que devuelve canvas.create_image()
        # Permitirá posteriormente eliminar visualmente a los enemigos derrotados usando canvas.delete()
    canvas_batalla.ids_enemigos = []  

#######
    # Se llama a la función que coloca la imagen de los acompañantes del hollow en la pantalla de batallas
     # Viene de la función acompanantes_hollow(posicion, canvas)   
    acompanantes_hollow(0, canvas_batalla)

###########################################
# Función que coloca a los guerreros sobre la pantalla  
def mostrar_personajes_batalla(posicion, canvas):


    # Si ya se rrecorrio la cantidad de personajes (3) no se debe hacer nada más
    if posicion >= len(personajes_seleccionados):
        return

    # Se obtiene el índice del personaje seleccionados en la pantalla de configuración 
    indice_personaje = personajes_seleccionados[posicion]

    # Como los personajes son guardados en una lista con el indice 0 se le suma 1 para que tome el valor correcto iniciando en 1
    numero = indice_personaje + 1

    # Se crea automáticamente el nombre de la imagen usando el número del personaje.
        #Por ejemplo: Guerrero1_espalda.png (donde número es igual al valor que tiene la lista almacenada con el ID del personaje seleccionado)
    nombre_archivo = f"Guerrero{numero}_espalda.png"
    #Define la ruta donde se tomarán las imagenes de los guerreros 
    ruta = os.path.join(BASE_DIR, "Imagenes", nombre_archivo)

    # Se carga la imagen de los guerreros de la ruta previamente definidad
    imagen = Image.open(ruta)
    #Se define el tamaño de las imagens 
    imagen = imagen.resize((140, 140), Image.LANCZOS)
    #Se convierte la imagen del guerrero en un formato que pueda usar tkinter 
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda referencia para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Posición horizontal de guerreros en pantalla
        #la posición se multiplica por la distancia entre cada imagen
    x = 80 + (posicion * 120)
    y = 380

    #Se crea la imagen del guerrero en el canvas y se guarda su ID
    id_guerrero = canvas.create_image(x, y, image=imagen_tk)

    # Se guarda el ID del guerrero en una lista. Por ejemplo [5, 6, 7]
    canvas.ids_guerreros.append(id_guerrero)

    # Se guarda la posición en la que esta colocada la imagen del guerrero. Por ejemplo [(180, 380), (280, 380), (380, 380)] 
    canvas.posiciones_guerreros.append((x, y))

    # Permite que se pueda dar clic sobre cada unos de los guerreros en pantalla 
    canvas.tag_bind(
                        id_guerrero,
                        "<Button-1>",
                        lambda event, p=posicion: seleccionar_guerrero_batalla(p, canvas) #Se llama a la función "seleccionar_guerrero_batalla" que permite que el guerrero se mueva hacia adelante 
                    )

    # Se llama a la función y se incrementa en uno la posición para el siguiente personaje 
    mostrar_personajes_batalla(posicion + 1, canvas)

 

###########################################
# Función que coloca el avatar seleccionado sobre la pantalla de batalla
def mostrar_avatar_batalla(canvas):

    # Si no hay avatar seleccionado, no hace nada
    if len(avatar_seleccionado) == 0:
        return

    # Se obtiene el índice del avatar seleccionado
    indice_avatar = avatar_seleccionado[0]

    # Como el índice inicia en 0, se suma 1 para formar el nombre del archivo
    numero = indice_avatar + 1

    # Se crea automáticamente el nombre de la imagen del avatar
        #Por ejemplo: Avatar1.png (donde número es igual al valor que tiene la lista almacenada con el ID del personaje seleccionado)
    nombre_archivo = f"Avatar{numero}.png"

    # Define la ruta donde está la imagen del avatar
    ruta = os.path.join(BASE_DIR, "Imagenes", nombre_archivo)

    # Se carga la imagen del avatar
    imagen = Image.open(ruta)

    # Se define el tamaño del avatar
    imagen = imagen.resize((80, 80), Image.LANCZOS)

    # Se convierte la imagen a formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda referencia para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Posición del avatar en pantalla
    x = 80
    y = 280

    # Se dibuja el avatar sobre el canvas
    canvas.create_image(x, y, image=imagen_tk)

###########################################

#Referencia: Función generada con Chat GPT 

# Función que selecciona cuál guerrero irá a pelear (se colocará al guerrero un paso más arriba que los otros personajes)
def seleccionar_guerrero_batalla(posicion, canvas):

    # Se valida si ya en el canvas hay un guerrero seleccionado
        #hasattr sirve para saber si hay un guerrero seleccionado; sino, no se hace nada
            #hasattr necesita dos parámetros (objeto, nombre del atributo)
                                            #(donde se guarda el objeto "canvas", id del guerrero seleccionado)
    if hasattr(canvas, "guerrero_seleccionado"):

        #Si había un guerrero seleccionado se guarda su ubicación actual en la variable guerrero_anterior 
        guerrero_anterior = canvas.guerrero_seleccionado

        # Se obtiene la posición original del guerrero que actualmente esta seleccionado (x, y)
        posicion_anterior = canvas.posiciones_guerreros[guerrero_anterior]

        #Se determina la posición previa del guerrero en la posicón "x" y posición "y"
        x_anterior = posicion_anterior[0]
        y_anterior = posicion_anterior[1]

        # Se obtien el ID del guerrero anterior
        id_anterior = canvas.ids_guerreros[guerrero_anterior]

        # Se devuelve el guerrero a su lugar original
        canvas.coords(id_anterior, x_anterior, y_anterior)

    # Se guardaa el nuevo guerrero seleccionado
    canvas.guerrero_seleccionado = posicion

    # Se obtiene la posición original del nuevo guerrero 
    posicion_actual = canvas.posiciones_guerreros[posicion]
    
    #Se obtiene la posición actual en el eje "x" y "y" del guerrero 
    x_actual = posicion_actual[0]
    y_actual = posicion_actual[1]

    # Obtener el ID del guerrero actual
    id_actual = canvas.ids_guerreros[posicion]

    # Se mueve el guerrero hacia adelante (sube 40 px)
    canvas.coords(id_actual, x_actual, y_actual - 40)

    #Se muestra el mensaje en consola ---
    print("Guerrero enviado a pelear:", posicion)

#######
    #Se llama a la función que dibuja la barra de vida de los guerreros 
    barra_vida_guerrero(canvas)

###########################################
# Función que coloca el botón Fight en la pantalla de batalla
def mostrar_boton_fight(canvas):

    # Se define la ruta de la imagen del botón Fight
    ruta = os.path.join(BASE_DIR, "Imagenes", "Fight.png")

    # Se abre la ruta que tiene imagen del botón
    imagen = Image.open(ruta)

    # Se ajusta el tamaño del botón
    imagen = imagen.resize((180, 70), Image.LANCZOS)

    # Se convierte la imagen a formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda referencia de la imagen del botón fight para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Se dibuja el botón fight debajo de los personajes
    id_boton_fight = canvas.create_image(180, 485, image=imagen_tk)

    # Se guarda la imagen del botón Fight dentro del canvas
    canvas.imagen_boton_fight = imagen_tk

    # Se permite dar clic sobre el botón Fight
    canvas.tag_bind(
                        id_boton_fight,
                        "<Button-1>",
                        lambda event: clic_boton_fight(canvas) # Se llama a la función clic_boton_fight que determina los puntos de ataque del personaje
                    )

###########################################

""" #Función que controla el ataque de los personajes guerreros 
def clic_boton_fight(canvas):

    # Se valida que se haya seleccionado un guerrero
    if not hasattr(canvas, "guerrero_seleccionado"):
        print("No has seleccionado un guerrero")
        return

    # Se obtiene el id de posición del guerrero que eligió el jugador para atacar (0,1,2)
        # 0 = primer guerrero
        # 1 = segundo guerrero
        # 2 = tercer guerrero
    posicion = canvas.guerrero_seleccionado

    # Índice real del CSV con base en la posición de los 3 personajes selecionado para luchar 
     #Por ejemplo el personaje de la posición #2 de los 3 que escogí para luchar, corresponde al personaje #7 del CSV. Por eso, se hace alusión 
        # a la función def seleccionar_personaje que contiene la variable "personajes_seleccionados". 
            # Por ejemplo personaje id 7 del CSV [corresponde a la posición #2 en el campo de batalla]
    indice_real = personajes_seleccionados[posicion]

    # Se obtiene los puntos de ataque del personaje con base en el ID de este en el archivo CSV (lista personajes)
    ataque = personajes[indice_real]["ataque"]

    # Se resta vida al enemigo con base en el ataque del personaje guerrero
    canvas.vida_enemigo -= ataque

    # Mostrar en consola
    print("Daño realizado:", ataque)
    print("Vida restante enemigo:", canvas.vida_enemigo)

    # Se muestra en pantalla un texto con la cantidad de ataque generada por el guerrero 
    canvas.create_text(
                            350, 420,
                            text=f"Daño: {ataque}",
                            fill="red",
                            font=("Arial", 16, "bold")
                        )

    #Se muestra un texto que indica la vida actual del enemigo tras el ataque 
    canvas.create_text(
                            350, 450,
                            text=f"Vida enemigo: {canvas.vida_enemigo}",
                            fill="white",
                            font=("Arial", 14, "bold")
                        )

    # Se valida si la vida del enemigo es igual o menor a 0 y alerta que ha muerto 
    if canvas.vida_enemigo <= 0:
        canvas.create_text(
                            350, 250,
                            text="¡ENEMIGO DERROTADO!",
                            fill="yellow",
                            font=("Arial", 22, "bold")
                             ) """

###########################################

#Función que controla el ataque de los personajes guerreros 
def clic_boton_fight(canvas):

    # Se valida que se haya seleccionado un guerrero para luchar (si se presiona el botón fight sin guerrero no se hace nada)
    if not hasattr(canvas, "guerrero_seleccionado"):
        print("No has seleccionado un guerrero")
        return

    # Se obtienela posición del guerrero seleccionado en la pantalla [0, 1, 2]
    posicion_en_pantalla = canvas.guerrero_seleccionado

    # Se valida si el guerrero seleccionado ya no tiene vida (no puede atacar)
        # Se obtiene la posición del guerrero seleccionado en pantalla
    if canvas.vidas_guerreros[posicion_en_pantalla] <= 0: 
        canvas.delete("mensaje_batalla")  

        canvas.create_text(
                            350, 450,
                            text="Este guerrero está KO y no puede luchar",
                            fill="white",
                            font=("Arial", 14, "bold"),
                            tags="mensaje_batalla"
                          )  
        return #como el guerrero no tiene vida no realiza ninguna acción 

    #Por ejemplo personaje id 7 del CSV [corresponde a la posición #2 en el campo de batalla]
    indice_real = personajes_seleccionados[posicion_en_pantalla]

    # Se obtiene el personaje completo desde el CSV
    personaje_actual = personajes[indice_real]

    # Se obtiene los atributos del personaje seleccionado por el jugador
    vida_personaje = canvas.vidas_guerreros[posicion_en_pantalla]
    ataque_personaje = personaje_actual["ataque"]
    defensa_personaje = personaje_actual["defensa"]

    #Se llama a la función que valida los turnos de la batalla entre el guerrero y el Hollow
    turno_batalla(canvas, posicion_en_pantalla, personaje_actual)

###########################################
# Función que calcula el daño entre los personajes 
def calcular_dano(ataque, defensa):

    #Fórmula del proyecto para calcular el daño 
        #Daño = ATK del Atacante - DEF del Defensor,
    dano = ataque - defensa

    # si el Daño es menor a cero entonces se asigna el daño mínimo 1.
    if dano < 1:
        dano = 1

    return dano
###########################################

# Función que calcula el ataque del guerrero hacia el hollow
    #la variable "personaje_actual" proviene de la función "clic_boton_fight"
def ataque_del_guerrero(canvas, personaje_actual):

    # Se obtiene el ataque del personaje
    ataque_personaje = personaje_actual["ataque"] 

    # Se obtiene el enemigo actual de la lista de enemigos
    enemigo_actual = canvas.enemigos[canvas.enemigo_actual]  

    # Se calcula el daño usando la defensa del enemigo actual
    dano = calcular_dano(ataque_personaje, enemigo_actual["defensa"])  

    # Se resta el daño a la vida del enemigo actual
    enemigo_actual["vida"] = enemigo_actual["vida"] - dano  

    canvas.create_text(
                        385, 485,
                        text=f"Daño a {enemigo_actual['nombre']}: {dano}",  
                        fill="yellow",
                        font=("Arial", 12, "bold"),
                        tags="mensaje_batalla"
                    )
    return dano
###########################################
# Función que determina el ataque del hollows y sus acompañantes hacia el guerrero seleccionado
def ataque_del_hollow(canvas, posicion_en_pantalla, personaje_actual):

    #Viene de la función clic_boton_fight(canvas)
     #Donde se obtiene el id del personaje y su valores del CSV 
    defensa_personaje = personaje_actual["defensa"]

    #Viene de la función iniciar_ventana_batalla()
        # Donde se identifica cual enemigo esta peleado si el hollow o sus acompañantes 
    enemigo_actual = canvas.enemigos[canvas.enemigo_actual]

    #Viene de la función Calcular_dano
        #Donde se toma el ataque del enemigo y lo compara contra la defensa del guerrero 
    dano = calcular_dano(enemigo_actual["ataque"], defensa_personaje)  

    #Viene de la función iniciar_ventana_batalla()
        #Donde se le resta solamente vida al guerrero que esta peleando 
    canvas.vidas_guerreros[posicion_en_pantalla] = (
        canvas.vidas_guerreros[posicion_en_pantalla] - dano
    )

    canvas.create_text(
        385, 468,
        text=f"{enemigo_actual['nombre']} hizo {dano} de daño",  
        fill="white",
        font=("Arial", 12, "bold"),
        tags="mensaje_batalla"
    )

    return dano
###########################################

# Función que dibuja la barra de vida del guerrero seleccionado
def barra_vida_guerrero(canvas):

    # Se eliminan barras anteriores para no dibujar una encima de otra
    canvas.delete("barra_vida_guerrero")

    # Si no hay guerrero seleccionado, no se dibuja la barra de vida
    if not hasattr(canvas, "guerrero_seleccionado"):
        return

    # Se obtiene la posición del guerrero seleccionado
    posicion = canvas.guerrero_seleccionado

    # Se obtiene la vida actual del guerrero
    vida_actual = canvas.vidas_guerreros[posicion]

    # Se obtiene el índice real del personaje seleccionado
    indice_real = personajes_seleccionados[posicion]

    # Se obtiene la vida máxima del personaje desde el CSV
    vida_maxima = personajes[indice_real]["vida"]

    # Se calcula qué porcentaje de vida le queda
    proporcion_vida = vida_actual / vida_maxima

    # Evita que la barra sea negativa si la vida baja de 0
    if proporcion_vida < 0:
        proporcion_vida = 0

    # Tamaño máximo de la barra
    ancho_maximo = 140
    alto_barra = 20

    # Se calcula el ancho actual según la vida restante
    ancho_actual = ancho_maximo * proporcion_vida

    # Posición de la barra en pantalla
    x = 80
    y = 40

    # Fondo de la barra
    canvas.create_rectangle(
                            x,
                            y,
                            x + ancho_maximo,
                            y + alto_barra,
                            fill="gray",
                            tags="barra_vida_guerrero"
                          )

    # Vida restante del guerrero
    canvas.create_rectangle(
                            x,
                            y,
                            x + ancho_actual,
                            y + alto_barra,
                            fill="green",
                            tags="barra_vida_guerrero"
                          )

    # Texto de vida
    canvas.create_text(
                        x + 50,
                        y - 10,
                        text=f"Vida guerrero: {vida_actual}",
                        fill="white",
                        font=("Arial", 10, "bold"),
                        tags="barra_vida_guerrero"
                      )

###########################################

# Función que dibuja la barra de vida del Hollow
def barra_vida_hollow(canvas):

    # Se eliminan barras anteriores para no duplicarlas
    canvas.delete("barra_vida_hollow")

    # Se obtiene el enemigo actual de la lista de enemigos
    enemigo_actual = canvas.enemigos[canvas.enemigo_actual] 

    # Se obtiene la vida actual del enemigo
    vida_actual = enemigo_actual["vida"]

    # Se obtiene la vida máxima del enemigo
    vida_maxima = enemigo_actual["vida_maxima"] 

    # Se calcula el porcentaje de vida
    proporcion_vida = vida_actual / vida_maxima

    # Se valida que no sea negativa
    if proporcion_vida < 0:
        proporcion_vida = 0

    # Tamaño de la barra
    ancho_maximo = 140
    alto_barra = 20

    # Se calcula el ancho actual
    ancho_actual = ancho_maximo * proporcion_vida

    # Posición en pantalla (parte superior)
    x = 480
    y = 50

    # Fondo de la barra
    canvas.create_rectangle(
                            x,
                            y,
                            x + ancho_maximo,
                            y + alto_barra,
                            fill="gray",
                            tags="barra_vida_hollow"
                          )

    # Vida restante
    canvas.create_rectangle(
                            x,
                            y,
                            x + ancho_actual,
                            y + alto_barra,
                            fill="red",
                            tags="barra_vida_hollow"
                          )

    # Texto de vida
    canvas.create_text(
                        x + 75,
                        y - 10,
                        text=f"{enemigo_actual['nombre']}: {vida_actual}", 
                        fill="white",
                        font=("Arial", 10, "bold"),
                        tags="barra_vida_hollow"
                      )

###########################################
# Función que muestra el Hollow en la pantalla de batalla 
def imagen_hollow_batalla(canvas):

    # Se obtiene la imagen del hollow actual
    nombre_imagen = canvas.hollow_actual["imagen"]

    # Se define la ruta de la imagen del hollow 
    ruta = os.path.join(BASE_DIR, "Imagenes", nombre_imagen)

    # Se carga la imagen del hollow 
    imagen = Image.open(ruta)

    # Se ajusta el tamaño del Hollow
    imagen = imagen.resize((130, 130), Image.LANCZOS)

    # Se convierte la imagen para Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda la referencia para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Se dibuja el Hollow en el lado derecho
    canvas.create_image(560, 330, image=imagen_tk)

###########################################

# Función que muestra los acompañantes del Hollow
def acompanantes_hollow(posicion, canvas):

    # Si la cantidad de acompañantes del hollow son mayor a 2 se detiene y no hace nada más 
    if posicion >= len(canvas.acompanantes):
        return

    # Se obtiene el índice del acompañante
    indice_personaje = canvas.acompanantes[posicion]

    # Como las imágenes empiezan en 1, se suma 1
    numero = indice_personaje + 1

    # Se define la imagen del acompañante
    nombre_archivo = f"Guerrero{numero}_frente.png"

    # Se define la ruta
    ruta = os.path.join(BASE_DIR, "Imagenes", nombre_archivo)

    # Se carga la imagen
    imagen = Image.open(ruta)

    # Se ajusta el tamaño
    imagen = imagen.resize((90, 90), Image.LANCZOS)

    # Se convierte a formato Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda la referencia
    referencias_imagenes.append(imagen_tk)

    # Posiciones de los acompañantes al lado del Hollow
    x = 500 + (posicion * 120)
    y = 400

    # Se dibuja el acompañante y se guarda su ID para poder eliminarlo si es derrotado
        # Viene de la función acompanantes_hollow(posicion, canvas)
    id_enemigo = canvas.create_image(x, y, image=imagen_tk)

    # Se guarda el ID  del acompañante enemigo
        # Viene de la inicialización de la lista canvas.ids_enemigos en iniciar_ventana_batalla()
        # Se utiliza para poder acceder posteriormente a cada imagen y eliminarla del canvas
    canvas.ids_enemigos.append(id_enemigo)

     # Se guarda el ID visual dentro del enemigo correspondiente (se evita problema de que visualmente el enemigo no se une al grupo de los guerreros )
        # posicion + 1 porque canvas.enemigos[0] es el Hollow principal
            # y los acompañantes empiezan desde canvas.enemigos[1]
    canvas.enemigos[posicion + 1]["id_canvas"] = id_enemigo

    # Llamada recursiva
    acompanantes_hollow(posicion + 1, canvas)

###########################################
# Función que controla los turnos de la batalla
def turno_batalla(canvas, posicion_en_pantalla, personaje_actual):

    # Se limpian mensajes anteriores de la batalla
    canvas.delete("mensaje_batalla")

     # Se valida si ya no quedan enemigos no se devuelve nada, para evitar error de índice
    if canvas.enemigo_actual >= len(canvas.enemigos):  
        return

#######
# ATAQUE DEL GUERRERO 

    # Se obtiene el enemigo actual antes del ataque
        #Viene de la función iniciar_ventana_batalla donde se obtiene la lista del hollow y sus acompañantes
            # [hollow,acompañante1, acompañante2]
    enemigo_actual = canvas.enemigos[canvas.enemigo_actual]

    # Se llama a la función ataque_del_guerrero
        # Donde se calcula el daño y se le resta vida al enemigo actual
        # personaje_actual: viene de la función clic_boton_fight que determina sobre cual personaje se dio clic para luchar 
    dano_guerrero = ataque_del_guerrero(canvas, personaje_actual)

    print("Daño al enemigo:", dano_guerrero)  
    print("Vida del enemigo:", enemigo_actual["vida"])  

#######
    # Se actualiza la barra de vida del enemigo actual
    barra_vida_hollow(canvas)  

#######
    # Se valida si el enemigo actual fue derrotado
    if enemigo_actual["vida"] <= 0: 
        

        # Se elimina visualmente el acompañante derrotado del lado de los enemigos
            # Viene de la función acompanantes_hollow(posicion, canvas)
                # En esa función se guardó el ID visual del enemigo en enemigo_actual["id_canvas"]
        if enemigo_actual["tipo"] == "acompanante" and enemigo_actual["id_canvas"] != None:
            canvas.delete(enemigo_actual["id_canvas"])

        # Se llama a la función enemigo_a_guerrero para convertir un enemigo derrotado en un nuevo guerrero
            # La función verifica si el enemigo es un acompañante y, en caso de serlo, lo agrega al equipo del jugador
            # Se utiliza para borrar del canvas la imagen del acompañante derrotado
        enemigo_a_guerrero(canvas, enemigo_actual)

        # Se pasa al siguiente enemigo de la lista
        canvas.enemigo_actual = canvas.enemigo_actual + 1 

        # Se valida que ya no quedan más enemigos aunado a que es la última ubicación 
        if canvas.enemigo_actual >= len(canvas.enemigos): 
            # Se valida que el jugador llegó a la última ubicación y debe finalizarse el juego 
            if canvas.indice_ubicacion == 4: 

                canvas.create_text(
                                    350, 250,
                                    text="¡FELICITACIONES!\nHas vencido a todos los Hollows de los reinos",
                                    fill="yellow",
                                    font=("Arial", 18, "bold"),
                                    tags="mensaje_batalla"
                                  )  
                # Se llama a la función  restaurar_personajes_base, que deja a los tres guerreros inciales seleccinados en la configuración 
                    #Se usa para evitar seleccionar entre los nuevos guerreros que ganamos en la pelea con los hollowws 
                restaurar_personajes_base()  

                canvas.after(5000, lambda: volver_pantalla_principal(canvas))  # AQUI ESTA EL CAMBIO
                return  

            canvas.create_text(
                                350, 250,
                                text="¡TODOS LOS ENEMIGOS DERROTADOS!",
                                fill="yellow",
                                font=("Arial", 22, "bold"),
                                tags="mensaje_batalla"
                              )
            
            # Se actualiza la ubicación actual del jugador en el mapa (solo cuando gana la batalla)
                # Viene de la función iniciar_ventana_batalla(indice, canvas_mapa)
                # Donde se guardó la referencia al canvas del mapa en canvas_batalla.canvas_mapa
                 # Se utiliza para registrar que el jugador ya superó la ubicación actual y puede avanzar al siguiente reino 
            canvas.canvas_mapa.ubicacion_actual[0] = canvas.indice_ubicacion

            # Se eliminan mensajes anteriores del mapa
                # Viene de la función seleccionar_ubicacion_mapa()
                    # Donde se crean mensajes como "Ingresando a la ubicación" o "Ubicación bloqueada"
                    # Se utiliza para evitar que se acumulen mensajes en pantalla
            canvas.canvas_mapa.delete("mensaje_mapa") 


            # Se muestra en el mapa que la ubicación fue superada
                # Viene de la función turno_batalla(canvas, posicion_en_pantalla, personaje_actual)
                    # Se utiliza para informarle al jugador que completó correctamente esa ubicación
            canvas.canvas_mapa.create_text(
                                            450, 560,
                                            text=f"Ubicación {canvas.indice_ubicacion + 1} superada",
                                            fill="white",
                                            font=("Arial", 16, "bold"),
                                            tags="mensaje_mapa"
                                          ) 
            

            # Se llama a la función  restaurar_personajes_base, que deja a los tres guerreros inciales seleccinados en la configuración 
                #Se usa para evitar seleccionar entre los nuevos guerreros que ganamos en la pelea con los hollowws 
            restaurar_personajes_base()
            # Se cierra la ventana de batalla después de mostrar el mensaje de todos los enemigos derrotados 
            canvas.after(1500, canvas.winfo_toplevel().destroy)  
            return

        # Si todavía quedan enemigos, se avisa que sigue el próximo
        siguiente_enemigo = canvas.enemigos[canvas.enemigo_actual] 

        # Se actualiza la barra para mostrar la vida del nuevo enemigo actual
        barra_vida_hollow(canvas)

        canvas.create_text(
                            350, 250,
                            text=f"¡ENEMIGO DERROTADO! Sigue {siguiente_enemigo['nombre']}",
                            fill="yellow",
                            font=("Arial", 18, "bold"),
                            tags="mensaje_batalla"
                          )
        return

#######
# ATAQUE DEL ENEMIGO ACTUAL

    # Se llama a la función ataque_del_hollow y sus acompañantes
    dano_hollow = ataque_del_hollow(canvas, posicion_en_pantalla, personaje_actual)

    print("Daño recibido:", dano_hollow)
    print("Vida del personaje:", canvas.vidas_guerreros[posicion_en_pantalla])

    # Se llama a la función que crea la barra de vida del guerrero
    barra_vida_guerrero(canvas)

    # Se valida si el guerrero quedó en KO
    if canvas.vidas_guerreros[posicion_en_pantalla] <= 0:
        canvas.create_text(
                            350, 450,
                            text="¡Perdiste, Tu personaje quedó en KO!",
                            fill="yellow",
                            font=("Arial", 12, "bold"),
                            tags="mensaje_batalla"
                          )
    
    # Se valida si ya no queda ningún guerrero vivo
     #Se llama a la función guerreros_con_vida y si su resultado es False, todos los guerrero murieron
        # y se regresa al jugador a la pantalla de configuración  
    if guerreros_con_vida(0, canvas) == False:  

        canvas.create_text(
                            350, 250,
                            text="¡PERDISTE!",
                            fill="red",
                            font=("Arial", 24, "bold"),
                            tags="mensaje_batalla"
                          )  
        #Se cierra la ventana y se regresa a la pantalla de parametrización 
        canvas.after(1500, lambda: volver_parametrizacion(canvas)) 
        return  
    
###########################################
#Función que asigna el hollows y sus acompañantes de forma aleatoria 
def obtener_acompanantes_hollows(cantidad, lista_acompanantes):

    # En la función iniciar_ventana_pantalla, se inicializan las variables (cantidad, lista_acompanantes) = (2,[])
    #Si ya no se ocupa agregar más acompañantes devuelve la lista de este 
    if cantidad == 0:
        return lista_acompanantes

    #Se genera un número aleatorio (servirá para definir el personaje ID que acompañará al hollow)
    indice = random.randint(0, len(personajes) - 1)

    #Se valida si el ID generado random no se ha utilizado ni que el enemigo seleccionado tampoco haya sido escogido por el jugador 
        #Viene de la lista personajes_seleccionados definida en la pantalla de parametrización
            # Se utiliza para evitar que el jugador tenga que pelear contra su propio personaje
    if indice not in lista_acompanantes and indice not in personajes_seleccionados:
        
        #Se asigna el ide del personaje a la lista de acompañantes 
        lista_acompanantes.append(indice)
        # Se reduce la cantidad de acompañantes del hollow en 1 
        return obtener_acompanantes_hollows(cantidad - 1, lista_acompanantes)

    return obtener_acompanantes_hollows(cantidad, lista_acompanantes)

###########################################

#Función que recorre la lista de enemigos que acompaña al hollow y los agrega a una lista con sus atributos (vida, defensa,etc)
def enemigos(posicion, canvas_batalla):

    #Se valida que si la cantidad de acompañantes es mayor a 2 se detenga y no haga nada 
    if posicion >= len(canvas_batalla.acompanantes):
        return

    #En la función "iniciar_ventana_batalla" a la variable "canvas_batalla.acompanantes" se le asigno la función  obtener_acompanantes_hollows
        # canvas_batalla.acompanantes = obtener_acompanantes_hollows(2, []), por eso se utiliza aqui para obtener sus posición 
    indice = canvas_batalla.acompanantes[posicion]
    personaje = personajes[indice]

    #Los valores vienes del CSV personajes 
    canvas_batalla.enemigos.append({
                                        "tipo": "acompanante", #Es el personaje que acompaña al Hollow en las batallas 
                                        "indice_personaje": indice, #Guarda el ID real del personaje del CSV 
                                        "nombre": personaje["nombre"], 
                                        "vida": personaje["vida"],
                                        "vida_maxima": personaje["vida"],
                                        "ataque": personaje["ataque"],
                                        "defensa": personaje["defensa"],
                                        "imagen": personaje["imagen"],
                                        "id_canvas": None # Guardará el id de la imgen del enemigo, se inicializa pero se llena en la fución acompanantes_hollow
                                    })

    enemigos(posicion + 1, canvas_batalla)

###########################################

#Función que hace que un enemigo derrotado se convierta en un guerrero 
def enemigo_a_guerrero(canvas, enemigo_derrotado):

    # Solo se reclutan acompañantes del Hollow, no el Hollow
        # Viene de la función turno_batalla(canvas, posicion_en_pantalla, personaje_actual)
        # específicamente del bloque:
            # if enemigo_actual["vida"] <= 0:
            # donde se detecta que el enemigo fue derrotado y se envía como parámetro
            # Se utiliza para asegurar que únicamente los acompañantes puedan convertirse en guerreros
    if enemigo_derrotado["tipo"] != "acompanante":
        return

    # Se obtiene el índice real del personaje desde el enemigo derrotado
        # Viene de la función enemigos(posicion, canvas_batalla)
        # Donde se creó cada acompañante como enemigo y se le agregó el campo "indice_personaje"
        # Este índice corresponde a la posición del personaje dentro de la lista "personajes" (cargada desde el CSV)
        # Se utiliza para identificar qué personaje original se debe agregar como guerrero
    indice_personaje = enemigo_derrotado["indice_personaje"]  
    
    # Se valida si el personaje ya fue seleccionado previamente
        # Viene de la función personaje_seleccionado(lista, valor, posicion)
        # Si el personaje ya existe en la lista, la función retorna True y se detiene el proceso
    if personaje_seleccionado(personajes_seleccionados, indice_personaje, 0):
        return

    # Se agrega el enemigo (acompañante) la lista de personajes seleccionados para poder usarlo como guerrero
        # Viene de la lógica de selección inicial del juego (pantalla de configuración)
        # Donde se almacenan los índices de los personajes elegidos por el jugador en la lista "personajes_seleccionados"
        # Este índice fue obtenido previamente desde el enemigo derrotado mediante "indice_personaje"
        # Se utiliza para integrar al acompañante derrotado dentro del equipo del jugador
        # permitiendo que pueda ser seleccionado y utilizado en los turnos de batalla
    personajes_seleccionados.append(indice_personaje)  

    # Se agrega su vida a la lista de vidas de guerreros
        # Viene de la función iniciar_ventana_batalla()
        # Donde se creó la lista canvas.vidas_guerreros con la vida de cada personaje seleccionado
        # El valor "vida_maxima" viene de la función enemigos(posicion, canvas_batalla)
        # donde se guarda la vida original del personaje desde el CSV
        # Se utiliza para asignarle vida completa al nuevo guerrero reclutado
    canvas.vidas_guerreros.append(enemigo_derrotado["vida_maxima"])  

    # Se dibuja el nuevo guerrero en pantalla (enemigo sin vida)
        # Viene de la función mostrar_personajes_batalla(posicion, canvas)
            # que se utiliza en iniciar_ventana_batalla() para mostrar los guerreros seleccionados al inicio
             # Esta función recorre la lista personajes_seleccionados y dibujar cada personaje
                 # len(personajes_seleccionados) - 1 representa la posición del nuevo guerrero agregado al final de la lista
    mostrar_personajes_batalla(len(personajes_seleccionados) - 1, canvas)  

###########################################
# Función recursiva que valida si todavía queda al menos un guerrero con vida 
def guerreros_con_vida(posicion, canvas):

    # Viene de la función iniciar_ventana_batalla()
        # donde se crea y se llena la lista canvas.vidas_guerreros con la vida de cada guerrero seleccionado
        # Si la posición es mayor o igual al tamaño de la lista significa que ya se revisaron todos los guerreros
        # y si ninguno de los guerrero tiene vida mayor a 0 return false 
    if posicion >= len(canvas.vidas_guerreros):
        return False

    
    # Viene de la función iniciar_ventana_batalla()
        # Donde se guarda el id de los personajes: personajes_seleccionados = [7, 12, 11]
        # Si los guerreros tienen vida retorna True 
    if canvas.vidas_guerreros[posicion] > 0:
        return True

    return guerreros_con_vida(posicion + 1, canvas)
###########################################

# Función que cierra la batalla y vuelve a la pantalla de parametrización se utilizará cuando no queden guerreros con vida 
def volver_parametrizacion(canvas):

    ventana_batalla = canvas.winfo_toplevel()
    ventana_batalla.destroy()

    boton_inicio()

###########################################

# Función que elimina los personajes que se ganaron durante la batalla y deja solo los 3 iniciales
def enemigos_ganados():

    # Si hay más de 3 personajes, elimina el último
    if len(personajes_seleccionados) > 3:
        personajes_seleccionados.pop() 
        return enemigos_ganados()
###########################################

# Función que restaura los personajes originales después de ganar una batalla
    # Se utilizará en la función turno_batalla(canvas, posicion_en_pantalla, personaje_actual) elimiando aquellos enemigos que pasaron a nuestro bando y dejando solo los guerreros originales 
def restaurar_personajes_base():

    personajes_seleccionados.clear() 

    #Conserva en una lista solo aquellos personajes que fueron seleccionados en la pantalla de configuración 
        #personaje_base es una copia que guarda los guerreros que seleccionamos al inicio del juego 
    personajes_seleccionados.append(personajes_base[0]) 
    personajes_seleccionados.append(personajes_base[1])  
    personajes_seleccionados.append(personajes_base[2])  

###########################################
# Función que cierra la pantalla de la última batalla al ganar y regresa al usuario a la  pantalla principal
def volver_pantalla_principal(canvas):

    # Se obtiene la ventana de batalla
    ventana_batalla = canvas.winfo_toplevel()

    # Se obtiene la ventana del mapa
    ventana_mapa = canvas.canvas_mapa.winfo_toplevel()

    # Se cierra la ventana de batalla
    ventana_batalla.destroy()

    # Se cierra la ventana del mapa
    ventana_mapa.destroy()

###########################################
# Se agrega el mainloop para que se muestre la ventana 
pantalla_principal.mainloop()
