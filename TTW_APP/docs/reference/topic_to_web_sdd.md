# Software Design Document (SDD): TopicToWeb Multi-Agent Pipeline

This document serves as the master architectural specification for the **TopicToWeb** system. 

Students should use this document to prompt their Coding AI tools to generate the necessary directory layouts, python modules, and Streamlit configurations.

---

## 1. System Architecture & Data Flow

The TopicToWeb system takes a raw user-input topic, runs it through an orchestration layer of 5 specialized AI agents, and produces a verified, beautifully styled single-file HTML/CSS web publication page.

```text
                                  [ User Input Prompt ]
                                           │
                                           ▼
                                 [ Input Security Shield ]
                                           │
                                           ▼
                                 [ Topic Refinement Stage ] ──► (Generates clean title & slug)
                                           │
                                           ▼
                     +─────────────────────────────────────────────+
                     |             Orchestrator State              |
                     +─────────────────────────────────────────────+
                                           │
                                           ▼
 +───────────────────────────────────────────────────────────────────────────────────+
 |                                Multi-Agent Stages                                 |
 |                                                                                   |
 |  Stage 1: Researcher Agent  ──► Calls 'web_search' tool ──► Context notes        |
 |                                                                                   |
 |  Stage 2: Writer Agent      ──► Synthesizes notes        ──► Essay Markdown       |
 |                                                                                   |
 |  Stage 3: Designer Agent    ──► Analyzes sentiment       ──► Style JSON blueprint |
 |                                                                                   |
 |  Stage 4: Developer Agent   ──► Compiles layout          ──► HTML string code     |
 |                                                                                   |
 |  Stage 5: Reviewer Agent    ──► Audits layout code       ──► PASS / FAIL report   |
 |                                                                                   |
 |  *Self-Correction: If Reviewer reports FAIL, Developer compiles edits using log.   |
 +───────────────────────────────────────────────────────────────────────────────────+
                                           │
                                           ▼
                              [ Save to output/essays/ ]
                                           │
                                           ▼
                            [ Render in Streamlit Iframe ]
```

---

## 2. Directory Structure Blueprint

Ensure your local project directory is structured exactly as follows:

```text
topic-to-web/
│
├── .env                       # API Credentials (OPENROUTER_API_KEY, TAVILY_API_KEY)
├── .gitignore                 # Tells git which files to ignore (.venv, .env, __pycache__)
├── requirements.txt           # Cloud package dependencies (streamlit, python-dotenv)
├── app.py                     # Streamlit Web UI Dashboard (Entrypoint)
│
├── output/
│   └── essays/                # Target directory where final compiled HTML pages are saved
│
├── sprint_1/                  # Foundations: Direct API & Conversation Memory
│   ├── lesson_1_1_first_call.py
│   ├── lesson_1_2_interactive.py
│   ├── lesson_1_3_memory.py
│   └── lesson_1_4_system.py
│
├── sprint_2/                  # Core Capabilities & Guardrails
│   ├── lesson_2_1_web_search.py
│   ├── lesson_2_2_file_io.py
│   ├── lesson_2_3_guardrails.py
│   └── lesson_2_4_json_validation.py
│
├── sprint_3/                  # Tool Calling & Agentic Loops
│   ├── lesson_3_1_schemas.py
│   ├── lesson_3_2_tool_parsing.py
│   └── lesson_3_3_single_agent.py
│
└── sprint_4/                  # Object-Oriented Multi-Agent Pipeline
    ├── lesson_4_1_base_agent.py
    ├── lesson_4_2_researcher.py
    ├── lesson_4_3_writer.py
    ├── lesson_4_4_designer.py
    ├── lesson_4_5_developer.py
    ├── lesson_4_6_reviewer.py
    └── lesson_4_7_orchestrator.py
```

---

## 3. File-by-File Specifications & Dependency Cross-References

Each lesson block is listed below with its technical requirements, parameters, output formats, and **cross-reference dependencies** (imports).

---

### Foundations: Sprint 1

#### `sprint_1/lesson_1_1_first_call.py`
*   **Objective:** Make a direct HTTP POST request to the OpenRouter API without using any external SDK wrappers.
*   **API Target:** `https://openrouter.ai/api/v1/chat/completions`
*   **Headers:** Requires `Authorization: Bearer <API_KEY>` and `Content-Type: application/json`.
*   **Payload Structure:** Standard JSON containing `"model"` (use `poolside/laguna-m.1:free`) and `"messages"` list containing `{"role": "user", "content": "..."}`.
*   **Logic:** Use Python's built-in `urllib.request` library to execute the call. Load the API key from a `.env` file using `os.getenv()`. Parse the JSON response and print the text content.
*   **Dependencies / Cross-References:** 
    *   Imports: None.
    *   Used By: Reference model for connection code.

