"""
Folder Organizer (GUI version)
-------------------------------
Same logic as the console version, but with a proper window,
buttons, and a live output log instead of typing commands.
Styled with a dark theme.

Usage:
    python folder_organizer_gui.py
"""

import json
import shutil
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, scrolledtext

# ---------- CONFIG ----------

# Map of folder name -> list of file extensions that go into it
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".apk"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".ipynb"],
}

# How many folder levels deep the fallback search is allowed to go
MAX_SEARCH_DEPTH = 3

# Where the move history is saved, used for the undo feature
LOG_FILE = Path.home() / "folder_organizer_log.json"

# ---------- THEME ----------

BG_COLOR = "#1e1e2e"       # main background
FRAME_COLOR = "#2a2a3d"    # panels/entry background
TEXT_COLOR = "#e0e0e0"     # light text for readability
ACCENT_COLOR = "#7c5cff"   # buttons/highlights (soft purple)
ACCENT_ACTIVE = "#6647cc"  # button color while being clicked
LOG_BG = "#12121c"         # activity log background (darker than main bg)
LOG_TEXT = "#8be9a4"       # green-ish, terminal-style text

FONT_LABEL = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 9)

# -----------------------------
# ---- CORE LOGIC (unchanged from the console version) ----
# -----------------------------


def get_category(extension: str) -> str:
    """Return the category folder name for a given file extension."""
    extension = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def find_folder(folder_name: str, max_depth: int = MAX_SEARCH_DEPTH) -> Path | None:
    """
    Search for a folder matching folder_name.
    Step 1: check common top-level locations (fast).
    Step 2: if not found, recursively search from home,
            limited to max_depth levels deep (slower, more thorough).
    Returns the matching Path, or None if nothing is found.
    """
    home = Path.home()

    search_locations = [
        home,
        home / "Desktop",
        home / "Documents",
        home / "Downloads",
        home / "Pictures",
        home / "Music",
        home / "Videos",
    ]

    for location in search_locations:
        if not location.exists():
            continue
        candidate = location / folder_name
        if candidate.exists() and candidate.is_dir():
            return candidate

    print("Not found in common locations — searching more broadly, this may take a moment...")

    def search_recursive(start: Path, target: str, depth: int) -> Path | None:
        if depth < 0:
            return None
        try:
            for item in start.iterdir():
                if item.is_dir():
                    if item.name.lower() == target.lower():
                        return item
                    result = search_recursive(item, target, depth - 1)
                    if result is not None:
                        return result
        except PermissionError:
            pass
        return None

    return search_recursive(home, folder_name, max_depth)


def save_log(move_log: list):
    """Save this run's moves to the log file, timestamped, so it can be undone later."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "moves": move_log
    }

    history = []
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            history = json.load(f)

    history.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print("Move log saved. You can undo this run with the Undo button.")


def undo_last_run():
    """Reverse the most recent run recorded in the log file."""
    if not LOG_FILE.exists():
        print("No move log found — nothing to undo.")
        return

    with open(LOG_FILE, "r") as f:
        history = json.load(f)

    if not history:
        print("Log file is empty — nothing to undo.")
        return

    last_run = history.pop()
    moves = last_run["moves"]

    print(f"Undoing run from {last_run['timestamp']} ({len(moves)} file(s))...")

    undone_count = 0
    for move in reversed(moves):
        original_path = Path(move["original_path"])
        new_path = Path(move["new_path"])

        if new_path.exists():
            original_path.parent.mkdir(exist_ok=True)
            shutil.move(str(new_path), str(original_path))
            print(f"Restored: {new_path.name} -> {original_path.parent}/")
            undone_count += 1
        else:
            print(f"Skipped (file not found): {new_path}")

    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print(f"\nUndo complete. Restored {undone_count} file(s).")


def organize_folder(target_folder: Path, dry_run: bool = False):
    if not target_folder.exists():
        print(f"Folder not found: {target_folder}")
        return

    moved_count = 0
    move_log = []

    for item in target_folder.iterdir():
        if item.is_dir():
            continue

        if item.suffix == ".py":
            continue

        category = get_category(item.suffix)
        destination_folder = target_folder / category
        destination_path = destination_folder / item.name

        if destination_path.exists():
            base = item.stem
            ext = item.suffix
            counter = 1
            while destination_path.exists():
                destination_path = destination_folder / f"{base}_{counter}{ext}"
                counter += 1

        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/")
        else:
            destination_folder.mkdir(exist_ok=True)
            original_path = str(item)
            new_path = str(destination_path)
            shutil.move(original_path, new_path)
            print(f"Moved: {item.name} -> {category}/")

            move_log.append({
                "original_path": original_path,
                "new_path": new_path
            })

        moved_count += 1

    if moved_count == 0:
        print("No files to organize. Everything's already sorted!")
    elif dry_run:
        print(f"\n[DRY RUN] Would have organized {moved_count} file(s). No files were actually moved.")
    else:
        print(f"\nDone. Organized {moved_count} file(s).")
        save_log(move_log)


# -----------------------------
# ---- GUI CODE ----
# -----------------------------


class TextRedirector:
    """Redirects print() output into a tkinter text widget instead of the console."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)  # auto-scroll to the latest line

    def flush(self):
        pass  # required for compatibility with Python's print system, but we don't need it


