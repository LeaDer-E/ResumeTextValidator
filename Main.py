# Let's implement the final version of the code with RTL/LTR direction detection per file
import os
import re
import sys
from datetime import datetime
from docx import Document
from colorama import init, Fore, Style
from collections import defaultdict

init(autoreset=True)

# Allowed characters and symbols
ARABIC = '\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF'
LATIN = 'A-Za-z'
# ALLOWED_SYMBOLS = r'\|\/\-\–\:\.%\.,;:!?\"\'’\(\)_\+\&\s\u200b0-9@éÉ'
# ALLOWED_SYMBOLS = r'\|\/\-\–\—\:\.%\.,;:!?\"\'’\(\)_\+\&\s\u200b0-9@éÉ\u2010\u2011\u2012\u2013\u2014'
ALLOWED_SYMBOLS = r'\|\/\-\–\—\:\.%\.,;:!?\"\'’\(\)_\+\&\s\u200b0-9@،”“\u2010\u2011\u2012\u2013\u2014'


EXCEPTION_WORDS = ['Café', 'café']
strange_pattern = re.compile(f'[^{LATIN}{ARABIC}{ALLOWED_SYMBOLS}]')

bad_keywords_list = [
    "Not", "غير", "unspecified", "Not Specified", "Not Mentioned", "Not Available",
    "Not Disclosed", "Not Applicable", "N/A", "Pending Update", "To Be Confirmed",
    "TBC", "Yet to Be Determined", "No Data Available", "غير محدد", "غير مذكور",
    "لم يتم الإفصاح", "غير متوفر", "لا ينطبق", "لم يُذكر", "تحت التحديث",
    "سيتم التحديد لاحقًا", "لم يُحدد بعد"
]
keywords = re.compile(r'\b(?:' + '|'.join(re.escape(k) for k in bad_keywords_list) + r')\b', re.IGNORECASE)

def is_mixed_word(word):
    return bool(re.search(f'[{LATIN}]', word) and re.search(f'[{ARABIC}]', word))

def is_arabic(text):
    return bool(re.search(f'[{ARABIC}]', text))

def load_exclusions(file="Ex.txt"):
    if not os.path.exists(file):
        return set(), set()
    files, folders = set(), set()
    with open(file, encoding='utf-8') as f:
        for line in f:
            name = line.strip().lower()
            if name.endswith('.docx'):
                files.add(name)
            elif name:
                folders.add(name)
    return files, folders

def highlight_issues_terminal(text):
    words = text.split()
    new_words = []
    for word in words:
        if word in EXCEPTION_WORDS:
            new_words.append(word)
        elif strange_pattern.search(word) or keywords.search(word) or is_mixed_word(word):
            new_words.append(Fore.RED + word + Style.RESET_ALL)
        else:
            new_words.append(word)
    return ' '.join(new_words)

def highlight_issues_html(text):
    words = text.split()
    new_words = []
    for word in words:
        if word in EXCEPTION_WORDS:
            new_words.append(word)
        elif strange_pattern.search(word) or keywords.search(word) or is_mixed_word(word):
            new_words.append(f'<span style="color:red;">{word}</span>')
        else:
            new_words.append(word)
    return ' '.join(new_words)

def scan_docx_file(path):
    issues_by_section = defaultdict(list)
    doc = Document(path)
    current_section = "–"
    for para in doc.paragraphs:
        if para.style.name == 'Heading 1':
            current_section = para.text.strip()
        text = para.text.strip()
        if not text or re.search(r'(https?://|www\.|linkedin\.com|github\.com)', text):
            continue
        words = text.split()
        if (
            any(w not in EXCEPTION_WORDS and strange_pattern.search(w) for w in words) or
            keywords.search(text) or
            any(is_mixed_word(w) for w in words)
        ):
            issues_by_section[current_section].append((
                text,
                highlight_issues_terminal(text),
                highlight_issues_html(text),
                is_arabic(text)
            ))
    return issues_by_section

def prepare_result_folder():
    os.makedirs("Result", exist_ok=True)
    txt_files = sorted([f for f in os.listdir("Result") if f.endswith(".txt") and not f.startswith("MainResult")])
    html_files = sorted([f for f in os.listdir("Result") if f.endswith(".html") and not f.startswith("MainResult")])
    for file_list in [txt_files, html_files]:
        while len(file_list) > 9:
            os.remove(os.path.join("Result", file_list.pop(0)))

