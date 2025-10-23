# Notion Habit Tracker  #center alignment

This code takes the input from the To-Do list of a Notion Page, reads the checked items and converts them into a score. It also sends you a mail of your score for the day and the analytics graph of your previous scores.

## Features

- 

---

# Setup Prerequisites

- Cloning the GitHub repository 👌
- Installing the requirements 👌
- Getting the Notion Integration Key 👌
- Getting the Notion Page ID 👌
- Getting the Google App Key
- Creating the .env file 👌
- Customizing the code for your needs
- Running the code

# Installation

## Installing the code and requirements

-   Clone the GitHub repository
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
- Under the Internal Integration Secret, click on the “Show” button and **copy the Integration key**.
- Under Capabilities, check the following boxes : Read content, Update content, Insert content.
- Then click on Access menu at the top and click on Edit access.
- Click Private and then select the page in which you have your To-Do list and hit Save.

## Getting the Notion Page ID

- Sign in to Notion in your browser and click on your page
- Copy the 32-digit alphanumeric code in the URL of your page. Example :

![image.png](attachment:71364e0b-9ffd-44fd-a1ee-d944b39d5fcc:image.png)

## Getting the Google App Key

- 

## Creating the .env file

- Make a file with the name `.env` in the same folder as [main.py](http://main.py)  (Caution : The file should be unnamed and the file extension should be .env)
- Right click on the .env file and click on → Edit with Notepad
- Paste the following in the .env file
- `NOTION_SECRET=your_notion_secret
PAGE_ID=your_page_id
GMAIL_SECRET=your_gmail_app_password
FROM_MAIL=your_sender_email
TO_MAIL=your_receiver_email`

## Customizing the code

## Running the code