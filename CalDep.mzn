include "globals.mzn";

int: n;
int: Min;
int: Max;
var int: costo;
set of int: FECHAS = 1..2*(n-1);
set of int: FECHAS2 = 1..(2*(n-1) + 1);
set of int: EQUIPOS = 1..n;
array[EQUIPOS, EQUIPOS] of var int: D;
array[FECHAS, EQUIPOS] of var -n..n: Cal;
array[FECHAS2, EQUIPOS] of var int: costoGira;

var int: count_pos = card({Cal[i, j] > 0 | i in 1..2*(n-1), j in 1..n});
var int: count_neg = card({Cal[i, j] < 0 | i in 1..2*(n-1), j in 1..n});

constraint forall(i in FECHAS, j in EQUIPOS) (
  Cal[i, j] != 0
);

constraint forall(i in FECHAS, j, k in EQUIPOS) (
  (Cal[i, j] = k) <-> (Cal[i, k] = -j)
);

constraint forall(i in FECHAS, j in EQUIPOS) (
  abs(Cal[i,j]) <= n /\ abs(Cal[i,j]) >= 1
);

constraint n/2 = count_pos;
constraint n/2 = count_neg;

constraint forall(j in EQUIPOS, k in EQUIPOS where k != j) (
  exists(i1, i2 in FECHAS) (
    Cal[i1, j] = k /\ Cal[i2, j] = -k
  )
);

constraint forall(i in FECHAS, j in EQUIPOS)(
  if Cal[i,j] < 0 then
    if Cal[i-1,j] < 0 then
      costoGira[i,j] = D[abs(Cal[i,j]), abs(Cal[i-1,j])]   
    else
      costoGira[i,j] = D[abs(Cal[i,j]),j]
    endif
  else
    if Cal[i-1,j] < 0 then
      costoGira[i,j] = D[j,abs(Cal[i-1,j])]
    else
      costoGira[i,j] = 0
    endif    
  endif
);

constraint forall(j in EQUIPOS)(
  if Cal[2*(n-1),j] < 0 then
    costoGira[2*(n-1) + 1,j] = D[-1*Cal[2*(n-1), j], j]
  else 
    costoGira[2*(n-1) + 1,j] = 0
  endif
);

solve minimize 5;

% output["MatrizD=\n", show2d(D),"\nMatrizCal=\n", show2d(Cal),"\nCosto=", show(costo),"\n"];
