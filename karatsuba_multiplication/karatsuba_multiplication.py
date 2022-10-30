#! python3

# %%
# Compile CPP module file
import os

for f in os.listdir():
    if f == 'karatsuba_mult.so':
        break
else:
    print("Compiling the shared cpp module...")
    os.system("g++ karatsuba_mult_naive.cpp -shared -o karatsuba_mult.so -I'/usr/include/python3.11' -fPIC")
    print("Compilation complete")
    

import karatsuba_mult

if __name__ == "__main__":
    x = 4543534
    y = 12371897
    print(f"{x} * {y} = {x*y}")
    print(f"{x} * {y} = {karatsuba_mult.multiply(x, y)}")
# %%
