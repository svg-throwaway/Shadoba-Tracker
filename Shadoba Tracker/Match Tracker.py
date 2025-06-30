import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# --- Setup database ---
conn = sqlite3.connect("match_history.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_class TEXT,
    opponent_class TEXT,
    result TEXT,
    match_date TEXT
)''')
conn.commit()

# --- Classes for Shadowverse ---
classes = ["Forestcraft", "Swordcraft", "Runecraft", "Dragoncraft", "Abysscraft", "Havencraft", "Portalcraft"]

# --- Languages ---
languages = {
    "English": {
        "your_class": "Class",
        "date": "Date",
        "clear": "Clear History",
        "confirm_clear": "Are you sure you want to clear the match history for this day?",
        "overall": "Overall",
        "all": "All",
        "win": "Win",
        "loss": "Loss",
        "select_class_prompt": "Please select a player class (not 'All') to enter results.",
        "toggle_history_show": "Show History",
        "toggle_history_hide": "Hide History",
        "overall_winrate": "Overall Winrate:",
        "language": "Language",
        "title": "Shadowverse: WB Match Tracker",
        "class_names": {
            "Forestcraft": "Forestcraft",
            "Swordcraft": "Swordcraft",
            "Runecraft": "Runecraft",
            "Dragoncraft": "Dragoncraft",
            "Abysscraft": "Abysscraft",
            "Havencraft": "Havencraft",
            "Portalcraft": "Portalcraft"
        }
    },
    "Japanese": {
        "your_class": "クラス",
        "date": "日付",
        "clear": "クリア",
        "confirm_clear": "試合履歴を消去しますか？",
        "overall": "全体",
        "all": "すべて",
        "win": "勝ち",
        "loss": "負け",
        "select_class_prompt": "結果を入力するには、プレイヤークラス（「すべて」以外）を選択してください。",
        "toggle_history_show": "試合履歴",
        "toggle_history_hide": "試合履歴",
        "overall_winrate": "勝率：",
        "language": "言語",
        "title": "シャドウバWB WIN トラッカー",
        "class_names": {
            "Forestcraft": "エルフ",
            "Swordcraft": "ロイヤル",
            "Runecraft": "ウィッチ",
            "Dragoncraft": "ドラゴン",
            "Abysscraft": "ナイトメア",
            "Havencraft": "ビショップ",
            "Portalcraft": "ネメシス"
        }
    }
}

current_language = "English"




# --- Tkinter setup ---
root = tk.Tk()
root.title(languages[current_language]["title"])
root.geometry("450x420")
root.minsize(450, 350)

icons = {}
for cls in classes:
    icons[cls] = tk.PhotoImage(file=f"icons/{cls.lower()}.png")  # adjust path as needed
icon_img = tk.PhotoImage(file=f"icons/favicon.png")  # or .ico
root.iconphoto(False, icon_img)

# Dark theme colors
bg_color = "#212121"
fg_color = "#EEEEEE"
entry_bg = "#757575"
button_win_bg = "#66BB6A"
button_win_active = "#2E7D32"
button_loss_bg = "#EF5350"
button_loss_active = "#C62828"
text_bg = "#212121"
text_fg = "#EEEEEE"

root.configure(bg=bg_color)

# --- Styles ---
style = ttk.Style()
style.theme_use('clam')  # Better for styling

style.configure('TLabel', background=bg_color, foreground=fg_color)
style.configure('TButton', background=bg_color, foreground=fg_color)
style.configure('TCombobox',
                fieldbackground='#444444',
                background='#444444',
                foreground='#EEEEEE')

style.map('TCombobox',
          fieldbackground=[('readonly', '#444444')],
          background=[('readonly', '#EEEEEE')],
          foreground=[('readonly', '#EEEEEE')])

# --- Variables ---
player_class_var = tk.StringVar()
date_var = tk.StringVar()
lang_var = tk.StringVar(value="EN")

# --- Track dates opened ---
cursor.execute("SELECT DISTINCT match_date FROM matches ORDER BY match_date DESC")
dates_opened = [row[0] for row in cursor.fetchall()]

def update_date_options():
    lang = languages[current_language]
    cursor.execute("SELECT DISTINCT match_date FROM matches ORDER BY match_date DESC")
    dates = [row[0] for row in cursor.fetchall()]

    today = datetime.today().strftime("%Y-%m-%d")
    if today not in dates:
        dates.insert(0, today)  # Add today at the top

    date_dropdown['values'] = [lang["overall"]] + dates

    # If current selected date is not valid, reset to overall
    if today in date_dropdown['values']:
        date_var.set(today)
    else:
        date_var.set(lang["overall"])

# --- UI Frames ---
top_frame = tk.Frame(root, bg=bg_color)
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
top_frame.grid_columnconfigure(1, weight=1)

button_container = tk.Frame(root, bg=bg_color)
button_container.grid(row=1, column=0, sticky="ew", padx=10)
button_container.grid_columnconfigure(0, weight=1)

history_container = tk.Frame(root, bg=bg_color)
history_container.grid(row=3, column=0, sticky="nsew", padx=10, pady=(5,10))
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Control frame for toggle, overall winrate, and clear button
control_frame = tk.Frame(root, bg=bg_color)
control_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5,0))
control_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(1, weight=1)
control_frame.grid_columnconfigure(2, weight=1)

# --- Top row widgets ---
your_class_label = ttk.Label(top_frame, text=languages[current_language]["your_class"])
your_class_label.grid(row=0, column=0, sticky="w")

player_class_options = [languages[current_language]["all"]] + classes
player_class_dropdown = ttk.Combobox(top_frame, textvariable=player_class_var, values=player_class_options, state='readonly', width=12)
player_class_dropdown.grid(row=0, column=1, sticky="w", padx=(5,15))
player_class_dropdown.current(0)

date_label = ttk.Label(top_frame, text=languages[current_language]["date"])
date_label.grid(row=0, column=2, sticky="w")

date_options = [languages[current_language]["overall"]] + dates_opened
date_dropdown = ttk.Combobox(top_frame, textvariable=date_var, values=date_options, state='readonly', width=12)
date_dropdown.grid(row=0, column=3, sticky="w", padx=5)
if date_options:
    date_var.set(date_options[0])

# Language dropdown
language_label = ttk.Label(top_frame, text=languages[current_language]["language"])
language_label.grid(row=0, column=4, sticky="w", padx=(20,5))

lang_dropdown = ttk.Combobox(top_frame, textvariable=lang_var, values=["EN", "JP"], state='readonly', width=5)
lang_dropdown.grid(row=0, column=5, sticky="w")
lang_dropdown.current(0)

# --- Buttons for classes ---
stat_labels = {}

def record_match(opponent_cls, result):
    selected = player_class_var.get()
    lang = languages[current_language]
    if selected == lang["all"]:
        pc = lang["all"]
    else:
        pc = next((cls for cls in classes if lang["class_names"][cls] == selected), lang["all"])

    dt = date_var.get()
    lang = languages[current_language]

    if pc == lang["all"]:
        messagebox.showwarning("Warning", lang["select_class_prompt"])
        return
    if dt == lang["overall"]:
        return

    cursor.execute("INSERT INTO matches (player_class, opponent_class, result, match_date) VALUES (?, ?, ?, ?)",
                   (pc, opponent_cls, result, dt))
    conn.commit()

    refresh_history()
    update_stats()

def clear_history():
    dt = date_var.get()
    lang = languages[current_language]

    if dt == lang["overall"]:
        return

    if messagebox.askyesno(title=lang["clear"], message=lang["confirm_clear"]):
        cursor.execute("DELETE FROM matches WHERE match_date=?", (dt,))
        conn.commit()
        update_date_options()
        refresh_history()
        update_stats()

def refresh_history():
    history_box.configure(state='normal')
    history_box.delete(1.0, tk.END)

    selected = player_class_var.get()
    lang = languages[current_language]

    # Map selected localized class name back to internal class key
    if selected == lang["all"]:
        pc = lang["all"]
    else:
        pc = next((cls for cls in classes if lang["class_names"][cls] == selected), lang["all"])

    dt = date_var.get()
    date_filter = "" if dt == lang["overall"] else dt

    # Build query based on selected filters
    if pc == lang["all"]:
        if date_filter:
            cursor.execute(
                "SELECT player_class, opponent_class, result, match_date FROM matches WHERE match_date=? ORDER BY id",
                (date_filter,)
            )
        else:
            cursor.execute("SELECT player_class, opponent_class, result, match_date FROM matches ORDER BY id")
    else:
        if date_filter:
            cursor.execute(
                "SELECT player_class, opponent_class, result, match_date FROM matches WHERE player_class=? AND match_date=? ORDER BY id",
                (pc, date_filter)
            )
        else:
            cursor.execute(
                "SELECT player_class, opponent_class, result, match_date FROM matches WHERE player_class=? ORDER BY id",
                (pc,)
            )

    matches = cursor.fetchall()

    for match in matches:
        player_cls = lang["class_names"].get(match[0], match[0])
        opponent_cls = lang["class_names"].get(match[1], match[1])
        result = match[2].capitalize()

        # Optional: localize result if you define 'results' in your lang dictionary
        # result = lang["results"].get(result, result)

        line = f"{match[3]} | You ({player_cls}) vs {opponent_cls} | {result}\n"
        history_box.insert(tk.END, line)

    history_box.configure(state='disabled')


def update_stats():
    selected = player_class_var.get()
    lang = languages[current_language]
    if selected == lang["all"]:
        pc = lang["all"]
    else:
        pc = next((cls for cls in classes if lang["class_names"][cls] == selected), lang["all"])

    dt = date_var.get()

    lang = languages[current_language]

    for cls in classes:
        win_count = loss_count = 0
        query = "SELECT result FROM matches WHERE opponent_class=?"
        params = [cls]

        if pc != lang["all"]:
            query += " AND player_class=?"
            params.append(pc)
        if dt != lang["overall"]:
            query += " AND match_date=?"
            params.append(dt)

        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        for r in results:
            if r[0] == 'win':
                win_count += 1
            elif r[0] == 'loss':
                loss_count += 1

        total = win_count + loss_count
        win_pct = (win_count / total * 100) if total > 0 else 0

        win_label = stat_labels[cls]['win']
        loss_label = stat_labels[cls]['loss']
        pct_label = stat_labels[cls]['pct']

        win_label.config(text=str(win_count))
        loss_label.config(text=str(loss_count))
        pct_label.config(text=f"{win_pct:.1f}%")

    # Overall winrate
    win_total = loss_total = 0
    params = []
    query = "SELECT result FROM matches"
    if pc != lang["all"]:
        query += " WHERE player_class=?"
        params.append(pc)
        if dt != lang["overall"]:
            query += " AND match_date=?"
            params.append(dt)
    else:
        if dt != lang["overall"]:
            query += " WHERE match_date=?"
            params.append(dt)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    for r in results:
        if r[0] == 'win':
            win_total += 1
        elif r[0] == 'loss':
            loss_total += 1

    total = win_total + loss_total
    winrate = (win_total / total * 100) if total > 0 else 0
    overall_label.config(text=f"{lang['overall_winrate']} {winrate:.1f}% ({win_total}/{total})")


def toggle_history():
    if history_container.winfo_ismapped():
        history_container.grid_remove()
        toggle_button.config(text=languages[current_language]["toggle_history_show"])
    else:
        history_container.grid()
        toggle_button.config(text=languages[current_language]["toggle_history_hide"])

def on_player_class_change(event=None):
    selected = player_class_var.get()
    lang = languages[current_language]

    # Map localized class name to internal key
    if selected == lang["all"]:
        pc = lang["all"]
    else:
        pc = next((cls for cls in classes if lang["class_names"][cls] == selected), lang["all"])
    player_class_var.set(lang["class_names"].get(pc, lang["all"]))

    # Disable buttons if 'all' is selected
    state = tk.NORMAL if pc != lang["all"] else tk.DISABLED

    for cls in classes:
        stat_labels[cls]['win_btn'].config(state=state)
        stat_labels[cls]['loss_btn'].config(state=state)

    refresh_history()
    update_stats()

def on_date_change(event=None):
    update_date_options()
    on_player_class_change()

def on_language_change(event=None):
    global current_language
    current_language = "English" if lang_var.get() == "EN" else "Japanese"
    lang = languages[current_language]

    # Update static labels
    your_class_label.config(text=lang["your_class"])
    date_label.config(text=lang["date"])
    language_label.config(text=lang["language"])
    clear_btn.config(text=lang["clear"])
    toggle_button.config(text=lang["toggle_history_hide"] if history_container.winfo_ismapped() else lang["toggle_history_show"])
    overall_label.config(text="")
    root.title(languages[current_language]["title"])

    # Update class name labels in stat_labels
    for cls in classes:
        stat_labels[cls]["label"].config(text=lang["class_names"][cls])

    # Update player class dropdown
    player_class_dropdown['values'] = [lang["all"]] + [lang["class_names"][cls] for cls in classes]
    if player_class_var.get() not in player_class_dropdown['values']:
        player_class_var.set(lang["all"])

    # Refresh everything
    update_date_options()
    refresh_history()
    update_stats()


# --- Create buttons for each class with win/loss and stats ---
for i, cls in enumerate(classes):
    frame = tk.Frame(button_container, bg=bg_color)
    frame.grid(row=i, column=0, pady=4, sticky="ew")
    frame.grid_columnconfigure(1, weight=1)
    # Class label
    lbl = tk.Label(frame,
                   text=languages[current_language]["class_names"][cls],
                   image=icons[cls],
                   anchor='center',
                   compound='left',  # icon on left, text on right
                   bg=bg_color, fg=fg_color,
                   font=("Arial", 12), padx=8)
    lbl.grid(row=0, column=0, sticky="w", padx=5)

    # Win button
    win_btn = tk.Button(frame, text=languages[current_language]["win"],
                        bg=button_win_bg, fg="white",
                        activebackground=button_win_active,
                        command=lambda c=cls: record_match(c, "win"),
                        width=6)
    win_btn.grid(row=0, column=1, sticky="e", padx=(10, 2))

    # Win count label
    win_lbl = tk.Label(frame, text="0", bg=bg_color, fg=fg_color, width=3, anchor="center", font=("Arial", 12))
    win_lbl.grid(row=0, column=2, sticky="w")

    # Loss button
    loss_btn = tk.Button(frame, text=languages[current_language]["loss"],
                         bg=button_loss_bg, fg="white",
                         activebackground=button_loss_active,
                         command=lambda c=cls: record_match(c, "loss"),
                         width=6)
    loss_btn.grid(row=0, column=3, sticky="e", padx=(10, 2))

    # Loss count label
    loss_lbl = tk.Label(frame, text="0", bg=bg_color, fg=fg_color, width=3, anchor="center", font=("Arial", 12))
    loss_lbl.grid(row=0, column=4, sticky="w")

    # Win % label
    pct_lbl = tk.Label(frame, text="0.0%", bg=bg_color, fg=fg_color, width=6, anchor="center", font=("Arial", 12))
    pct_lbl.grid(row=0, column=5, sticky="w", padx=(10,0))

    stat_labels[cls] = {
        "win_btn": win_btn,
        "loss_btn": loss_btn,
        "win": win_lbl,
        "loss": loss_lbl,
        "pct": pct_lbl,
        "label": lbl
    }

# --- History Text box with scrollbar ---
history_box = tk.Text(history_container, bg=text_bg, fg=text_fg, state='disabled', wrap='none', height=10, font=("Arial", 12), padx=4)
history_box.grid(row=0, column=0, sticky="nsew")
history_container.grid_rowconfigure(0, weight=1)
history_container.grid_columnconfigure(0, weight=1)

scrollbar = tk.Scrollbar(history_container, command=history_box.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
history_box.config(yscrollcommand=scrollbar.set)

# --- Control bar widgets ---
toggle_button = tk.Button(control_frame, text=languages[current_language]["toggle_history_hide"],
                          command=toggle_history,
                          bg=bg_color, fg=fg_color)
toggle_button.grid(row=0, column=0, sticky="w")

overall_label = tk.Label(control_frame, text="", bg=bg_color, fg=fg_color,
                         font=("Arial", 12, "bold"))
overall_label.grid(row=0, column=1, sticky="ew")

clear_btn = tk.Button(control_frame, text=languages[current_language]["clear"],
                      command=clear_history,
                      bg=button_loss_bg, fg="white",
                      activebackground="#a62a28",
                      relief="raised", bd=1)
clear_btn.grid(row=0, column=2, sticky="e")

# --- Bindings ---
player_class_dropdown.bind("<<ComboboxSelected>>", on_player_class_change)
date_dropdown.bind("<<ComboboxSelected>>", on_date_change)
lang_dropdown.bind("<<ComboboxSelected>>", on_language_change)

# --- Initial Setup ---
update_date_options()
refresh_history()
update_stats()

# Center win/loss buttons based on player class selected at startup
on_player_class_change()

root.mainloop()
