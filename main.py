from datetime import datetime
from notion_client import Client
import yagmail
import json
import score_plot
import os
from dotenv import load_dotenv


SCORE_LIMIT = 14  # Choose your daily score limit here
DEFAULT_PTS = 1  # default point if not specified

# Define paths for data files
data_dir = os.path.join(os.path.dirname(__file__), "data")
highest_streak_path = os.path.join(data_dir, "highest_streak.json")
history_data_path = os.path.join(data_dir, "history_data.json")
score_data_path = os.path.join(data_dir, "score_data.json")
# TO get environment variables create .env file
"""Example .env file content:
NOTION_SECRET=your_notion_secret
PAGE_ID=your_page_id
GMAIL_SECRET=your_gmail_app_password
FROM_MAIL=your_email
TO_MAIL=your_email
"""

# ------------------------ ENV Variables ------------------------#
# Load environment variables from a .env file in the project root
load_dotenv()

# Expect a variable named NOTION_SECRET in the .env file
SECRET = os.getenv("NOTION_SECRET")
if not SECRET:
    raise RuntimeError(
        "NOTION_SECRET not found. Add NOTION_SECRET=your_secret to your .env or set the environment variable."
    )
# SECRET = ""
page_id = os.getenv("PAGE_ID")
if not page_id:
    raise RuntimeError(
        "PAGE_ID not found. Add PAGE_ID=your_page_id to your .env or set the environment variable."
    )

gmail_secret = os.getenv("GMAIL_SECRET")
if not gmail_secret:
    raise RuntimeError(
        "GMAIL_SECRET not found. Add GMAIL_SECRET=your_gmail_app_password to your .env or set the environment variable."
    )

FROM_MAIL = os.getenv("FROM_MAIL")
if not FROM_MAIL:
    raise RuntimeError(
        "FROM_MAIL not found. Add FROM_MAIL=your_email to your .env or set the environment variable."
    )

TO_MAIL = os.getenv("TO_MAIL")
if not TO_MAIL:
    raise RuntimeError(
        "TO_MAIL not found. Add TO_MAIL=your_email to your .env or set the environment variable."
    )
# ---------------------------------------------------------------#


notion = Client(auth=SECRET)


current_date = datetime.now().strftime("%y-%m-%d")
# current_date = "25-10-26"  # for testing purposes
print(f"📅  {current_date} ------------------------: \n")

# ----- Fetch page blocks -----
blocks = []
start_cursor = None

while True:
    response = notion.blocks.children.list(page_id, start_cursor=start_cursor)
    blocks.extend(response["results"])
    if response.get("next_cursor"):
        start_cursor = response["next_cursor"]
    else:
        break

# ----- Count checkboxes -----
done_count = 0
total_count = 0
today_history = {}

for block in blocks:
    if block["type"] == "to_do":
        total_count += 1
        text = "".join([t["plain_text"] for t in block["to_do"]["rich_text"]])
        if block["to_do"]["checked"]:
            today_history[text] = True
            try:
                pts = int(text[text.index("(") + 1 : text.index(")")])
            except ValueError:
                pts = DEFAULT_PTS  # default point if not specified

            done_count += pts
        else:
            today_history[text] = False

print(f" Score : {done_count} / {total_count}")


score = done_count  # calibrate your score here

"""Total score SCORE_LIMIT>="""


# ----- Update JSON File 's -----

""" Update History """
with open(history_data_path, "r") as f:
    history_data = json.load(f)
    history_data[current_date] = today_history
with open(history_data_path, "w") as f:
    json.dump(history_data, f, indent=4)

""" Update Scores """
# Read existing scores
try:
    with open(score_data_path, "r") as f:
        score_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    score_data = {}

# Update with today's score
last_key = list(score_data.keys())[-1] if score_data else None
prev_streak = score_data[last_key][1] if last_key else None


if prev_streak:
    streak = prev_streak + 1
else:
    streak = 1

if score < SCORE_LIMIT:
    streak = 0

# Write back to file


score_data[current_date] = [score, streak, score >= SCORE_LIMIT]

with open(score_data_path, "w") as f:
    json.dump(score_data, f, indent=2)

# get highest streak / update if needed
with open(highest_streak_path, "r") as f:
    highest_streak_data = json.load(f)

highest_streak = highest_streak_data.get("highest_streak", 0)

extra_html = ""
# check if new record
if streak > highest_streak and streak != 0:
    # new record
    extra_html = f"""
      <h2 style="color:#FFD700;">🏆 New Highest Streak Record! 🎉
      """
    highest_streak = streak
    with open(highest_streak_path, "w") as f:
        json.dump({"highest_streak": highest_streak}, f, indent=2)
# --------------


# ----- Decide message -----
if score >= SCORE_LIMIT:
    title = "🎉 Congrats! Great Job Today!"
    message = "You did amazing! Keep up the good work and stay consistent."
    color = "#4CAF50"  # green
else:
    title = "⚡ Keep Improving!"
    message = "Don't worry! Tomorrow is another chance to improve. Stay motivated!"
    color = "#F44336"  # red

# ----- HTML Email Template -----

# Generate and save the score plot
plot_img_path = score_plot.plot(
    list(score_data.keys()),
    [score_data[date][0] for date in score_data.keys()],
    score_limit=SCORE_LIMIT,
)

html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
    <div style="max-width:700px; margin:auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;">
      <h1 style="color:{color};">{title}</h1>
      <p style="font-size:18px;">Score 💯: <strong>{score} pts</strong></p>
      <p style="font-size:18px;"> streak 🥩: <strong>{streak} days</strong></p>
      <p style="font-size:18px;">Highest streak 🥩: <strong>{highest_streak} days</strong></p>
    {extra_html}
      <p style="font-size:16px; color:#555;">{message}</p>
      <!-- Embed the saved plot -->
    </div>
  </body>
</html>
"""


# ----- Send Email -----
yag = yagmail.SMTP(FROM_MAIL, gmail_secret)
# Attach an image
attachments = [plot_img_path]  # path to your image file

yag.send(
    to=TO_MAIL,
    subject=f"Your Daily Score: {score}",
    contents=html_content,
    attachments=attachments,
)

print("📧 Email sent successfully!")


# Uncheck all boxes
def get_children(block_id):
    """Fetch children blocks of a page or block."""
    response = notion.blocks.children.list(block_id)
    return response.get("results", [])


def uncheck_todo_block(block_id):
    """Set 'checked' field of to-do block to False."""
    notion.blocks.update(block_id, to_do={"checked": False})


def process_block(block_id):
    """Recursively uncheck all to-do blocks inside the page."""
    children = get_children(block_id)
    for block in children:
        block_type = block["type"]
        block_id = block["id"]

        # if it's a to_do block and checked
        if block_type == "to_do" and block["to_do"]["checked"]:
            text_items = block["to_do"]["rich_text"]
            text_content = "".join([t["plain_text"] for t in text_items])
            print(f"Unchecking: {text_content}")
            uncheck_todo_block(block_id)

        # if block has children, recurse
        if block.get("has_children"):
            process_block(block_id)


process_block(page_id)
print("✅ Done — all checkboxes unchecked!")
