"""Агломеративная кластеризация методом ближайшего соседа. Проверка через SciPy."""

from __future__ import annotations

import argparse
import sys
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results" / "single"


def format_decimal(value: float, precision: int = 20) -> str:
    """Format a number without scientific notation, trimming insignificant zeros."""
    if not np.isfinite(value):
        return str(value)
    formatted = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return "0" if formatted in {"", "-0"} else formatted


DATASETS = [
    {
        "key": "small_regions",
        "title": "Регионы — учебный набор из шести объектов",
        "file": "small_regions.csv",
        "label_column": "Область",
        "feature_columns": ["Машиностроение %", "Электроэнергетика %"],
        "visual_columns": ["Машиностроение %", "Электроэнергетика %"],
    },
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
        "key": "attenu",
        "title": "Записи сейсмостанций Калифорнии",
        "file": "attenu.csv",
        "label_column": "Номер наблюдения",
        "feature_columns": ["Моментная магнитуда", "Расстояние до гипоцентра, км", "Пиковое ускорение, g"],
        "visual_columns": ["Моментная магнитуда", "Расстояние до гипоцентра, км", "Пиковое ускорение, g"],
    },
]


def read_dataset_choice() -> str:
    print("0. Все наборы по очереди")
    for number, config in enumerate(DATASETS, start=1):
        print(f"{number}. {config['title']} ({config['file']})")
    while True:
        choice = input("Выберите набор данных (Enter = все): ").strip()
        if choice in ("", "0"):
            return "all"
        for number, config in enumerate(DATASETS, start=1):
            if choice == str(number):
                return config["key"]
        print(f"Введите номер от 0 до {len(DATASETS)}.")