#### `sprint_1/lesson_1_2_interactive.py`
*   **Objective:** Wrap the API connection from Lesson 1.1 inside a continuous interactive console chat loop.
*   **Logic:** Implement a `while True` loop that prompts the user for input. If the user types `"exit"` or `"quit"`, break the loop. Otherwise, send the user's input to the OpenRouter API and print the model's response.
*   **Dependencies / Cross-References:**
    *   Imports: None (duplicates and refactors the request logic from `lesson_1_1.py` into a console loop).
    *   Used By: None.

#### `sprint_1/lesson_1_3_memory.py`
*   **Objective:** Introduce persistent conversation history so the chatbot can remember previous inputs.
*   **Memory Structure:** Maintain a local python list: `messages = []`.
*   **Logic:** Before making the API call, append the user input to the list: `{"role": "user", "content": user_input}`. Pass the entire list inside the API payload's `"messages"` key. When the API returns a response, append the assistant response: `{"role": "assistant", "content": response_text}` to the list.
*   **Dependencies / Cross-References:**
    *   Imports: None (refactors `lesson_1_2.py` loop to add local array state).
    *   Used By: Base blueprint for agent memory.

#### `sprint_1/lesson_1_4_system.py`
*   **Objective:** Implement system instructions to dictate the persona and constraints of the LLM.
*   **Logic:** Prepend a system prompt message block `{"role": "system", "content": "System persona instructions..."}` at the absolute beginning (index 0) of the `"messages"` list before sending payloads to OpenRouter.
*   **Dependencies / Cross-References:**
    *   Imports: None.
    *   Used By: Base blueprint for system instructions.

---

### Core Capabilities & Guardrails: Sprint 2

#### `sprint_2/lesson_2_1_web_search.py`
*   **Objective:** Build a Python helper utility to retrieve live web results using Tavily or Serper API services.
*   **Parameters:** Accepts `query: str` and `max_results: int` (default `3`).
*   **Logic:** Execute an HTTP POST to `https://api.tavily.com/search` sending `query` and `max_results` in the payload. Include `api_key` in the header or payload body. Return a structured text summary string containing search results, titles, and URLs.
*   **Dependencies / Cross-References:**
    *   Imports: None (utility file).
    *   Used By: Imported by `sprint_3/lesson_3_3_single_agent.py` and `sprint_4/lesson_4_7_orchestrator.py` to run search queries.

#### `sprint_2/lesson_2_2_file_io.py`
*   **Objective:** Create a file-writing helper function that prevents path escape attacks.
*   **Parameters:** Accepts `file_path: str` and `content: str`.
*   **Security Guardrail:** Ensure that the target file path is restricted to write *only* inside the `output/` directory. Resolve absolute paths using `os.path.abspath`. If the resolved path does not start with the directory prefix of `output/`, raise a `ValueError` indicating a security violation.
*   **Logic:** Write the string contents to disk if paths are cleared.
*   **Dependencies / Cross-References:**
    *   Imports: None (utility file).
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py` to write HTML pages safely.

#### `sprint_2/lesson_2_3_guardrails.py`
*   **Objective:** Create input and output protection filters.
*   **Functions:**
    1.  `input_shield(text)`: Checks if the input contains blocked words (case-insensitive check for terms like "hack", "bypass", "exploit"). If found, raises a `ValueError`.
    2.  `truncate_text(text, max_chars)`: Slices long text blocks (e.g. web search outputs) to a specific character limit (default `2500` characters) to keep API payloads within safe token context window boundaries.
*   **Dependencies / Cross-References:**
    *   Imports: None (utility file).
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py` to filter user queries and truncate search data.

#### `sprint_2/lesson_2_4_json_validation.py`
*   **Objective:** Create a validator to parse JSON strings and enforce exact schema validation.
*   **Schema Requirements:** The parsed JSON dictionary must contain the following keys exactly:
    *   `"detected_sentiment"`
    *   `"theme"` (which must contain `"background_color"`, `"primary_text"`, `"accent_color"`, `"font_family_heading"`, `"font_family_body"`)
    *   `"layout_style"`
