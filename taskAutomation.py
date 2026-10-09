"""
Task Automation with Python Scripts:
A single menu-driven tool that bundles three small real-life automations:

  1. Move all .jpg / .jpeg files from one folder to another
  2. Extract all email addresses from a .txt file into a new file
  3. Scrape the <title> of a fixed webpage and save it

Concepts used: os, shutil, re, requests, file handling.
"""

import os
import re
import shutil
from datetime import datetime

# optional dependency handling
try:
    import requests
except ImportError:          # keeps tasks 1 & 2 working without requests
    requests = None


def unique_path(folder: str, filename: str) -> str:
    """Return a path in `folder` that doesn't overwrite an existing file."""
    base, ext = os.path.splitext(filename)
    candidate = os.path.join(folder, filename)
    counter = 1
    while os.path.exists(candidate):
        candidate = os.path.join(folder, f"{base}_{counter}{ext}")
        counter += 1
    return candidate


def pause():
    input("\nPress Enter to return to the menu...")


# TASK 1 — MOVE ALL .jpg FILES TO A NEW FOLDER
def move_jpg_files(source_folder: str, dest_folder: str) -> None:
    """Move every .jpg/.jpeg file from source_folder into dest_folder."""
    source_folder = os.path.expanduser(source_folder.strip())
    dest_folder = os.path.expanduser(dest_folder.strip())

    # validate source
    if not os.path.isdir(source_folder):
        print(f"✗ Source folder not found: {source_folder}")
        return

    if os.path.abspath(source_folder) == os.path.abspath(dest_folder):
        print("✗ Source and destination are the same folder. Nothing to do.")
        return

    # create destination
    try:
        os.makedirs(dest_folder, exist_ok=True)
    except OSError as e:
        print(f"✗ Could not create destination folder: {e}")
        return

    moved, skipped = 0, 0

    # walk through the folder
    for name in os.listdir(source_folder):
        src_path = os.path.join(source_folder, name)

        # only real files (skip sub-folders), and only .jpg / .jpeg
        if not os.path.isfile(src_path):
            continue
        if os.path.splitext(name)[1].lower() not in (".jpg", ".jpeg"):
            continue

        try:
            target = unique_path(dest_folder, name)
            shutil.move(src_path, target)     # shutil handles cross-drive moves
            moved += 1
            print(f"  → moved: {name}")
        except (OSError, shutil.Error) as e:
            skipped += 1
            print(f"  ! skipped {name}: {e}")

    print(f"\n✔ Done. {moved} file(s) moved, {skipped} skipped.")
    print(f"  Destination: {dest_folder}")


# TASK 2 — EXTRACT EMAILS FROM A .txt FILE
EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}"
)


def extract_emails(input_file: str, output_file: str) -> None:
    """Find every email address in input_file and write the unique ones out."""
    input_file = os.path.expanduser(input_file.strip())
    output_file = os.path.expanduser(output_file.strip())

    if not os.path.isfile(input_file):
        print(f"✗ File not found: {input_file}")
        return

    # read
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except OSError as e:
        print(f"✗ Could not read file: {e}")
        return

    # regex search + de-duplicate (dict preserves insertion order)
    found = EMAIL_PATTERN.findall(text)
    unique = list(dict.fromkeys(email.lower() for email in found))

    if not unique:
        print("✗ No email addresses found in that file.")
        return

    # write
    out_dir = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(out_dir, exist_ok=True)

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(unique) + "\n")
    except OSError as e:
        print(f"✗ Could not write output file: {e}")
        return

    print(f"\n✔ Found {len(found)} email(s); {len(unique)} unique.")
    for email in unique[:15]:                 # preview the first 15
        print(f"  • {email}")
    if len(unique) > 15:
        print(f"  ... and {len(unique) - 15} more")
    print(f"\n  Saved to: {output_file}")


# TASK 3 — SCRAPE THE TITLE OF A FIXED WEBPAGE
TITLE_PATTERN = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def scrape_title(url: str, output_file: str) -> None:
    """Fetch `url`, pull out its <title>, and append it to output_file."""
    if requests is None:
        print("✗ The 'requests' library is not installed.")
        print("  Install it with:  pip install requests")
        return

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # fetch
    try:
        headers = {"User-Agent": "Mozilla/5.0 (TaskAutomationScript/1.0)"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not reach the page: {e}")
        return

    # parse
    match = TITLE_PATTERN.search(response.text)
    if not match:
        print("✗ No <title> tag found on that page.")
        return

    # collapse whitespace/newlines inside the title
    title = re.sub(r"\s+", " ", match.group(1)).strip()
    print(f"\n✔ Page title: {title}")

    # save (append, with a timestamp)
    output_file = os.path.expanduser(output_file.strip())
    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"[{stamp}] {url} -> {title}\n")
    except OSError as e:
        print(f"✗ Could not write output file: {e}")
        return

    print(f"  Saved to: {output_file}")


MENU = """
============================================================
              TASK AUTOMATION WITH PYTHON
============================================================
  1. Move all .jpg files from a folder to a new folder
  2. Extract all email addresses from a .txt file
  3. Scrape the title of a webpage
  0. Exit
============================================================"""


def main() -> None:
    while True:
        print(MENU)
        choice = input("Choose a task (0-3): ").strip()

        if choice == "1":
            print("\n--- MOVE .jpg FILES ---")
            src = input("Source folder (e.g. ~/Downloads): ")
            dst = input("Destination folder (e.g. ~/Pictures/jpg): ")
            move_jpg_files(src, dst)
            pause()

        elif choice == "2":
            print("\n--- EXTRACT EMAILS ---")
            infile = input("Input .txt file: ")
            outfile = input("Output file [emails_found.txt]: ").strip() or "emails_found.txt"
            extract_emails(infile, outfile)
            pause()

        elif choice == "3":
            print("\n--- SCRAPE PAGE TITLE ---")
            url = input("URL (e.g. https://example.com): ")
            outfile = input("Output file [titles.txt]: ").strip() or "titles.txt"
            scrape_title(url, outfile)
            pause()

        elif choice == "0":
            print("\nGoodbye! 👋")
            break

        else:
            print("✗ Invalid choice. Please enter 0, 1, 2 or 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 👋")