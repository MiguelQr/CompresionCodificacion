# Autores: Ceballos Daniel, Martinez Rubén, Quiñones Miguel

import pickle
import argparse

from huffman import construir_arbol, contar_frecuencias, asignar_codigos, comprimir, imprimir_arbol
from hamming import codificarArchivo

# Parser para el nombre del archivo y verbose
parser = argparse.ArgumentParser(description='Nombre de archivo para comprimir.')
parser.add_argument('nombre_archivo', nargs='?', help='nombre del archivo a comprimir')
parser.add_argument('-v', '--verbose', action='store_true', help='imprimir contenido de arbole de huffman y archivos compresos')
args = parser.parse_args()

archivo_imagen = False

# Si no se proporciona nombre de archivo, pedir cadena de texto y guardarla
if args.nombre_archivo:
    nombre_archivo = args.nombre_archivo
    if nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        archivo_imagen = True
else:
    user_input = input('Ingrese una cadena de texto para comprimir: ')
    nombre_archivo = 'texto.bin'
    with open(nombre_archivo, 'w') as file:
        file.write(user_input)

# Mostar contenido original
if args.verbose and not archivo_imagen:
    with open(nombre_archivo, 'rb') as file:
        contenido_original = file.read()
    print("\n\nContenido del archivo Original (en texto):")
    print(contenido_original.decode())
    print("\nContenido del archivo Original (en binario):")
    for byte in contenido_original:
        print(f"{byte:08b}", end=' ')
    print("")

# Generar el árbol de Huffman
frecuencias = contar_frecuencias(nombre_archivo)
arbol_huffman = construir_arbol(frecuencias)

# Guardar el árbol de Huffman
with open('arbol_huffman.pkl', 'wb') as file:
    pickle.dump(arbol_huffman, file)
print("\nArbol de huffman creado con éxito.")

# Mostrar el árbol de Huffman
if args.verbose:
    print("\nÁrbol de Huffman:")
    imprimir_arbol(arbol_huffman)

# Comprimir el archivo
tabla_codigos = {}
asignar_codigos(arbol_huffman, '', tabla_codigos)
archivo_comprimido = comprimir(nombre_archivo, tabla_codigos)
print("\nArchivo comprimido con éxito.")


# Mostrar contenido del archivo comprimido
if args.verbose and not archivo_imagen:
    with open(archivo_comprimido, 'rb') as file:
        contenido_comprimido = file.read()
    print("\nContenido del archivo comprimido (en binario):")
    for byte in contenido_comprimido:
        print(f"{byte:08b}", end=' ')
    print("")

#Codifica el archivo
nombre_codificado = 'Entrada.bin' # Para compatibilidad con el programa que agrega error
codificarArchivo(archivo_comprimido, nombre_codificado)
print("\nArchivo codificado con éxito.")

# Mostrar contenido del archivo codificado
if args.verbose and not archivo_imagen:
    with open(nombre_codificado, 'rb') as file:
        contenido_codificado = file.read()
    print("\nContenido del archivo codificado (en binario):")
    for byte in contenido_codificado:
        print(f"{byte:08b}", end=' ')
    print("")