def save_reports(results, timestamp):
    txt_path = os.path.join("Result", f"report_{timestamp}.txt")
    html_path = os.path.join("Result", f"report_{timestamp}.html")
    main_html_path = os.path.join("Result", "MainResult.html")

    html_head = '''<html><head><meta charset="UTF-8">
    <style>
    body{font-family:Arial;background:#111;color:#eee;padding:20px}
    .file{margin:20px 0;padding:15px;border:1px solid #444;background:#1a1a1a;border-radius:8px}
    .section{color:#0af;font-size:16px;margin-top:10px;}
    .problem{color:#eee;margin-left:20px;}
    </style></head><body>\n'''
    html_content = []

    with open(txt_path, "w", encoding="utf-8") as txt:
        for filename, full_path, folder, issues in results:
            txt.write("="*60 + "\n")
            txt.write(f"📄 File: {filename}\n")
            txt.write("="*60 + "\n")
            txt.write(f"📍 Path: {full_path}\n")
            txt.write(f"📁 Folder: {folder}\n")

            file_html = [f'<div class="file"><h3>📄 {filename}</h3><p><b>📍 Path:</b> {full_path}</p><p><b>📁 Folder:</b> {folder}</p>\n']
            arabic_lines = 0
            total_lines = 0

            for section, lines in issues.items():
                file_html.append(f'<div class="section">🔸 Section: {section}</div>\n')
                txt.write(f"\n🔸 Section: {section}\n" + "-"*45 + "\n")
                for original, highlighted_terminal, highlighted_html, is_arab in lines:
                    txt.write("❗ Problem Line:\n   → " + highlighted_terminal + "\n")
                    dir_attr = ' dir="rtl"' if is_arab else ''
                    file_html.append(f'<div class="problem"{dir_attr}>❗ {highlighted_html}</div>\n')
                    total_lines += 1
                    if is_arab:
                        arabic_lines += 1

            file_html.append('</div>\n')
            html_content.append(''.join(file_html))

    html_final = html_head + ''.join(html_content) + f'<p style="color:#888;">Report created: {timestamp}</p>\n</body></html>'
    with open(html_path, "w", encoding="utf-8") as html, open(main_html_path, "w", encoding="utf-8") as main_html:
        html.write(html_final)
        main_html.write(html_final)

def walk_and_scan_directory(root):
    excluded_files, excluded_dirs = load_exclusions()
    result_data = []
    for dirpath, _, filenames in os.walk(root):
        if any(ex in dirpath.lower() for ex in excluded_dirs.union({"~temp", "my env"})):
            continue
        for filename in filenames:
            lower_name = filename.lower()
            if (
                not lower_name.endswith(".docx") or
                lower_name.startswith("~$") or
                lower_name in excluded_files
            ):
                continue
            full_path = os.path.join(dirpath, filename)
            relative_folder = os.path.relpath(dirpath, root)
            issues = scan_docx_file(full_path)
            if issues:
                print(Fore.CYAN + Style.BRIGHT + "\n" + "="*60)
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"📄 File: {filename}")
                print(Fore.CYAN + Style.BRIGHT + "="*60)
                print(Fore.YELLOW + f"📍 Path: {full_path}")
                print(Fore.LIGHTMAGENTA_EX + f"📁 Folder: {relative_folder}")
                for section, lines in issues.items():
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + f"\n🔸 Section: {section}")
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "-"*45)
                    for _, highlighted, _, _ in lines:
                        print(Fore.LIGHTRED_EX + "❗ Problem Line:")
                        print(Fore.WHITE + "   → " + highlighted)
                result_data.append((filename, full_path, relative_folder, issues))
    prepare_result_folder()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_reports(result_data, timestamp)
    print(Style.BRIGHT + Fore.GREEN + '\n✅ Scan complete. Press Enter to rescan or Ctrl+C to exit.')

def select_path():
    print(Fore.YELLOW + "Choose path input method:")
    print(Fore.YELLOW + "1) Manual input")
    print(Fore.YELLOW + "2) Read from Main_Path.txt")
    choice = input("Your choice [1/2]: ").strip()
    if choice == '1':
        return input("Enter full folder path: ").strip()
    elif choice == '2':
        try:
            with open('Main_Path.txt', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(Fore.RED + "Main_Path.txt not found.")
            sys.exit(1)
    else:
        print(Fore.RED + "Invalid choice. Try again.\n")
        return select_path()

def main():
    path = select_path()
    print(Fore.BLUE + f'\n🚀 Scanning started in: {path}')
    try:
        while True:
            walk_and_scan_directory(path)
            input(Fore.YELLOW + "\n↩️ Press Enter to rescan...")
    except KeyboardInterrupt:
        print(Fore.GREEN + "\n👋 Exiting.")
        sys.exit()
       
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {e}")
        input(Fore.YELLOW + "\n↩️ Press Enter to exit...")

if __name__ == "__main__":
    main()

