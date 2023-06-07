include "globals.mzn";

int: n;
int: Min;
int: Max;
var int: costo;
set of int: FECHAS = 1..2*(n-1);
set of int: FECHAS2 = 1..(2*(n-1) + 1);
set of int: EQUIPOS = 1..n;
array[EQUIPOS, EQUIPOS] of int: D;
array[FECHAS, EQUIPOS] of var -n..n: Cal;
array[FECHAS2, EQUIPOS] of var int: costoGira;

var int: count_pos = card({Cal[i, j] > 0 | i in FECHAS, j in EQUIPOS});
var int: count_neg = card({Cal[i, j] < 0 | i in FECHAS, j in EQUIPOS});

constraint forall(i in FECHAS, j, k in EQUIPOS) (
  (Cal[i, j] = k) <-> (Cal[i, k] = -j)
);

constraint forall(i in FECHAS, j in EQUIPOS) (
  Cal[i, j] != 0
);


constraint n/2 = count_pos;
constraint n/2 = count_neg;

constraint forall(j, k in EQUIPOS where k != j) (
  exists(i1, i2 in FECHAS) (
    Cal[i1, j] = k /\ Cal[i2, j] = -k
  )
);

constraint forall(i in 2..2*(n-1), j in EQUIPOS)(
  Cal[i-1, abs(Cal[i,j])] != j
);


constraint forall(i in FECHAS, j in EQUIPOS)(
  if Cal[i,j] < 0 then
    if i > 1 /\ Cal[i-1,j] < 0 then
      costoGira[i,j] = D[abs(Cal[i-1,j]), abs(Cal[i,j])]   
    else
      costoGira[i,j] = D[j, abs(Cal[i,j])]
    endif
  else
    if i > 1 /\ Cal[i-1,j] < 0 then
      costoGira[i,j] = D[abs(Cal[i-1,j]), j]
    else
      costoGira[i,j] = 0
    endif    
  endif
);

constraint forall(j in EQUIPOS)(
  let{
    array[FECHAS] of var 1..(n-1): gira;
  } in
   forall(i in FECHAS)(
   if Cal[i, j] < 0 then 
      if i>1 /\ Cal[i-1,j] < 0 then 
        gira[i]=gira[i-1] + 1 
      else  gira[i]=1 
      endif
    else  true
    endif /\ gira[i]<= Max /\ gira[i]>=Min)
);


constraint forall(j in EQUIPOS)(
  if Cal[2*(n-1),j] < 0 then
    costoGira[2*(n-1) + 1,j] = D[abs(Cal[2*(n-1), j]), j]
  else 
    costoGira[2*(n-1) + 1,j] = 0
  endif
);

constraint costo = sum(i in FECHAS2, j in EQUIPOS) (costoGira[i,j]);
solve minimize costo;





% output["MatrizD=\n", show2d(D),"\nMatrizCal=\n", show2d(Cal),"\nCosto=", show(costo),"\n"];
output["MatrizCal=\n", show2d(Cal),"\nCosto=", show(costo),"\n"];
