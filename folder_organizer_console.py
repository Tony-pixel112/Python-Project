"""
Folder Organizer
-----------------
Automatically sorts files in a target folder into subfolders
based on file type. Supports a dry-run preview mode and an
undo option that reverses the most recent run.

Instead of typing a full path, just type the folder's name
(e.g. "Downloads" or "Tony") and the script will search common
locations, then fall back to a broader recursive search if needed.

Usage:
    python folder_organizer.py
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

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

    # --- Step 1: fast check of common locations ---
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

    # --- Step 2: recursive fallback search ---
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
            # Some system folders block access — skip them instead of crashing
            pass
        return None

    return search_recursive(home, folder_name, max_depth)


def save_log(move_log: list):
    """Save this run's moves to the log file, timestamped, so it can be undone later."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "moves": move_log
    }

    # Load existing history if it exists, so we don't overwrite past runs
    history = []
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            history = json.load(f)

    history.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print("Move log saved. You can undo this run with the undo option.")


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

    last_run = history.pop()  # remove and get the most recent entry
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

    # Save the updated history with the undone run removed
    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)

    print(f"\nUndo complete. Restored {undone_count} file(s).")


def organize_folder(target_folder: Path, dry_run: bool = False):
    if not target_folder.exists():
        print(f"Folder not found: {target_folder}")
        return

    moved_count = 0
    move_log = []  # collects records of every real move this run

    for item in target_folder.iterdir():
        # Skip folders — only move files
        if item.is_dir():
            continue

        # Skip the script itself if it happens to sit in the same folder
        if item.suffix == ".py":
            continue

        category = get_category(item.suffix)
        destination_folder = target_folder / category
        destination_path = destination_folder / item.name

        # Avoid overwriting existing files with the same name
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


def show_menu():
    print("\n===== Folder Organizer =====")
    print("1. Organize a folder")
    print("2. Undo last run")
    print("3. Exit")
    print("=============================")


if __name__ == "__main__":
    # Looping here just means you can organize, undo, organize again, etc.
    # all in one session. The undo function itself still works exactly the
    # same way even if you close the script and run it fresh later --
    # it always reads from LOG_FILE on disk, not from anything in memory.
    while True:
        show_menu()
        choice = input("Choose an option (1-3): ").strip()

        if choice == "3":
            print("Goodbye!")
            break

        elif choice == "2":
            undo_last_run()

        elif choice == "1":
            folder_name = input("Enter the folder name you want to organize: ").strip()
            found_folder = find_folder(folder_name)

            if found_folder is None:
                print(f"Couldn't find a folder named '{folder_name}' in common locations.")
                print("Try typing the full path instead.")
            else:
                print(f"Found folder: {found_folder}")

                preview = input("Run as a preview first? (y/n): ").strip().lower()
                if preview == "y":
                    organize_folder(found_folder, dry_run=True)
                    confirm = input("\nProceed with the real move? (y/n): ").strip().lower()
                    if confirm == "y":
                        organize_folder(found_folder, dry_run=False)
                    else:
                        print("Cancelled. No files were moved.")
                else:
                    organize_folder(found_folder, dry_run=False)

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
