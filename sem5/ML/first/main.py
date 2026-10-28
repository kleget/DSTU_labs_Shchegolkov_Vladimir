"""Агломеративная кластеризация Минковского с методом центроидов.

Ручная часть каждый раз пересчитывает центры активных кластеров и расстояния
между ними. SciPy используется как независимая библиотечная реализация при p=2.
"""

from __future__ import annotations

import argparse
import sys
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
MATRIX_DATASET_LIMIT = 20


DATASETS = [
    {
        "key": "regions",
        "title": "Регионы России — показатели расходов",
        "file": "regions.csv",
        "label_column": "Название",
        "feature_columns": [
            "Покупка товаров и оплата услуг",
            "Приобретение недвижимости",
            "Прирост (уменьшение) денег на руках у населения",
        ],
        "visual_columns": [
            "Покупка товаров и оплата услуг",
            "Приобретение недвижимости",
            "Прирост (уменьшение) денег на руках у населения",
        ],
    },
    {
        "key": "small_regions",
        "title": "Регионы — учебный набор из шести объектов",
        "file": "small_regions.csv",
        "label_column": "Область",
        "feature_columns": ["Машиностроение %", "Электроэнергетика %"],
        "visual_columns": ["Машиностроение %", "Электроэнергетика %"],
    },
    {
        "key": "iris",
        "title": "Измерения цветков UCI Iris",
        "file": "iris.csv",
        "label_column": "Object",
        "feature_columns": [
            "Sepal_length_cm",
            "Sepal_width_cm",
            "Petal_length_cm",
            "Petal_width_cm",
        ],
        "visual_columns": ["Sepal_length_cm", "Petal_length_cm", "Petal_width_cm"],
    },
]


