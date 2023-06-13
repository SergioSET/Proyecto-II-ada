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
array[FECHAS2, EQUIPOS] of var {D[i, j] | i, j in EQUIPOS}: costoGira;

% Restricción de problemas validos
constraint (n-1) >= Min /\ exists(l, m in Min..Max where m<l)(((n-1) mod l) = m);

% Restricción de no nulidad
constraint forall(i in FECHAS, j in EQUIPOS) (
  Cal[i, j] != 0 /\ abs(Cal[i, j]) != j
);

% Restricción de calendarios validos
constraint forall(i in FECHAS, j in EQUIPOS ) (
  not exists(k in EQUIPOS where k != j)(Cal[i, j]=Cal[i, k])
  /\ not exists(l in FECHAS where l != i)(Cal[i, j]=Cal[l, j])
);
% Restricción de que en cada fecha juegan todos los equipos
constraint forall(i in FECHAS)(
  {abs(Cal[i, j]) | j in EQUIPOS} = EQUIPOS
);

constraint forall(j, k in EQUIPOS where k != j) (
  count(i in FECHAS) (abs(Cal[i, j]) = k) = 2
);


% Restricción de que cada en cada fecha la mitad de equipos juegue de local y la otra mitad de visitante
constraint forall(i in FECHAS) (count(j in EQUIPOS) (Cal[i, j] > 0) = n / 2);
constraint forall(i in FECHAS) (count(j in EQUIPOS) (Cal[i, j] < 0) = n / 2);

% Restricción de implicación de partidos
constraint forall(i in FECHAS, j, k in EQUIPOS) (
  (Cal[i, j] = k) <-> (Cal[i, k] = -j)
);

% Restricción de que no se repitan los partidos en fechas consecutivas
constraint forall(j in EQUIPOS, i in FECHAS where i > 1) (
  abs(Cal[i-1, j]) != abs(Cal[i, j])
);



% Restricción de ida y vuelta con cada equipo
constraint forall(j, k in EQUIPOS where k != j) (
  exists(i1, i2 in FECHAS) (
    Cal[i1, j] = k /\ Cal[i2, j] = -k
  )
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

% Restricción de min y max de las giras
constraint forall(j in EQUIPOS)(
  let{
    array[FECHAS] of var -Max..Max: giraEquipo;
  } in
   forall(i in FECHAS)(giraEquipo[i] != 0)/\
   forall(i in FECHAS)(
   if Cal[i, j] < 0 then
      if i>1 /\ Cal[i-1,j] < 0 then
        giraEquipo[i]=giraEquipo[i-1] + 1
      else giraEquipo[i]=1
      endif
   else
      if i>1 /\ Cal[i-1,j] > 0 then
        giraEquipo[i]=giraEquipo[i-1] - 1
      else giraEquipo[i]= -1
      endif

   endif) /\
   forall(i in FECHAS)(
   if (i < 2*(n-1) /\ giraEquipo[i+1] < 0 /\ giraEquipo[i] > 0)
   \/ (i < 2*(n-1) /\ giraEquipo[i+1] > 0 /\ giraEquipo[i] < 0)
   \/ (i = 2*(n-1)) then
     abs(giraEquipo[i]) >= Min
   else
      true
   endif)
);
constraint costo = sum(i in FECHAS2, j in EQUIPOS) (costoGira[i,j]);
solve minimize costo;
output[show2d(Cal),"\n", show(costo),"\n"];
