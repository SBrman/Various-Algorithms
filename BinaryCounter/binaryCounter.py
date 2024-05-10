

class BinaryCounter:
    def __init__(self, n: int):
        self.n = n
        self.A = [0 for _ in range(n)]

        # pointer to high-order 1-bit in the counter
        self.max_one = 0

    def increment(self):
        i = 0
        while i < len(self.A) and self.A[i] == 1:
            self.A[i] = 0
            i += 1
        
        if i < len(self.A):
            self.A[i] = 1

        if i > self.max_one:
            self.max_one = i
            
    def decrement(self):
        i = 0
        while i < len(self.A) and self.A[i] == 0:
            self.A[i] = 1
            i += 1

        if i < len(self.A):
            self.A[i] = 0
        
        if i == self.max_one:
            self.max_one = i-1
            
    def reset(self):
        i = 0
        while i < self.max_one:
            self.A[i] = 0
            i += 1

        self.A[i] = 0
        
    def print(self):
        print("".join(map(str, self.A[::-1])))


if __name__ == "__main__":
    n = 3
    bc = BinaryCounter(n)
    bc.print()
    
    for j in range(1, 2**n - 1):
        print("Increments:")
        for i in range(j):
            bc.increment()
            print(i, end=': ')
            bc.print()
    
        print("\nDecrements:")
        for k in range(j-2):
            bc.decrement()
            print(k+1, end=": ")
            bc.print()
        
        bc.reset()
        print("\nReset", end=": ")
        bc.print()
        print()
    