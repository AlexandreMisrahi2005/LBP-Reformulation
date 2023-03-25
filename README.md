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
