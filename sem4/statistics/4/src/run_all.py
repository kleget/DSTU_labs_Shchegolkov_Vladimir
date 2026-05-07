"""
Практическая работа по байесовскому анализу и вероятностному программированию.

Запуск из папки проекта:
    python src/run_all.py

Код специально написан простыми функциями: pandas читает таблицы,
numpy считает выборки, scipy дает распределения, matplotlib строит графики.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats, optimize
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PLOTS = ROOT / "plots"
RESULTS = ROOT / "results"

RNG = np.random.default_rng(42)


def save_plot(name):
    """Сохранить текущий график в папку plots."""
    PLOTS.mkdir(exist_ok=True)
    path = PLOTS / name
    plt.tight_layout()
    plt.savefig(path, dpi=180, bbox_inches="tight")
    plt.close()
    return path


def hdi(samples, level=0.94):
    """Короткий интервал высокой плотности для одномерных выборок."""
    s = np.sort(np.asarray(samples))
    n = len(s)
    width = int(np.floor(level * n))
    if width < 2:
        return np.nan, np.nan
    spans = s[width:] - s[: n - width]
    left = np.argmin(spans)
    return float(s[left]), float(s[left + width])


def summarize(samples, name):
    """Сводка по апостериорным выборкам."""
    lo, hi = hdi(samples)
    return {
        "param": name,
        "mean": np.mean(samples),
        "sd": np.std(samples, ddof=1),
        "hdi_3": lo,
        "hdi_97": hi,
    }


# -----------------------------------------------------------------------------
# Один новый датасет из интернета, но храним локально, чтобы работа запускалась без сети.
# Источник: R datasets ToothGrowth. Второй датасет для вероятностного
# программирования — anscombe.csv, который был дан в задании.
# -----------------------------------------------------------------------------

def make_toothgrowth():
    rows = [
        (4.2, "VC", 0.5), (11.5, "VC", 0.5), (7.3, "VC", 0.5),
        (5.8, "VC", 0.5), (6.4, "VC", 0.5), (10.0, "VC", 0.5),
        (11.2, "VC", 0.5), (11.2, "VC", 0.5), (5.2, "VC", 0.5),
        (7.0, "VC", 0.5), (16.5, "VC", 1.0), (16.5, "VC", 1.0),
        (15.2, "VC", 1.0), (17.3, "VC", 1.0), (22.5, "VC", 1.0),
        (17.3, "VC", 1.0), (13.6, "VC", 1.0), (14.5, "VC", 1.0),
        (18.8, "VC", 1.0), (15.5, "VC", 1.0), (23.6, "VC", 2.0),
        (18.5, "VC", 2.0), (33.9, "VC", 2.0), (25.5, "VC", 2.0),
        (26.4, "VC", 2.0), (32.5, "VC", 2.0), (26.7, "VC", 2.0),
        (21.5, "VC", 2.0), (23.3, "VC", 2.0), (29.5, "VC", 2.0),
        (15.2, "OJ", 0.5), (21.5, "OJ", 0.5), (17.6, "OJ", 0.5),
        (9.7, "OJ", 0.5), (14.5, "OJ", 0.5), (10.0, "OJ", 0.5),
        (8.2, "OJ", 0.5), (9.4, "OJ", 0.5), (16.5, "OJ", 0.5),
        (9.7, "OJ", 0.5), (19.7, "OJ", 1.0), (23.3, "OJ", 1.0),
        (23.6, "OJ", 1.0), (26.4, "OJ", 1.0), (20.0, "OJ", 1.0),
        (25.2, "OJ", 1.0), (25.8, "OJ", 1.0), (21.2, "OJ", 1.0),
        (14.5, "OJ", 1.0), (27.3, "OJ", 1.0), (25.5, "OJ", 2.0),
        (26.4, "OJ", 2.0), (22.4, "OJ", 2.0), (24.5, "OJ", 2.0),
        (24.8, "OJ", 2.0), (30.9, "OJ", 2.0), (26.4, "OJ", 2.0),
        (27.3, "OJ", 2.0), (29.4, "OJ", 2.0), (23.0, "OJ", 2.0),
    ]
    df = pd.DataFrame(rows, columns=["length", "supp", "dose"])
    df.to_csv(DATA / "toothgrowth.csv", index=False)
    return df


def make_iris_small():
    iris = load_iris(as_frame=True)
    df = iris.frame.copy()
    df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
    df = df.drop(columns="target")
    # По 30 объектов каждого класса: готовый iris, но общий размер меньше 100.
    small = df.groupby("species", group_keys=False).head(30).reset_index(drop=True)
    small.to_csv(DATA / "iris_small.csv", index=False)
    return small


# -----------------------------------------------------------------------------
# Байесовский анализ на Python, стр. 35-41: монета, Beta-Binomial.
# -----------------------------------------------------------------------------

def coin_example():
    x = np.arange(0, 8)
    settings = [(5, 0.25), (5, 0.50), (5, 0.75)]

    plt.figure(figsize=(9, 3.6))
    for i, (n, p) in enumerate(settings, 1):
        plt.subplot(1, 3, i)
        prob = stats.binom(n=n, p=p).pmf(x)
        plt.vlines(x, 0, prob, lw=5)
        plt.title(f"N={n}, θ={p}")
        plt.xlabel("число успехов y")
        plt.ylabel("P(y | θ, N)")
        plt.ylim(0, 0.45)
    save_plot("01_coin_binomial.png")

    n = 12
    heads = 9
    priors = [(1, 1), (2, 2), (8, 4)]
    grid = np.linspace(0, 1, 500)
    rows = []

    plt.figure(figsize=(8, 5))
    for a, b in priors:
        post_a = a + heads
        post_b = b + n - heads
        density = stats.beta(post_a, post_b).pdf(grid)
        plt.plot(grid, density, label=f"Beta({post_a}, {post_b}) из prior Beta({a}, {b})")
        samples = stats.beta(post_a, post_b).rvs(20000, random_state=RNG)
        item = summarize(samples, f"theta_prior_{a}_{b}")
        item.update({"n": n, "heads": heads, "prior_a": a, "prior_b": b})
        rows.append(item)

    plt.axvline(heads / n, ls="--", label="частота в данных")
    plt.title("Апостериорное распределение вероятности успеха θ")
    plt.xlabel("θ")
    plt.ylabel("плотность")
    plt.legend(fontsize=8)
    save_plot("02_coin_posterior.png")

    pd.DataFrame(rows).to_csv(RESULTS / "coin_summary.csv", index=False)


# -----------------------------------------------------------------------------
# Стр. 101-114: простая линейная регрессия и квартет Энскомба.
# -----------------------------------------------------------------------------

def ols_draws(x, y, count=800):
    """Приближенные апостериорные линии вокруг OLS."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(len(x)), x])
    coef = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ coef
    dof = max(len(y) - 2, 1)
    sig2 = np.sum(resid**2) / dof
    cov = sig2 * np.linalg.inv(X.T @ X)
    coefs = RNG.multivariate_normal(coef, cov, size=count)
    sig = np.sqrt(sig2)
    return coef, coefs, sig


