# LBP-Reformulation

This is a Python framework to reformulate a class of linear bilevel programs (LBP) to (one-level) nonlinear programs, and solve the latter using a nonlinear solver such as *baron*.

$$
\DeclareMathOperator*{\argmin}{arg\min}
\begin{equation}\tag{LBP}
\min_{x\in\mathbb{R}^n, y\in\mathbb{R}^q}{\langle c,x\rangle+\langle d,y\rangle}\quad\text{s.t.}\quad
\begin{cases}
    Ax=b\\
    x\geq0\\
    y\geq0\\
    y\in\argmin_{y'\geq0}{\{\langle e,x\rangle+\langle f,y'\rangle|Cy'=a-Bx\}}
\end{cases}
\end{equation}
$$

To run the project, please check the AMPL executable's path should be in the system PATH. We use python <br>

To run the project with test instances:<br>
```python3 blevp2nlp.py -t```

To run the project with an AMPL-formatted ".dat" file:<br>
```python3 blevp2nlp.py -d [path to '.dat' file]```

For instance:<br>
```python3 blevp2nlp.py -d tests/test_pb_4.dat```

Solver statuses according to the [AMPL book](https://ampl.com/wp-content/uploads/Chapter-14-Interactions-with-Solvers-AMPL-Book.pdf):

| Message    | Interpretation                                          |
|------------|---------------------------------------------------------|
| solved     | optimal solution found                                  |
| solved?    | optimal solution indicated, but error likely            |
| infeasible | constraints cannot be satisfied                         |
| unbounded  | objective can be improved without limit                 |
| limit      | stopped by a limit that you set (such as on iterations) |
| failure    | stopped by an error condition in the solver             |
