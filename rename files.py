import os
from pathlib import Path

def rename_files_and_folders(base_folder: str):
    base = Path(base_folder)

    if not base.exists():
        print(f"❌ Path not found: {base}")
        return

    # Rename files first
    for path in base.rglob("*"):
        if path.is_file():
            new_name = path.name.replace(" ", "-")
            if new_name != path.name:
                new_path = path.with_name(new_name)
                print(f"📄 File rename:\n   {path}\n   ➡ {new_path}")
                path.rename(new_path)

    # Rename folders (deepest first, so reverse sort by path length)
    for path in sorted(base.rglob("*"), key=lambda p: len(str(p)), reverse=True):
        if path.is_dir():
            new_name = path.name.replace(" ", "-")
            if new_name != path.name:
                new_path = path.with_name(new_name)
                print(f"📁 Folder rename:\n   {path}\n   ➡ {new_path}")
                path.rename(new_path)

if __name__ == "__main__":
    folder = input("Enter the base directory path: ").strip()
    rename_files_and_folders(folder)
