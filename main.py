#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# main.py: 
# Programa python para gestionar una pequeña base de datos
#
# Autor: Pablo Vilán Mancuello (pablo.viland@udc.es)
# Autor: 
#

import psycopg2;
import psycopg2.extras;

# Parámetros de conexión
dbname = ''
user = ''
password = ''
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


def main():
    print("Conectando a la base de datos")
    conn = connect_db()

    if conn is None:
        return 0
    
    print("Conectado.")

    print("Desconectando de la nbase de datos")
    disconnect_db(conn)
    print("Desconectado.")


if __name__ == '__main__':
    main()



