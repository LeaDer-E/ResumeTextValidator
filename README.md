# ResumeTextValidator

**ResumeTextValidator** is an advanced document inspection tool designed to validate and analyze `.docx` resume files for formatting, character consistency, and placeholder content. It intelligently detects unusual symbols, unwanted phrases, and mixed Arabic-English text in professional documents.

---

## ✨ Key Features

* 🌐 **Multi-language Support:** Detects mixed Arabic and Latin content in single words.
* ✏️ **Smart Keyword Flagging:** Highlights placeholder phrases like `Not Specified`, `غير مذكور`, `N/A`, etc.
* 🔦 **Highlight Issues:** Only problematic words or characters are highlighted—not the whole sentence.
* ⇄ **RTL/LTR Detection:** Automatically adapts HTML report directionality based on detected language.
* 📃 **Readable Reports:** Generates well-structured terminal output and dark-themed HTML reports.
* 📅 **Auto Cleanup:** Keeps only the latest 10 reports + `MainResult.html` as the latest snapshot.
* 📁 **Path Filtering:** Skips temporary or ignored folders like `~temp`, `my env`, etc.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/LeaDer-E/ResumeTextValidator.git
cd ResumeTextValidator
```

### 2. Setup Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🌐 How to Use

### Option A: Manual Path Input

```bash
python main.py
```

Choose option `1` and enter the path to your resume folder.

### Option B: Use Main\_Path.txt

Create a file named `Main_Path.txt` and paste your folder path inside:

```
C:\Users\yourname\Documents\Resumes
```

Then run the tool and select option `2`.

---

## 📑 Output Overview

All scan results are saved to the `/Result` directory. The structure includes:

```bash
Result/
├─ report_YYYY-MM-DD_HH-MM-SS.txt     # Text report
├─ report_YYYY-MM-DD_HH-MM-SS.html    # HTML report
└─ MainResult.html                    # Always holds the latest result
```

* Reports include:

  * 📄 File name
  * 📍 Full path
  * 📁 Folder name
  * 📈 Section-wise detected issues
  * ⚡ Highlighted problematic words only

---

## 🔍 Keywords & Symbols Filtered

**Common flagged keywords:**

* Not Specified, Not Disclosed, Not Available, TBC, Yet to Be Determined
* غير مذكور, غير متوفر, لم يُذكر, لا ينطبق, etc.

**Allowed symbols:**

* Basic punctuation: `.`, `,`, `:`, `;`, `%`, `@`, `&`, `|`, `-`, `+`, `(`, `)`
* RTL/LTR dashes: `‐`, `‑`, `‒`, `–`, `—`
* Space + Zero-width space `\u200b`

**Explicitly allowed words:**

* `Café`, `cafe`, `Driver’s` (apostrophe handled)

---

## 📊 Example Use Case

```bash
📄 File: example_resume.docx
📍 Path: C:\Documents\Resumes\example_resume.docx
📁 Folder: Resumes
🔸 Section: Summary
❗ "Intermediate proficiency"  ← (contains invisible Unicode space)
```

HTML output auto-switches between RTL and LTR based on paragraph language.

---

## 🚀 Planned Enhancements

* Support for `.pdf` scanning.
* Export issues as CSV.
* Resume text correction suggestions using LLMs.

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

