INF = float("inf")

class Matrix:
    """
    list[list]
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        
    def __str__(self) -> None:
        return f"{self.rows=}, {self.cols}"

    def __repr__(self) -> None:
        return f"Matrix<{self.rows}, {self.cols}>"
    

class Recursive_MCM:
    def __init__(self, A: list[Matrix]):
        self.A = A
        self.n = len(A)

        self.memo: list[list] = [[INF for _ in range(self.n)] for _ in range(self.n)]
        self.s: list[list] = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        self.order = []
    
    def constant(self, i, k, j):
        return self.A[i].rows * self.A[k].cols * self.A[j].cols
    
    def rec_MCM(self, i, j):
        assert i <= j, f"ill posed problem: {i=} > {j=}"

        if self.memo[i][j] != INF:
            return self.memo[i][j]

        if i == j: 
            self.memo[i][j] = 0
        else:
            for k in range(i, j):
                temp_mij = self.rec_MCM(i, k) + self.rec_MCM(k+1, j) + self.constant(i, k, j)
                
                if temp_mij < self.memo[i][j]:
                    self.memo[i][j] = temp_mij
                    self.s[i][j] = k
                
        return self.memo[i][j]
    
    def iter_MCM(self, i, j):
        for i in range(self.n):
            self.memo[i][i] = 0
        
        for delta in range(1, self.n):
            for i in range(self.n - delta):
                j = i + delta
                self.memo[i][j] = INF
                for k in range(i, j):
                    temp_mij = self.memo[i][k] + self.memo[k+1][j] + self.constant(i, k, j)

                    if temp_mij < self.memo[i][j]:
                        self.memo[i][j] = temp_mij
                        self.s[i][j] = k

        return self.memo
    
    def optimal_multiplication_order(self, i, j):
        if i == j:
            self.order.append(i)
            return

        self.order.append("(")

        self.optimal_multiplication_order(i, self.s[i][j])
        self.optimal_multiplication_order(self.s[i][j] + 1, j)
        
        self.order.append(")")
        

if __name__ == "__main__":
    p = (10, 5, 15, 30, 1, 100, 20)
    A = [Matrix(p[i], p[i+1]) for i in range(len(p) - 1)]

    rmcm = Recursive_MCM(A)
    # rmcm.rec_MCM(0, len(A)-1)
    rmcm.iter_MCM(0, len(A)-1)
    
    print("\nM matrix:")
    for row in rmcm.memo:
        print(row)

    print("\nS matrix:")
    for row in rmcm.s:
        print([val+1 for val in row])

    print("\nMultiplication order:")
    rmcm.optimal_multiplication_order(0, len(A)-1)
    print(" ".join(f"A{i+1}" if i not in {"(", ")"} else i for i in rmcm.order))
