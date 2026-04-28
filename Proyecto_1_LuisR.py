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

# Función que controla a que ubicación puede moverse el jugador 
def seleccionar_ubicacion_mapa(indice, canvas):

    #Se valida si el usuario previamente dio clic sobre la ubicación (para que no haga ninguna acción)
    if indice == canvas.ubicacion_actual[0]:
        print("Reingresando a la  ubicación")
        #Se llama a la función que abre la ventana de batalla nuevamente en caso que el usuario diera clic sobre la x la primera vez que ingresó 
        iniciar_ventana_batalla(indice)
        return

    #Se valida que el jugador solo pueda acceder a otro mapa si esta en secuencia (ubicación anterio = 0 + nueva ubicación =1)
    if indice == canvas.ubicacion_actual[0] + 1:

        #Se encarga de actualizar la posición del jugador luego de haber pasado un mapa 
        canvas.ubicacion_actual[0] = indice
        print("Se actualiza la ubicación del jugador:", indice + 1)

        #Mensaje que le indica al usuario a que ubicación avanzó
        canvas.create_text(
                            450, 560,
                            text=f"Avanzaste a la ubicación {indice + 1}",
                            fill="white",
                            font=("Arial", 16, "bold")
                             )

        #Se llama a la función que abre la pantalla de inicio de batallas    
        iniciar_ventana_batalla(indice)

    #Mensaje de advertencia que le indica al usuario que debe seguir el mapa en orden secuencial 
    else:
        canvas.create_text(
                            450, 560,
                            text="Debes avanzar en orden secuencial por las ubicaciones",
                            fill="red",
                            font=("Arial", 16, "bold")
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

# Función que dibuja las ubicaciones del mapa
def mostrar_ubicaciones_mapa(indice, ubicaciones, canvas):

    # Caso base: si ya recorrió toda la lista, se detiene
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

    # Guarda la referencia de las imágenes para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Se dibuja la imagen en el mapa
    icono = canvas.create_image(x, y, image=imagen_tk)

    # Dibuja el nombre de la ubicación debajo de la imagen
    texto = canvas.create_text(
                                x,
                                y + 45,
                                text=nombre, # Toma el nombre de la ubicación de esta posición definidad previamente: nombre = ubicacion[2]
                                fill="white",
                                font=("Arial", 10, "bold")
                            )

    #  Si el usuario hace clic en la "imagen" de la ubicación se llama a la función de selección de ubicación mapa
    canvas.tag_bind(
                        icono,
                        "<Button-1>", #Clic izquierdo
                        #lambda: permite llamara a la función seleccionar_ubicacion_mapa que abre la ventana de batallas
                        lambda event, i=indice: seleccionar_ubicacion_mapa(i, canvas)
                    )

    #  Si el usuario hace clic en el "texto" de la ubicación se llama a la función de selección de ubicación mapa
    canvas.tag_bind(
                        texto,
                        "<Button-1>",
                        lambda event, i=indice: seleccionar_ubicacion_mapa(i, canvas)
                    )

    # Llamada recursiva para la siguiente ubicación
    mostrar_ubicaciones_mapa(indice + 1, ubicaciones, canvas)

###########################################

#Función que crea la pantalla para iniciar la batalla del juego 
def iniciar_ventana_batalla(indice):

    #Se crea la ventana de batalla  
    ventana_batalla = Toplevel(pantalla_principal)
    #Se da el nombre a la ventana de btallas 
    ventana_batalla.title("Batalla contra Hollow")
    #Se define el tamaño que tiene la pantalla de batallas 
    ventana_batalla.geometry("700x500+385+150")
    #Se impide ampliar el tamaño de la pantalla de batallas 
    ventana_batalla.resizable(False, False)

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


    # Se crea el canvas donde se colocará la imagen de fondo de la pantalla de batallas 
    canvas_batalla = Canvas(ventana_batalla, width=700, height=500, highlightthickness=0)
    canvas_batalla.place(x=0, y=0)

    #Variable que inicializa la vida del enemigo con 100 puntos de vida (cada vez que se ingresa a la pantalla de batalla se inicializa con 100) 
    canvas_batalla.vida_enemigo = 100

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
    
    # Se llama a la función que carga la imagenes de los guerrero en la pantalla de juego 
    mostrar_avatar_batalla(canvas_batalla)

    # Se crea la lista vacía donde se guardará el ID de los personajes guerreros
    canvas_batalla.ids_guerreros = []

    # Se crea la lista vacía donde se almacenará la posición de los guerreros 
    canvas_batalla.posiciones_guerreros = []

    # Se llama a la función que carga la imagen del avatar en la pantalla de juego 
    mostrar_personajes_batalla(0, canvas_batalla)

    
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
    imagen = imagen.resize((90, 90), Image.LANCZOS)
    #Se convierte la imagen del guerrero en un formato que pueda usar tkinter 
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda referencia para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Posición horizontal de guerreros en pantalla
    x = 80 + (posicion * 80)
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
###########################################
# Función que coloca el botón Fight en la pantalla de batalla
def mostrar_boton_fight(canvas):

    # Se define la ruta de la imagen del botón Fight
    ruta = os.path.join(BASE_DIR, "Imagenes", "BotonFight.png")

    # Se abre la ruta que tiene imagen del botón
    imagen = Image.open(ruta)

    # Se ajusta el tamaño del botón
    imagen = imagen.resize((180, 70), Image.LANCZOS)

    # Se convierte la imagen a formato compatible con Tkinter
    imagen_tk = ImageTk.PhotoImage(imagen)

    # Se guarda referencia de la imagen del botón fight para que no desaparezca
    referencias_imagenes.append(imagen_tk)

    # Se dibuja el botón fight debajo de los personajes
    id_boton_fight = canvas.create_image(180, 455, image=imagen_tk)

    # Se guarda la imagen del botón Fight dentro del canvas
    canvas.imagen_boton_fight = imagen_tk

    # Se permite dar clic sobre el botón Fight
    canvas.tag_bind(
                        id_boton_fight,
                        "<Button-1>",
                        lambda event: clic_boton_fight(canvas) # Se llama a la función clic_boton_fight que determina los puntos de ataque del personaje
                    )

###########################################

#Función que controla el ataque de los personajes guerreros 
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
                             )

###########################################
# Se agrega el mainloop para que se muestre la ventana 
pantalla_principal.mainloop()
