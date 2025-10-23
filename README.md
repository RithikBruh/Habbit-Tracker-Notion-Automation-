#                                                          Notion Habit Tracker  

This code takes the input from the To-Do list of a Notion Page, reads the checked items and converts them into a score. It also sends you a mail of your score for the day and the analytics graph of your previous scores.

---

# Setup Prerequisites

- Make sure you have python installed ([python.org](https://www.python.org/)) 👌
- Cloning the GitHub repository/Download Zip File and extract 👌
- Installing the requirements 👌
- Getting the Notion Integration Key 👌
- Getting the Notion Page ID 👌
- Getting the Google App Password 👌
- Creating the .env file 👌
- Customizing the Notion Page 👌
- Customizing the code for your needs 👌
- Running the code 👌

# Installation

This Installation Procedure Assumes That You Already Have Python Installed In Your Computer. If Not, Install Python From Their Official Website : [www.python.org](https://www.python.org/)

## Installing the code and requirements

- Clone the GitHub repository/Download Zip File and extract
- Open CMD in the folder and run the following command : `pip install -r requirements.txt`

## Getting the Notion Integration Key

- Paste this link in your browser : https://www.notion.so/my-integrations
- Sign in to Notion in the browser
- Click on → New Integration
- Enter your desired name for the integration
- Select your workspace in Associated workspace
- In the Type field select → Internal
- Click on the Save button

- Now click on your integration
- Under the Internal Integration Secret, click on the “Show” button and **copy the Integration key**
- Under Capabilities, check the following boxes : Read content, Update content, Insert content
- Then click on Access menu at the top and click on Edit access
- Click Private and then select the page in which you have your To-Do list and hit Save

## Getting the Notion Page ID

- Sign in to Notion in your browser and click on your page
- **Copy the 32-digit alphanumeric code in the URL of your page**. Example :

![image.png](attachment:71364e0b-9ffd-44fd-a1ee-d944b39d5fcc:image.png)

## Getting the Google App Password

- Log in to the Google Account you want to receive the mail from
- Click on Manage Your Google Account
- Search for App Passwords (Make sure you have 2FA ON or this won’t show up)
- Enter a name for your app and click on Create
- **Copy the 16 letter App Password**

## Creating the .env file

- Make a file with the name `.env` in the same folder as [main.py](http://main.py)  (Caution : The file should be unnamed and the file extension should be .env)
- Right click on the .env file and click on → Edit with Notepad
- Paste the following in the .env file

```
NOTION_SECRET=your_notion_secret
PAGE_ID=your_page_id
GMAIL_SECRET=your_gmail_app_password
FROM_MAIL=your_sender_email
TO_MAIL=your_receiver_email
```

- Enter the required details in the respective fields and save the file

## Customizing the Notion Page

- In your Notion Page, you just have to add a few To-do list blocks and name them
- Make sure you have a unique keyword in each block (You’ll need the keywords for the code to work)

## Customizing the code

- In the double quotes, write the unique keyword in the To-do list blocks of your notion page. You can change the score awarded to each block when you check them by changing the number after the `done_count +=`

```python
if "Health Goals" in text :
	done_count += 7 #choose your own weights
elif "Gym" in text :
	done_count += 3 #choose your own weights
```

- You can add as much `elif` statements as you want and edit them

```python
elif "Sleep" in text :
	done_count += 2 #choose your own weights
```
**IMPORTANT NOTICE : 
- The score limit is the Boarderline Score , which means it will be marked as good (taken into the streak).Its basically the minimum score you need to achive in a day.

```python
SCORE_LIMIT = 13 #Choose your daily score limit here
```

## Running the code

- To run the code, open CMD in the folder where [main.py](http://main.py) is located in
- Enter the following command `py main.py`