*   **Logic:** Use `json.loads` to deserialize the string. Perform validation. Collect all missing keys into an error list. If any missing keys exist, raise a `ValueError` listing all missing elements. If successful, return the parsed dictionary.
*   **Dependencies / Cross-References:**
    *   Imports: None (utility file).
    *   Used By: Imported by `sprint_4/lesson_4_4_designer.py` and `sprint_4/lesson_4_7_orchestrator.py` to validate layout specifications.

---

### Tool Calling & Single Agentic Loops: Sprint 3

#### `sprint_3/lesson_3_1_schemas.py`
*   **Objective:** Define the JSON Schema declaration configurations for tools.
*   **Logic:** Create a list `TOOLS = [...]` conforming to OpenRouter's tool schema parameters. Declare a tool named `web_search` with parameters `query` (string) and `max_results` (integer, optional) and list `query` as a required parameter.
*   **Dependencies / Cross-References:**
    *   Imports: None (configuration schema file).
    *   Used By: Imported by `sprint_3/lesson_3_3_single_agent.py` and `sprint_4/lesson_4_2_researcher.py` to declare search tool capabilities to the API.

#### `sprint_3/lesson_3_2_tool_parsing.py`
*   **Objective:** Build a router parser to decode tool calls returned by the LLM.
*   **Logic:** Extract `"tool_calls"` from the choice response block. Parse `"function"` details extracting `"name"` and `"arguments"`. Use `json.loads` to decode argument strings. Route execution to local functions (e.g. calling `web_search()` helper) using argument variables.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_2.lesson_2_1_web_search import web_search`
    *   Used By: Reference logic for tool execution routing.

#### `sprint_3/lesson_3_3_single_agent.py`
*   **Objective:** Build a single-agent autonomous reasoning loop that executes tools and feeds output back to the LLM.
*   **Logic:** Implement a 5-iteration loop. Send prompt to API along with `TOOLS` schemas. 
    *   If assistant returns text content: break loop and print response.
    *   If assistant returns a `tool_calls` request: execute the local tool function, append the tool execution results using role `"tool"` and the `"tool_call_id"` to the messages memory array, and immediately run the next reasoning loop iteration.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_3.lesson_3_1_schemas import TOOLS`, `from sprint_2.lesson_2_1_web_search import web_search`
    *   Used By: None.

---

### Object-Oriented Multi-Agent Pipeline: Sprint 4

#### `sprint_4/lesson_4_1_base_agent.py`
*   **Objective:** Build an object-oriented parent `Agent` class to encapsulate conversation state memory and OpenRouter HTTP completions setup.
*   **Properties & Constructor:**
    *   `__init__(name, system_instruction, tools, model)`: Sets local properties, credentials, and initializes a private `self.messages = []` history list.
    *   `execute(user_prompt)`: Appends user prompt to history, structures payload (prepending system instruction), sends HTTP POST request, updates history, and returns either text response or raw `message_obj` containing `tool_calls` requests.
*   **Dependencies / Cross-References:**
    *   Imports: None (base class).
    *   Used By: Inherited by `lesson_4_2_researcher.py`, `lesson_4_3_writer.py`, `lesson_4_4_designer.py`, `lesson_4_5_developer.py`, and `lesson_4_6_reviewer.py`.

#### `sprint_4/lesson_4_2_researcher.py`
*   **Objective:** Build a specialized `ResearcherAgent` subclass inheriting from the base `Agent`.
*   **Persona:** Expert Research Analyst. System instructions direct it to call the `web_search` tool to gather facts.
*   **Scope:** Set `tools` to only contain the `web_search` tool schema definition.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_4.lesson_4_1_base_agent import Agent`, `from sprint_3.lesson_3_1_schemas import TOOLS`
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py`.

#### `sprint_4/lesson_4_3_writer.py`
*   **Objective:** Build a vibe-coded (no tools) `WriterAgent` subclass inheriting from the base `Agent`.
*   **Persona:** Expert Creative Writer. Instructions dictate reading research notes and writing an essay structured in Markdown (H1 title, H2 subheadings, intro, body, conclusion). Set `tools=None`.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_4.lesson_4_1_base_agent import Agent`
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py`.

#### `sprint_4/lesson_4_4_designer.py`
*   **Objective:** Build a structured-output `DesignerAgent` subclass inheriting from the base `Agent`.
*   **Persona:** Creative UI/UX Designer. Instructions dictate analyzing essay text, determining sentiment, selecting layout themes, and returning ONLY a single valid JSON block matching the schema in `lesson_2_4`.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_4.lesson_4_1_base_agent import Agent`, `from sprint_2.lesson_2_4_json_validation import validate_designer_json`
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py`.

