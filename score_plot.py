import matplotlib.pyplot as plt
import os


def plot(dates, scores, score_limit=12):
    img_path = os.path.join(
        os.path.dirname(__file__), "plot", f"score_plot_{dates[-1]}.png"
    )
    # Bar colors: green if score > 13 else red
    colors = ["green" if s > 13 else "red" for s in scores]

    # Dark background
    plt.figure(figsize=(8, 4), facecolor="#2c3e50")
    ax = plt.gca()
    ax.set_facecolor("#2c3e50")  # chart background

    # Bar chart
    bars = plt.bar(dates, scores, color=colors, width=0.5)

    # Add white text on bars
    max_score = max(scores)

    for bar, score in zip(bars, scores):
        height = bar.get_height()
        extra = "!" if score == max_score and score >= score_limit else ""
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height - 0.5,
            str(score) + extra,
            ha="center",
            va="top",
            color="white",
            fontsize=12,
            fontweight="bold",
        )

    # Axes labels and title in white
    plt.ylabel("Score", color="white", fontsize=12)
    plt.xlabel("Date", color="white", fontsize=12)
    plt.title("Score Over Days", color="white", fontsize=14, fontweight="bold")

    # Tick labels in white
    plt.xticks(rotation=45, color="white")
    plt.yticks(color="white")

    plt.axhline(y=score_limit, color="yellow", linestyle="--", label="")

    # Remove spines or make them white
    for spine in ax.spines.values():
        spine.set_color("white")

    plt.ylim(0, max(max(scores) + 5, 20))
    plt.tight_layout()

    # Save image

    plt.savefig(img_path, facecolor="#2c3e50", transparent=False)
    return img_path


if __name__ == "__main__":
    plot(
        [
            "2025-10-15",
            "2025-10-16",
            "2025-10-17",
            "2025-10-18",
            "2025-10-19",
            "2025-10-20",
            "2025-10-21",
            "2025-10-22",
            "2025-10-23",
            "2025-10-24",
            "2025-10-25",
        ],
        [75, 88, 92, 85, 90, 12, 12, 34, 5, 23, 4],
    )
