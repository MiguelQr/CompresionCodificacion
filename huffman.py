# Autores: Ceballos Daniel, Martinez Rubén, Quiñones Miguel


import heapq

"""
Funciones para compresión de Huffman y descompresión de Huffman
- Para la compresión de Huffman se requiere: 
1) calcular la frecuencia de los símbolos de entrada, 
2) crear un nodo para cada símbolo con su frecuencia como peso, 
3) construir un árbol binario combinando nodos en uno nuevo cuyo peso es la suma del peso de ambos, 
4) Asignar códigos binarios a los símbolos etiquetando caminos izquiedos con 0 y derechos con 1, 
5) Comprimir el archivo utilizando los códigos Huffman asignados a cada símbolo.

- Para la descompresión se requiere: 
1) leer la estructura del árbol Huffman con la que se comprimió y construir el árbol,
2) Recorrer el arbol para decodificar los bits comprimidos moviéndose hacia la izquierda o derecha según el 0 o 1.
"""

# Función para contar las frecuencias de cada byte en el archivo
def contar_frecuencias(archivo):
    frecuencias = {}
    with open(archivo, 'rb') as file:
        byte = file.read(1)
        while byte:
            if byte in frecuencias:
                frecuencias[byte] += 1
            else:
                frecuencias[byte] = 1
            byte = file.read(1)
    return frecuencias

# Clase para el nodo del árbol de Huffman
class NodoHuffman:
    def __init__(self, valor, frecuencia):
        self.valor = valor
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función para construir el árbol de Huffman
# Se apoya de heapq y los nuevos nodos toman la suma de frecuencia de sus hijos
def construir_arbol(frecuencias):
    heap = [NodoHuffman(byte, frecuencia) for byte, frecuencia in frecuencias.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        nodo_izq = heapq.heappop(heap)
        nodo_der = heapq.heappop(heap)
        nodo_nuevo = NodoHuffman(None, nodo_izq.frecuencia + nodo_der.frecuencia)
        nodo_nuevo.izquierda = nodo_izq
        nodo_nuevo.derecha = nodo_der
        heapq.heappush(heap, nodo_nuevo)
    return heap[0]

# Función auxiliar para imprimir el árbol de Huffman
def imprimir_arbol(nodo, prefijo=''):
    if nodo.valor is not None:
        print(f"{prefijo}Valor: {nodo.valor}, Frecuencia: {nodo.frecuencia}")
    else:
        print(f"{prefijo}Frecuencia: {nodo.frecuencia}")
        print(f"{prefijo}Izquierda:")
        imprimir_arbol(nodo.izquierda, prefijo + "  ")
        print(f"{prefijo}Derecha:")
        imprimir_arbol(nodo.derecha, prefijo + "  ")

# Función para asignar códigos a los bytes en el árbol de Huffman
# Recursivamente se asigna un código a cada símbolo al recorrer el árbol
# y formar combinaciones de 0s y 1s
def asignar_codigos(nodo, codigo, tabla_codigos):
    if nodo is not None:
        if nodo.valor is not None:
            tabla_codigos[nodo.valor] = codigo
        asignar_codigos(nodo.izquierda, codigo + '0', tabla_codigos)    #Izquierda es 0
        asignar_codigos(nodo.derecha, codigo + '1', tabla_codigos)      #Derecha es 1

"""
Compresión y descompresión Huffman
"""

# Función para comprimir el archivo utilizando el árbol de Huffman
def comprimir(archivo, tabla_codigos):
    nombre_archivo_comprimido = archivo + '.huff'
    with open(archivo, 'rb') as archivo_entrada, open(nombre_archivo_comprimido, 'wb') as archivo_salida:
        archivo_salida.write(int('0', 2).to_bytes(1, byteorder='big'))
        byte = archivo_entrada.read(1)
        padding = 0
        codigo = ''
        while byte:
            #print(tabla_codigos[byte])
            codigo += tabla_codigos[byte]
            while len(codigo) >= 8:
                byte_comprimido = int(codigo[:8], 2).to_bytes(1, byteorder='big')
                archivo_salida.write(byte_comprimido)
                codigo = codigo[8:]
            byte = archivo_entrada.read(1)
        # Escribir los últimos bits si no forman un byte completo
        if codigo:
            padding = 8 - len(codigo)
            codigo += '0' * padding
            byte_comprimido = int(codigo, 2).to_bytes(1, byteorder='big')
            archivo_salida.write(byte_comprimido)

        archivo_salida.seek(0)
        archivo_salida.write(padding.to_bytes(1, byteorder='big'))

    return nombre_archivo_comprimido

# Función para descomprimir el archivo utilizando el árbol de Huffman
def descomprimir(archivo_comprimido, arbol_huffman):
    nombre_archivo_descomprimido = archivo_comprimido + '.descomprimido'
    with open(archivo_comprimido, 'rb') as archivo_entrada, open(nombre_archivo_descomprimido, 'wb') as archivo_salida:
        byte = archivo_entrada.read(1)
        padding = 8 - int.from_bytes(byte, byteorder='big')
        bit_actual = ''
        nodo_actual = arbol_huffman  # Iniciar desde la raíz del árbol
        byte = archivo_entrada.read(1)
        while byte:
            bits = bin(int.from_bytes(byte, byteorder='big'))[2:].rjust(8, '0')
            byte = archivo_entrada.read(1)
            if not byte:
                #print(padding)
                bits = bits[:padding]

            #print(bits)
            for bit in bits:
                bit_actual += bit
                # Moverse a través del árbol según los bits
                if bit == '0':
                    nodo_actual = nodo_actual.izquierda
                else:
                    nodo_actual = nodo_actual.derecha
                # Si llegamos a un nodo hoja, escribir el valor y volver a la raíz
                if nodo_actual.valor is not None:
                    #print(bit_actual, nodo_actual.valor)
                    archivo_salida.write(nodo_actual.valor)
                    nodo_actual = arbol_huffman
                    bit_actual = ''

    return nombre_archivo_descomprimido
