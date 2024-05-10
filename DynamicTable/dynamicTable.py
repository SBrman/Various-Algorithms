import numpy as np


class DynamicTable:
    def __init__(self):
        self.table = np.zeros(1)
        self.items = 0
        
    def insert(self, x):

        if self.table.size == self.items:
            # Allocate new table with double the size
            new_table = np.zeros(2 * self.table.size)

            # Copy everything from the old table to the new table
            for i in range(self.table.size):
                new_table[i] = self.table[i]
            
            # Free the old table and point to the new table
            del self.table          # not really necessary
            self.table = new_table

        self.push_back(x)

    def push_back(self, x):
        self.table[self.items] = x
        self.items += 1
        
    def __repr__(self):
        return str(self.table)
    

if __name__ == "__main__":
    dt = DynamicTable()

    for i in range(1, 10):
        dt.insert(i)
        print(dt)
        