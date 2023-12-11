# Autores: Ceballos Daniel, Martinez Rubén, Quiñones Miguel


import numpy as np

"""
Funciones para codificación y decodificación de Hamming extendida
- Para la codificación de Hamming extendida se requiere: 
1) determinar el número de bits de paridad k y agregar r bits de paridad, 
2) ubicar los bits de paridad en la posición 2^i, para i de 0 a r -1,
3) calcular el valor de cada bit de paridad según los bits que cubre,
4) insertar bits de paridad en sus posiciones respectivas para codificar

- Para la decodificación se requiere:
1) utilizando la estrucutra de paridad para la codificación, calcular los valores de los bits de paridad,
2) comparar los valores de los bits de paridad calculados con los reales e identificar la posición de bits de paridad con errores, 
3) si el error está asociado con un conjunto de bits de datos, se corrige invirtiendo el valor del bit
3) se eliminan los bits de paridad y se obtiene la cadena original
"""

# Calcular cantidad de bits de paridad de la cadena antes de codificar o decodificar
def calcularCantidadBitsParidad(longitud):
    for i in range(longitud):
        if(2**i >= longitud + i + 1):
            return i

# Agregar los r bits de paridad
def agregarParidad(bitsDatos, numeroBitsParidad):
    longitudPalabraCodigo = 8
    palabraCodigo = np.zeros(longitudPalabraCodigo, dtype=np.uint8)
    longitudDatos = bitsDatos.shape[0]

    #print(bitsDatos)

    #Asigna los datos a la palabra codigo
    iteradorDatos = 0
    iteradorPotencias = 0
    for i in range(longitudPalabraCodigo):
        if(2**iteradorPotencias == i + 1):
            iteradorPotencias += 1
        else:
            palabraCodigo[i] = bitsDatos[iteradorDatos]
            iteradorDatos += 1

    #Calcula el valor de cada bit de paridad
    for i in range(numeroBitsParidad):
        val = 0
        for j in range(1, longitudPalabraCodigo + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ palabraCodigo[j - 1]
        palabraCodigo[2**i - 1] = val

    #print(palabraCodigo)

    return palabraCodigo

# Eliminar el error en la decodificación al comparar los bits de paridad de
# las palabrascódigo tras el error
def eliminarError(palabraCodigo, cantidadBitsParidad, cantidadBitsDatos):
    longitudPalabraCodigo = palabraCodigo.shape[0]

    # Calcula los bits de paridad
    res = ''
    for i in range(cantidadBitsParidad):
        val = 0
        for j in range(1, longitudPalabraCodigo + 1):
            if(j & (2**i) == (2**i)):
                val = val ^ palabraCodigo[j - 1]
        res = str(val) + res

    # Encuentra el indice de error
    indiceError = int(res, 2)
    if(indiceError > 0):
        #print(palabraCodigo, res)
        palabraCodigo[indiceError - 1] = (palabraCodigo[indiceError - 1] + 1) % 2
        #print(palabraCodigo, indiceError)

    #Asigna los datos a un arreglo
    datos = np.zeros(cantidadBitsDatos, dtype=np.uint8)
    iteradorDatos = 0
    iteradorPotencias = 0
    for i in range(longitudPalabraCodigo):
        if(2**iteradorPotencias == i + 1):
            iteradorPotencias += 1
        else:
            datos[iteradorDatos] = palabraCodigo[i]
            iteradorDatos += 1

    return datos, indiceError

"""
Codificación y decodificación de Hamming extendida
"""

# Función para la codificación de Hamming extendida de un archivo binario/comprimido
def codificarArchivo(archivoEntrada, archivoSalida):
    longitudParticion = 4
    cantidadBitsParidad = calcularCantidadBitsParidad(longitudParticion) + 1
    #print(cantidadBitsParidad)
    with open(archivoEntrada, 'rb') as archivo, open(archivoSalida, 'wb') as archivoCodificado:
        byte = archivo.read(1)
        while(byte):
            datos = np.unpackbits(np.array([int.from_bytes(byte, byteorder = 'big')], dtype = np.uint8))

            datosIzquierda = datos[:longitudParticion]
            palabraCodigo = agregarParidad(datosIzquierda, cantidadBitsParidad)
            archivoCodificado.write(np.packbits(palabraCodigo).tobytes())

            datosDerecha = datos[longitudParticion:]
            palabraCodigo = agregarParidad(datosDerecha, cantidadBitsParidad)
            archivoCodificado.write(np.packbits(palabraCodigo).tobytes())

            byte = archivo.read(1)

# Función para la decodificación de Hamming extendida de un archivo binario/comprimido, que puede tener errores
def decodificarArchivo(archivoEntrada, archivoSalida):
    longitudParticion = 8
    cantidadBitsDatos = 4
    cantidadBitsParidad = calcularCantidadBitsParidad(cantidadBitsDatos) + 1

    with open(archivoEntrada, 'rb') as archivoCodificado, open(archivoSalida, 'wb') as archivoDecodificado, open(archivoSalida + 'ReporteErrores.txt', 'w') as reporteErrores:
        bytesTomados = 0
        byte = archivoCodificado.read(1)
        while(byte):
            palabraCodigo = np.unpackbits(np.array([int.from_bytes(byte, byteorder = 'big')], dtype = np.uint8))
            datosDerecha, indiceError = eliminarError(palabraCodigo, cantidadBitsParidad, cantidadBitsDatos)
            if(indiceError > 0):
                reporteErrores.write(f'Corregido error en el bit {longitudParticion - indiceError} del byte {bytesTomados}\n')
            bytesTomados += 1
            byte = archivoCodificado.read(1)

            palabraCodigo = np.unpackbits(np.array([int.from_bytes(byte, byteorder = 'big')], dtype = np.uint8))
            datosIzquierda, indiceError = eliminarError(palabraCodigo, cantidadBitsParidad, cantidadBitsDatos)
            if(indiceError > 0):
                reporteErrores.write(f'Corregido error en el bit {longitudParticion - indiceError} del byte {bytesTomados}\n')
            bytesTomados += 1
            byte = archivoCodificado.read(1)

            datos = np.concatenate((datosDerecha, datosIzquierda))
            archivoDecodificado.write(np.packbits(datos).tobytes())
            #print(datosDerecha, datosIzquierda, datos)