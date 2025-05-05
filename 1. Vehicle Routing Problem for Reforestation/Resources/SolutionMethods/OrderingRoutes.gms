* Definici�n de par�metros y conjuntos
* Conjunto de rutas (n rutas)
* Conjunto de d�as disponibles (T d�as)

option OptCR = 0.01
Sets
   i /1*115/
   t /1*43/;

Parameters
   c(i) /1 5.701, 2 7.891, 3 1.12, 4 1.12, 5 1.12,
           6 1.12, 7 1.12, 8 1.12, 9 1.12, 10 1.12,
           11 1.115, 12 1.115, 13 1.115, 14 1.115, 15 1.115,
           16 1.115, 17 1.115, 18 1.115, 19 7.79, 20 1.13,
           21 1.13, 22 1.13, 23 1.13, 24 1.111, 25 1.111,
           26 1.111, 27 1.111, 28 1.111, 29 1.111, 30 7.653,
           31 1.082, 32 1.082, 33 1.082, 34 1.082, 35 1.082,
           36 1.082, 37 1.082, 38 1.082, 39 1.074, 40 1.074,
           41 1.074, 42 1.074, 43 1.074, 44 1.074, 45 1.074,
           46 1.074, 47 7.5, 48 1.06, 49 7.609, 50 7.389,
           51 5.205, 52 5.237, 53 1.023, 54 1.023, 55 1.023,
           56 1.023, 57 1.023, 58 1.023, 59 0.0, 60 1.063,
           61 1.063, 62 1.063, 63 1.063, 64 1.094, 65 1.083,
           66 1.083, 67 1.083, 68 1.083, 69 1.083, 70 1.083,
           71 1.083, 72 1.083, 73 7.43, 74 5.203, 75 5.104,
           76 5.422, 77 1.109, 78 1.109, 79 1.109, 80 1.109,
           81 1.102, 82 1.09, 83 1.09, 84 1.09, 85 1.09,
           86 1.09, 87 1.09, 88 1.072, 89 1.072, 90 1.072,
           91 1.072, 92 1.072, 93 1.072, 94 1.05, 95 1.05,
           96 1.05, 97 1.05, 98 1.05, 99 1.05, 100 5.215,
           101 1.0, 102 1.0, 103 1.0, 104 1.0, 105 1.0,
           106 1.0, 107 1.0, 108 1.0, 109 1.0, 110 1.0,
           111 1.0, 112 1.0, 113 1.0, 114 1.0, 115 1.0/;



* Variable binaria que indica si el d�a es usado o no
Binary Variables
   d(t)
   x(i,t);

* Variable de funci�n objetivo
Variables
   z;

* Funci�n objetivo: minimizar la suma de d�as usados
Equations
   obj,
   restric(t),
   unica_ruta(i);

* Definir funci�n objetivo
obj..
   z =e= sum(t, d(t));

* Definir restricciones de costo por d�a
restric(t)..
   sum(i, c(i) * x(i,t)) =l= 8 * d(t);

* Restricci�n que asegura que cada ruta se asigne a solo un d�a
unica_ruta(i)..
   sum(t, x(i,t)) =e= 1;

* Resolver el modelo
Model rutas /all/;
Solve rutas using mip minimizing z;
