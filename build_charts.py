import os, shutil, itertools
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

SRC = "data"
P = "."
CH = f"{P}/charts"; DA = f"{P}/data"
os.makedirs(CH, exist_ok=True); os.makedirs(DA, exist_ok=True)

BLUE, ORANGE, INK, MUTED, GRID, BG = "#2b5fb3", "#d9822b", "#1d2433", "#6b7280", "#e5e7eb", "#ffffff"
LIGHT, DARK = "#c9d6ee", "#3b4252"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK, "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": BG, "axes.facecolor": BG})

def finish(fig, name, title, sub):
    fig.suptitle(title, x=0.01, ha="left", fontsize=15, fontweight="bold", color=INK, y=1.01)
    fig.text(0.01, 0.945, sub, ha="left", fontsize=10, color=MUTED)
    fig.savefig(f"{CH}/{name}.png", dpi=160, bbox_inches="tight", facecolor=BG)
    plt.close(fig)

c = pd.read_csv(f"{DA}/contestants.csv"); ep = pd.read_csv(f"{DA}/episodes.csv")
pr = pd.read_csv(f"{DA}/contestant_episode_progress.csv"); gp = pd.read_csv(f"{DA}/group_performances.csv")
disc = pd.read_csv(f"{DA}/irl_discography.csv")

# 1 survival ---------------------------------------------------------------
x = ["Start"] + [f"Ep {e}" for e in ep.episode]
y = [30, 18] + list(ep.contestants_remaining_after)
x = ["Auditions", "Top 18"] + [f"Ep {e}" for e in ep.episode]
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.plot(range(len(y)), y, color=BLUE, lw=2.2)
ax.plot(range(len(y)), y, "o", color=BLUE, ms=7, mec=BG, mew=2)
for i, v in enumerate(y):
    ax.annotate(str(v), (i, v), textcoords="offset points", xytext=(10, 8), ha="center", fontsize=9, color=INK)
ax.set_xticks(range(len(x))); ax.set_xticklabels(x, rotation=0, fontsize=8)
ax.set_ylim(0, 34); ax.set_ylabel("Contestants remaining"); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
ax.annotate("12 cut on night one", (0.55, 25), fontsize=9, color=MUTED, ha="left")
finish(fig, "01_survival_curve", "Thirty boys to five in ten weeks",
       "Contestants remaining after each episode, Boy Band (ABC, 2017)")

# 2 ratings ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 4.4))
bars = ax.bar(ep.episode, ep.us_viewers_millions, color=BLUE, width=0.72)
ax.bar(10, ep.us_viewers_millions.iloc[-1], color=ORANGE, width=0.72)
ax.set_xticks(ep.episode); ax.set_ylim(0, 3.4); ax.set_ylabel("US viewers (millions)")
ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)
for e, v in zip(ep.episode, ep.us_viewers_millions):
    if e in (1, 9, 10): ax.text(e, v + 0.06, f"{v:.2f}", ha="center", fontsize=9)
ax.text(10, 0.15, "finale", ha="center", fontsize=8, color="white")
finish(fig, "02_ratings", "Viewers fell about 29% from premiere to the Ep 9 low",
       "US viewers by episode (millions); finale ticked back up to 2.40")

# 3 age strip --------------------------------------------------------------
grp = np.where(c.irl_member == "Y", "IRL final five", np.where(c.made_top18 == "Y", "Top 18, eliminated", "Cut on night one"))
c["grp"] = grp
order = ["IRL final five", "Top 18, eliminated", "Cut on night one"]
colors = {"IRL final five": BLUE, "Top 18, eliminated": ORANGE, "Cut on night one": "#9aa3b2"}
rng = np.random.default_rng(3)
fig, ax = plt.subplots(figsize=(9, 4.2))
for i, g in enumerate(order):
    d = c[c.grp == g]
    ax.scatter(d.age_wikipedia, i + rng.uniform(-0.12, 0.12, len(d)), s=90, color=colors[g], ec=BG, lw=2, zorder=3)
    m = d.age_wikipedia.median()
    ax.plot([m, m], [i - 0.28, i + 0.28], color=INK, lw=2, zorder=4)
    ax.text(25.2, i, f"n={len(d)}, median {m:g}", va="center", fontsize=9, color=MUTED)
