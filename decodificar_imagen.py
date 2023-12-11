# Autores: Ceballos Daniel, Martinez Rubén, Quiñones Miguel

import pickle
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from huffman import descomprimir, imprimir_arbol
from hamming import decodificarArchivo

# Parser para verbose
parser = argparse.ArgumentParser(description='Nombre de archivo para comprimir.')
parser.add_argument('-v', '--verbose', action='store_true', help='imprimir contenido de arbole de huffman y archivos compresos')
args = parser.parse_args()

archivo_error = 'Salida.bin' # Para compatibilidad con el programa que agrega error
archivo_decodificado = 'Decodificado.bin'

#Decodifica el archivo
decodificarArchivo(archivo_error, archivo_decodificado)
print("\Archivo decodificado con éxito.")

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
print("\Archivo descomprimido con éxito.")

# Mostrar contenido del archivo descomprimido
if args.verbose:
    img = mpimg.imread(archivo_descomprimido)
    imgplot = plt.imshow(img)
    plt.show()