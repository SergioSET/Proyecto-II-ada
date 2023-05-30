import minizinc
import easygui
import sys
from os import system
import numpy as np
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
    # result = system("minizinc CalDep.mzn DatosCalDep.dzn --solver Gecode")
    modelo = minizinc.Model("./CalDep.mzn")
    solver = minizinc.Solver.lookup("gecode")
    instance = minizinc.Instance(solver, modelo)
    instance.add_file("./DatosCalDep.dzn")
    result = instance.solve()
    # print("resultado", result.status)

    matrizCal = list()
    matrizStr = ""

    if str(result.status) == "OPTIMAL_SOLUTION":
        matrizCal = result["Cal"]
        matriz_np = np.array(matrizCal)
        filas, columnas = matriz_np.shape
        fig, ax = plt.subplots()
        ax.imshow(matriz_np, cmap='Greens')
        ax.set_xticks(np.arange(columnas))
        ax.set_yticks(np.arange(filas))
        ax.set_xticklabels(np.arange(1, columnas + 1))
        ax.set_yticklabels(np.arange(1, filas + 1))
        ax.text(0.5, -0.1, "Costo: " +
                str(result["costo"]), transform=ax.transAxes, ha='center', va='center')

        for i in range(filas):
            for j in range(columnas):
                valor = matriz_np[i, j]
                ax.text(j, i, str(valor), ha='center',
                        va='center', color='black')
        plt.show()

    elif str(result.status) == "SATISFIABLE":
        matrizCal = result["Cal"]
        longitudes = [max(len(str(matrizCal[i][j])) for i in range(
            len(matrizCal))) for j in range(len(matrizCal[0]))]

        for fila in matrizCal:
            elementos_formateados = [str(elemento).rjust(
                longitud + 1) for elemento, longitud in zip(fila, longitudes)]
            matrizStr += " ".join(elementos_formateados) + "\n"

        easygui.msgbox(msg="Se ha encontrado una solución óptima satisfactoria\n\n" +
                       matrizStr + "\n\nCon costo: " + str(result["costo"]), title="Calendario Deportivo")

    elif str(result.status) == "UNSATISFIABLE":
        easygui.msgbox(
            msg="No se ha encontrado una solución satisfactoria", title="Calendario Deportivo")

    else:
        easygui.msgbox(msg="No se puede determinar si hay solución",
                       title="Calendario Deportivo")


def main():
    convertirTxtADzn()
    ejecutarMzn()


if __name__ == "__main__":
    main()
