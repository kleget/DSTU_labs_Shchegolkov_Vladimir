"""Парный линейный дискриминантный анализ. Класс 1 соответствует большему F."""
import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
RESULTS = BASE / "results"
np.set_printoptions(precision=3, suppress=True, threshold=np.inf)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def fit_and_score(train, labels, test):
    groups = [train[labels == c] for c in (1, 0)]
    if min(map(len, groups)) < 2 or len(train) < train.shape[1] + 2:
        raise ValueError("Для LDA нужны минимум два объекта каждого класса и n ≥ p + 2.")
    print("1. X1, X2, X0 (строки × признаки)")
    for name, matrix in zip(("X1", "X2", "X0"), [*groups, test]):
        print(name, matrix.shape, "\n", matrix)
    means = [g.mean(axis=0) for g in groups]
    print("2. Средние признаков", *means)
    centered = [g - mean for g, mean in zip(groups, means)]
    covs = [z.T @ z / (len(z) - 1) for z in centered]
    print("3. Ковариационные матрицы\n", covs[0], "\n", covs[1])
    pooled = sum((len(g) - 1) * s for g, s in zip(groups, covs)) / (len(train) - 2)
    rank = np.linalg.matrix_rank(pooled)
    print("4. Общая ковариационная матрица\n", pooled,
          f"\ndet={np.linalg.det(pooled):.9f}, ранг={rank}, число обусловленности={np.linalg.cond(pooled):.3f}")
    if rank < pooled.shape[0]:
        raise ValueError("Ковариационная матрица вырождена. Проверьте зависимость признаков.")
    scales = np.sqrt(np.diag(pooled))
    correlation = pooled / np.outer(scales, scales)
    print("VIF по внутриклассовой корреляции:", np.diag(np.linalg.inv(correlation)))
    inverse = np.linalg.inv(pooled)
    print("5. Обратная матрица\n", inverse)
    weights = inverse @ (means[0] - means[1])
    print("6. Коэффициенты A", weights)
    scores = train @ weights
    print("7. F для обучающих объектов класса 1 и класса 0", scores[labels == 1], scores[labels == 0])
    centers = np.array([scores[labels == c].mean() for c in (1, 0)])
    print("8. Средние F", centers)
    threshold = centers.mean()
    print(f"9. Константа дискриминации = {threshold:.3f}")
    test_scores = test @ weights
    print("10. Классы тестовых объектов (в порядке строк X0)")
    for value in test_scores:
        print(f"{value:.3f} {'>' if value > threshold else '≤'} {threshold:.3f} → {int(value > threshold)}")
    return scores - threshold, test_scores - threshold, centers, threshold, weights


def experiment(ax, x, y, train, test, title, class_names, known):
    train_margin, test_margin, centers, threshold, weights = fit_and_score(x[train], y[train], x[test])
    pred = (test_margin > 0).astype(int)
    library = LinearDiscriminantAnalysis(priors=[0.5, 0.5]).fit(x[train], y[train])
    reference = library.predict(x[test])
    for cls, color in enumerate(("tab:blue", "tab:orange")):
        mask = y[train] == cls
        ax.scatter(train[mask] + 1, train_margin[mask], s=13, color=color, label=class_names[cls])
        mask = pred == cls
        ax.scatter(test[mask] + 1, test_margin[mask], marker="^", facecolors="none",
                   edgecolors=color, label=f"Тест → {class_names[cls]}")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set(xlabel="Номер объекта", ylabel="F − порог", title=title)
    errors = (pred != y[test]) if known else np.zeros(len(test), dtype=bool)
    if errors.any():
        ax.scatter(test[errors] + 1, test_margin[errors], marker="x", color="red", label="Ошибка")
    ax.legend(fontsize=7)
    print(f"Совпадения прогнозов со sklearn: {(pred == reference).sum()}/{len(test)}")
    if not known:
        actual = np.r_[weights, threshold, test_margin + threshold]
        expected = [0.156720, 3.594781, -1.291500, 31.87564, 26.58859, 34.40685, 52.15991]
        print("Контроль из задания", expected, "\nПолучено", actual)
        print("Контроль пройден" if np.allclose(actual, expected, atol=0.00001, rtol=0)
              and np.allclose(centers, [53.29, 10.46], atol=0.005, rtol=0)
              and pred.tolist() == [0, 1, 1] else "Есть расхождение с контрольным примером")
        return []
    rows = []
    for method, prediction in (("Вручную", pred), ("sklearn", reference)):
        matrix = confusion_matrix(y[test], prediction, labels=[0, 1])
        print(method, "— матрица ошибок (строки: истина, столбцы: прогноз, классы 0 и 1)\n", matrix)
        tn, fp, fn, tp = matrix.ravel()
        precision, recall, f1, _ = precision_recall_fscore_support(
            y[test], prediction, average="binary", zero_division=0)
        rows.append(dict(Разбиение=title, Метод=method, TN=tn, FP=fp, FN=fn, TP=tp,
                         Верно=tn+tp, Ошибок=fp+fn, Ошибка_pct=100*(fp+fn)/len(test),
                         Accuracy=accuracy_score(y[test], prediction), Precision=precision,
                         Recall=recall, F1=f1))
    print("Номера ошибочно классифицированных крабов:", (test[errors] + 1).tolist())
    pd.DataFrame({"Объект": test+1, "Истина": y[test], "F минус порог": test_margin,
                  "Вручную": pred, "sklearn": reference}).to_csv(
        RESULTS / f"crabs_{len(test)}_test.csv", index=False, encoding="utf-8-sig")
    return rows


