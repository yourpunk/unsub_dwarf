# 🧙🏻‍♂️ Unsub Dwarf

## 🤔 Who are you taking about?
<img src="https://github.com/user-attachments/assets/53726f02-43a3-4f52-bc64-9d591285ef60" align="right" width="128">

**Unsub Dwarf** is a tiny desktop wizard who helps you fight the eternal war against newsletter spam and dead-weight emails.  

💫 One click — and your **Gmail** looks a little less like a dump.

## 🫧 Features

- ✅ Sniffs out `List-Unsubscribe` headers automatically
- 🔍 Hunts for unsubscribe links hidden in email bodies
- 🧹 Cleans up old promotional, social, and update tabs
- 🕹️ You set how deep the cleanup goes
- 🌎 Multilingual interface `(ENG / RU / CZ)`

## 🧰 Built With
- **Python 3.10+** — main staff
- **Gmail API** — access to your inbox (legally, promise)
- **Tkinter** — smooth and simple interface

## 🔐 Heads Up

- Gmail **only**
- Needs **internet connection**
- Google might be a little suspicious of new apps (**OAuth stuff**)
> 💬 If you see a warning during login, **don’t panic**.<br>  If you wanna be added as a **trusted tester** — just ping me at  [aleks.creatrix@gmail.com](mailto:aleks.creatrix@gmail.com). 

## 🛠️ How to Set It Up

### Requirements
- Python 3.10+
- Gmail account + API credentials
- `pip install -r requirements.txt`
- (Optional) Coffee. Lots of coffee.

### 🦾 Quickstart

1. Run the app:
```bash
python dwarf.py
```
2. Enter how many emails you want to process (e.g. 50, 100...).
3. Click **Start**.
4. Sit back while the dwarf reads through your inbox:
   - If it finds an unsubscribe link → clicks it or sends an unsubscribe email.
   - If it sees a promotional email you've already read → moves it to Trash.
   - If it's spammy with no unsubscribe option → deletes it too.
   - If it looks fine → it gets skipped.

You **also can**:
- Click **Stop** anytime to cancel the process.
- Choose your interface language (top right corner).
- Customization -> add new keywords to filter out spam (`keywords.py`)
  
## 👀 Screenshots

_coming soon..._

## 👤 Author
Originally born out of pure frustration with morning inbox chaos ⁽⁽(੭ꐦ •̀Д•́ )੭*⁾⁾ <br>
by Aleksandra Kenig (aka [yourpunk](https://github.com/yourpunk)). 

💌 Wanna collab or throw some feedback? You know where to find me.