ax.set_yticks(range(3)); ax.set_yticklabels(order); ax.set_xlim(13, 29); ax.set_xlabel("Age at show (Wikipedia listing)")
ax.invert_yaxis(); ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)
finish(fig, "03_age_by_outcome", "Age did not pick the winners: medians 18, 17 and 18.5",
       "Contestant age by outcome; black tick is the median. Small sample (30), descriptive only")

# 4 path heatmap -----------------------------------------------------------
t18 = c[c.made_top18 == "Y"].copy()
t18["exit"] = t18.elimination_episode.fillna(11)
t18 = t18.sort_values(["exit", "contestant_id"], ascending=[False, True])
code = {"advanced": 1, "advanced_not_yet_performed": 1, "bottom_saved": 2, "eliminated": 3, "winner_IRL": 4}
M = np.full((len(t18), 10), np.nan)
for r, (_, row) in enumerate(t18.iterrows()):
    for _, q in pr[pr.contestant == row.contestant].iterrows():
        M[r, q.episode - 1] = code.get(q.outcome, 1)
from matplotlib.colors import ListedColormap
cm = ListedColormap([LIGHT, ORANGE, DARK, BLUE])
fig, ax = plt.subplots(figsize=(9, 7))
ax.imshow(np.ma.masked_invalid(M), cmap=cm, vmin=0.5, vmax=4.5, aspect="auto")
ax.set_xticks(range(10)); ax.set_xticklabels(range(1, 11)); ax.set_xlabel("Episode")
ax.set_yticks(range(len(t18))); ax.set_yticklabels(t18.contestant, fontsize=9)
ax.set_xticks(np.arange(-.5, 10, 1), minor=True); ax.set_yticks(np.arange(-.5, len(t18), 1), minor=True)
ax.grid(which="minor", color=BG, lw=2); ax.tick_params(which="both", length=0)
for s in ax.spines.values(): s.set_visible(False)
for r in range(M.shape[0]):
    for k in range(10):
        v = M[r, k]
        if v == 2: ax.text(k, r, "B", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        if v == 3: ax.text(k, r, "X", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
        if v == 4: ax.text(k, r, "W", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=LIGHT, label="Advanced"), Patch(color=ORANGE, label="B  Bottom, saved"),
    Patch(color=DARK, label="X  Eliminated"), Patch(color=BLUE, label="W  Winner (IRL)")],
    loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=4, frameon=False, fontsize=9)
finish(fig, "04_path_to_irl", "Path to In Real Life, contestant by contestant",
       "Top 18 only; rows ordered by when each boy left. Documented outcomes only (Ep 5 and 6 bottoms incomplete)")

# 5 bottoms ----------------------------------------------------------------
b = t18.sort_values(["bottom_appearances", "contestant_id"], ascending=[True, False])
fig, ax = plt.subplots(figsize=(9, 6))
cols = [BLUE if m == "Y" else ORANGE for m in b.irl_member]
ax.barh(b.contestant, b.bottom_appearances, color=cols, height=0.7)
for i, v in enumerate(b.bottom_appearances): ax.text(v + 0.04, i, str(v), va="center", fontsize=9)
ax.set_xlim(0, 2.6); ax.set_xlabel("Documented bottom placements")
ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)
ax.legend(handles=[Patch(color=BLUE, label="IRL member"), Patch(color=ORANGE, label="Eliminated")], frameon=False, loc="lower right")
finish(fig, "05_bottom_placements", "Only one of the five ever landed in the bottom",
       "Documented bottom placements (eliminated or saved). Sergio Calderon Jr., Ep 8, saved by viewers")

