import minizinc
import easygui
import sys
from os import system

def decision ():
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

    matrizStr = ""

    for i in range(n):
        for j in range(n):
            matrizStr += str(matriz[i][j]) + " "
        matrizStr += "\n"

    archivoOutput = open("DatosCalDep.dzn", 'w')
    archivoOutput.write("n = " + str(n) + ";\n")
    archivoOutput.write("Min = " + str(min) + ";\n")
    archivoOutput.write("Max = " + str(max) + ";\n")
    matrizPlana = list()
    for i in range(n):
        for j in range(n):
            matrizPlana.append(matriz[i][j])
    archivoOutput.write("D = array2d(EQUIPOS, EQUIPOS, " + str(matrizPlana) + ");")
    archivoOutput.close()

def ejecutarMzn():    
    # result = system("minizinc CalDep.mzn DatosCalDep.dzn --solver Gecode")
    modelo = minizinc.Model("./CalDep.mzn")
    solver = minizinc.Solver.lookup("gecode")
    instance = minizinc.Instance(solver, modelo)
    instance.add_file("./DatosCalDep.dzn")
    result = instance.solve()
    print("resultado", result.status)

    matrizStr = ""
    if str(result.status) == "OPTIMAL_SOLUTION":
        for i in range(instance["n"]):
            for j in range(instance["n"]):
                matrizStr += str(result["Cal"][i][j]) + " "
            matrizStr += "\n"

        easygui.msgbox(msg="Se ha encontrado una solución óptima\n\n" + matrizStr + "\n\nCon costo: " + str(result["costo"]), title="Calendario Deportivo")
    elif str(result.status) == "SATISFIABLE":
        for i in range(instance["n"]):
            for j in range(instance["n"]):
                matrizStr += str(result["Cal"][i][j]) + " "
            matrizStr += "\n"
        easygui.msgbox(msg="Se ha encontrado una solución óptima satisfactoria\n\n" + matrizStr + "\n\nCon costo: " + str(result["costo"]), title="Calendario Deportivo")
    elif str(result.status) == "UNSATISFIABLE":
        easygui.msgbox(msg="No se ha encontrado una solución satisfactoria", title="Calendario Deportivo")
    else:
        easygui.msgbox(msg="No se puede determinar si hay solución", title="Calendario Deportivo")


def main():
    convertirTxtADzn()
    ejecutarMzn()

if __name__ == "__main__":
    main()