def crabs():
    frame = pd.read_csv(BASE / "crabs.csv")
    columns = ["Лобная доля, мм", "Задняя ширина, мм", "Толщина тела, мм"]
    measurements = frame[[*columns, "Ширина панциря, мм"]].to_numpy(float)
    labels = frame["Цветовая форма"].map({"Синяя": 0, "Оранжевая": 1})
    if labels.isna().any() or not np.isfinite(measurements).all() or (measurements <= 0).any():
        raise ValueError("Проверьте метки классов и положительность измерений в crabs.csv.")
    # Сравниваем пропорции тела у особей разного размера.
    x = 100 * measurements[:, :3] / measurements[:, 3:4]
    print("Число крабов по классам:", frame["Цветовая форма"].value_counts().to_dict())
    print("Повторов сочетания промеров:", frame[columns + ["Ширина панциря, мм"]].duplicated().sum())
    print("Признаки в процентах ширины панциря: лобная доля, задняя ширина, толщина тела.")
    y = labels.to_numpy(int)
    fig, axes = plt.subplots(3, 1, figsize=(12, 10), layout="constrained")
    rows = []
    for ax, percent in zip(axes, [30, 20, 10]):
        train, test = train_test_split(np.arange(len(x)), test_size=percent/100,
                                       stratify=y, random_state=42)
        title = f"{100-percent}/{percent}"
        print("\nЦветовые формы крабов", title)
        rows.extend(experiment(ax, x, y, np.sort(train), np.sort(test), title,
                               ("Синяя", "Оранжевая"), True))
    summary = pd.DataFrame(rows)
    print(summary.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    summary.to_csv(RESULTS / "metrics.csv", index=False, encoding="utf-8-sig")
    fig.savefig(RESULTS / "crabs.png", dpi=150)


def enterprises(path):
    frame = pd.read_csv(path)
    columns = ["Основные фонды", "Численность", "Прибыль"]
    print("Предприятия. Порядок признаков:", columns)
    y = frame["Класс"].fillna(-1).to_numpy(float)
    x = frame[columns].to_numpy(float)
    if len(y) != 12 or [(y == c).sum() for c in (1, 0, -1)] != [4, 5, 3] or not np.isfinite(x).all():
        raise ValueError("Нужны 4 передовых (1), 5 отстающих (0), 3 неизвестных и конечные признаки.")
    fig, ax = plt.subplots(layout="constrained")
    experiment(ax, x, y.astype(int), np.flatnonzero(y >= 0), np.flatnonzero(y < 0),
               "Промышленные предприятия", ("Отстающее", "Передовое"), False)
    fig.savefig(RESULTS / "enterprises.png", dpi=150)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", choices=["all", "enterprises", "crabs"], default="all")
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    RESULTS.mkdir(exist_ok=True)
    if args.dataset in ("all", "enterprises"):
        enterprises(BASE / "enterprises.csv")
    if args.dataset in ("all", "crabs"):
        crabs()
    if not args.no_show:
        plt.show()
