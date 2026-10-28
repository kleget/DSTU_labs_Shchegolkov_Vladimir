#include <iostream>
#include <cmath>

using namespace std;

int main() {
	double x, y, z;
	cout << "x: ";
	cin >> x;
	cout << "y: ";
	cin >> y;
	
	z = x * sin(sin(y)) + sqrt(abs(x * y));

	cout << "z = " << z << "\n\n\n";


	// -------------------------------------------------

	const int MAX_SIZE = 100;
	int arr[MAX_SIZE] = {};
	int n = 0, k = 0;

	cout << "Enter n:";
	cin >> n;

	// цикл ввода первоначального массива
	for (int i = 0; i <= n-1; i++) {
		cout << "Enter arr[" << i << "]";
		cin >> arr[i];
	}

	cout << "Enter k: ";
	cin >> k;

	
	// цикл где мы смещаем все элементы с конца до k и потом после цикла на индекс к-1 ставим 0
	for (int i = n; i < k; i--) {
		arr[i] = arr[i - 1];
	}


	// цикл вывода массивчика получившегося
	for (int i = 0; i < n; i++) {
		cout << arr[i] << ' ';
	}

	

	// -------------------------------------------------

	int matrix[50][50];
	int M, N;
	long long res[50] = {};
	long long multip;
	cout << "\nEnter M: ";
	cin >> M;
	cout << "Enter N: ";
	cin >> N;


	// циклы где мы заполняем нашу пустую матрицу элементами, где каждый элемент строки равен порядковому номеру строки умноженному на 10
	// и тут-же считаем произведением все элементов строки для массивчика res
	for (int i = 0; i <= M; i++) {
		int numm = 1;
		for (int j = 0; j <= N; j++) {
			matrix[i][j] = (i + 1) * 10;
			numm *= matrix[i][j];
		}
		res[i] = numm;
	}

	// цикл вывода получившейся матрицы 
	for (int i = 0; i < M; i++) {
		for (int j = 0; j < N; j++) {
			cout << matrix[i][j] << "\t";
		}
		cout << "\n";
	}

	// цикл вывода массивчика с элементами произведенией строк
	for (int i = 0; i < M; i++) {
		cout << res[i] << ' ';
	}

	return 0;
}
