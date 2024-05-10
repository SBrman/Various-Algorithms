INF = float("inf")


class OptimalBinarySearchTree:
    def __init__(self, keys: list[int], success_prob: list, unsuccessful_prob: list):
        self.key = keys
        self.p = success_prob
        self.q = unsuccessful_prob
        self.n = len(keys)

        self.dummies = [f"d{i}" for i in range(self.n+1)]

        self.reset()

    def reset(self):
        self.e = {i: {j: " " for j in range(self.n)} for i in range(1, self.n+1)}
        self.w = {i: {j: " " for j in range(self.n)} for i in range(1, self.n+1)}
        self.root = {i: {j: " " for j in range(1, self.n)} for i in range(1, self.n)}

    def optimal_BST(self):
        """O(n^3)"""

        for i in range(1, self.n+1):
            self.e[i][i-1] = self.q[i-1]
            self.w[i][i-1] = self.q[i-1]
        
        for l in range(1, self.n+1):
            for i in range(1, self.n-l+1):
                j = i + l - 1

                self.e[i][j] = INF
                self.w[i][j] = self.w[i][j-1] + self.p[j] + self.q[j]

                for r in range(i, j+1):
                    print(f"{l=}, {i=}", end=',')
                    t = self.e[i][r-1] + self.e[r+1][j] + self.w[i][j]
                    if t < self.e[i][j]:
                        self.e[i][j] = t
                        self.root[i][j] = r
            print()
        return self.e, self.root

    def optimal_BST_better(self):
        """O(n^2)"""
        # self.root = {i: {j: 0 for j in range(self.n)} for i in range(self.n)}

        for i in range(1, self.n+1):
            self.e[i][i-1] = self.q[i-1]
            self.w[i][i-1] = self.q[i-1]

        for l in range(1, self.n+1):
            for i in range(1, self.n-l+1):
                j = i + l - 1

                self.e[i][j] = INF
                self.w[i][j] = self.w[i][j-1] + self.p[j] + self.q[j]

                r_range = {i} if l == 1 else range(self.root[i][j-1], self.root[i+1][j]+1)
                
                for r in r_range:
                    # print(f"{l=}, {i=}", end=',')
                    #print(l, i)
                    t = self.e[i][r-1] + self.e[r+1][j] + self.w[i][j]
                    if t < self.e[i][j]:
                        self.e[i][j] = t
                        self.root[i][j] = r
            print()
        return self.e, self.root


def pretty_print(x):
    for _, row in x.items():
        for r in row.values():
            print(round(r, 2) if not isinstance(r, str) else r, end=', ')
        print()


if __name__ == "__main__":
    keys = [f"k{i}" for i in range(1, 7)]
    # success_probs = [0, 4, 2, 1, 1]
    # unsuccessful_probs = [2, 3, 1, 1, 1]
    success_probs = [0, 0.15, 0.10, 0.05, 0.10, 0.20]
    unsuccessful_probs = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]

    obst = OptimalBinarySearchTree(keys, success_probs, unsuccessful_probs)
    e, root = obst.optimal_BST()
    pretty_print(e)
    print()
    # print(root)
    pretty_print(root)

    e, root = obst.optimal_BST_better()

    pretty_print(e)
    print()
    # print(root)
    pretty_print(root)
