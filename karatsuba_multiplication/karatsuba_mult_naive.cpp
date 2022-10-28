#include <iostream>
#include <string>
#include <cmath>
#include <Python.h>


const std::string LEFT = "left";
const std::string RIGHT = "right";
const static int MULTIPLICATION_TABLE[10][10] = { 
    { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 },
    { 0, 2, 4, 6, 8, 10, 12, 14, 16, 18 },
    { 0, 3, 6, 9, 12, 15, 18, 21, 24, 27 },
    { 0, 4, 8, 12, 16, 20, 24, 28, 32, 36 },
    { 0, 5, 10, 15, 20, 25, 30, 35, 40, 45 }, 
    { 0, 6, 12, 18, 24, 30, 36, 42, 48, 54 },
    { 0, 7, 14, 21, 28, 35, 42, 49, 56, 63 },
    { 0, 8, 16, 24, 32, 40, 48, 56, 64, 72 },
    { 0, 9, 18, 27, 36, 45, 54, 63, 72, 81 }
};


/*Adds '0' padding to the number based on the side provided. side in {left, right}*/
std::string pad(std::string numString, int padding, std::string side){

    std::string paddedNum = "";
    
    if (side == LEFT) 
    {
        for (int i=0; i < padding; i++) {
            paddedNum += "0";
        }
        paddedNum += numString; 

    } else if (side == RIGHT) {
        paddedNum += numString;
        for (int i=0; i < padding; i++) {
            paddedNum += "0";
        }
    }

    return paddedNum;
}


long cppKaratsuba(long x, long y) {
    
    std::string xString = std::to_string(x);
    std::string yString = std::to_string(y);

    if (xString.length() == 1 &&  yString.length() == 1) {
        return MULTIPLICATION_TABLE[x][y];
    }

    int xy_length_diff = xString.length() - yString.length();

    // Add padding if the number strings are not of equal lengths
    if (xy_length_diff < 0) {
        xString = pad(xString, std::abs(xy_length_diff), LEFT);
    } else if (xy_length_diff > 0) {
        yString = pad(yString, std::abs(xy_length_diff), LEFT);
    }

    // Get half length
    long half = std::floor(xString.length()/2);

    // Split x into a, b and y into c, d
    long a = std::stol(xString.substr(0, half));
    long b = std::stol(xString.substr(half));
    long c = std::stol(yString.substr(0, half));
    long d = std::stol(yString.substr(half));

    // Get the recursive call results
    long res1 = cppKaratsuba(a, c);
    long res2 = cppKaratsuba(b, d);
    long res3 = cppKaratsuba(a+b, c+d);

    // Get res3 - res2 - res1
    long res4 = res3 - res2 - res1;

    // Pad the numbers and add them
    // Can't use muliply because that operator is being implemented in this algorithm
    long res1Padding = (xString.length() - half) + (xString.length() - half);
    long res1Padded = std::stol(pad(std::to_string(res1), res1Padding, RIGHT));

    long res4Padding = (xString.length() - half);
    long res4Padded = std::stol(pad(std::to_string(res4), res4Padding, RIGHT));

    return res1Padded + res2 + res4Padded;
}


int main(){
    long x, y;
    x = 544;
    y = 3254;
    std::cout << cppKaratsuba(x, y) << std::endl;
    return 0;
}


PyObject *multiply(PyObject *self, PyObject *args) {
    long x;
    long y;
    PyArg_ParseTuple(args, "ll", &x, &y);
    long result = cppKaratsuba(x, y);
    return PyLong_FromLong(result);
}


static PyMethodDef methods[] = {
    { "multiply", multiply, METH_VARARGS, "Multiplies two numbers together in C." }, 
    { NULL, NULL, 0, NULL }
};


static struct PyModuleDef karatsuba_mult = {
    PyModuleDef_HEAD_INIT, 
    "karatsuba_mult",
    "Multiplies two large integers using the Karatsuba multiplication algorithm.",
    -1,
    methods
};


PyMODINIT_FUNC PyInit_karatsuba_mult() {
    // PyMODINIT_FUNC function = PyModule_Create(&karatsuba_mult);
    return PyModule_Create(&karatsuba_mult);
    // return function;
}