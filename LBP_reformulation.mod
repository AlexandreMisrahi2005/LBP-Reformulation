param Nmax integer;
param Qmax integer;
param Mmax integer;
param Pmax integer;

set N := 1..Nmax;
set Q := 1..Qmax;
set M := 1..Mmax;
set P := 1..Pmax;

param c{N};
param d{Q};
param A{M,N};
param b{M};
param e{N};
param f{Q};
param a{P};
param B{P,N};
param C{P,Q};

var x{N} >= 0;
var y{Q} >= 0;
var z{P};


minimize obj: sum{i in N} c[i]*x[i] + sum{j in Q} d[j]*y[j];
subject to C1{i in M}: sum{j in N} A[i,j]*x[j] == b[i];
subject to C2{i in P}: sum{j in N} B[i,j]*x[j]+sum{k in Q} C[i,k]*y[k] == a[i];
subject to C3: sum{i in Q} f[i]*y[i] <= sum{j in P} z[j]*(a[j]-(sum{k in N} B[j,k]*x[k]));
subject to C4{i in Q}:sum{j in P} z[j]*C[j,i] <= f[i];