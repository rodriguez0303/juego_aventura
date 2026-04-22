#Importación de librerías 

import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk  # Usamos Pillow para cargar imágenes JPG
import os 
from tkinter import Toplevel, Canvas, NO
import random #se utilizará para generar el movimiento de las motos enemigas 
import winsound  # se utilizará para reproducir  la música  



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

def cargar_imagen_boton_jugar():
    
    # Se define la ruta de la imagen del botón
    ruta = os.path.join(BASE_DIR, 'Imagenes', 'Fondo2.png')
    
    # Se abre la ruta donde esta la imagén de fondo del botón 
    imagen = Image.open(ruta)

    # Se define el tamaño máximo permitido para el botón
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
    ventana.label_mensaje.config(text="")

    # llama a la función avatar_seleccionado y Se revisa si ya había un avatar seleccionado
    resultado_avatar = validar_avatar_seleccionado(avatar_seleccionado, 0)

    # Si todavía no hay avatar seleccionado
    if resultado_avatar == False:

        # Se guarda el índice del avatar seleccionado
        avatar_seleccionado.append(indice)

        # Se marca visualmente el botón del avatar seleccionado 
        boton.config(highlightbackground="yellow", highlightthickness=3)

        # Se muestra en consola
        print("Avatar seleccionado:", avatar_seleccionado)

        # Mensaje en pantalla
        ventana.label_mensaje.config(text="Avatar seleccionado correctamente")

    else:
        ventana.label_mensaje.config(text="Ya seleccionaste un avatar. No puedes elegir otro")
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
    frame_avatars.place(x=230, y=555, width=340, height=110)

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
    
    
    #Toplevel: permite abrir una ventana secundaria sobre la ventana principal (para escribir el nombre del usuario) 
    ventana_boton_inicio = Toplevel(pantalla_principal)
    ventana_boton_inicio.title("Parametrización") # Da el nombre a la ventana del nombre del jugador 
    ventana_boton_inicio.geometry("800x690+410+80") # Se define el tamaño  de la ventana para que el usuario ingrese su nombre  + posición eje x + posición eje  y
    ventana_boton_inicio.resizable(False, False) # Evita que se pueda aumentar o disminuir el tamaño de la ventana 
    
    # mantiene la ventana del botón jugar siempre al frente
    ventana_boton_inicio.attributes('-topmost', True)
    
    # Se coloca una imagen a la pantalla  de parametrización
    ruta_imagen_fondo = os.path.join(BASE_DIR, 'Imagenes', 'Fondo3.png')  # Ruta donde esta ubicada la imagen 
    print(f"Ruta de la imagen: {ruta_imagen_fondo}") 
    imagen_fondo = Image.open(ruta_imagen_fondo) # Abre la carpeta donde esta colocada la imagen 
    imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo.resize((800, 750), Image.LANCZOS))  # Redimensiona la imagen 

    # Se crea un Label para mostrar la imagen de fondo
    label_fondo = Label(ventana_boton_inicio, image=imagen_fondo_tk)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa todo el fondo de la ventana

    # Mantiene la imagen en memoria
    label_fondo.imagen_fondo = imagen_fondo_tk

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
    label_mensaje = Label(ventana_boton_inicio, text="", bg="black", fg="yellow", font=("Arial", 12))
    label_mensaje.place(x=290, y=480)

    # Se guarda la referencia en la ventana
    ventana_boton_inicio.label_mensaje = label_mensaje
    
###########################################

# Función que crea y muestra el botón de inicio en la pantalla principal
def crear_boton_inicio():
    
    # Se obtiene la imagen del botón llamando a la función de carga
    imagen_boton = cargar_imagen_boton_jugar()

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
# Se agrega el mainloop para que se muestre la ventana 
pantalla_principal.mainloop()