def linear_anscombe():
    ans = pd.read_csv(DATA / "anscombe.csv")
    groups = sorted(ans["dataset"].unique())
    rows = []

    plt.figure(figsize=(8, 7))
    for i, g in enumerate(groups, 1):
        part = ans[ans["dataset"] == g]
        x = part["x"].to_numpy()
        y = part["y"].to_numpy()
        coef, draws, sig = ols_draws(x, y)
        a, b = coef
        corr = np.corrcoef(x, y)[0, 1]
        rows.append({"dataset": g, "alpha": a, "beta": b, "sigma": sig, "pearson_r": corr, "r2": corr**2})

        xx = np.linspace(x.min() - 0.5, x.max() + 0.5, 100)
        plt.subplot(2, 2, i)
        plt.scatter(x, y)
        plt.plot(xx, a + b * xx, lw=2)
        for aa, bb in draws[:60]:
            plt.plot(xx, aa + bb * xx, alpha=0.04)
        plt.title(f"Anscombe {g}")
        plt.xlabel("x")
        plt.ylabel("y")
    save_plot("03_anscombe_bayes_lines.png")
    pd.DataFrame(rows).to_csv(RESULTS / "anscombe_linear_summary.csv", index=False)


# -----------------------------------------------------------------------------
# Стр. 118-127: робастная и иерархическая регрессия.
# -----------------------------------------------------------------------------

