# 🧙🏻‍♂️ Unsub Dwarf

## 💌 Description
**Unsub Dwarf** is a simple desktop assistant that helps you clean up your Gmail inbox by automatically unsubscribing from unwanted newsletters and moving promotional emails to trash.  

## ✨ Features

- ✅ Automatically detects `List-Unsubscribe` headers in emails
- 🔍 Searches for unsubscribe links even in the **HTML body**
- 🧹 Removes promotional, social, and update emails you've already read
- 📬 Allows manual control over how many messages to process
- 🗣️ Supports **multiple languages** (English, Russian, Czech)

## 🛠️ Technologies Used
- Python 3.10+
- Gmail API via `google-api-python-client`
- `Tkinter` for the graphical interface
## 👀 Screenshot

_coming soon..._

## 🎨 Customization

The interface uses a warm pastel theme by default — but you can:
- Change the color palette in `dwarf.py`
- Add new keywords to filter out spam (`keywords.py`)
- Add more languages in `interface_langs.py`

## 🛠️ Setup & Usage

### 🧪 Requirements

- Python 3.10+
- Gmail account with enabled API access
- `pip install -r requirements.txt`

You’ll also need to **set up a Google Cloud project** with Gmail API and download `credentials.json`.

### 🚫 Limitations

- The app currently works with **Gmail only**.
- It needs internet access and valid API credentials.
- Unsubscribing via email might not always be effective.
- Google limits API usage for unverified apps.

### 🔐 Google OAuth Setup

Due to Google security policies, only **authorized test users** can log in unless the app is verified.

> 💡 If you’re not a listed tester, you’ll see an error when trying to log in.

To become a tester:
1. Send your Gmail address to [aleks.creatrix@gmail.com](mailto:aleks.creatrix@gmail.com)
2. Wait for adding you to the OAuth test user list.
3. Restart the app and authorize.

### 🧙🏻‍♂️ How to Run

1. Run the app:
```bash
python dwarf.py
```
2. Choose your interface language (top right corner).
3. Enter how many emails you want to process (e.g. 50, 100...).
4. Click **Start**.
5. Sit back while the dwarf reads through your inbox:
   - If it finds an unsubscribe link → clicks it or sends an unsubscribe email.
   - If it sees a promotional email you've already read → moves it to Trash.
   - If it's spammy with no unsubscribe option → deletes it too.
   - If it looks fine → it gets skipped.

6. Click **Stop** anytime to cancel the process.

## 👥 Contributors
Developed by Aleksandra Kenig. Special thanks to everyone who provided feedback, bug reports, and support!

### 📩 Feel free to reach out with questions or suggestions!
