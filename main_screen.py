import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import shared
from unsubscribe import get_messages
from lang_manager import get_lang, current_lang

class MainScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#83b3fa")
        self.lang = get_lang()
        self.build_ui()

    def build_ui(self):
        # Цвета и шрифты
        self.bg_color = "#83b3fa"
        self.fg_color = "#18212d"
        self.btn_bg = "#fbcc5d"
        self.btn_fg = "#243144"
        self.entry_bg = "#f1ecf6"
        self.entry_fg = "#18212d"
        self.log_bg = "#ddeafe"
        self.log_fg = "#243144"
        self.scrol_bg = "#f4f8ff"
        self.scrol_fg = "#f9cd70"
        self.font_button = ("Fira Code", 10, "bold")
        self.font_entry = ("Fira Code", 11)
        self.font_label = ("Segoe UI", 10, "bold")
        self.font_log = ("Fira Code", 10)

        # Основной блок
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(pady=10)

        try:
            img = Image.open("dwarf.png").resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            image_label = tk.Label(main_frame, image=img_tk, bg=self.bg_color)
            image_label.image = img_tk
            image_label.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print("🛑 Failed to load image:", e)

        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side=tk.LEFT, padx=10)

        self.label_entry = tk.Label(right_frame, text=self.lang["label"],
                                    bg=self.bg_color, fg=self.fg_color, font=self.font_label)
        self.label_entry.pack(pady=5)

        self.entry = tk.Entry(right_frame, bg=self.entry_bg, fg=self.entry_fg,
                              insertbackground=self.entry_fg, font=self.font_entry,
                              justify='center', width=10)
        self.entry.insert(0, "50")
        self.entry.pack(pady=5)

        self.dynamic_btn = tk.Button(right_frame, text=self.lang["start"], bg=self.btn_bg, fg=self.btn_fg,
                                     font=self.font_button, command=self.run_unsubscribe)
        self.dynamic_btn.pack(pady=5)

        # лог
        log_frame = tk.Frame(self, bg=self.bg_color)
        log_frame.pack(padx=10, pady=10, fill='both', expand=True)

        style = ttk.Style()
        style.theme_use('default')
        style.configure('Vertical.TScrollbar',
                        background=self.btn_bg,
                        troughcolor=self.scrol_bg,
                        bordercolor=self.scrol_bg,
                        arrowcolor=self.btn_fg,
                        relief='flat')

        self.log = tk.Text(log_frame, wrap='word',
                           bg=self.log_bg, fg=self.log_fg,
                           insertbackground=self.log_fg,
                           font=self.font_log)
        self.log.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient='vertical', command=self.log.yview, style='Vertical.TScrollbar')
        scrollbar.pack(side='right', fill='y')

        self.log.configure(yscrollcommand=scrollbar.set)

    def run_unsubscribe(self):
        self.dynamic_btn.config(text=self.lang["stop"], command=self.stop_unsubscribe)
        try:
            limit = int(self.entry.get())
        except ValueError:
            self.log.insert(tk.END, self.lang["error"] + "\n")
            self.log.see(tk.END)
            return

        self.log.insert(tk.END, self.lang["launch"] + "\n")
        shared.stop_flag = False

        def threaded_run():
            try:
                get_messages(limit=limit, log_output=self.log, lang_code=current_lang.get())
            except Exception as e:
                self.log.insert(tk.END, f"{self.lang['process_error']} {e}\n")
            finally:
                self.dynamic_btn.config(text=self.lang["start"], command=self.run_unsubscribe)

        threading.Thread(target=threaded_run).start()

    def stop_unsubscribe(self):
        shared.stop_flag = True
        self.log.insert(tk.END, self.lang["cancel"] + "\n")
        self.dynamic_btn.config(text=self.lang["start"], command=self.run_unsubscribe)
