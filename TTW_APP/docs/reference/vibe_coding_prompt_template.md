# AI Vibe-Coding Prompt Template

Copy and paste this template when prompting your coding AI (like Cursor, VS Code Copilot, or Claude) to write any module in the curriculum. 

Fill in the brackets `[...]` by copying the specific parameters and requirements from the corresponding file specifications inside the **Software Design Document (SDD)**.

---

## 💡 Pro-Tip: Setup "Rules for AI" (Global Configuration)

Instead of copy-pasting the commenting and imports rules for every single file, you can configure it globally in your coding editor!

*   **In VS Code (GitHub Copilot):** 
    1. Create a file named `.github/copilot-instructions.md` in the root of your project workspace folder.
    2. Paste these global rules into that file:
        ```markdown
        # Coding Guidelines
        - Always write extremely comprehensive, simple comments for LITERALLY EVERY SINGLE LINE, method, and function.
        - Explain the purpose of standard Python built-ins or library functions in plain English.
        - Keep comments simple enough for a non-technical 10-year-old child to understand.
        - When importing from sibling packages, always append parent folders to sys.path at the top:
          sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ```
    Copilot will automatically read this file and apply these guidelines to every generation query!
*   **In other LLM Chat windows (Claude, ChatGPT):** Pin the rules text above as a "Custom Instruction" or "System Instruction" in your chat configuration settings.

Once configured, the editor will automatically apply these comments and import rules to every file you generate, so you only need to prompt it with the **Objective** and **Logic** from the SDD!

---

## The Master Prompt

```text
Act as an expert Python software engineer and technical educator.
Write the script for the file: [file_path]
conforming exactly to the following specifications:

=== OBJECTIVE ===
[Copy Paste file objective from SDD]

=== INTER-FILE IMPORTS & DEPENDENCIES ===
[Copy Paste list of dependencies from SDD for this file]

=== LOGIC & CODING REQUIREMENTS ===
[Copy Paste file logic from SDD]

=== FILE-SPECIFIC METADATA & CONSTRAINTS ===
[Paste any extra details from the SDD (e.g., API URLs, JSON schemas, visual theme styles, parameter inputs) if applicable. Otherwise, write "None".]

=== PATH RESOLUTION RULES ===
Remember that the project structure uses python packages. If importing sibling folders, use full absolute references (e.g. from sprint_2.lesson_2_2 import write_file) and ensure you append parent folder directories to sys.path at the beginning of the script:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

=== COMMENTING & DOCUMENTATION REQUIREMENT (CRITICAL) ===
The code itself MUST serve as the learning guide. Write extremely comprehensive, simple comments for:
1. LITERALLY EVERY SINGLE LINE, METHOD, AND FUNCTION.
2. Explain the purpose of every standard Python built-in feature, package import, and library method used (e.g. explain what urllib.request.Request, json.dumps, time.sleep, dict.get, or super().__init__() actually do).
3. The tone of the comments must be so clear, simple, and detailed that a complete non-technical 10-year-old child with no programming experience can read the code and understand exactly what is happening in every line.

Double-check syntax, handle exceptions gracefully, and ensure there are no unreferenced variables. Output ONLY the clean code block.
```
