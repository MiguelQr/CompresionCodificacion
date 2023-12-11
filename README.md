# Proyecto Compresión de Huffman y Codificación de Hamming

Este proyecto es para la asignatura de Matemáticas Discretas.

## Autores:

- Ceballos Uc Daniel Israel
- Martinez Gonzalez Ruben
- Quiñones Ramirez Miguel Angel

## Descripcion

El proyecto consta principalmente de dos archivos que contienen los algoritmos de Huffman y Hamming extendido:
- `huffman.py`: Contiene la clase y funciones para elaborar el árbol de Huffman, así como las funciones de compresión y descompresión de un archivo.
- `hamming.py`: Contiene las funciones para codificar y decidificar un archivo, quitándole los errores en el proceso.

Se incluyen también tres archivos para realizar las operaciones:
- `codificacion.py`: Se encarga de tomar un archivo o cadena de entrada, realizar el árbol de Huffman, comprimirla y codificarla
. `decodificacion.py`: decodifica un archivo codificado y con error de una cadena o texto, y toma el árbol de Huffman para descomprimirlo posteriormente
- `decodificar_imagen.py`: Realiza los mismo que `decodificacion.py`, pero es de uso para imágenes codificadas

Adicionalmente, se proveen algunos archivos de utilidad:
- `loremipsum.txt`: Contiene un texto de longitud de 100 palabras.
- `gato.jpg`: Contiene una imagen libre de uso.
- `injectError.c`: Es el archivo proporcionado con el código para agregarle error al archivo codificado
- `Makefile`: Es el archivo proporcionado para compilar `injectError.c`.
- `injectError`: Es el archivo compilado para ejecutarse que agrega error (puede requerir ser recompilado)
- `requirements.txt`: Contiene los paquetes utilizados de python para las pruebas

## Requerimientos

- Se requiere un compilador de C y las herramientas de make para compilar el archivo que genera errores.
- Las pruebas se realizaron con python 3.11.4
- Las bibliotecas requeridas de python son 'numpy y 'matplotlib', de todas formas se proporciona requirements.txt

## Uso

### 1) Compresión y codificación
Primero se debe llevar a cabo la compresión  y codificicación del archivo o cadena.

Si se ejecuta el programa de codificación sin ningún argumento, se le pedirá al usuario que ingrese una cadena de texto. 

```
python codificacion.py
```

El primer argumento opcional puede utilizarse para ingresar un archivo que contenga texto o una imágen.
```
python codificacion.py loremipsum.txt
```
```
python codificacion.py gato.jpg
```

Mientras que la bandera '-v' (de verbose) puede agregarse al final para imprimir el contenido del árbol de Huffman y del archivo en las diferentes etapas de compresión y codificación
```
python codificacion.py loremipsum.txt -v
```
Generará el archivo que contiene el árbol de huffman `arbol_huffman.pkl`, el archivo compreso `{nombre_archivo_entrada}.huff` y el archivo `Entrada.bin` con el texto o imagen codificado.

### 2) Incorporar error
El flujo de ejecución del programa toma en cuenta que el archivo de C proporcionado para agregarle error a un archivo codificado toma como entrada "Entrada.bin" y tiene como salida "Salida.bin", por lo que no realizar el paso intermedio de agrgar error puede requerir modificar los nombres correspondientes en los demás scripts.

Se proporciona el archivo compilado para agregar error, pero de no funcionar se requiere compilar en el sistema operativo en que se está ejecutando. 

Para compilarlo ya sea usando o no el Makefile
```
make -f Makefile
```
```
gcc -o injectError injectError.c
```

Y al ejecutar el archivo compilado se requiere añadir el argumento de la proporción del error
```
./injectError 0.5
```
Generará el archivo `Salida.bin` con el archivo codifcado que tiene error agregado, y el archivo `ReporteErrores.txt` con la lista de errores agregados.

### 3) Decodificación y descompresión
Finalmente se ejecuta el programa de decodificación y descompresión.

Depende de si el contenido comprimido es un texto o una imágen.
```
python decodificacion.py
```
```
python decodificar_imagen.py
```

Y también permite el argumento para modo verbose.
```
python decodificacion.py -v
```

Se genera el archivo `Decodificado.bin` con el archivo decodificado sin errores, `Decodificado.binReporteErrores.txt` con la lista de errores corregidos, y `Decodificado.bin.descomprimido` con el archivo final descomprimido. 