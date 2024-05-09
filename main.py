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
import datetime


# Parámetros de conexión
dbname = 'aplicacion'
user = ''
password = ''
host = ''  

## ------------------------------------------------------------
def connect_db():

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password)

        conn.autocommit = False
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE)
        
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

##-------------------------------------------------------------
def add_product(conn):
    """
    Pide por teclado numero referencia, nombre, colección, si es personalizable,
    y su referencia a categoria
    """
    n_reference = input("Número de Referencia: ")
    if n_reference == "": n_reference = None

    name = input("Nombre: ")
    if name == "": name = None

    colection = input("Colección: ")
    if colection == "": colection = None

    sisPersonalizable = input("Es personalizable y/[n]") ## por defecto no es personalizable
    isPersonalizable = False
    if sisPersonalizable == "y": isPersonalizable = True

    scategory_id = input("Id categoria: ")
    category_id = None if scategory_id == "" else int(scategory_id)

    sql="""
            INSERT INTO Producto(nombre,numero_referencia,coleccion,es_personalizable,
            id_categoria) values(%(n)s, %(r)s, %(c)s, %(p)s, %(i)s) returning id
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':name, 'r':n_reference, 'c': colection, 'p':isPersonalizable,
                              'i':category_id})  
            conn.commit()
            id = cur.fetchone()[0]
            print(f"Producto Añadido con id: {id}.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Error al añadir producto, {e.diag.message_detail}")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print(f"Error al añadir producto, la categoria no existe")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al añadir producto, hay campos que no pueden ser nulos")
            else:
                print(f"Error al añadir el producto: {e}")
            conn.rollback()

##-------------------------------------------------------------
def add_color(conn):
    """
    Añade un nuevo color a la base de datos y muestra el ID del color añadido.
    """
    s_product_id = input("Id del Producto que se quiere añadir un nuevo color: ")
    product_id = None if s_product_id == "" else int(s_product_id)
    
    color_name = input("Color del Producto: ")
    if color_name == "": color_name = None
    
    s_price = input("Precio del producto")
    price = None if s_price == "" else float(s_price)
    
    composition = input("Composición: ")
    if composition == "": composition = None
    
    sql="""
            INSERT INTO Color(nombre, precio, composicion, id_producto) 
            VALUES (%(n)s, %(p)s, %(c)s, %(i)s) RETURNING id
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n': color_name, 'p': price, 'c': composition, 'i': product_id})
            color_id = cur.fetchone()[0]
            conn.commit()
            print(f"Color añadido con éxito. ID: {color_id}")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Error al añadir color, {e.diag.message_detail}")
            elif e.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
                print(f"Error al añadir color, el producto no existe")
            elif e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al añadir color, el {e.diag.column_name} no pueden ser nulo")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print(f"Error al añadir color, el precio ha de ser > 0")

            else:
                print(f"Error al añadir el color: {e}")
            conn.rollback()

##-------------------------------------------------------------
def delete_product(conn):
    """
    Elimina un color de la base de datos dado un Id introducido por pantalla
    """
    s_product_id = input("Id del Producto: ")
    product_id = None if s_product_id == "" else int(s_product_id)

    sql="""
            DELETE FROM Producto WHERE id = %(i)s
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'i': product_id})
            if cur.rowcount == 0:
                print(f"El producto con ID: {product_id} non existe")
            else:
                print(f"El producto con ID: {product_id} eliminado")
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al eliminar producto: {e}")

##-------------------------------------------------------------
def delete_color(conn):
    """
    Elimina un color de la base de datos dado un Id introducido por pantalla
    """
    s_color_id = input("Id del Producto: ")
    color_id = None if s_color_id == "" else int(s_color_id)

    sql="""
            DELETE FROM Color WHERE id = %(i)s
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'i': color_id})
            if cur.rowcount == 0:
                print(f"El producto con Color: {color_id} non existe")
            else:
                print(f"El producto con Color: {color_id} eliminado")
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al añadir color: {e}")

##-------------------------------------------------------------
def add_category(conn):
    """
    Pide por teclado nombre de categoria y devuelve el id autogenerado
    si la inserción en BD se realiza correctamente
    """

    category_name = input("Nombre categoria: ")
    if category_name ==  "": category_name = None

    sql="""
            INSERT INTO Categoria(nombre) values(%(n)s) returning id
        """
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'n':category_name}) 
            conn.commit() 
            id = cur.fetchone()[0]
            print(f"Categoria añadida con id: {id}.")
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al añadir Categoria, el {e.diag.column_name} no pueden ser nulo")
            elif e.pgcode == psycopg2.errorcodes.UNIQUE_VIOLATION:
                print(f"Error al añadir Categoria, el Nombre ya existe")
            else:
                print(f"Error al añadir la Categoria: {e}, {e.pgcode}")
            conn.rollback()

