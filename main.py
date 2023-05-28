from minizinc import Instance, Model, Solver



modelo = Model("./CalDep.mzn")

solver = Solver.lookup("highs")

instance = Instance(solver, modelo)

instance.add_file("DatosCalDep.dzn")

result = instance.solve()

print(result)