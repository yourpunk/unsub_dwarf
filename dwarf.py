import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from unsubscribe import get_messages
from interface_langs import interface_langs
import shared
from lang_manager import init_lang_var, get_lang
from PIL import Image, ImageTk

root = tk.Tk()
current_lang = init_lang_var()
lang = get_lang()

# 🌈 Цветовая тема
bg_color   = "#83b3fa"
fg_color   = "#18212d"
btn_bg     = "#fbcc5d"
btn_fg     = "#243144"
entry_bg   = "#f1ecf6"
entry_fg   = "#18212d"
log_bg     = "#ddeafe"
log_fg     = "#243144"
scrol_bg   = "#f4f8ff"
scrol_fg   = "#f9cd70"

# ✨ Шрифты
font_label  = ("Segoe UI", 10, "bold")
font_entry  = ("Fira Code", 11)
font_button = ("Fira Code", 10, "bold")
font_log    = ("Fira Code", 10)

# 🧙🏻‍♂️ Оформление окна
root.title(lang["title"])
root.configure(bg=bg_color)

# 🌐 Язык интерфейса (в правом верхнем углу)
lang_frame = tk.Frame(root, bg=bg_color)
label_lang = tk.Label(lang_frame, text="Language:", bg=bg_color, fg=fg_color, font=font_label)
label_lang.pack(side=tk.LEFT)

lang_menu = tk.OptionMenu(lang_frame, current_lang, *interface_langs.keys())
lang_menu.config(bg=btn_bg, fg=btn_fg, font=font_button, highlightthickness=0, bd=0,
                 activebackground=btn_bg, activeforeground=btn_fg)
lang_menu["menu"].config(bg=btn_bg, fg=btn_fg, font=font_button)
lang_menu.pack(side=tk.LEFT)

lang_frame.pack(anchor="ne", padx=10, pady=5)

def update_language(*args):
    global lang
    lang = get_lang()
    root.title(lang["title"])
    label_lang.config(text="Language:")
    label_entry.config(text=lang["label"])
    dynamic_btn.config(text=lang["start"])

current_lang.trace_add("write", update_language)

# 📦 Основной фрейм (слева — изображение, справа — элементы)
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(pady=10)

# 🖼️ Картинка гнома
try:
    img = Image.open("dwarf.png").resize((100, 100))
    img_tk = ImageTk.PhotoImage(img)
    image_label = tk.Label(main_frame, image=img_tk, bg=bg_color)
    image_label.image = img_tk
    image_label.pack(side=tk.LEFT, padx=10)
except Exception as e:
    print("🛑 Failed to load image:", e)

# 🔤 Правый блок
right_frame = tk.Frame(main_frame, bg=bg_color)
right_frame.pack(side=tk.LEFT, padx=10)

label_entry = tk.Label(right_frame, text=lang["label"], bg=bg_color, fg=fg_color, font=font_label)
label_entry.pack(pady=5)

entry = tk.Entry(right_frame, bg=entry_bg, fg=entry_fg,
                 insertbackground=entry_fg, font=font_entry, justify='center', width=10)
entry.pack(pady=5)
entry.insert(0, "50")

# 🔁 Кнопка с переключением
def run_unsubscribe():
    dynamic_btn.config(text=lang["stop"], command=stop_unsubscribe)
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
        finally:
            dynamic_btn.config(text=lang["start"], command=run_unsubscribe)

    thread = threading.Thread(target=threaded_run)
    thread.start()

def stop_unsubscribe():
    shared.stop_flag = True
    log.insert(tk.END, lang["cancel"] + "\n")
    dynamic_btn.config(text=lang["start"], command=run_unsubscribe)

dynamic_btn = tk.Button(right_frame, text=lang["start"], bg=btn_bg, fg=btn_fg,
                        font=font_button, command=run_unsubscribe)
dynamic_btn.pack(pady=5)

# 🪵 Лог с кастомным скроллом
log_frame = tk.Frame(root, bg=bg_color)
log_frame.pack(padx=10, pady=10, fill='both', expand=True)

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

# ❌ Закрытие окна
def on_close():
    shared.stop_flag = True
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
