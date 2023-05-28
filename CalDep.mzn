include "globals.mzn";

int: n;
int: Min;
int: Max;
var int: costo;
set of int: FECHAS = 1..2*(n-1);
set of int: EQUIPOS = 1..n;
array[EQUIPOS, EQUIPOS] of var int: D;
array[FECHAS, EQUIPOS] of var int: Cal;

constraint forall(i in 1..2*(n-1), j in 1..n)(Cal[i,j]=10*j);


constraint costo = 5*n;

solve minimize costo;

output["MatrizD=", show(D),"\nMatrizCal=", show(Cal),"\nCosto=", show(costo),"\n"];
