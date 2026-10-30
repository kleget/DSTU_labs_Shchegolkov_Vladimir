#include <iostream>
#include <stdio.h>

using namespace std;

int main() {
    int num = 116;

    // int * - это указатель на переменную типа int
    // &num - тут & значит получить адрес переменной которая идет после &
    // int *p_num = &num; 
    
    // // тут *name - получение значения переменной на которую ссылается указатель
    // printf("num = %d", *p_num);


    // *p_num = 10000; // изменили num через указатель p_num
    // printf("num = %d", *p_num);
    // printf("num = %d", num);

    int *num_2 = &num;
    int *num_1 = &num;

    *num_2 = 19999;

    cout << *num_2 << "\n\n";
    cout << *num_1;
    return 0;
}