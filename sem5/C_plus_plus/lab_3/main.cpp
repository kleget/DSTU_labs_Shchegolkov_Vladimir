#include "lab.h"
#include <iostream>
#include <cmath>

using namespace std;

int main(){
    double a, b, c, x1, x2, y1, y2, U;
    cout << "Enter a: ";
    cin >> a;
    cout << "Enter b: ";
    cin >> b;
    cout << "Enter c: ";
    cin >> c;
    
    findRoots(a, b, -1.5, x1, x2);
    findRoots(2, -1, c, y1, y2);
    U = exp(x1+y1)+exp(x2-y2);
    cout << U << "\n\n";

    //--------------------------
    int n;
    cout << "Enter n: ";
    cin >> n;
    double S = recursiveSum(n);
    cout << S;
}