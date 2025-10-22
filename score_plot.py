import matplotlib.pyplot as plt

def plot(dates,scores) :
    # Example data

    # Bar colors: green if score > 13 else red
    colors = ['green' if s > 13 else 'red' for s in scores]

    # Dark background
    plt.figure(figsize=(8,4), facecolor='#2c3e50')
    ax = plt.gca()
    ax.set_facecolor('#2c3e50')  # chart background

    # Bar chart
    bars = plt.bar(dates, scores, color=colors, width=0.5)

    # Add white text on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height - 0.5,
                str(score), ha='center', va='top', color='white', fontsize=12, fontweight='bold')

    # Axes labels and title in white
    plt.ylabel("Score", color='white', fontsize=12)
    plt.xlabel("Date", color='white', fontsize=12)
    plt.title("Score Over Days", color='white', fontsize=14, fontweight='bold')

    # Tick labels in white
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')

    # Remove spines or make them white
    for spine in ax.spines.values():
        spine.set_color('white')

    plt.ylim(0, max(max(scores)+5, 20))
    plt.tight_layout()

    # Save image
    img_path = "score_plot.png"
    plt.savefig(img_path, facecolor='#2c3e50', transparent=False)
    #conv to base 64

    # import io, base64

    # buf = io.BytesIO()
    # plt.savefig(buf, format='png', facecolor='#f5f5f5')  # match card bg
    # plt.close()
    # buf.seek(0)
    # img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    # plt.close()
    # return img_base64


if __name__ == "__main__":
    plot(['2025-10-15', '2025-10-16', '2025-10-17', '2025-10-18', '2025-10-19', '2025-10-20', '2025-10-21', '2025-10-22', '2025-10-23', '2025-10-24', '2025-10-25'], [75, 88, 92, 85, 90, 12, 12, 34, 5, 23, 4])
