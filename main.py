from datetime import datetime
from notion_client import Client
import yagmail
import json
import score_plot
import os
from dotenv import load_dotenv


SCORE_LIMIT = 13 #Choose your daily score limit here


#TO get environment variables create .env file
"""Example .env file content:
NOTION_SECRET=your_notion_secret
PAGE_ID=your_page_id
GMAIL_SECRET=your_gmail_app_password
"""
#------------------------ ENV Variables ------------------------#
# Load environment variables from a .env file in the project root
load_dotenv()

# Expect a variable named NOTION_SECRET in the .env file
SECRET = os.getenv("NOTION_SECRET")
if not SECRET:
    raise RuntimeError("NOTION_SECRET not found. Add NOTION_SECRET=your_secret to your .env or set the environment variable.")
# SECRET = ""
page_id = os.getenv("PAGE_ID")
if not page_id:
    raise RuntimeError("PAGE_ID not found. Add PAGE_ID=your_page_id to your .env or set the environment variable.")

gmail_secret = os.getenv("GMAIL_SECRET")
if not gmail_secret:
    raise RuntimeError("GMAIL_SECRET not found. Add GMAIL_SECRET=your_gmail_app_password to your .env or set the environment variable.")

FROM_MAIL = os.getenv("FROM_MAIL")
if not FROM_MAIL:
    raise RuntimeError("FROM_MAIL not found. Add FROM_MAIL=your_email to your .env or set the environment variable.")

TO_MAIL = os.getenv("TO_MAIL")
if not TO_MAIL:
    raise RuntimeError("TO_MAIL not found. Add TO_MAIL=your_email to your .env or set the environment variable.")
#---------------------------------------------------------------#


notion = Client(auth=SECRET)





current_date = datetime.now().strftime("%y-%m-%d")
# current_date = "25-10-26"  # for testing
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

for block in blocks:
    if block["type"] == "to_do":
        total_count += 1
        text = "".join([t["plain_text"] for t in block["to_do"]["rich_text"]])
        if block["to_do"]["checked"]:
            if "Health Goals" in text :
                done_count += 7 #choose your own weights
            elif "gym" in text :
                done_count += 3 #choose your own weights
            elif "Family" in text :
                done_count += 1 #choose your own weights
            elif "Scrolling" in text :
                done_count += 5 #choose your own weights
            elif "SLEEP" in text :
                done_count += 2 #choose your own weights
            else :
                done_count += 1 #choose your own weights


print(f" Score : {done_count} / 23")


score = done_count 

"""Total score SCORE_LIMIT>="""


# ----- Update JSON File -----
json_file_path = "data.json"

# Read existing scores
try:
    with open(json_file_path, "r") as f:
        score_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    score_data = {}

# Update with today's score
last_key = list(score_data.keys())[-1] if score_data else None
prev_steak = score_data[last_key][1] if last_key else None


if prev_steak:
    steak = prev_steak + 1
else:
    steak = 1

if score < SCORE_LIMIT:
    steak = 0

# Write back to file


score_data[current_date] = [score, steak, score >= SCORE_LIMIT]

with open(json_file_path, "w") as f:
    json.dump(score_data, f, indent=2)

# get highest steak / update if needed
with open("highest_steak.json", "r") as f:
    highest_steak_data = json.load(f)

highest_steak = highest_steak_data.get("highest_steak", 0)

extra_html = ""
# check if new record
if steak > highest_steak and steak != 0:
    # new record 
    extra_html = f"""
      <h2 style="color:#FFD700;">🏆 New Highest Streak Record! 🎉
      """
    highest_steak = steak
    with open("highest_steak.json", "w") as f:
        json.dump({"highest_steak": highest_steak}, f, indent=2)
#--------------


# ----- Your score -----
# score = 15  # Replace with your score

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
score_plot.plot(
    list(score_data.keys()),
    [score_data[date][0] for date in score_data.keys()]
)

html_content = f"""
<html>
  <body style="font-family: Arial, sans-serif; background-color:#f5f5f5; padding:20px;">
    <div style="max-width:700px; margin:auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;">
      <h1 style="color:{color};">{title}</h1>
      <p style="font-size:18px;">Score 💯: <strong>{score} pts</strong></p>
      <p style="font-size:18px;"> streak 🥩: <strong>{steak} days</strong></p>
      <p style="font-size:18px;">Highest streak 🥩: <strong>{highest_steak} days</strong></p>
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
attachments = ["score_plot.png"]  # path to your image file

# Send the email
# yag.send(to=to, subject=subject, contents=body, attachments=attachments)

yag.send(to=TO_MAIL, subject=f"Your Daily Score: {score}", contents=html_content,attachments=attachments)

print("📧 Email sent successfully!")




#Unchceck al boxex 
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