def read_p(prompt: str = "Введите p для расстояния Минковского (Enter = 2, евклидово): ") -> float:
    """Запросить допустимый показатель Минковского."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        if not raw:
            return 2.0
        try:
            p = float(raw)
        except ValueError:
            print("Введите число, например 1 или 2.")
            continue
        if np.isfinite(p) and p >= 1:
            return p
        print("Для метрики Минковского p должен быть конечным числом не меньше 1.")


def read_cluster_count(maximum: int, title: str) -> int:
    """Запросить число кластеров для раскраски графиков."""
    default = min(2, maximum)
    while True:
        raw = input(f"{title}: сколько кластеров показать? [2..{maximum}, Enter = {default}]: ").strip()
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


def read_dataset(config: dict) -> tuple[pd.DataFrame, list[str], np.ndarray]:
    """Загрузить CSV; использовать числовые признаки в исходном масштабе."""
    path = BASE_DIR / config["file"]
    if not path.is_file():
        raise FileNotFoundError(f"Не найден набор данных: {path}")

    frame = pd.read_csv(path, encoding="utf-8-sig")
    required = [config["label_column"], *config["feature_columns"]]
    missing_columns = [column for column in required if column not in frame.columns]
    if missing_columns:
        raise ValueError(f"В файле {path.name} отсутствуют столбцы: {missing_columns}")

    identifiers = frame[config["label_column"]]
    if identifiers.isna().any() or identifiers.duplicated().any():
        raise ValueError(f"В {path.name} пропущен или повторяется идентификатор объекта.")
    labels = frame[config["label_column"]].astype(str).tolist()
    values = frame[config["feature_columns"]].apply(pd.to_numeric, errors="coerce")
    if values.isna().any().any():
        bad_columns = values.columns[values.isna().any()].tolist()
        raise ValueError(f"В {path.name} есть пропуски/нечисловые значения в {bad_columns}.")

    raw_x = values.to_numpy(dtype=float)
    if len(raw_x) < 2 or not np.isfinite(raw_x).all():
        raise ValueError(f"Для кластеризации в {path.name} нужно не менее двух конечных строк.")
    if config["key"] == "attenu" and (values[["Расстояние до гипоцентра, км", "Пиковое ускорение, g"]] < 0).any().any():
        raise ValueError(f"В {path.name} расстояние и пиковое ускорение должны быть неотрицательными.")

    return frame, labels, raw_x


def minkowski_distance(first: np.ndarray, second: np.ndarray, p: float) -> float:
    """Расстояние Минковского между двумя векторами признаков."""
    delta = np.abs(first - second)
    scale = delta.max()
    if scale == 0:
        return 0.0
    # Масштабирование внутри формулы защищает степень от переполнения при большом p.
    return float(scale * np.sum((delta / scale) ** p) ** (1.0 / p))


def initial_distance_matrix(x: np.ndarray, p: float) -> np.ndarray:
    matrix = np.zeros((len(x), len(x)))
    for i, j in combinations(range(len(x)), 2):
        matrix[i, j] = matrix[j, i] = minkowski_distance(x[i], x[j], p)
    return matrix


def lance_williams_single(d_ac, d_bc, d_ab):
    """Для single: α_A = α_B = 1/2, β = 0, γ = −1/2."""
    alpha_a, alpha_b, beta, gamma = 0.5, 0.5, 0.0, -0.5
    return alpha_a * d_ac + alpha_b * d_bc + beta * d_ab + gamma * np.abs(d_ac - d_bc)


def manual_single_linkage(
    initial: np.ndarray, keep_matrices: bool = False,
) -> tuple[np.ndarray, list[dict], list[tuple[int, pd.DataFrame]]]:
    """В R_t находим минимум, сохраняем старый блок и добавляем строку и столбец."""
    distances = initial
    n_objects = len(initial)
    active_ids = list(range(n_objects))
    sizes = {i: 1 for i in active_ids}
    merges = []
    history = []
    snapshots = []
    for step in range(n_objects - 1):
        if keep_matrices:
            names = [f"C{i + 1}" for i in active_ids]
            snapshots.append((step, pd.DataFrame(distances, index=names, columns=names)))
        rows, cols = np.triu_indices(len(active_ids), k=1)
        closest = np.argmin(distances[rows, cols])
        i, j = rows[closest], cols[closest]
        left, right = active_ids[i], active_ids[j]
        height = distances[i, j]
        new_id = n_objects + step
        sizes[new_id] = sizes[left] + sizes[right]
        merges.append([left, right, height, sizes[new_id]])
        history.append({
            "step": step + 1, "cluster_a": f"C{left + 1}", "cluster_b": f"C{right + 1}",
            "distance": height, "merged_cluster": f"C{new_id + 1}",
            "size": sizes[new_id], "clusters_left": len(active_ids) - 1,
        })

        remaining = [t for t in range(len(active_ids)) if t != i and t != j]
        updated = np.zeros((len(remaining) + 1, len(remaining) + 1))
        updated[:-1, :-1] = distances[np.ix_(remaining, remaining)]
        new_distances = lance_williams_single(distances[i, remaining], distances[j, remaining], height)
        updated[-1, :-1] = updated[:-1, -1] = new_distances
        distances = updated
        active_ids = [active_ids[t] for t in remaining] + [new_id]

    return np.asarray(merges), history, snapshots


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


def merge_groups(z: np.ndarray) -> list[frozenset]:
    """Состав каждого нового узла по шагам, независимо от внутренних номеров SciPy."""
    groups = [frozenset([i]) for i in range(len(z) + 1)]
    for left, right, *_ in z:
        groups.append(groups[int(left)] | groups[int(right)])
    return groups[len(z) + 1:]


def print_small_steps(snapshots: list[tuple[int, pd.DataFrame]], history: list[dict]) -> None:
    for (step, matrix), merge in zip(snapshots, history):
        upper_triangle = matrix.mask(np.tril(np.ones(matrix.shape, dtype=bool)))
        print(f"\nR_{step} — расстояния между активными кластерами:")
        print(upper_triangle.to_string(float_format=lambda value: f"{value:8.4f}", na_rep=""))
        a, b, new = merge["cluster_a"], merge["cluster_b"], merge["merged_cluster"]
        print(f"{a} + {b} → {new}, расстояние {merge['distance']:.5f}, "
              f"осталось кластеров: {merge['clusters_left']}.")
        if step == 0:
            c = next(name for name in matrix if name not in (a, b))
            ac, bc = matrix.loc[a, c], matrix.loc[b, c]
            print(f"Ланс — Уильямс для d({new},{c}): "
                  f"0.5 × {ac:.5f} + 0.5 × {bc:.5f} + 0 × {merge['distance']:.5f} "
                  f"− 0.5 × |{ac:.5f} − {bc:.5f}| = {lance_williams_single(ac, bc, merge['distance']):.5f}")


def save_matrix_snapshots(
    snapshots: list[tuple[int, pd.DataFrame]],
    output_dir: Path,
    dataset_key: str,
    p: float,
) -> None:
    """Сохранить полные симметричные матрицы учебного примера в CSV."""
    matrix_dir = output_dir / "matrices"
    matrix_dir.mkdir(parents=True, exist_ok=True)
    p_tag = f"{p:g}".replace(".", "_")
    for step, matrix in snapshots:
        matrix.to_csv(
            matrix_dir / f"{dataset_key}_p{p_tag}_R{step:02d}.csv",
            encoding="utf-8-sig",
            float_format="%.8f",
            lineterminator="\n",
        )


def plot_dendrogram(
    z: np.ndarray,
    object_labels: list[str],
    title: str,
    p: float,
    k: int,
    destination: Path,
    cluster_labels: np.ndarray,
    colors: dict,
    scale: str,
) -> None:
    """Полное дерево или свёрнутый обзор с теми же цветами, что у точек."""
    n_objects = len(object_labels)
    node_cluster = list(cluster_labels)
    for left, right, *_ in z:
        a, b = node_cluster[int(left)], node_cluster[int(right)]
        node_cluster.append(a if a == b else 0)

    full = scale == "full"
    fig, ax = plt.subplots(figsize=(max(12, n_objects * 0.10) if full else 12, 6.5))
    options = {}
    if not full:
        options.update(truncate_mode="lastp", p=30 if scale == "overview" else 10,
                       show_contracted=True)

    def leaf_label(node: int) -> str:
        if node < n_objects:
            return object_labels[node]
        return f"Группа ({int(z[node - n_objects, 3])})"

    tree = dendrogram(z, ax=ax, leaf_rotation=90, leaf_font_size=7,
                      leaf_label_func=leaf_label,
                      link_color_func=lambda node: colors.get(node_cluster[node], "#555555"),
                      **options)
    for tick, node in zip(ax.get_xticklabels(), tree["leaves"]):
        tick.set_color(colors.get(node_cluster[node], "#555555"))
    ax.set_title(f"Дендрограмма: {title}\nБлижайший сосед, Минковский p={p:g}")
    ax.set_xlabel("Объекты" if full else "Объекты и свёрнутые группы (число записей)")
    ax.set_ylabel("Расстояние слияния")
    completed = n_objects - k
    lower = float(np.max(z[:completed, 2])) if completed else 0.0
    upper = float(np.min(z[completed:, 2]))
    if lower < upper:
        cut_height = (lower + upper) / 2
        ax.axhline(cut_height, color="black", linestyle="--", linewidth=1.1)
        ax.text(0.99, cut_height, f" разрез: k={k}",
                transform=ax.get_yaxis_transform(), ha="right", va="bottom", fontsize=8)
    else:
        ax.text(0.01, 0.99, f"k={k}: после {completed} слияний; единого горизонтального разреза нет",
                transform=ax.transAxes, va="top", fontsize=8)

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
    colors: dict,
) -> None:
    """Нарисовать цветную 2D- или 3D-проекцию кластеров."""
    indices = [feature_columns.index(column) for column in visual_columns]
    points = x[:, indices]
    cluster_numbers = np.unique(cluster_labels)
    legend_columns = (len(cluster_numbers) + 19) // 20
    figsize = (9 + 1.25 * legend_columns, 7.5)
    if len(indices) == 2:
        fig, ax = plt.subplots(figsize=figsize, layout="constrained")
        for cluster_number in cluster_numbers:
            mask = cluster_labels == cluster_number
            ax.scatter(
                points[mask, 0],
                points[mask, 1],
                s=65,
                color=colors[cluster_number],
                label=f"{cluster_number}: {mask.sum()}",
                edgecolors="black",
                linewidths=0.35,
            )
        if len(object_labels) <= 20:
            for index, label in enumerate(object_labels):
                ax.annotate(label, (points[index, 0], points[index, 1]), fontsize=7,
                            xytext=(4, 3), textcoords="offset points")
        ax.set_xlabel(visual_columns[0])
        ax.set_ylabel(visual_columns[1])
        ax.grid(alpha=0.25)
    elif len(indices) == 3:
        fig = plt.figure(figsize=figsize, layout="constrained")
        ax = fig.add_subplot(111, projection="3d")
        for cluster_number in cluster_numbers:
            mask = cluster_labels == cluster_number
            ax.scatter(
                points[mask, 0],
                points[mask, 1],
                points[mask, 2],
                s=48,
                color=colors[cluster_number],
                label=f"{cluster_number}: {mask.sum()}",
                edgecolors="black",
                linewidths=0.3,
            )
        ax.set_xlabel(visual_columns[0])
        ax.set_ylabel(visual_columns[1])
        ax.set_zlabel(visual_columns[2])
        if len(object_labels) <= 20:
            for point, label in zip(points, object_labels):
                ax.text(*point, label.split(". ", 1)[0], fontsize=7)
        ax.view_init(elev=24, azim=35)
    else:
        raise ValueError("Для визуализации выберите два или три признака.")

    fig.suptitle(f"{title}: кластеры, p={p:g}, k={len(cluster_numbers)}")
    fig.legend(loc="outside right center", ncols=legend_columns, title="Кластер: число объектов",
               fontsize=9, columnspacing=1, handletextpad=0.3, borderaxespad=1)
    fig.savefig(destination, dpi=160, bbox_inches="tight")


def save_merge_history(history: list[dict], destination: Path) -> None:
    pd.DataFrame(history).to_csv(
        destination,
        index=False,
        encoding="utf-8-sig",
        float_format="%.8f",
        lineterminator="\n",
    )


def run_dataset(
    config: dict,
    dataset: tuple[pd.DataFrame, list[str], np.ndarray],
    p: float,
    k: int,
    output_dir: Path,
    normalize: bool,
    dendrogram_scale: str,
    save_region_matrices: bool,
) -> dict:
    frame, object_labels, raw_x = dataset
    key = config["key"]
    n_objects = len(raw_x)
    x = raw_x
    feature_labels = {name: name for name in config["feature_columns"]}
    mode = "исходный масштаб"
    if normalize:
        span = np.ptp(raw_x, axis=0)
        x = (raw_x - raw_x.min(axis=0)) / np.where(span == 0, 1, span)
        mode = "min–max [0, 1]"
        feature_labels = {name: f"{name.split(',')[0]} [0–1]" for name in feature_labels}
    title = f"{config['title']} ({mode})"
    print(f"\n{'=' * 72}\n{title}\nОбъектов: {n_objects}, признаков: {x.shape[1]}.")
    if key == "attenu":
        print("Объект — запись наблюдения. Признаки: магнитуда, расстояние до гипоцентра "
              "(км), пиковое ускорение (в единицах g).")
    else:
        object_labels = [f"{i}. {name}" for i, name in enumerate(object_labels, start=1)]

    initial = initial_distance_matrix(x, p)
    keep_matrices = key == "small_regions" or (key == "regions" and save_region_matrices)
    z_manual, history, snapshots = manual_single_linkage(initial, keep_matrices)
    if keep_matrices:
        save_matrix_snapshots(snapshots, output_dir, key, p)
    if key == "small_regions":
        print_small_steps(snapshots, history)

    labels_manual = labels_at_k(z_manual, n_objects, k)
    result_dir = output_dir
    result_dir.mkdir(parents=True, exist_ok=True)
    p_tag = f"{p:g}".replace(".", "_")

    cluster_file = result_dir / f"{config['key']}_clusters_p{p_tag}_k{k}.csv"
    profiles = pd.DataFrame(x, columns=list(feature_labels.values()))
    details = profiles.copy()
    details.insert(0, "Объект", frame[config["label_column"]].to_numpy())
    details["Кластер"] = labels_manual
    details.to_csv(cluster_file, index=False, encoding="utf-8-sig", lineterminator="\n")
    profiles.insert(0, "Кластер", labels_manual)
    means = profiles.groupby("Кластер").mean()
    means.insert(0, "Объектов", profiles.groupby("Кластер").size())
    means.to_csv(result_dir / f"{config['key']}_cluster_profiles_p{p_tag}_k{k}.csv",
                 encoding="utf-8-sig", lineterminator="\n")
    print(f"\nРазмеры кластеров и средние значения признаков ({mode}):")
    print(means.to_string(float_format=lambda value: f"{value:.3f}"))
    if key == "attenu":
        print("\nПример наблюдений (полная таблица с измерениями и кластерами сохранена в CSV):")
        print(details.head().to_string(index=False, float_format=lambda value: format_decimal(value, 6)))
    save_merge_history(history, result_dir / f"{config['key']}_merges_p{p_tag}.csv")

    dendrogram_path = result_dir / f"{config['key']}_dendrogram_p{p_tag}.png"
    palette = plt.get_cmap("tab10" if k <= 10 else "turbo", k if k > 10 else 10)
    colors = {number: to_hex(palette(number - 1)) for number in range(1, k + 1)}
    plot_dendrogram(z_manual, object_labels, title, p, k, dendrogram_path,
                    labels_manual, colors, dendrogram_scale)

    scatter_path = result_dir / f"{config['key']}_scatter_p{p_tag}.png"
    plot_scatter(
        x,
        list(feature_labels.values()),
        [feature_labels[column] for column in config["visual_columns"]],
        object_labels,
        labels_manual,
        title,
        p,
        scatter_path,
        colors,
    )

    reference_distances = pdist(x, metric="minkowski", p=p)
    if not np.isfinite(reference_distances).all() or np.any(
        (reference_distances == 0) & (squareform(initial) != 0)
    ):
        # При больших p прямое возведение в степень в pdist может выйти за диапазон.
        # scipy.linalg.norm с нормированием каждой пары сохраняет сравнимую точность.
        from scipy.linalg import norm

        def scaled_norm(a, b):
            delta = a - b
            scale = np.max(np.abs(delta))
            return scale * norm(delta / scale, ord=p) if scale else 0.0

        reference_distances = pdist(x, metric=scaled_norm)
    z_scipy = linkage(reference_distances, method="single")
    labels_scipy = labels_at_k(z_scipy, n_objects, k)
    agreement = pairwise_partition_agreement(labels_manual, labels_scipy)
    height_difference = float(np.max(np.abs(z_manual[:, 2] - z_scipy[:, 2])))
    first_matrix_difference = float(np.max(np.abs(squareform(initial) - reference_distances)))
    manual_groups, scipy_groups = merge_groups(z_manual), merge_groups(z_scipy)
    matching_steps = sum(a == b for a, b in zip(manual_groups, scipy_groups))
    shared_nodes = len(set(manual_groups) & set(scipy_groups))
    scipy_sizes = np.bincount(labels_scipy)[1:]
    print(f"\nSciPy single при p={format_decimal(p)}. Разбиение при k={k}: "
          f"согласие пар {agreement:.1%}, размеры SciPy {scipy_sizes.tolist()}.")
    print(f"Совпало новых групп по шагам: {matching_steps}/{len(history)}, "
          f"узлов дерева по составу: {shared_nodes}/{len(history)}.")
    print(f"Макс. расхождение начальных расстояний: {format_decimal(first_matrix_difference)}. "
          f"Макс. разница высот слияний: {height_difference:.5f}.")

    return {
        "dataset": key, "objects": n_objects, "features": x.shape[1], "p": p, "k": k,
        "scale": mode, "initial_matrix_max_abs_error": first_matrix_difference,
        "pair_agreement": agreement, "max_merge_height_difference": f"{height_difference:.5f}",
        "matching_steps": matching_steps, "shared_tree_nodes": shared_nodes,
        "manual_sizes": ",".join(map(str, np.bincount(labels_manual)[1:])),
        "scipy_sizes": ",".join(map(str, scipy_sizes)),
        "scatter_dimensions": len(config["visual_columns"]),
        "cluster_file": str(cluster_file.relative_to(BASE_DIR)),
        "dendrogram_file": str(dendrogram_path.relative_to(BASE_DIR)),
        "scatter_file": str(scatter_path.relative_to(BASE_DIR)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ручная агломеративная кластеризация методом ближайшего соседа с расстоянием Минковского."
    )
    parser.add_argument("--dataset", choices=["all", *(config["key"] for config in DATASETS)],
                        help="Имя набора без .csv или all для запуска всех наборов.")
    parser.add_argument("--p", type=float, help="Показатель Минковского (например, 1 или 2).")
    parser.add_argument("--k", type=int, help="Общее число кластеров, если для набора не указано отдельное.")
    parser.add_argument("--normalize-large", action=argparse.BooleanOptionalAction, default=None,
                        help="Нормализация min–max только для записей сейсмостанций (по умолчанию выключена).")
    parser.add_argument("--dendrogram-scale", choices=["full", "overview", "top"], default="full",
                        help="Все листья, последние 30 или последние 10 групп.")
    parser.add_argument("--save-region-matrices", action="store_true",
                        help="Сохранить матрицы 18 регионов в CSV без печати в терминал.")
    for config in DATASETS:
        parser.add_argument(f"--axes-{config['key'].replace('_', '-')}", nargs="+", type=int,
                            help="Номера двух или трёх признаков для осей, начиная с 1.")
        parser.add_argument(f"--k-{config['key'].replace('_', '-')}", type=int,
                            help=f"Число кластеров: {config['title']}.")
    parser.add_argument("--no-show", action="store_true", help="Только сохранить графики, не открывать окна.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    selected = args.dataset or (read_dataset_choice() if len(sys.argv) == 1 else "all")
    configs = [config for config in DATASETS if selected in ("all", config["key"])]
    p = args.p if args.p is not None else read_p()
    if not np.isfinite(p) or p < 1:
        raise SystemExit("Параметр --p должен быть конечным и не меньше 1.")
    includes_large = selected in ("all", "attenu")
    if includes_large and args.normalize_large is None and args.p is None:
        while True:
            answer = input("Нормализовать признаки сейсмостанций? [1 — да, 0 или Enter — нет]: ").strip()
            if answer in ("", "0", "1"):
                args.normalize_large = answer == "1"
                break
            print("Введите 1 или 0.")

    loaded = []
    for template in configs:
        config = template.copy()
        axes = getattr(args, f"axes_{config['key']}")
        features = config["feature_columns"]
        if axes is not None:
            if (len(axes) not in (2, 3) or len(set(axes)) != len(axes)
                    or any(i < 1 or i > len(features) for i in axes)):
                raise SystemExit(f"{config['title']}: выберите две или три различные оси из 1..{len(features)}.")
            config["visual_columns"] = [features[i - 1] for i in axes]
        loaded.append((config, read_dataset(config)))
    cluster_counts = {}
    for config, dataset in loaded:
        k = getattr(args, f"k_{config['key']}")
        if k is None:
            k = args.k
        if k is not None and not 2 <= k <= len(dataset[1]):
            raise SystemExit(f"{config['title']}: число кластеров должно быть от 2 до {len(dataset[1])}.")
        cluster_counts[config["key"]] = k

    scale_dir = "large_minmax" if includes_large and args.normalize_large else "raw"
    output_dir = RESULTS_DIR / f"p_{p:g}".replace(".", "_") / scale_dir
    if selected != "all":
        output_dir = output_dir / selected
    output_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict] = []
    for config, dataset in loaded:
        k = cluster_counts[config["key"]]
        if k is None:
            k = read_cluster_count(len(dataset[1]), config["title"])
        summaries.append(run_dataset(config, dataset, p, k, output_dir,
                                     config["key"] == "attenu" and args.normalize_large,
                                     args.dendrogram_scale, args.save_region_matrices))

        if args.no_show:
            plt.close("all")
        else:
            print("\nОткрыты две диаграммы текущего набора. Для продолжения закройте оба окна.")
            plt.show()

    pd.DataFrame(summaries).to_csv(
        output_dir / "comparison_summary.csv",
        index=False,
        encoding="utf-8-sig",
        float_format=lambda value: format_decimal(value),
        lineterminator="\n",
    )
    print(f"\nГрафиков сохранено: {2 * len(summaries)}. Папка результатов: {output_dir}")
    if selected in ("all", "small_regions"):
        print("Матрицы R₀…R₄ для шести регионов сохранены в подпапке matrices.")

if __name__ == "__main__":
    main()