def read_p(prompt: str = "Введите p для расстояния Минковского (p >= 1): ") -> float:
    """Запросить допустимый показатель Минковского."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            p = float(raw)
        except ValueError:
            print("Введите число, например 1 или 2.")
            continue
        if np.isfinite(p) and p >= 1:
            return p
        print("Для метрики Минковского p должен быть конечным числом не меньше 1.")


def read_cluster_count(maximum: int) -> int:
    """Запросить число кластеров для раскраски графиков."""
    default = min(2, maximum)
    while True:
        raw = input(f"Сколько кластеров показать? [2..{maximum}, Enter = {default}]: ").strip()
        if not raw:
            return default
        try:
            count = int(raw)
        except ValueError:
            print("Введите целое число.")
            continue
        if 2 <= count <= maximum:
            return count
        print(f"Допустимое число кластеров: от 2 до {maximum}.")


def read_dataset(config: dict) -> tuple[pd.DataFrame, list[str], np.ndarray, np.ndarray]:
    """Загрузить CSV и стандартизировать числовые признаки."""
    path = BASE_DIR / config["file"]
    if not path.is_file():
        raise FileNotFoundError(f"Не найден набор данных: {path}")

    frame = pd.read_csv(path, encoding="utf-8-sig")
    required = [config["label_column"], *config["feature_columns"]]
    missing_columns = [column for column in required if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"В файле {path.name} отсутствуют столбцы: {missing_columns}")

    labels = frame[config["label_column"]].astype(str).tolist()
    values = frame[config["feature_columns"]].apply(pd.to_numeric, errors="coerce")
    if values.isna().any().any():
        bad_columns = values.columns[values.isna().any()].tolist()
        raise ValueError(f"В {path.name} есть пропуски/нечисловые значения в {bad_columns}.")

    raw_x = values.to_numpy(dtype=float)
    if len(raw_x) < 2 or not np.isfinite(raw_x).all():
        raise ValueError(f"Для кластеризации в {path.name} нужно не менее двух конечных строк.")

    mean = raw_x.mean(axis=0)
    scale = raw_x.std(axis=0)
    scale[scale == 0] = 1.0
    standardized_x = (raw_x - mean) / scale
    return frame, labels, raw_x, standardized_x


def minkowski_distance(first: np.ndarray, second: np.ndarray, p: float) -> float:
    """Расстояние Минковского между двумя векторами признаков."""
    return float(np.sum(np.abs(first - second) ** p) ** (1.0 / p))


def cluster_distance_matrix(
    active_ids: list[int],
    members: dict[int, list[int]],
    x: np.ndarray,
    p: float,
) -> np.ndarray:
    """Построить матрицу расстояний между центроидами активных кластеров."""
    centers = {
        cluster_id: x[members[cluster_id]].mean(axis=0)
        for cluster_id in active_ids
    }
    matrix = np.zeros((len(active_ids), len(active_ids)), dtype=float)
    for i, j in combinations(range(len(active_ids)), 2):
        distance = minkowski_distance(centers[active_ids[i]], centers[active_ids[j]], p)
        matrix[i, j] = distance
        matrix[j, i] = distance
    return matrix


def manual_centroid_linkage(
    x: np.ndarray,
    p: float,
    keep_matrices: bool = False,
) -> tuple[np.ndarray, list[dict], list[tuple[int, pd.DataFrame]]]:
    """Построить полную иерархию ручным методом ближайших центроидов."""
    n_objects = len(x)
    active_ids = list(range(n_objects))
    members = {object_id: [object_id] for object_id in active_ids}
    next_id = n_objects
    merges: list[list[float]] = []
    history: list[dict] = []
    snapshots: list[tuple[int, pd.DataFrame]] = []

    while len(active_ids) > 1:
        active_ids.sort()
        distances = cluster_distance_matrix(active_ids, members, x, p)

        if keep_matrices:
            cluster_names = [f"C{cluster_id + 1}" for cluster_id in active_ids]
            snapshot = pd.DataFrame(distances, index=cluster_names, columns=cluster_names)
            snapshots.append((n_objects - len(active_ids), snapshot))

        candidates = [
            (distances[i, j], active_ids[i], active_ids[j])
            for i, j in combinations(range(len(active_ids)), 2)
        ]
        distance, left_id, right_id = min(candidates, key=lambda item: (item[0], item[1], item[2]))

        new_id = next_id
        next_id += 1
        merged_members = members[left_id] + members[right_id]
        members[new_id] = merged_members
        history.append(
            {
                "step": len(history) + 1,
                "cluster_a": f"C{left_id + 1}",
                "cluster_b": f"C{right_id + 1}",
                "distance": distance,
                "merged_cluster": f"C{new_id + 1}",
                "size": len(merged_members),
            }
        )
        merges.append([left_id, right_id, distance, len(merged_members)])
        active_ids = [cluster_id for cluster_id in active_ids if cluster_id not in (left_id, right_id)]
        active_ids.append(new_id)

    return np.asarray(merges, dtype=float), history, snapshots


def labels_at_k(linkage_matrix: np.ndarray, n_objects: int, n_clusters: int) -> np.ndarray:
    """Получить разбиение после первых n-k слияний."""
    clusters = {object_id: [object_id] for object_id in range(n_objects)}
    for step, row in enumerate(linkage_matrix[: n_objects - n_clusters]):
        left_id, right_id = int(row[0]), int(row[1])
        clusters[n_objects + step] = clusters.pop(left_id) + clusters.pop(right_id)

    ordered = sorted(clusters.values(), key=min)
    result = np.empty(n_objects, dtype=int)
    for cluster_number, object_ids in enumerate(ordered, start=1):
        result[object_ids] = cluster_number
    return result


def pairwise_partition_agreement(first: np.ndarray, second: np.ndarray) -> float:
    """Доля пар объектов, для которых совпадает факт совместного членства."""
    n_objects = len(first)
    if n_objects < 2:
        return 1.0
    matches = 0
    total = 0
    for i, j in combinations(range(n_objects), 2):
        matches += (first[i] == first[j]) == (second[i] == second[j])
        total += 1
    return matches / total


def initial_distance_check(x: np.ndarray, p: float) -> float:
    """Сравнить начальную матрицу ручных расстояний с scipy.spatial.distance.pdist."""
    hand_matrix = cluster_distance_matrix(
        list(range(len(x))), {i: [i] for i in range(len(x))}, x, p
    )
    scipy_matrix = squareform(pdist(x, metric="minkowski", p=p))
    return float(np.max(np.abs(hand_matrix - scipy_matrix)))


def print_matrix_examples(snapshots: list[tuple[int, pd.DataFrame]], n_objects: int) -> None:
    """Показать матрицы R_t: все для набора из шести строк, выборочно для 18 строк."""
    if not snapshots:
        return
    if n_objects <= 6:
        selected = snapshots
    else:
        indices = sorted({0, min(1, len(snapshots) - 1), len(snapshots) - 1})
        selected = [snapshots[index] for index in indices]
    for step, matrix in selected:
        print(f"\nR_{step} — расстояния между текущими центроидами:")
        print(matrix.to_string(float_format=lambda value: f"{value:8.4f}"))


def save_matrix_snapshots(
    snapshots: list[tuple[int, pd.DataFrame]],
    output_dir: Path,
    dataset_key: str,
    p: float,
) -> None:
    """Сохранить промежуточные матрицы маленьких учебных наборов в CSV."""
    matrix_dir = output_dir / "matrices"
    matrix_dir.mkdir(parents=True, exist_ok=True)
    p_tag = f"{p:g}".replace(".", "_")
    for step, matrix in snapshots:
        matrix.to_csv(
            matrix_dir / f"{dataset_key}_p{p_tag}_R{step:02d}.csv",
            encoding="utf-8-sig",
            float_format="%.8f",
        )


def plot_dendrogram(
    z: np.ndarray,
    object_labels: list[str],
    title: str,
    p: float,
    destination: Path,
) -> None:
    """Нарисовать дендрограмму ручной иерархии."""
    fig, ax = plt.subplots(figsize=(12, 6.5))
    options: dict = {
        "leaf_rotation": 90,
        "leaf_font_size": 8,
        "ax": ax,
    }
    if len(object_labels) <= 40:
        options["labels"] = object_labels
    else:
        options["truncate_mode"] = "lastp"
        options["p"] = 30
        options["show_contracted"] = True
    dendrogram(z, **options)
    ax.set_title(f"Дендрограмма: {title}; центроид, Минковский p={p:g}")
    ax.set_xlabel("Объекты" if len(object_labels) <= 40 else "Последние слияния групп")
    ax.set_ylabel("Расстояние между центроидами")
    fig.tight_layout()
    fig.savefig(destination, dpi=160, bbox_inches="tight")


def plot_scatter(
    x: np.ndarray,
    feature_columns: list[str],
    visual_columns: list[str],
    object_labels: list[str],
    cluster_labels: np.ndarray,
    title: str,
    p: float,
    destination: Path,
) -> None:
    """Нарисовать цветную 2D- или 3D-проекцию кластеров."""
    indices = [feature_columns.index(column) for column in visual_columns]
    points = x[:, indices]
    colors = plt.get_cmap("tab10")

    if len(indices) == 2:
        fig, ax = plt.subplots(figsize=(9, 6.5))
        for cluster_number in sorted(np.unique(cluster_labels)):
            mask = cluster_labels == cluster_number
            ax.scatter(
                points[mask, 0],
                points[mask, 1],
                s=65,
                color=colors((cluster_number - 1) % 10),
                label=f"Кластер {cluster_number}",
                edgecolors="black",
                linewidths=0.35,
            )
        if len(object_labels) <= 20:
            for index, label in enumerate(object_labels):
                ax.annotate(label, (points[index, 0], points[index, 1]), fontsize=7,
                            xytext=(4, 3), textcoords="offset points")
        ax.set_xlabel(f"{visual_columns[0]} (z-score)")
        ax.set_ylabel(f"{visual_columns[1]} (z-score)")
        ax.grid(alpha=0.25)
        ax.legend()
    elif len(indices) == 3:
        fig = plt.figure(figsize=(10, 7.5))
        ax = fig.add_subplot(111, projection="3d")
        for cluster_number in sorted(np.unique(cluster_labels)):
            mask = cluster_labels == cluster_number
            ax.scatter(
                points[mask, 0],
                points[mask, 1],
                points[mask, 2],
                s=48,
                color=colors((cluster_number - 1) % 10),
                label=f"Кластер {cluster_number}",
                edgecolors="black",
                linewidths=0.3,
            )
        ax.set_xlabel(f"{visual_columns[0]} (z-score)")
        ax.set_ylabel(f"{visual_columns[1]} (z-score)")
        ax.set_zlabel(f"{visual_columns[2]} (z-score)")
        ax.view_init(elev=24, azim=35)
        ax.legend()
    else:
        raise ValueError("Для визуализации выберите два или три признака.")

    fig.suptitle(f"{title}: кластеры, p={p:g}, k={len(np.unique(cluster_labels))}")
    fig.tight_layout()
    fig.savefig(destination, dpi=160, bbox_inches="tight")


def save_merge_history(history: list[dict], destination: Path) -> None:
    pd.DataFrame(history).to_csv(destination, index=False, encoding="utf-8-sig", float_format="%.8f")


def run_dataset(
    config: dict,
    dataset: tuple[pd.DataFrame, list[str], np.ndarray, np.ndarray],
    p: float,
    k: int,
    output_dir: Path,
    figures: list[plt.Figure],
) -> dict:
    _frame, object_labels, _raw_x, x = dataset
    n_objects = len(x)
    print(f"\n{'=' * 72}\n{config['title']}\nОбъектов: {n_objects}; признаков для кластеризации: {x.shape[1]}")

    keep_matrices = n_objects <= MATRIX_DATASET_LIMIT
    z_manual, history, snapshots = manual_centroid_linkage(x, p, keep_matrices=keep_matrices)
    if keep_matrices:
        print_matrix_examples(snapshots, n_objects)
        save_matrix_snapshots(snapshots, output_dir, config["key"], p)

    labels_manual = labels_at_k(z_manual, n_objects, k)
    result_dir = output_dir / f"p_{p:g}".replace(".", "_")
    result_dir.mkdir(parents=True, exist_ok=True)
    p_tag = f"{p:g}".replace(".", "_")

    cluster_file = result_dir / f"{config['key']}_clusters_p{p_tag}_k{k}.csv"
    pd.DataFrame(
        {"Объект": object_labels, "Кластер": labels_manual}
    ).to_csv(cluster_file, index=False, encoding="utf-8-sig")
    save_merge_history(history, result_dir / f"{config['key']}_merges_p{p_tag}.csv")

    dendrogram_path = result_dir / f"{config['key']}_dendrogram_p{p_tag}.png"
    plot_dendrogram(z_manual, object_labels, config["title"], p, dendrogram_path)
    figures.append(plt.gcf())

    scatter_path = result_dir / f"{config['key']}_scatter_p{p_tag}.png"
    plot_scatter(
        x,
        config["feature_columns"],
        config["visual_columns"],
        object_labels,
        labels_manual,
        config["title"],
        p,
        scatter_path,
    )
    figures.append(plt.gcf())

    # SciPy centroid linkage is mathematically defined for Euclidean distances (p=2).
    # If another p was requested, p=2 is still run as an independent reference check.
    z_manual_p2 = z_manual if np.isclose(p, 2.0) else manual_centroid_linkage(x, 2.0)[0]
    z_scipy_p2 = linkage(x, method="centroid", metric="euclidean")
    labels_hand_p2 = labels_at_k(z_manual_p2, n_objects, k)
    labels_scipy_p2 = labels_at_k(z_scipy_p2, n_objects, k)
    agreement = pairwise_partition_agreement(labels_hand_p2, labels_scipy_p2)
    height_difference = float(np.max(np.abs(z_manual_p2[:, 2] - z_scipy_p2[:, 2])))
    first_matrix_difference = initial_distance_check(x, p)

    print(f"\nСлияния ручного алгоритма: {len(history)}; итоговое разбиение для графика: k={k}.")
    print(f"Максимальное расхождение начальной матрицы и scipy.pdist при p={p:g}: {first_matrix_difference:.3e}")
    print(f"Ручной алгоритм и SciPy centroid при p=2: согласие пар на k={k} — {agreement:.1%}; "
          f"макс. разница высот слияний — {height_difference:.3e}.")
    if not np.isclose(p, 2.0):
        print("Для выбранного p SciPy не используется как centroid-кластеризатор: его centroid-linkage "
              "определён для евклидовой метрики. Сравнение полной иерархии выше выполнено отдельно при p=2.")

    return {
        "dataset": config["key"],
        "objects": n_objects,
        "features": x.shape[1],
        "p_requested": p,
        "k": k,
        "initial_matrix_max_abs_error": first_matrix_difference,
        "p2_pair_agreement": agreement,
        "p2_max_merge_height_difference": height_difference,
        "scatter_dimensions": len(config["visual_columns"]),
        "cluster_file": str(cluster_file.relative_to(BASE_DIR)),
        "dendrogram_file": str(dendrogram_path.relative_to(BASE_DIR)),
        "scatter_file": str(scatter_path.relative_to(BASE_DIR)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ручная агломеративная кластеризация центроидов с расстоянием Минковского."
    )
    parser.add_argument("--p", type=float, help="Показатель Минковского (например, 1 или 2).")
    parser.add_argument("--k", type=int, help="Число кластеров для раскраски (по умолчанию 2).")
    parser.add_argument("--no-show", action="store_true", help="Только сохранить графики, не открывать окна.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    p = args.p if args.p is not None else read_p()
    if not np.isfinite(p) or p < 1:
        raise SystemExit("Параметр --p должен быть конечным и не меньше 1.")

    loaded = [(config, read_dataset(config)) for config in DATASETS]
    min_objects = min(len(data[1]) for _, data in loaded)
    k = args.k if args.k is not None else read_cluster_count(min_objects)
    if not 2 <= k <= min_objects:
        raise SystemExit(f"Значение --k должно быть от 2 до {min_objects} для всех трёх наборов.")

    output_dir = RESULTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    figures: list[plt.Figure] = []
    summaries = [
        run_dataset(config, dataset, p, k, output_dir, figures)
        for config, dataset in loaded
    ]

    summary_dir = output_dir / f"p_{p:g}".replace(".", "_")
    summary_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summaries).to_csv(
        summary_dir / "comparison_summary.csv", index=False, encoding="utf-8-sig", float_format="%.12g"
    )
    print(f"\nСозданы 6 графиков и таблицы результатов: {summary_dir}")
    print("Матрицы R_t для двух малых наборов сохранены в папке results/matrices.")

    if args.no_show:
        for figure in figures:
            plt.close(figure)
    else:
        plt.show()


if __name__ == "__main__":
    main()
