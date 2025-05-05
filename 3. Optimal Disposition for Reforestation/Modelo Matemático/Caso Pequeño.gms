*Metodo manual de uso de tablas con problema de asignacion
Set
i /1*9/
a /1*4/;
alias(i,j);
alias(a,b);
Variable x;
Binary Variable z(i,j,a,b), p(i,a);
parameter l(a)/
1 1
2 2
3 3
4 3
/;

Table
g(i,j)
    1   2   3   4   5   6   7   8   9
1   0   1   0   1   0   0   0   0   0
2   1   0   1   0   1   0   0   0   0
3   0   1   0   0   0   1   0   0   0
4   1   0   0   0   1   0   1   0   0
5   0   1   0   1   0   1   0   1   0
6   0   0   1   0   1   0   0   0   1
7   0   0   0   1   0   0   0   1   0
8   0   0   0   0   1   0   1   0   1
9   0   0   0   0   0   1   0   1   0;

Table
h(a,b)
    1    2   3   4
1   2    6   7   10
2   6    2   8   7
3   7    8   2   7
4   10   7   7   2;

Equations
obj,r1,r2, r3, r4, r5;
obj.. x =E= sum((a,b,i,j),(g(i,j)*z(i,j,a,b)*h(a,b)))/2;
r1(i).. sum(a,p(i,a))=E=1;
r2(a).. sum(i,p(i,a))=E=l(a);
r3(i,j,a,b).. z(i,j,a,b)=G= p(i,a)+p(j,b)-1;
r4(i,j,a,b).. z(i,j,a,b)=L=p(i,a);
r5(i,j,a,b).. z(i,j,a,b)=L=p(j,b);


model estocastico /all/;
solve estocastico using MIP min x;