#### `sprint_4/lesson_4_5_developer.py`
*   **Objective:** Build a vibe-coded `DeveloperAgent` subclass inheriting from the base `Agent`.
*   **Persona:** Front-End Web Developer. Instructions dictate reading markdown text and style JSON configuration to compile a single-file, production-ready, beautifully styled HTML page.
*   **Visual Guidelines:** Combine background_color with linear gradients, center the content in a glassmorphic layout card with rounded corners (`border-radius: 16px`), custom padding (`padding: 3rem`), drop shadows, and styled headings with accent underlines.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_4.lesson_4_1_base_agent import Agent`
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py`.

#### `sprint_4/lesson_4_6_reviewer.py`
*   **Objective:** Build a vibe-coded code auditor `ReviewerAgent` subclass inheriting from the base `Agent`.
*   **Persona:** QA Code Auditor. Instructions dictate inspecting compiled HTML pages for tag closing syntax errors, CSS variable compliance, and content verification.
*   **Response Rules:** Return exactly `PASS` if the code compiles cleanly, or return `FAIL` followed by a bulleted list of bugs.
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_4.lesson_4_1_base_agent import Agent`
    *   Used By: Imported by `sprint_4/lesson_4_7_orchestrator.py`.

#### `sprint_4/lesson_4_7_orchestrator.py`
*   **Objective:** Build the central pipeline execution coordinator.
*   **Functions:**
    *   `run_publication_pipeline(prompt, log_callback=None)`: Coordinates the data handoffs and fires `log_callback(log_message)`:
        1. Run `input_shield(prompt)`. Fire log notifications.
        2. Execute Topic Refinement: Send raw prompt payload to OpenRouter to extract a clean 3-6 word alphanumeric title string (the refined topic). Use this refined topic as the filename slug and agent argument context.
        3. Execute `ResearcherAgent` ➔ If tool calls are requested, execute `web_search` locally ➔ Run `truncate_text()` on search summaries. Fire detailed logs showing tools requested vs local execution.
        4. Pass notes to `WriterAgent` ➔ Retrieve Markdown essay. Fire logs.
        5. Pass essay to `DesignerAgent` ➔ Validate style JSON using `validate_designer_json()` (with default theme fallback). Fire logs.
        6. Compile Loop (Run up to 3 times):
           - Pass essay + design to `DeveloperAgent` ➔ Retrieve compiled HTML. Fire status updates.
           - Pass HTML to `ReviewerAgent` ➔ Check response.
           - If `PASS`: break loop.
           - If `FAIL`: append error report to Developer prompt for retry. Fire log explaining compile errors.
        7. Save successfully compiled HTML to `output/essays/` using `write_file`.
*   **Local Test Block:** Implement a `while True` loop to run interactive CLI prompt requests from the terminal (passing a standard print callback to output logs to terminal).
*   **Dependencies / Cross-References:**
    *   Imports: 
        *   `from sprint_2.lesson_2_1_web_search import web_search`
        *   `from sprint_2.lesson_2_2_file_io import write_file`
        *   `from sprint_2.lesson_2_3_guardrails import input_shield, truncate_text`
        *   `from sprint_2.lesson_2_4_json_validation import validate_designer_json`
        *   `from sprint_4.lesson_4_2_researcher import ResearcherAgent`
        *   `from sprint_4.lesson_4_3_writer import WriterAgent`
        *   `from sprint_4.lesson_4_4_designer import DesignerAgent`
        *   `from sprint_4.lesson_4_5_developer import DeveloperAgent`
        *   `from sprint_4.lesson_4_6_reviewer import ReviewerAgent`
    *   Used By: Imported by `app.py` Streamlit entrypoint.

#### `app.py` (Streamlit Dashboard)
*   **Objective:** Build a browser UI dashboard wrapping the pipeline.
*   **Features:**
    1. Sidebar text input box to enter custom topics.
    2. Sidebar "Published Gallery" listing all `.html` files in `output/essays/` as buttons. Clicking a button loads the page immediately from disk.
    3. Main button to trigger `run_publication_pipeline`.
    4. Renders a live `st.status()` execution logs panel showing updates from the orchestrator callback in real-time.
    5. Two-column layout on completion: Left column shows expandable raw HTML code; Right column embeds the rendered page inside a Streamlit sandboxed iframe container (`st.components.v1.html`).
*   **Dependencies / Cross-References:**
    *   Imports: `from sprint_4.lesson_4_7_orchestrator import run_publication_pipeline`
    *   Used By: Application Entrypoint (run by Streamlit).


