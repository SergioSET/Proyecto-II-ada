import ast
import sys
import easygui
import numpy as np
from os import system
import matplotlib.pyplot as plt


def decision():
    decision = easygui.buttonbox("¿Qué desea hacer?", "Calendario Deportivo", [
        "Generar matriz equipos", "Ver matriz equipos", "Salir"])


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


def ejecutarMzn():
    system("minizinc --solver Gecode CalDep.mzn DatosCalDep.dzn --time-limit 120000")

    # with open("salida.txt", "r") as file:   
    #     linea = file.readline()
    #     costo = file.readline()

    # if str(linea) == '=====UNSATISFIABLE=====\n':
    #     easygui.msgbox(
    #         msg="No se ha encontrado una solución satisfactoria", title="Calendario Deportivo")
    # else:
    #     lista = ast.literal_eval(linea)
    #     num_columnas = 4
    #     matriz = [lista[i:i+num_columnas]
    #               for i in range(0, len(lista), num_columnas)]

    #     matriz_np = np.array(matriz)
    #     filas, columnas = matriz_np.shape
    #     fig, ax = plt.subplots()
    #     ax.imshow(matriz_np, cmap='Blues')
    #     ax.set_xticks(np.arange(columnas))
    #     ax.set_yticks(np.arange(filas))
    #     ax.set_xticklabels(np.arange(1, columnas + 1))
    #     ax.set_yticklabels(np.arange(1, filas + 1), va="top")

    #     ax.text(0.5, 1.05, "Costo: " +
    #             str(costo), transform=ax.transAxes, ha='center', va='center', )

    #     for i in range(filas):
    #         for j in range(columnas):
    #             valor = matriz_np[i, j]
    #             ax.text(j, i, str(valor), ha='center',
    #                     va='center', color='black', fontsize=15)

    #     plt.show()


def repetir():
    repetir = easygui.indexbox(msg="¿Desea generar otro calendario?", title="Calendario Deportivo", choices=[
        "Sí", "No"])
    if repetir == 0:
        main()
    else:
        sys.exit(0)


def main():
    convertirTxtADzn()
    ejecutarMzn()
    repetir()


if __name__ == "__main__":
    main()
