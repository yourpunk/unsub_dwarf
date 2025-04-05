import tkinter as tk
from tkinter import ttk
root = tk.Tk()

from tkinter import scrolledtext
import threading
from unsubscribe import get_messages
from interface_langs import interface_langs
import shared
from lang_manager import init_lang_var, get_lang
current_lang = init_lang_var()


lang = get_lang()

# 🌚 Color theme
bg_color = "#83b3fa" # light blue background
fg_color = "#18212d" # dark text
btn_bg = "#fbcc5d" # warm yellow button
btn_fg = "#243144"   # dark text on button
entry_bg = "#f1ecf6" # white input field
entry_fg = "#18212d" # dark text
log_bg = "#ddeafe" # light blue log background
log_fg = "#243144"   # contrasting, but not black
scrol_bg = "#f4f8ff" # light blue background
scrol_fg = "#f9cd70" # light yellow slider

# ✨ Fonts
font_label = ("Segoe UI", 10, "bold")
font_entry = ("Fira Code", 11)
font_button = ("Fira Code", 10, "bold")
font_log = ("Fira Code", 10)

# 🧙🏻‍♂️ Apply colors
root.title(lang["title"])
root.configure(bg=bg_color)



# 🌐 Interface language (top right)
lang_frame = tk.Frame(root, bg=bg_color)
label_lang = tk.Label(lang_frame, text="Language:", bg=bg_color, fg=fg_color, font=font_label)
label_lang.pack(side=tk.LEFT)

def update_language(*args):
    lang = get_lang()
    root.title(lang["title"])
    label_lang.config(text="Language:")
    label_entry.config(text=lang["label"])
    start_btn.config(text=lang["start"])
    stop_btn.config(text=lang["stop"])

current_lang.trace_add("write", update_language)

lang_menu = tk.OptionMenu(lang_frame, current_lang, *interface_langs.keys())
lang_menu.config(
    bg=btn_bg, fg=btn_fg, font=font_button,
    highlightthickness=0, bd=0,
    activebackground=btn_bg, activeforeground=btn_fg
)
lang_menu["menu"].config(bg=btn_bg, fg=btn_fg, font=font_button)
lang_menu.pack(side=tk.LEFT)

lang_frame.pack(anchor="ne", padx=10, pady=5)

# 📝 Label + input field
label_entry = tk.Label(root, text=lang["label"], bg=bg_color, fg=fg_color, font=font_label)
label_entry.pack(pady=5)
entry = tk.Entry(root, bg=entry_bg, fg=entry_fg,
                 insertbackground=entry_fg, font=font_entry, justify='center')
entry.pack(pady=5)
entry.insert(0, "50")

# 🔘 Buttons
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=5)

start_btn = tk.Button(button_frame, text=lang["start"], bg=btn_bg, fg=btn_fg,
                      font=font_button, command=lambda: run_unsubscribe())
start_btn.pack(side=tk.LEFT, padx=5)

stop_btn = tk.Button(button_frame, text=lang["stop"], bg=btn_bg, fg=btn_fg,
                     font=font_button, command=lambda: stop_unsubscribe())
stop_btn.pack(side=tk.LEFT, padx=5)

# 🪵 Log with yellow scrollbar
log_frame = tk.Frame(root, bg=bg_color)
log_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Customize the scrollbar style
style = ttk.Style()
style.theme_use('default')
style.configure('Vertical.TScrollbar',
                background=btn_bg,
                troughcolor=scrol_bg,
                bordercolor=scrol_bg,
                arrowcolor=btn_fg,
                relief='flat')

log = tk.Text(log_frame, wrap='word',
              bg=log_bg, fg=log_fg,
              insertbackground=log_fg,
              font=font_log)
log.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=log.yview, style='Vertical.TScrollbar')
scrollbar.pack(side='right', fill='y')

log.configure(yscrollcommand=scrollbar.set)

# 🧠 Logic
def run_unsubscribe():
    try:
        limit = int(entry.get())
    except ValueError:
        log.insert(tk.END, lang["error"] + "\n")
        log.see(tk.END)
        return

    log.insert(tk.END, lang["launch"] + "\n")
    shared.stop_flag = False

    def threaded_run():
        try:
            get_messages(limit=limit, log_output=log, lang_code=current_lang.get())
        except Exception as e:
            log.insert(tk.END, f"{lang['process_error']} {e}\n")

    thread = threading.Thread(target=threaded_run)
    thread.start()

def stop_unsubscribe():
    shared.stop_flag = True
    log.insert(tk.END, lang["cancel"] + "\n")

def on_close():
    shared.stop_flag = True # stop unsubscribing if it is in progress
    root.destroy() # close the window


root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

