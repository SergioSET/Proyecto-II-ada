from minizinc import Instance, Model, Solver
import easygui
import sys

decision = easygui.buttonbox("¿Qué desea hacer?", "Calendario Deportivo", [
                             "Generar matriz equipos", "Ver matriz equipos", "Salir"])

if decision == "Generar matriz equipos":
    print("Opción no válida aún")
elif decision == "Ver matriz equipos":
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

    editar = easygui.buttonbox(msg="¿Desea editar el calendario?\n\nCantidad de equipos: " + str(n) + "\nMinimo: " +
                               str(min) + "\nMaximo: " + str(max) + "\nMatriz de distancia entre equipos: \n" + matrizStr, title="Calendario Deportivo", choices=["Sí", "No"])
    
    if editar == "Sí":
        pass
    elif editar == "No":
        pass

    archivoOutput = open("DatosCalDep.dzn", 'w')
    archivoOutput.write("n = " + str(n) + ";\n")
    archivoOutput.write("Min = " + str(min) + ";\n")
    archivoOutput.write("Max = " + str(max) + ";\n")
    matrizPlana = list()
    for i in range(n):
        for j in range(n):
            matrizPlana.append(matriz[i][j])
    # D = array2d(EQUIPOS, EQUIPOS, [0, 745, 665, 929, 745, 0, 80, 337, 665, 80, 0, 380, 929, 337, 380, 0]);
    archivoOutput.write("D = array2d(EQUIPOS, EQUIPOS, " + str(matrizPlana) + ");")

    
    modelo = Model("./CalDep.mzn")
    solver = Solver.lookup("chuffed")
    instance = Instance(solver, modelo)
    instance.add_file("DatosCalDep.dzn")
    result = instance.solve()
    print(result)
