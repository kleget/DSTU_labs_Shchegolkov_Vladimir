#include "lab.h"
#include <cmath>

void findRoots(double a, double b, double c, double& root1, double& root2){
    double d = b*b - 4 * a * c;
    if (a != 0){
        if ( d < 0){
            root1 = 0, root2=0; 
        } else{
            root1=(-b+sqrt(d))/(2*a);
            root2=(-b-sqrt(d))/(2*a);
        }
    } else{
        root1=0;
        root2=0;
    }
}

double recursiveSum(int n){
    if (n == 0){
        return 0;
    }
    if (n >= 0){
        return recursiveSum(n-1) + cos(n)/(4.0*n - 1.0);
    }
}