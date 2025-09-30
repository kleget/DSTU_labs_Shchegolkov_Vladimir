import pandas as pd
import os
import matplotlib.pyplot as plt
from typing import Optional
from mpl_toolkits.mplot3d import Axes3D  # Для 3D-графика


class DatasetProcessor:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")
        self.df = pd.read_csv(file_path)
        self._preprocess_data()

    def _preprocess_data(self):
        """Задание 1: Замена пропущенных значений."""
        for column in self.df.columns:
            if self.df[column].dtype in ['int64', 'float64']:
                self.df[column] = self.df[column].fillna(self.df[column].mean())
            else:
                mode_values = self.df[column].mode()
                if not mode_values.empty:
                    self.df[column] = self.df[column].fillna(mode_values[0])
                else:
                    self.df[column] = self.df[column].fillna(self.df[column].iloc[0])

    def display(self, n: int = 5) -> pd.DataFrame:
        """Вывод датасета."""
        return self.df.head(n)

    def calculate_statistics(self) -> pd.DataFrame:
        """Задание 3: Статистики для числовых полей."""
        stats = self.df.describe(include='number').T
        stats['median'] = self.df.select_dtypes(include='number').median()
        return stats[['min', 'max', 'mean', 'median']]

    def check_values_in_column(self, column: str, values: list) -> pd.Series:
        """Задание 2: Проверка наличия значений."""
        return self.df[column].isin(values)

    def group_and_aggregate(self, group_by: str, agg_column: str, asc: bool = True) -> pd.DataFrame:
        """Задание 4: Группировка и агрегация."""
        grouped = self.df.groupby(group_by)[agg_column].mean().sort_values(ascending=asc).reset_index()
        return grouped

    def plot_grouped_histogram(self, group_by: str, agg_column: str, asc: bool = True):
        """Задание 4: Гистограмма средних значений групп."""
        grouped = self.group_and_aggregate(group_by, agg_column, asc)
        plt.figure(figsize=(10, 6))
        plt.bar(grouped[group_by], grouped[agg_column])
        plt.title(f"Средние значения {agg_column} по группам {group_by}")
        plt.xticks(rotation=45)
        plt.show()

    def filter_and_statistics(self, condition: str, column: str) -> pd.Series:
        """Задание 5: Фильтрация и статистики."""
        filtered = self.df.query(condition)
        return filtered[column].agg(['min', 'max', 'mean', 'median'])

    def create_cross_sample(self) -> pd.DataFrame:
        """Задание 7: Перекрестная выборка статистик."""
        numeric_cols = self.df.select_dtypes(include='number').columns
        cross_sample = self.df[numeric_cols].agg(['min', 'max', 'mean', 'median']).T
        return cross_sample

    def plot_3d_histogram(self):
        """Задание 7: 3D-гистограмма (пример для Age, Sleep Duration, Stress Level)."""
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        x = self.df['Age']
        y = self.df['Sleep Duration']
        z = self.df['Stress Level']

        ax.bar3d(x, y, z, dx=1, dy=1, dz=0.1, shade=True)
        ax.set_xlabel('Age')
        ax.set_ylabel('Sleep Duration')
        ax.set_zlabel('Stress Level')
        plt.title("3D-гистограмма")
        plt.show()


# Пример выполнения всех заданий
if __name__ == "__main__":
    try:
        processor = DatasetProcessor("Sleep_health_and_lifestyle_dataset.csv")

        # Задание 1: Проверка пропусков (вывод первых строк после обработки)
        print("=" * 50)
        print("Задание 1: Проверка обработки пропусков (первые 5 строк):")
        print(processor.display())

        # Задание 2: Проверка значений в столбце 'Occupation'
        print("\n" + "=" * 50)
        print("Задание 2: Наличие значений ['Doctor', 'Engineer'] в Occupation:")
        print(processor.check_values_in_column('Occupation', ['Doctor', 'Engineer']).head())

        # Задание 3: Статистики числовых полей
        print("\n" + "=" * 50)
        print("Задание 3: Статистики числовых полей:")
        print(processor.calculate_statistics())

        # Задание 4: Группировка и гистограмма
        print("\n" + "=" * 50)
        print("Задание 4: Гистограмма среднего Sleep Duration по Occupation")
        processor.plot_grouped_histogram('Occupation', 'Sleep Duration')

        # Задание 5: Фильтрация и статистики
        print("\n" + "=" * 50)
        print("Задание 5: Статистики Sleep Duration для людей старше 40 лет:")
        print(processor.filter_and_statistics("Age > 40", "Sleep Duration"))

        # Задание 7: Перекрестная выборка и 3D-график
        print("\n" + "=" * 50)
        print("Задание 7: Перекрестная выборка статистик:")
        print(processor.create_cross_sample())
        print("\nПопытка построить 3D-гистограмму (может потребоваться другой датасет):")
        processor.plot_3d_histogram()

    except FileNotFoundError as e:
        print(e)