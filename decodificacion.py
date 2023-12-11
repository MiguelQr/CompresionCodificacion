# Autores: Ceballos Daniel, Martinez Rubén, Quiñones Miguel

import pickle
import argparse

from huffman import descomprimir, imprimir_arbol
from hamming import decodificarArchivo

# Parser para verbose
parser = argparse.ArgumentParser(description='Nombre de archivo para comprimir.')
parser.add_argument('-v', '--verbose', action='store_true', help='imprimir contenido de arbole de huffman y archivos compresos')
args = parser.parse_args()

archivo_error = 'Salida.bin' # Para compatibilidad con el programa que agrega error
archivo_decodificado = 'Decodificado.bin'

# Mostrar contenido del archivo condificado (con error)
if args.verbose:
    with open(archivo_error, 'rb') as file:
        contenido_error = file.read()
    print("\nContenido del archivo codificado con error (en binario):")
    for byte in contenido_error:
        print(f"{byte:08b}", end=' ')
    print("")

#Decodifica el archivo
decodificarArchivo(archivo_error, archivo_decodificado)
print("\nArchivo decodificado con éxito.")

# Mostrar contenido del archivo decodificado (sin error)
if args.verbose:
    with open(archivo_decodificado, 'rb') as file:
        contenido_decodificado = file.read()
    print("\nContenido del archivo decodificado sin error (en binario):")
    for byte in contenido_decodificado:
        print(f"{byte:08b}", end=' ')
    print("")

#Carga el arbol de Huffman
with open('arbol_huffman.pkl', 'rb') as file:
    arbol_huffman_descomprimir = pickle.load(file)
print("\nArbol de huffman cargado con éxito.")

# Mostrar el árbol de Huffman
if args.verbose:
    print("\nÁrbol de Huffman:")
    imprimir_arbol(arbol_huffman_descomprimir)


# Descomprime el archivo utilizando el árbol de Huffman guardado
archivo_descomprimido = descomprimir(archivo_decodificado, arbol_huffman_descomprimir)
print("\nArchivo descomprimido con éxito.")

# Mostrar contenido del archivo descomprimido
if args.verbose:
    with open(archivo_descomprimido, 'rb') as file:
        contenido_descomprimido = file.read()
    print("\nContenido del archivo decodificado sin error (en binario):")
    for byte in contenido_descomprimido:
        print(f"{byte:08b}", end=' ')
    print("\n\nContenido del archivo decodificado sin error (en texto):")
    print(contenido_descomprimido.decode())