# 6 co-performance ---------------------------------------------------------
names = list(t18.sort_values("contestant_id").contestant)
idx = {n: i for i, n in enumerate(names)}
A = np.zeros((len(names), len(names)))
for _, r in gp.iterrows():
    mem = [m.strip() for m in r.members.split(";")]
    for a, bb in itertools.combinations(mem, 2):
        if a in idx and bb in idx:
            A[idx[a], idx[bb]] += 1; A[idx[bb], idx[a]] += 1
np.fill_diagonal(A, np.nan)
fig, ax = plt.subplots(figsize=(8.4, 7.4))
im = ax.imshow(A, cmap="Blues", vmin=0, vmax=np.nanmax(A))
ax.set_xticks(range(len(names))); ax.set_yticks(range(len(names)))
ax.set_xticklabels(names, rotation=90, fontsize=8); ax.set_yticklabels(names, fontsize=8)
for i in range(len(names)):
    for j in range(len(names)):
        if not np.isnan(A[i, j]) and A[i, j] > 0:
            ax.text(j, i, int(A[i, j]), ha="center", va="center", fontsize=7, color="white" if A[i, j] > 2.5 else INK)
ax.set_xticks(np.arange(-.5, len(names), 1), minor=True); ax.set_yticks(np.arange(-.5, len(names), 1), minor=True)
ax.grid(which="minor", color=BG, lw=1.5); ax.tick_params(which="both", length=0)
for s in ax.spines.values(): s.set_visible(False)
ax.add_patch(plt.Rectangle((-.5, -.5), 5, 5, fill=False, ec=ORANGE, lw=2.5, clip_on=False, zorder=10))
cb = fig.colorbar(im, ax=ax, shrink=0.6); cb.set_label("Shared group performances")
finish(fig, "06_who_sang_with_whom", "Who shared a stage with whom",
       "Co-appearances in the same group, Eps 1 to 8. Orange box is the final five, listed first")

# 7 IRL timeline -----------------------------------------------------------
D = pd.Timestamp
bars = [("Boy Band (ABC)", D("2017-06-22"), D("2017-08-24"), BLUE),
        ("American Idol Live!", D("2018-07-11"), D("2018-08-10"), ORANGE),
        ("Tonight Belongs to You Tour", D("2018-09-09"), D("2018-11-11"), ORANGE),
        ("For U Tour", D("2019-10-02"), D("2019-10-29"), ORANGE)]
marks = [("Eyes Closed", D("2017-08-25")), ("Tattoo (How 'Bout You)", D("2018-02-02")),
         ("Tonight Belongs to You", D("2018-07-15")), ("Crazy AF", D("2019-03-22")),
         ("She Do (album)", D("2019-08-23")), ("Split announced", D("2020-01-20"))]
fig, ax = plt.subplots(figsize=(10, 4.8))
for i, (n, s, e, col) in enumerate(bars):
    ax.barh(i, (e - s).days, left=mdates.date2num(s), color=col, height=0.45)
    ax.text(mdates.date2num(e) + 12, i, n, va="center", fontsize=9)
for j, (n, d) in enumerate(marks):
    yy = 4.2 + (j % 2) * 0.9
    ax.plot([mdates.date2num(d)] * 2, [3.6, yy], color=GRID, lw=1.2)
    ax.plot(mdates.date2num(d), 3.6, "o", color=INK, ms=7, mec=BG, mew=2)
    ax.text(mdates.date2num(d), yy + 0.08, n, ha="center", fontsize=8.5)
ax.set_ylim(5.8, -0.7); ax.set_yticks([])
ax.xaxis_date(); ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7))); ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.spines["left"].set_visible(False)
ax.set_xlim(mdates.date2num(D("2017-05-01")), mdates.date2num(D("2020-10-01")))
finish(fig, "07_irl_timeline", "In Real Life: 29 months from finale to split",
       "Show, tours and key releases. Some release dates are month-level in the sources (Tattoo, Tonight Belongs to You)")

print(sorted(os.listdir(CH)))
