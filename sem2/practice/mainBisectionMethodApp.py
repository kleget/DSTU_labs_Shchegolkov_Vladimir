import os
import sys

import numpy as np

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QGroupBox,
    QFormLayout,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import symbols, sympify, lambdify


class BisectionMethodApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Метод половинного деления")
        self.resize(900, 700)
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f2f2f2;
                color: #222222;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 1px solid #bbbbbb;
                padding: 6px;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #357ab8;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #cccccc;
            }
            QHeaderView::section {
                background-color: #e6e6e6;
                color: #333333;
                padding: 4px;
                border: none;
            }
        """
        )

        self.setupUI()

    def setupUI(self):
        main_layout = QVBoxLayout()

        # Ввод
        input_group = QGroupBox("Входные данные")
        input_layout = QFormLayout()

        self.le_func = QLineEdit()
        self.le_func.setPlaceholderText("например, tan(x)**3 - x + 1")

        self.txt_a = QLineEdit()
        self.txt_a.setPlaceholderText("например, -1.0")

        self.txt_b = QLineEdit()
        self.txt_b.setPlaceholderText("например, 0.5")

        self.txt_eps = QLineEdit()
        self.txt_eps.setText("0.001")

        self.btn_solve = QPushButton("Решить")

        input_layout.addRow("Функция f(x):", self.le_func)
        input_layout.addRow("Левая граница a:", self.txt_a)
        input_layout.addRow("Правая граница b:", self.txt_b)
        input_layout.addRow("Точность ε:", self.txt_eps)
        input_layout.addRow(self.btn_solve)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Увеличиваем количество столбцов
        self.table.setHorizontalHeaderLabels(["n", "a", "b", "c", "f(c)"])
        main_layout.addWidget(self.table)

        # График
        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)
        self.btn_solve.clicked.connect(self.execute_calculation)

    def validate_input(self):
        """Проверка корректности введенных данных"""
        errors = []
        
        # Проверка функции
        func_str = self.le_func.text().strip()
        if not func_str:
            errors.append("Функция не введена")
        else:
            try:
                x = symbols("x")
                sympify(func_str)
            except Exception as e:
                errors.append(f"Ошибка в функции: {str(e)}")
        
        # Проверка границ интервала
        try:
            a_val = float(self.txt_a.text())
        except ValueError:
            errors.append("Левая граница 'a' должна быть числом")
            
        try:
            b_val = float(self.txt_b.text())
        except ValueError:
            errors.append("Правая граница 'b' должна быть числом")
            
        if len(errors) == 0 and a_val >= b_val:
            errors.append("Левая граница 'a' должна быть меньше правой границы 'b'")
            
        # Проверка точности
        try:
            eps = float(self.txt_eps.text())
            if eps <= 0:
                errors.append("Точность 'ε' должна быть положительным числом")
        except ValueError:
            errors.append("Точность 'ε' должна быть числом")
            
        return errors

    def execute_calculation(self):
        # Сначала проверяем ввод
        errors = self.validate_input()
        if errors:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Ошибка ввода")
            msg.setText("Обнаружены ошибки во входных данных:")
            msg.setInformativeText("\n".join(f"• {error}" for error in errors))
            msg.setDetailedText("Пожалуйста, исправьте следующие ошибки:\n\n" + 
                              "\n".join(f"- {error}" for error in errors))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
            
        try:
            func_str = self.le_func.text().strip()
            a_val = float(self.txt_a.text())
            b_val = float(self.txt_b.text())
            eps = float(self.txt_eps.text())

            x = symbols("x")
            f_expr = sympify(func_str)
            f = lambdify(x, f_expr, modules=["numpy"])

            # Инициализация переменных
            a = a_val
            b = b_val
            fa = f(a)
            fb = f(b)

            if fa * fb > 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Ошибка сходимости")
                msg.setText("❌ Условия сходимости не выполнены!")
                msg.setInformativeText(
                    f"Для метода половинного деления требуется, чтобы функция имела разные знаки на концах интервала.\n\n"
                    f"Текущие значения:\n"
                    f"f({a:.3f}) = {fa:.3f}\n"
                    f"f({b:.3f}) = {fb:.3f}\n\n"
                    "Пожалуйста, выберите другой интервал [a, b], "
                    "где функция меняет знак (переходит через ноль)."
                )
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

            # Остальной код метода solve остается без изменений
            self.table.setRowCount(0)
            iteration = 0
            max_iterations = 1000

            # Основной цикл
            while iteration < max_iterations:
                iteration += 1
                c = (a + b) / 2
                fc = f(c)

                # Добавление строки в таблицу
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(iteration)))
                self.table.setItem(row, 1, QTableWidgetItem(f"{a:.8f}"))
                self.table.setItem(row, 2, QTableWidgetItem(f"{b:.8f}"))
                self.table.setItem(row, 3, QTableWidgetItem(f"{c:.8f}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"{fc:.8e}"))

                # Проверка условий выхода (по блок-схеме)
                if abs(fc) < 1e-12:  # Найден точный корень
                    break

                if abs(fc) <= eps and abs(b - a) <= eps:
                    break

                # Выбор нового интервала (по блок-схеме)
                if f(a) * fc > 0:
                    a = c
                else:
                    b = c

            # Проверка на превышение максимального числа итераций
            if iteration == max_iterations:
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    "Достигнуто максимальное число итераций. Решение может быть неточным.",
                )

            root = (a + b) / 2
            QMessageBox.information(
                self,
                "Результат",
                f"Корень: {root:.8f}\nЗначение функции: {f(root):.3e}\nИтераций: {iteration}",
            )
            self.draw_function_plot(func_str, root, a_val, b_val)

        except Exception as e:
            QMessageBox.critical(
                self, 
                "Ошибка вычислений", 
                f"Произошла ошибка при выполнении вычислений:\n{str(e)}\n\n"
                "Проверьте корректность введенной функции и параметров."
            )

    def draw_function_plot(self, func_str, root, a, b):
        try:
            x = symbols("x")
            f_expr = sympify(func_str)
            f = lambdify(x, f_expr, modules=["numpy"])

            # Создаем безопасный диапазон для построения графика
            x_min = min(a, b, root) - 0.5
            x_max = max(a, b, root) + 0.5
            x_vals = np.linspace(x_min, x_max, 1000)

            # Обработка особых случаев (например, tan(x))
            with np.errstate(all="ignore"):
                y_vals = f(x_vals)
                valid_mask = np.isfinite(y_vals)
                x_vals = x_vals[valid_mask]
                y_vals = y_vals[valid_mask]

            fig = self.canvas.figure
            fig.clf()
            ax = fig.add_subplot()

            ax.plot(x_vals, y_vals, color="#4a90e2", label=f"f(x) = {func_str}")
            ax.axhline(0, color="gray", linewidth=0.8)
            ax.axvline(0, color="gray", linewidth=0.8)
            ax.scatter([root], [0], color="red", s=50, label=f"Корень: {root:.6f}")

            # Отмечаем начальные границы
            ax.scatter([a, b], [f(a), f(b)], color="green", s=30, label="Границы")

            ax.grid(True, color="#cccccc", linestyle="--", linewidth=0.5)
            ax.legend()
            ax.set_facecolor("#ffffff")
            ax.set_title("График функции и найденный корень")
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            fig.tight_layout()
            self.canvas.draw()
        except Exception as e:
            QMessageBox.warning(
                self, 
                "Ошибка построения графика", 
                f"Не удалось построить график функции:\n{str(e)}\n\n"
                "Возможно, функция не определена на всем интервале или имеет особенности."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BisectionMethodApp()
    window.show()
    sys.exit(app.exec_())