##-------------------------------------------------------------
def delete_category(conn):
    """
    Elimina una categoria de la base de datos dado un Id proporcionado
    """
    s_cat_id = input("Id de Categoria: ")
    cat_id = None if s_cat_id == "" else int(s_cat_id)

    sql="""
            DELETE FROM Categoria WHERE id = %(i)s
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'i': cat_id})
            if cur.rowcount == 0:
                print(f"La Categoria: {cat_id} non existe")
            else:
                print(f"La Categoria: {cat_id} ha sido eliminada")
            conn.commit()
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al añadir color: {e}")

##-------------------------------------------------------------
def change_product_color_price(conn):
    """
    Cambia el valor del precio de un color de un determinado Producto
    segun un porcentaje establecido
    """
    s_color_id = input("Id de Color Producto: ")
    color_id = None if s_color_id == "" else int(s_color_id)

    s_porcentaje = input("Porcentaje del precio(a aumentar): ")
    porcentaje = None if s_porcentaje == "" else float(s_porcentaje)

    sql="""
            UPDATE Color 
            set precio = precio + precio * %(porcentaje)s/100.0
            WHERE id = %(i)s
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'porcentaje': porcentaje,'i': color_id})
            if cur.rowcount == 0:
                print(f"El producto con Color: {color_id} non existe")
            else:
                print(f"El producto con Color: {color_id} updateado")
            conn.commit()
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al updatear el precio, el precio del color no pueden ser nulo")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print(f"Error al updatear el precio, el precio del color debe ser positivo")
            else:
                print(f"Error al añadir color: {e}")
            conn.rollback()

##-------------------------------------------------------------
def update_product_color_price(conn):
    """
    Cambia el valor del precio de un color de un determinado Producto
    """
    s_color_id = input("Id de Color Producto: ")
    color_id = None if s_color_id == "" else int(s_color_id)

    s_price = input("Nuevo precio: ")
    price = None if s_price == "" else float(s_price)

    sql="""
            UPDATE Color 
            set precio = %(p)s 
            WHERE id = %(i)s
        """
    
    with conn.cursor() as cur:
        try:
            cur.execute(sql, {'p': price,'i': color_id})
            if cur.rowcount == 0:
                print(f"El producto con Color ID: {color_id} non existe")
            else:
                print(f"El producto con Color ID: {color_id} updateado")
            conn.commit()
        except psycopg2.Error as e:
            if e.pgcode == psycopg2.errorcodes.NOT_NULL_VIOLATION:
                print(f"Error al updatear el precio, el precio del color no pueden ser nulo")
            elif e.pgcode == psycopg2.errorcodes.CHECK_VIOLATION:
                print(f"Error al updatear el precio, el precio del color debe ser positivo")
            else:
                print(f"Error al añadir color: {e}, {e.pgcode}")
            conn.rollback()


## ------------------------------------------------------------
def end_offer(conn):
    """
    Pide por teclado el nombre de una oferta y si no está terminada la termina con fecha actual
    Si la oferta está terminada dará un aviso de que no se puede realizar la operación
    Si la oferta no existe mostrará una advertencia 
    """

    name = input("Nombre de la oferta que quiere terminar: ")
    if name.strip() == "":
        print("Error: No se ha proporcionado ningún nombre")
        print("Volviendo al menú principal")
        return
    
    query_offer = "SELECT * FROM Oferta WHERE nombre_oferta = %(nombre_oferta)s"
    query_end = "UPDATE Oferta SET fecha_fin = CURRENT_DATE WHERE id = %(oferta_id)s;"

    with conn.cursor() as cur:
        try:
            cur.execute(query_offer, {'nombre_oferta' : name})
            if cur.rowcount == 0:
                print("No se ha encontrado ninguna oferta con ese nombre")
            else:
                offer = cur.fetchone()
                if offer[4] is None:
                    print(offer)
                    cur.execute(query_end, {'oferta_id' : offer[0]})
                    conn.commit()
                    print("Se ha actualizado correctamente")
                else:
                    print("La oferta ya está finalizada")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Tipo de excepción: {type(e)}")
            print(f"Código: {e.pgcode}")
            print(f"Mensaxe: {e.pgerror}")
            return None



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
 7 - Porcentaje precio       8 - Actualizar precio   9 - Categorias de Oferta
10 - Productos de Oferta    11 - Ofertas            12 - Terminar oferta
13 - Comparar precio antes y despues de Oferta       q - Salir 
"""
    MENU_OPTIONS = {
        '1' : add_product,
        '2' : add_color,
        '3' : delete_product,
        '4' : delete_color,
        '5' : add_category,
        '6' : delete_category,
        '7' : change_product_color_price,
        '8' : update_product_color_price,
        '12' : end_offer,
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
    print("Conectando a la base de datos")
    conn = connect_db()

    if conn is None:
        print("Error al conectar con la base de datos")
        return 

    print("Conectado.")
    menu(conn)
    print("Desconectando de la base de datos")
    disconnect_db(conn)
    print("Desconectado.")


if __name__ == '__main__':
    main()