def fit_student_t_line(x, y, nu=3.0):
    """Вариант из книги: линия с t-правдоподобием, которое слабее реагирует на выбросы."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    beta, alpha = stats.linregress(x, y)[:2]
    start = np.array([alpha, beta, np.log(np.std(y - (alpha + beta * x)) + 0.5)])

    def loss(par):
        a, b, log_s = par
        s = np.exp(log_s) + 1e-6
        return -np.sum(stats.t.logpdf(y, df=nu, loc=a + b * x, scale=s))

    res = optimize.minimize(loss, start, method="Nelder-Mead")
    a, b, log_s = res.x
    return a, b, np.exp(log_s), res.fun


def robust_regression():
    ans = pd.read_csv(DATA / "anscombe.csv")
    part = ans[ans["dataset"] == "III"].copy()
    x_raw = part["x"].to_numpy()
    y = part["y"].to_numpy()
    x = x_raw - x_raw.mean()

    # Неробастная линия.
    ols_beta, ols_alpha = stats.linregress(x, y)[:2]

    # Свой вариант: Huber-регрессия. Она постепенно уменьшает вес далекой точки.
    X = sm.add_constant(x)
    huber = sm.RLM(y, X, M=sm.robust.norms.HuberT()).fit()
    hub_alpha, hub_beta = huber.params

    # Вариант из книги: t-распределение Стьюдента вместо нормального шума.
    t_alpha, t_beta, t_sigma, _ = fit_student_t_line(x, y, nu=3.0)

    xx = np.linspace(x.min() - 1, x.max() + 1, 100)
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, label="данные")
    plt.plot(xx, ols_alpha + ols_beta * xx, label="не робастная OLS")
    plt.plot(xx, hub_alpha + hub_beta * xx, label="свой вариант: Huber")
    plt.plot(xx, t_alpha + t_beta * xx, label="из книги: Student-t")
    plt.title("Робастная регрессия на III группе Энскомба")
    plt.xlabel("x, центрированный")
    plt.ylabel("y")
    plt.legend()
    save_plot("04_robust_regression.png")

    rows = [
        {"model": "OLS", "alpha": ols_alpha, "beta": ols_beta, "sigma": np.std(y - (ols_alpha + ols_beta * x), ddof=2)},
        {"model": "Huber_own", "alpha": hub_alpha, "beta": hub_beta, "sigma": np.std(y - (hub_alpha + hub_beta * x), ddof=2)},
        {"model": "StudentT_book", "alpha": t_alpha, "beta": t_beta, "sigma": t_sigma},
    ]
    pd.DataFrame(rows).to_csv(RESULTS / "robust_regression_summary.csv", index=False)


def hierarchical_regression():
    """Маленький пример частичного объединения групп, как на стр. 122-127."""
    n = 20
    groups = 8
    idx = np.repeat(np.arange(groups - 1), n)
    idx = np.append(idx, groups - 1)  # последняя группа содержит одну точку

    alpha_true = RNG.normal(2.5, 0.5, size=groups)
    beta_true = RNG.beta(6, 1, size=groups)
    x = RNG.normal(10, 1, len(idx))
    y = alpha_true[idx] + beta_true[idx] * x + RNG.normal(0, 0.5, len(idx))

    global_coef = np.linalg.lstsq(np.column_stack([np.ones(len(x)), x]), y, rcond=None)[0]
    alpha_g, beta_g = global_coef

    rows = []
    plt.figure(figsize=(9, 7))
    for g in range(groups):
        mask = idx == g
        xg, yg = x[mask], y[mask]
        weight = len(xg) / (len(xg) + 6)  # чем меньше данных, тем сильнее редуцирование к общему уровню
        if len(xg) >= 2:
            a_u, b_u = np.linalg.lstsq(np.column_stack([np.ones(len(xg)), xg]), yg, rcond=None)[0]
        else:
            b_u = beta_g
            a_u = yg[0] - b_u * xg[0]
        a_p = weight * a_u + (1 - weight) * alpha_g
        b_p = weight * b_u + (1 - weight) * beta_g
        rows.append({"group": g, "n": len(xg), "alpha_partial": a_p, "beta_partial": b_p, "weight": weight})

        xx = np.linspace(x.min(), x.max(), 50)
        plt.subplot(2, 4, g + 1)
        plt.scatter(xg, yg)
        plt.plot(xx, a_p + b_p * xx)
        plt.title(f"группа {g}, n={len(xg)}")
        plt.xlabel("x")
        plt.ylabel("y")
    save_plot("05_hierarchical_regression.png")
    pd.DataFrame(rows).to_csv(RESULTS / "hierarchical_summary.csv", index=False)


# -----------------------------------------------------------------------------
# Стр. 157-175: логистическая регрессия, softmax и порождающая LDA на iris.
# -----------------------------------------------------------------------------

def iris_logistic():
    iris = make_iris_small()
    feat = ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)"]

    # Бинарный случай: setosa против versicolor, один признак как в учебном примере.
    two = iris[iris["species"].isin(["setosa", "versicolor"])].copy()
    x = two[["sepal length (cm)"]].to_numpy()
    y = (two["species"] == "versicolor").astype(int).to_numpy()
    model = LogisticRegression(C=4.0, solver="lbfgs")
    model.fit(x, y)

    grid = np.linspace(x.min() - 0.3, x.max() + 0.3, 200).reshape(-1, 1)
    prob = model.predict_proba(grid)[:, 1]
    boundary = -model.intercept_[0] / model.coef_[0, 0]

    # LDA-граница как порождающая модель: середина между средними двух классов.
    mean0 = x[y == 0].mean()
    mean1 = x[y == 1].mean()
    lda_boundary = (mean0 + mean1) / 2

    plt.figure(figsize=(8, 4.7))
    jitter = RNG.normal(0, 0.025, size=len(y))
    plt.scatter(x[:, 0], y + jitter, label="наблюдения")
    plt.plot(grid[:, 0], prob, label="логистическая вероятность")
    plt.axvline(boundary, ls="--", label="граница logistic")
    plt.axvline(lda_boundary, ls=":", label="граница LDA")
    plt.title("Iris: бинарная логистическая модель")
    plt.xlabel("sepal length (cm)")
    plt.ylabel("P(versicolor)")
    plt.legend()
    save_plot("06_iris_binary_logistic.png")

    # Softmax: три класса и четыре признака.
    X = iris[feat].to_numpy()
    y3, labels = pd.factorize(iris["species"])
    Xs = (X - X.mean(axis=0)) / X.std(axis=0)
    soft = LogisticRegression(max_iter=1000, C=3.0)
    soft.fit(Xs, y3)
    pred = soft.predict(Xs)
    cm = confusion_matrix(y3, pred)
    acc = accuracy_score(y3, pred)

    plt.figure(figsize=(5.8, 4.8))
    plt.imshow(cm)
    plt.title(f"Softmax-классификация iris, accuracy={acc:.2f}")
    plt.xlabel("прогноз")
    plt.ylabel("факт")
    plt.xticks(range(3), labels, rotation=20)
    plt.yticks(range(3), labels)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center")
    save_plot("07_iris_softmax_confusion.png")

    rows = [
        {"model": "binary_logistic", "coef": model.coef_[0, 0], "intercept": model.intercept_[0], "boundary": boundary},
        {"model": "LDA_generative", "coef": np.nan, "intercept": np.nan, "boundary": lda_boundary},
        {"model": "softmax", "coef": np.nan, "intercept": np.nan, "boundary": np.nan, "accuracy": acc},
    ]
    pd.DataFrame(rows).to_csv(RESULTS / "iris_logistic_summary.csv", index=False)


# -----------------------------------------------------------------------------
# Вероятностное программирование, стр. 62-94 и 231-249.
# Два датасета: anscombe из задания и один новый маленький интернет-датасет ToothGrowth.
# -----------------------------------------------------------------------------

def make_ab_table(df, dataset):
    """Сделать из маленькой таблицы A/B-эксперимент с бинарным исходом."""
    if dataset == "anscombe":
        # Берем две серии квартета как две версии A/B.
        # Значение — y, успех — y не ниже медианы по этим двум сериям.
        two = df[df["dataset"].isin(["I", "II"])].copy()
        out = pd.DataFrame({
            "group": two["dataset"],
            "value": two["y"],
        })
        out["success"] = (out["value"] >= out["value"].median()).astype(int)
        a_name, b_name = "I", "II"
    elif dataset == "toothgrowth":
        out = pd.DataFrame({
            "group": df["supp"],
            "value": df["length"],
        })
        out["success"] = (out["value"] >= 20).astype(int)
        a_name, b_name = "VC", "OJ"
    else:
        raise ValueError(dataset)
    return out, a_name, b_name

def beta_ab_analysis(out, a_name, b_name, dataset):
    rows = []
    samples = {}
    for name in [a_name, b_name]:
        part = out[out["group"] == name]
        n = len(part)
        k = int(part["success"].sum())
        a_post = 1 + k
        b_post = 1 + n - k
        draw = stats.beta(a_post, b_post).rvs(20000, random_state=RNG)
        samples[name] = draw
        item = summarize(draw, f"p_{name}")
        item.update({"dataset": dataset, "group": name, "n": n, "success": k})
        rows.append(item)

    p_better = float((samples[b_name] > samples[a_name]).mean())
    lift = (samples[b_name] - samples[a_name]) / np.maximum(samples[a_name], 1e-9)
    rows.append({"dataset": dataset, "param": f"P({b_name}>{a_name})", "mean": p_better})
    rows.append({"dataset": dataset, "param": "lift_median", "mean": np.median(lift)})
    rows.append({"dataset": dataset, "param": "lift_30_percentile", "mean": np.percentile(lift, 30)})

    grid = np.linspace(0, 1, 500)
    plt.figure(figsize=(8, 4.7))
    for name in [a_name, b_name]:
        part = out[out["group"] == name]
        n = len(part)
        k = int(part["success"].sum())
        plt.plot(grid, stats.beta(1 + k, 1 + n - k).pdf(grid), label=name)
    plt.title(f"{dataset}: апостериорные конверсии A/B")
    plt.xlabel("p")
    plt.ylabel("плотность")
    plt.legend()
    save_plot(f"08_{dataset}_ab_beta.png")

    plt.figure(figsize=(8, 4.7))
    plt.hist(lift, bins=55, density=True, alpha=0.8)
    plt.axvline(0, ls="--")
    plt.axvline(np.median(lift), ls=":", label="медиана")
    plt.axvline(np.percentile(lift, 30), ls="-.", label="30-й процентиль")
    plt.title(f"{dataset}: апостериорное распределение lift")
    plt.xlabel("относительный рост")
    plt.ylabel("плотность")
    plt.legend()
    save_plot(f"09_{dataset}_lift.png")

    return rows, samples


def dirichlet_revenue(out, dataset):
    """Аналог раздела про ожидаемую выручку: категории -> распределение Дирихле."""
    vals = out["value"]
    bins = pd.qcut(vals, 4, labels=["низкий", "средний", "высокий", "очень_высокий"])
    counts = bins.value_counts().sort_index().to_numpy()
    alpha = np.ones(4) + counts
    probs = RNG.dirichlet(alpha, size=20000)
    # Условная ценность категорий. Это не реальные деньги, а учебная функция полезности.
    worth = np.array([0, 25, 49, 79])
    revenue = probs @ worth

    plt.figure(figsize=(8, 4.7))
    plt.hist(revenue, bins=50, density=True, alpha=0.85)
    plt.title(f"{dataset}: апостериорная ожидаемая полезность")
    plt.xlabel("E[value]")
    plt.ylabel("плотность")
    save_plot(f"10_{dataset}_dirichlet_value.png")

    row = summarize(revenue, f"{dataset}_expected_value")
    row.update({"dataset": dataset, "counts": str(counts.tolist())})
    return row


def student_t_groups(out, a_name, b_name, dataset):
    """Байесовский аналог t-test: берем робастные bootstrap-выборки разности средних."""
    a = out[out["group"] == a_name]["value"].to_numpy()
    b = out[out["group"] == b_name]["value"].to_numpy()

    # Небольшой робастный bootstrap: средние считаются по выборкам с возвращением.
    draws = 15000
    mean_a = RNG.choice(a, size=(draws, len(a)), replace=True).mean(axis=1)
    mean_b = RNG.choice(b, size=(draws, len(b)), replace=True).mean(axis=1)
    diff = mean_b - mean_a
    prob = float((diff > 0).mean())

    plt.figure(figsize=(8, 4.7))
    plt.hist(diff, bins=55, density=True, alpha=0.85)
    plt.axvline(0, ls="--")
    plt.title(f"{dataset}: разность средних {b_name} - {a_name}")
    plt.xlabel("разность")
    plt.ylabel("плотность")
    save_plot(f"11_{dataset}_mean_diff.png")

    row = summarize(diff, f"mean_{b_name}_minus_{a_name}")
    row.update({"dataset": dataset, "prob_positive": prob})
    return row


def probabilistic_programming_examples():
    ans = pd.read_csv(DATA / "anscombe.csv")
    tooth = make_toothgrowth()
    all_rows = []
    value_rows = []

    for df, name in [(ans, "anscombe"), (tooth, "toothgrowth")]:
        out, a_name, b_name = make_ab_table(df, name)
        out.to_csv(DATA / f"{name}_ab_ready.csv", index=False)
        rows, _ = beta_ab_analysis(out, a_name, b_name, name)
        all_rows.extend(rows)
        value_rows.append(dirichlet_revenue(out, name))
        value_rows.append(student_t_groups(out, a_name, b_name, name))

    pd.DataFrame(all_rows).to_csv(RESULTS / "pp_ab_summary.csv", index=False)
    pd.DataFrame(value_rows).to_csv(RESULTS / "pp_value_summary.csv", index=False)


# -----------------------------------------------------------------------------
# Главный запуск.
# -----------------------------------------------------------------------------

def main():
    DATA.mkdir(exist_ok=True)
    PLOTS.mkdir(exist_ok=True)
    RESULTS.mkdir(exist_ok=True)

    coin_example()
    linear_anscombe()
    robust_regression()
    hierarchical_regression()
    iris_logistic()
    probabilistic_programming_examples()

    print("Готово. Графики лежат в plots/, таблицы со сводками — в results/.")


if __name__ == "__main__":
    main()
