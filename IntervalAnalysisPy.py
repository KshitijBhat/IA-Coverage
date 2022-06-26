# import the module
import ctypes

# compiling instructions
# g++ -c -fPIC Intersections.cpp -o Intersections.o -std=c++11 -lmpfr -lgmp -lCGAL
# g++ -shared -Wl,-soname,libIntersections.so -o libIntersections.so Intersections.o -std=c++11 -lmpfr -lgmp -lCGAL

# load the library
lib = ctypes.cdll.LoadLibrary('./libIntersections.so')

lib.interval_analysis.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                  ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]  
# function calling
lib.interval_analysis(1.00,2.00,0.500,1.700,  0.00,0.00,   
                      1.00,2.00,2.00,3.5,     3.00,2.00)

