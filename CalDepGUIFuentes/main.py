import ast
import sys
import easygui
import numpy as np
from os import system
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

colores = ['lightgrey']
cmap = ListedColormap(colores)
n = 0

easygui.msgbox(msg="Bienvenido al programa de generación de calendarios deportivos, en la siguiente ventana porfavor seleccione el archivo txt con el cual se generará el archivo DatosCalDep.dzn", title="Calendario Deportivo")


def convertirTxtADzn():
    archivo = easygui.fileopenbox(msg="Seleccione el archivo del calendario",
                                  title="Calendario Deportivo", default="pruebas/*.txt", filetypes=["*.txt"])

    if archivo is None:
        sys.exit(0)
    archivoInput = open(archivo, 'r')
    n = int(archivoInput.readline())
    min = int(archivoInput.readline())
    max = int(archivoInput.readline())
    matriz = list()
    for i in range(n):
        matriz.append(list(map(int, archivoInput.readline().split())))
    archivoInput.close()

    archivoOutput = open("DatosCalDep.dzn", 'w')
    archivoOutput.write("n = " + str(n) + ";\n")
    archivoOutput.write("Min = " + str(min) + ";\n")
    archivoOutput.write("Max = " + str(max) + ";\n")
    matrizPlana = list()
    for i in range(n):
        for j in range(n):
            matrizPlana.append(matriz[i][j])
    archivoOutput.write(
        "D = array2d(EQUIPOS, EQUIPOS, " + str(matrizPlana) + ");")
    archivoOutput.close()
    return n


def ejecutarMzn(n):
    system("minizinc --solver Gecode CalDep.mzn DatosCalDep.dzn --time-limit 120000 > salida.txt")

    with open("salida.txt", "r") as file:
        linea = file.readline()
        costo = file.readline()

    if str(linea) == '=====UNSATISFIABLE=====\n':
        easygui.msgbox(
            msg="No se ha podido determinar si existe una solución", title="Calendario Deportivo")

    elif str(linea) == '=====UNKNOWN=====\n':
        easygui.msgbox(
            msg="No se ha encontrado una solución satisfactoria", title="Calendario Deportivo")
    else:
        lista = ast.literal_eval(linea)
        num_columnas = n
        matriz = [lista[i:i+num_columnas]
                  for i in range(0, len(lista), num_columnas)]

        matriz_np = np.array(matriz)
        filas, columnas = matriz_np.shape
        fig, ax = plt.subplots()
        ax.set_xticks(np.arange(columnas))
        ax.set_yticks(np.arange(filas))
        ax.set_xticklabels(np.arange(1, columnas + 1))
        ax.set_yticklabels(np.arange(1, filas + 1))
        plt.xlabel('EQUIPOS')
        plt.ylabel('FECHAS')
        plt.imshow(matriz_np, cmap=cmap, interpolation='none')

        ax.text(0.5, 1.05, "Costo: " +
                str(costo), transform=ax.transAxes, ha='center', va='center', )

        for i in range(filas):
            for j in range(columnas):
                valor = matriz_np[i, j]
                ax.text(j, i, str(valor), ha='center',
                        va='center', color='black', fontsize=15)

        plt.vlines(np.arange(columnas)+0.5, -0.5, filas-0.5)
        plt.hlines(np.arange(filas)+0.5, -0.5, columnas-0.5)

        plt.show()


def repetir():
    repetir = easygui.indexbox(msg="¿Desea generar otro calendario?", title="Calendario Deportivo", choices=[
        "Sí", "No"])
    if repetir == 0:
        main()
    else:
        sys.exit(0)


def main():
    n = convertirTxtADzn()
    ejecutarMzn(n)
    repetir()


if __name__ == "__main__":
    main()
