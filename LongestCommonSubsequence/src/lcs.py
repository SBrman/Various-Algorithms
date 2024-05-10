
INF = float("inf")


class CommonSubsequence:
    """
    Assumptions:
        A and B are both words consisting of upper case letters
        |A| > 0 and |B| > 0
    """ 

    def __init__(self, A: str, B: str):
        self.A = A
        self.B = B

        m, n = len(A), len(B)
        self.memo = [[INF for j in range(n)] for i in range(m)]
        self.s = [["" for j in range(n)] for i in range(m)]
    
        self.Z = []

    def equality_check(self, i, j):
        return self.A[i].lower() == self.B[j].lower()

    def LCS(self, i: int, j: int):
        if i < 0 or j < 0:
            return 0

        if self.memo[i][j] != INF:
            return self.memo[i][j]

        if self.equality_check(i, j):
            self.memo[i][j] = 1 + self.LCS(i-1, j-1)
            self.s[i][j] = "diag"
        else:
            self.memo[i][j] = max(self.LCS(i-1, j), self.LCS(i, j-1))

            if self.LCS(i-1, j) >= self.LCS(i, j-1):
                self.s[i][j] = "up"
            else:
                self.s[i][j] = "left"

        return self.memo[i][j]
    

    def retrieve_lcs(self, i, j):
        if i < 0 or j < 0:
            self.Z = "".join(self.Z[::-1])
            return
        if self.s[i][j] == "diag":
            self.Z.append(self.A[i])
            self.retrieve_lcs(i-1, j-1)
        elif self.s[i][j] == "up":
            self.retrieve_lcs(i-1, j)
        elif self.s[i][j] == "left":
            self.retrieve_lcs(i, j-1)
        else:
            raise Exception("Error!")


if __name__ == "__main__":
    A = "Mental"
    B = "Metal"

    cs = CommonSubsequence(A, B)
    lcs_cost = cs.LCS(len(A) - 1, len(B) - 1)
    cs.retrieve_lcs(len(A) - 1, len(B) - 1)
