# ResumeTextValidator

**ResumeTextValidator** is an intelligent analyzer for `.docx` resume files. It detects text issues such as invalid symbols, unprofessional placeholder phrases, and mixed Arabic-English content within a single word.

It supports both Arabic and English and generates professional reports.

---

## ✨ Features

* ✅ **Smart Text Analysis:** Detects words with invalid symbols or mixed-language characters.
* 🌐 **RTL/LTR Direction Detection:** Automatically adjusts paragraph direction in HTML reports based on content language.
* 🔍 **Precise Highlighting:** Only problematic words or characters are marked—not full lines.
* 🧠 **Smart Banned Keywords List:** Flags entries like `Not Specified`, `N/A`, `غير مذكور`, and more.
* 📑 **Multiple Reports:** Clean dark-themed HTML and organized text reports with the latest 10 kept.
* 🚫 **File/Folder Skipping:** Supports exclusion via `Ex.txt`.
* 🌍 **Supports full Unicode including common punctuation (Arabic and English).**

---

## ⚙️ Requirements

```bash
pip install -r requirements.txt
```

#### `requirements.txt` content:

```txt
docx
colorama
```

---

## 🚀 How to Use

### Option 1: Manual Path Entry

```bash
python main.py
```

Then select option `1` and provide the folder path containing `.docx` files.

### Option 2: Use `Main_Path.txt`

* Create a file named `Main_Path.txt`
* Paste the full path inside:

```txt
C:\Users\YourName\Documents\Resumes
```

Then run the script and select option `2`.

---

## 📂 Output Structure

All scan results are saved in the `Result/` directory:

```
Result/
├─ report_YYYY-MM-DD_HH-MM-SS.txt     # Plain text report
├─ report_YYYY-MM-DD_HH-MM-SS.html    # Dark-themed HTML report
└─ MainResult.html                    # Always holds the latest output
```

Each report includes:

* 📄 File name
* 📍 Full path
* 📁 Folder name
* 🔸 Section headers from the resume
* ❗ Problematic lines, with only the suspicious content highlighted

---

## 🔒 Exclusions

### To exclude files/folders:

* Create an `Ex.txt` file
* List:

  * Any `.docx` filenames to ignore
  * Folder names to skip

Example:

```txt
bad_resume.docx
Old_Resumes
```

---

## 🧠 Sample Banned Keywords:

* `Not Specified`, `Not Disclosed`, `TBC`, `N/A`, `Yet to Be Determined`
* `غير مذكور`, `غير متوفر`, `لم يُذكر`, `لا ينطبق`

## ✒️ Allowed Symbols:

* Basic punctuation: `.,:;!?-+@|()[]%`
* Regular and zero-width spaces
* Arabic dash variants: `–`, `—`, `‑`

## ✅ Whitelisted Words:

* `Café`, `café`

---

## 📦 Sample Output

```bash
📄 File: AhmedCV.docx
📍 Path: C:\Resumes\AhmedCV.docx
📁 Folder: Resumes
🔸 Section: Objective
❗ Problem Line:
   → I am a <span style="color:red;">Café</span> developer who...
```

---

## 📌 Important Notes

* Skips MS Word temp files starting with `~$`
* If the script exits immediately in GUI mode, ensure this line is at the end:

```python
if __name__ == "__main__":
    main()
```

---

## 📄 License

MIT License

---

