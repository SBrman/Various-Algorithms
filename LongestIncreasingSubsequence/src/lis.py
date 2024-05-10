
class IncreasingSubsequence:
    def __init__(self, A: list):
        self.A = A
        self.n = len(A)
        self.memo = [-1 for _ in range(self.n)]
        self.memo[0] = 1

    def lis_recursive(self, i):

        if self.memo[i] != -1:
            return self.memo[i]

        if self.A[i] > self.A[i-1]:
            self.memo[i] = max(self.lis_recursive(j) for j in range(i-1, -1, -1)) + 1
        else:
            self.memo[i] = 1
            self.lis_recursive(i-1)
        
        return self.memo[i]

    def lis_iterative(self):
        for i in range(1, self.n):
            if self.A[i] > self.A[i-1]:
                self.memo[i] = max(self.memo[:i], default=1) + 1
            else:
                self.memo[i] = 1

        return self.memo

    def retrieve_increasing_subsequence(self, i):
        u = max(self.memo)
        lis = []
        for i in range(self.n-1, -1, -1):
            if u == self.memo[i]:
                lis.append(self.A[i])
                u -= 1
        return lis[::-1]


if __name__ == "__main__":
    A = [1, 4, 2, 7, 5, 9, 10, 8]
    # A = [10, 1, 4, 2, 7, 5, 9, 10, 8]
    print(A)

    increasing_sseq = IncreasingSubsequence(A)
    increasing_sseq.lis_iterative()
    #increasing_sseq.lis_recursive(len(A)-1)
    #print(increasing_sseq.memo)
    print(increasing_sseq.retrieve_increasing_subsequence(len(A) - 1))
