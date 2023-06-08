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

% Restricción de que no se repitan los partidos
constraint forall(j in EQUIPOS, i in FECHAS where i > 1) (
  abs(Cal[i-1, j]) != abs(Cal[i, j])
);

% Restricción de implicación de partidos
constraint forall(i in FECHAS, j, k in EQUIPOS) (
  (Cal[i, j] = k) <-> (Cal[i, k] = -j)
);

% Restricción en una fila deben estar los valores de 1 a n
% constraint forall(i in FECHAS) (forall(j in EQUIPOS) (
%   abs(Cal[i, j]) <= n
%   )
% );

% Restricción de que cada equipo juegue n/2 partidos de local y n/2 de visitante
constraint forall(i in FECHAS) (count(j in EQUIPOS) (Cal[i, j] > 0) = n / 2);
constraint forall(i in FECHAS) (count(j in EQUIPOS) (Cal[i, j] < 0) = n / 2);

% Restricción de ida y vuelta con cada equipo
constraint forall(j, k in EQUIPOS where k != j) (
  exists(i1, i2 in FECHAS) (
    Cal[i1, j] = k /\ Cal[i2, j] = -k
  )
);

% Restricción de min y max de las giras
constraint forall(j in EQUIPOS)(
  let{
    array[FECHAS] of var 1..(n-1): gira;
  } in
   forall(i in FECHAS)(
   if Cal[i, j] < 0 then 
      if i>1 /\ Cal[i-1,j] < 0 then 
        gira[i]=gira[i-1] + 1 
      else gira[i]=1 
      endif
    else true
    endif /\ gira[i]<= Max /\ gira[i]>=Min)
);

% Restricción para los costos de la gira
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

% Restricción para los costos de la gira
constraint forall(j in EQUIPOS)(
  if Cal[2*(n-1),j] < 0 then
    costoGira[2*(n-1) + 1,j] = D[abs(Cal[2*(n-1), j]), j]
  else 
    costoGira[2*(n-1) + 1,j] = 0
  endif
);

constraint costo = sum(i in FECHAS2, j in EQUIPOS) (costoGira[i,j]);

solve minimize costo;

output[show2d(Cal),"\n", show(costo),"\n"];
