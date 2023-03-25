param lambda integer, >0;  			# number of levels
set L := 1..lambda;					# set of index levels
param n{k in L} integer, >0;        # number of variables at level k
param m{k in L} integer, >0;        # number of constraints at level k
set N{k in L} := 1..n[k];           # set of variable indices at level k
set M{k in L} := 1..m[k];           # set of constraint indices at level k

# objective function coefficient of (variable j in level h) at level k
param c{k in L, h in L, j in N[h]} default 0;

# coefficient of (variable j in level h) of constraint i at level k
param A{k in L, h in L, i in M[k], j in N[h]} default 0;

# right-hand-side coefficient of constraint i at level k
param b{k in L, i in M[k]} default 0;

var x{k in L, j in N[k]} >= 0;
var z{M[2]};

minimize obj: sum{i in N[1]} c[1,1,i]*x[1,i] + sum{j in N[2]} c[1,2,j]*x[2,j];
subject to C1{i in M[1]}: sum{j in N[1]} A[1,1,i,j]*x[1,j] == b[1,i];
subject to C2{i in M[2]}: sum{j in N[1]} A[2,1,i,j]*x[1,j]+sum{k in N[2]} A[2,2,i,k]*x[2,k] == b[2,i];
subject to C3: sum{i in N[2]} c[2,2,i]*x[2,i] <= sum{j in M[2]} z[j]*(b[2,j]-(sum{k in N[1]} A[2,1,j,k]*x[1,k]));
subject to C4{i in N[2]}:sum{j in M[2]} z[j]*A[2,2,j,i] <= c[2,2,i];