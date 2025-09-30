import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import symbols, diff, lambdify, sympify

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Метод Ньютона")
        self.resize(800, 600)
        self.setStyleSheet("""
            QWidget { background-color: #f0f8ff; }
            QLabel { color: #0066cc; font-size: 12px; }
            QLineEdit { 
                background-color: #ffffff; 
                border: 1px solid #66b3ff;
                padding: 5px;
            }
            QPushButton {
                background-color: #3399ff;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #66b3ff;
            }
        """)

        # Элементы интерфейса
        self.lbl_func = QLabel("Функция f(x):")
        self.le_func = QLineEdit()
        self.le_func.setPlaceholderText("например, log(x) + (x+1)**3")
        
        self.lbl_x0 = QLabel("Начальное x0:")
        self.txt_x0 = QLineEdit()
        self.txt_x0.setPlaceholderText("например, 1.0")
        
        self.lbl_eps = QLabel("Точность:")
        self.txt_eps = QLineEdit()
        self.txt_eps.setText("0.001")
        
        self.btn_solve = QPushButton("Решить")
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["x", "f(x)", "Δx"])
        
        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        
        # Разметка
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.lbl_func)
        input_layout.addWidget(self.le_func)
        input_layout.addWidget(self.lbl_x0)
        input_layout.addWidget(self.txt_x0)
        input_layout.addWidget(self.lbl_eps)
        input_layout.addWidget(self.txt_eps)
        input_layout.addWidget(self.btn_solve)
        
        layout.addLayout(input_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.btn_solve.clicked.connect(self.solve)

    def solve(self):
        try:
            # Получение данных
            func_str = self.le_func.text().strip()
            x0_input = float(self.txt_x0.text())
            eps = float(self.txt_eps.text())

            x = symbols('x')
            fx_expr = sympify(func_str)
            f = lambdify(x, fx_expr)
            df = lambdify(x, diff(fx_expr, x))
            d2f = lambdify(x, diff(fx_expr, x, 2))

            x0 = x0_input

            # Проверка условия f(x0) * f''(x0) > 0
            if f(x0) * d2f(x0) <= 0:
                b_str, ok = QInputDialog.getText(
                    self, "Выбор другого края",
                    "f(x₀) · f''(x₀) <= 0\nВведите альтернативное значение x (например, другой край отрезка):"
                )
                if not ok:
                    return
                b = float(b_str)
                if f(b) * d2f(b) <= 0:
                    QMessageBox.warning(self, "Ошибка", "Ни одно из значений не удовлетворяет условию f(x) · f''(x) > 0")
                    return
                x0 = b  # заменяем начальное значение на альтернативное

            # Очистка таблицы
            self.table.setRowCount(0)

            # Метод Ньютона
            for i in range(100):
                fx = f(x0)
                dfx = df(x0)

                if abs(dfx) < 1e-12:
                    QMessageBox.warning(self, "Ошибка", "Производная равна нулю")
                    return

                delta_x = fx / dfx
                x_new = x0 - delta_x

                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(f"{x0:.8f}"))
                self.table.setItem(row, 1, QTableWidgetItem(f"{fx:.8f}"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{abs(delta_x):.8f}"))

                if abs(delta_x) < eps:
                    break

                x0 = x_new

            self.plot_graph(func_str, x0, x0_input)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Проверьте ввод:\n{str(e)}")

    def plot_graph(self, func_str, root, x0_initial):
        x = symbols('x')
        f = lambdify(x, func_str)

        x_min = min(-2, x0_initial - 2, root - 2)
        x_max = max(2, x0_initial + 2, root + 2)
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = [f(val) for val in x_vals]

        fig = self.canvas.figure
        fig.clf()
        ax = fig.add_subplot()

        ax.plot(x_vals, y_vals, 'b-', label=f'f(x) = {func_str}')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.scatter([root], [0], color='red', label=f'Корень: {root:.6f}')
        ax.scatter([x0_initial], [f(x0_initial)], color='green', label=f'Нач. x₀: {x0_initial:.2f}')

        ax.grid(True)
        ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
