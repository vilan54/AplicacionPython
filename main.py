#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# main.py: 
# Programa python para gestionar una pequeña base de datos
#
# Autor: Pablo Vilán Mancuello (pablo.viland@udc.es)
# Autor: 
#

import psycopg2
import psycopg2.errorcodes
import psycopg2.extras
import decimal

# Parámetros de conexión
dbname = 'aplicacion'
user = 'pablo'
password = 'pablo'
host = ''  

## ------------------------------------------------------------
def connect_db():

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password)

        conn.autocommit = False
        
        return conn
    
    except psycopg2.OperationalError as e:
            print(f"Tipo de excepción: {type(e)}")
            print(f"Código: {e.pgcode}")
            print(f"Mensaxe: {e.pgerror}")
            print("Cancelando transacción..")
            return None


## ------------------------------------------------------------
def disconnect_db(conn):
    
    try:
        if conn is not None:
            conn.close()
        else:
            print("No hay una conexión que cerrar")

    except psycopg2.OperationarError as e:
        print("Error al desconectar de la base de datos")
        return None


## ------------------------------------------------------------
def get_idproduct(conn, name):

    query_name = "SELECT id FROM Producto WHERE nombre = %(name)s"

    with conn.cursor() as cur:
        try:
            cur.execute(query_name, {'name' : name})
            
            if cur.rowcount == 0:
                return None
            else:
                product_id = cur.fetchone()

                if product_id:
                    return product_id[0]
                else:
                    return None
        except psycopg2.Error as e:
            print(f"Tipo de excepción: {type(e)}")
            print(f"Código: {e.pgcode}")
            print(f"Mensaxe: {e.pgerror}")
            return None


## ------------------------------------------------------------
def get_colors_product(conn, id_product):
    """
    Dado un id de un producto, devuelve una lista con todos id y el nombre de los colores de dicho producto
    En caso de no tener ningun color o que el id proporcionado no exista, devuelve Null
    """

    query_colors = "SELECT id, nombre, precio FROM Color WHERE id_producto = %(id_product)s"

    with conn.cursor() as cur:
        try:
            cur.execute(query_colors, {'id_product': id_product})
            colors = cur.fetchall()

            if colors:
                return colors
            else:
                return None
        except psycopg2.Error as e:
            print(f"Tipo de excepción: {type(e)}")
            print(f"Código: {e.pgcode}")
            print(f"Mensaxe: {e.pgerror}")
            return None  


## ------------------------------------------------------------
def get_offer_color(conn, id_color):
    """
    Dado el id de un color, devuele una lista con el nombre y el porcentaje de descuento para 
    cada oferta que tiene el color, si no tiene ofertas devuelve Null
    """

    query_offer = """SELECT o.nombre_oferta, o.porcentaje_oferta FROM OFERTA o
                        INNER JOIN Oferta_Ropa op ON o.id = op.id_oferta WHERE op.id_color = %(id_color)s"""

    with conn.cursor() as cur:
        try:
            cur.execute(query_offer, {'id_color' : id_color})
            if cur.rowcount == 0:
                return None
            offers = cur.fetchall()
            if offers:
                return offers
            else: 
                return None
        except psycopg2.Error as e:
            print(f"Tipo de excepción: {type(e)}")
            print(f"Código: {e.pgcode}")
            print(f"Mensaxe: {e.pgerror}")
            return None 

## ------------------------------------------------------------
def add_product(conn):
    """
    Pide por teclado numero referencia, nombre, colección, si es personalizable,
    y su referencia a categoria
    """

    n_reference = input("Número de Referencia: ")
    
    name = input("Nombre: ")
    
    colection = input("Colección: ")
    if colection == "": 
        colection = None
    
    sisPersonalizable = input("Es personalizable y/[n]") ## por defecto no es personalizable
    isPersonalizable = False
    
    if sisPersonalizable == "y": 
        isPersonalizable = True
    
    scategory_id = input("Id categoria: ")
    category_id = int(scategory_id)

    sql="""
            INSERT INTO Producto(nombre,numero_referencia,coleccion,es_personalizable,
            id_categoria) values(%(n)s, %(r)s, %(c)s, %(p)s, %(i)s)
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':name, 'r':n_reference, 'c': colection, 'p':isPersonalizable,
                              'i':category_id})  
            conn.commit()
            print("Producto Añadido.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"El Producto con referencia{n_reference} ya existe. No se añade")
            conn.rollback()


## ------------------------------------------------------------
def compare_prize_product(conn):
    """
    Pide por teclado el nombre del producto y presenta una lista con todas las ofertas del 
    producto, presentando el nombre de la oferta, el precio original y precio tras la oferta

    Si no se proporciona un nombre, la funcion termina 
    """

    name = input("Nombre del producto: ")
    if name.strip() == "":
        print("Error: No se ha proporcionado ningún nombre")
        print("Volviendo al menú principal")
        return
    
    id_product = get_idproduct(conn, name)
    if id_product is None:
        print("No se ha encontrado un producto con este nombre")
        return
    
    colors = get_colors_product(conn, id_product)
    if colors is None:
        print("El producto no tiene colores disponibles, por lo tanto no tiene ofertas")
        return 
    
    for id_color in colors:
        color_offers = get_offer_color(conn, id_color[0])

        if color_offers:
            print(f"\n\nOfertas para el color {id_color[1]}:")
            for offer in color_offers:
                original = decimal.Decimal(id_color[2])
                porcentaje = decimal.Decimal(offer[1])/100
                descuento = original - (original * porcentaje)

                print("{:<20}\tOriginal: {:<10}\tCon descuento: {:.2f}".format(offer[0], id_color[2], descuento))

        else:
            print(f"No hay ofertas para el color {id_color[1]}")
            



## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opciones, solicita la opción y ejecuta la función asociada.
    'q' para salir.
    """
    MENU_TEXT = """
      -- MENÚ --
 1 - Añadir Producto         2 - Añadir Color        3 - Eliminar Producto
 4 - Eliminar Color          5 - Añadir Categoria    6 - Eliminar Categoria
 7 - Oferta Producto         8 - Oferta Categoria    9 - Categorias de Oferta
10 - Productos de Oferta    11 - Ofertas            12 - Terminar oferta
13 - Comparar precio antes y despues de Oferta
"""
    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla == '1':
            add_product(conn)  


## ------------------------------------------------------------
def menu(conn):
    """
    Imprime un menú de opciones, solicita la opción y ejecuta la función asociada.
    'q' para salir.
    """
    MENU_TEXT = """
    
      -- MENÚ --
 1 - Añadir Producto         2 - Añadir Color        3 - Eliminar Producto
 4 - Eliminar Color          5 - Añadir Categoria    6 - Eliminar Categoria
 7 - Oferta Producto         8 - Oferta Categoria    9 - Categorias de Oferta
10 - Productos de Oferta    11 - Ofertas            12 - Terminar oferta
13 - Comparar precio antes y despues de Oferta       q - Salir 
"""
    MENU_OPTIONS = {
        '1': add_product,
        '13' : compare_prize_product,
    }

    while True:
        print(MENU_TEXT)
        tecla = input('Opción> ')
        if tecla == 'q':
            break
        elif tecla in MENU_OPTIONS:
            MENU_OPTIONS[tecla](conn)
        else:
            print("Opción no implementada")
 


def main():
    """
    Función principal. Conecta a la bd y ejecuta el menú.
    Al salir del menu, desconecta la BD y finaliza el programa
    """
    print('Conectando a PosgreSQL...')
    conn = connect_db()
    print('Conectado.')
    menu(conn)
    disconnect_db(conn)


if __name__ == '__main__':
    main()