def set_status(text, color=ACCENT_COLOR):
    status_label.config(text=text, fg=color)
    root.update_idletasks()


def on_preview():
    folder_name = folder_entry.get().strip()
    if not folder_name:
        messagebox.showwarning("Missing Folder", "Please enter a folder name first.")
        return

    set_status("Searching...")
    found = find_folder(folder_name)
    if found is None:
        set_status("Not found", color="#ff6b6b")
        messagebox.showerror("Not Found", f"Couldn't find folder '{folder_name}'")
        return

    print(f"Found folder: {found}")
    set_status("Previewing...")
    organize_folder(found, dry_run=True)
    set_status("Ready")


def on_organize():
    folder_name = folder_entry.get().strip()
    if not folder_name:
        messagebox.showwarning("Missing Folder", "Please enter a folder name first.")
        return

    set_status("Searching...")
    found = find_folder(folder_name)
    if found is None:
        set_status("Not found", color="#ff6b6b")
        messagebox.showerror("Not Found", f"Couldn't find folder '{folder_name}'")
        return

    confirm = messagebox.askyesno("Confirm", f"Organize files in:\n{found}?")
    if confirm:
        set_status("Organizing...")
        organize_folder(found, dry_run=False)
        set_status("Done", color="#8be9a4")
    else:
        set_status("Ready")


def on_undo():
    confirm = messagebox.askyesno("Confirm Undo", "Undo the most recent organize run?")
    if confirm:
        set_status("Undoing...")
        undo_last_run()
        set_status("Done", color="#8be9a4")


def styled_button(parent, text, command):
    return tk.Button(
        parent, text=text, command=command,
        bg=ACCENT_COLOR, fg="white",
        activebackground=ACCENT_ACTIVE,
        activeforeground="white",
        font=FONT_LABEL,
        relief="flat",
        width=14,
        cursor="hand2"
    )


# --- Build the window ---

root = tk.Tk()
root.title("Folder Organizer")
root.geometry("520x500")
root.resizable(True, True)
root.configure(bg=BG_COLOR)

tk.Label(root, text="Folder name:", font=FONT_LABEL, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(15, 0))

folder_entry = tk.Entry(
    root, width=40, font=FONT_LABEL,
    bg=FRAME_COLOR, fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat"
)
folder_entry.pack(pady=5, ipady=4)

button_frame = tk.Frame(root, bg=BG_COLOR)
button_frame.pack(pady=15)

styled_button(button_frame, "Preview", on_preview).grid(row=0, column=0, padx=5)
styled_button(button_frame, "Organize", on_organize).grid(row=0, column=1, padx=5)
styled_button(button_frame, "Undo Last Run", on_undo).grid(row=0, column=2, padx=5)

status_label = tk.Label(root, text="Ready", font=FONT_LABEL, bg=BG_COLOR, fg=ACCENT_COLOR)
status_label.pack(pady=(0, 10))

tk.Label(root, text="Activity Log:", font=FONT_LABEL, bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=(0, 5))

output_box = scrolledtext.ScrolledText(
    root, width=62, height=15,
    bg=LOG_BG, fg=LOG_TEXT,
    insertbackground=LOG_TEXT,
    font=FONT_MONO,
    relief="flat"
)
output_box.pack(pady=5, padx=10, fill="both", expand=True)

# From this point on, every print() call writes into output_box instead of a console
sys.stdout = TextRedirector(output_box)

print("Ready. Enter a folder name above and choose an action.")

if __name__ == "__main__":
    root.mainloop()
