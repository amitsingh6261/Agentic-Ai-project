# Product Requirements Document (PRD): TopicToWeb Multi-Agent Publisher

This document defines the product vision, feature requirements, user experience, and success criteria for **TopicToWeb**. 

Students should use this document to understand the "Why" and "What" of the application before referencing the technical Software Design Document (SDD) for implementation.

---

## 1. Executive Summary & Product Vision

### The Problem
Publishing high-quality, topic-specific content on the web is a time-consuming, fragmented process. Content creators must research facts, write drafts, design visual themes, write HTML/CSS code, audit pages for bugs, and host the code online. This requires multiple skill sets (researcher, writer, designer, developer, QA tester) and hours of manual coordination.

### The Solution: TopicToWeb
TopicToWeb is an automated **Content OS** that collapses the entire publishing pipeline into a single, browser-based click. 

By inputting a natural language prompt, the user triggers an orchestra of 5 specialized, coordinating AI agents (Researcher, Writer, Designer, Developer, and Reviewer) that collaborate autonomously to output a verified, visually stunning single-file web publication page live in the cloud.

---

## 2. Target Audience & Personas

*   **Content Creators & Journalists:** Want to generate up-to-date, topic-focused newsletters or articles with unique, custom layouts.
*   **Web Publishers & Marketers:** Want to spin up visually distinct, themed landing pages for various topics without waiting for design or engineering cycles.
*   **AI Enthusiasts & Hackathon Builders:** Want a modular blueprint showing how multiple LLM pipelines coordinate, self-correct, and save files.

---

## 3. Core User Experience & User Flow

The application provides a clean, two-panel web dashboard interface:

1.  **Input Phase:** 
    *   The user opens the dashboard in their browser.
    *   The user types a prompt in a sidebar input field (e.g. *“Write an essay about AI. Research before writing.”*).
    *   The user clicks a primary **"Generate Web Publication"** action button.
2.  **Processing Phase:**
    *   The dashboard shows visual loading states (spinners) explaining the current active stage of the multi-agent reasoning chain.
3.  **Completion & Gallery Phase:**
    *   The user immediately views the rendered webpage inside a central browser container card.
    *   The user can expand a side drawer to view and copy the raw compiled source HTML code.
    *   The sidebar displays a history panel ("Published Gallery") showing all previously created publications for instant reloading.

---

## 4. Functional Requirements

To fulfill the product vision, the system must deliver the following functional modules:

### FR-1: Security Input Shield
*   **Description:** The system must inspect user inputs before starting the agent pipeline to prevent prompt injection or script exploit attempts.
*   **Behavior:** Check for blocked terms (e.g. "hack", "bypass"). If flagged, terminate the pipeline immediately and display a clean error message to the user.

### FR-2: Topic Refinement Stage
*   **Description:** The system must separate instructions or meta-prompts (e.g. "research before writing") from the core essay subject. It must extract a clean, concise title string to be used for the file slug and search queries.
*   **Behavior:** Send the raw user prompt to a fast LLM request turn. The model must extract a clean, 3-6 word subject title and ignore secondary instructions. Use this refined topic to title the page, pass to agents, and format the output file name slug.

### FR-3: Live Context Research
*   **Description:** The system must retrieve up-to-date facts from the web to ensure the generated publication is factual and timely.
*   **Behavior:** The Researcher Agent must call a web search API, retrieve summaries, filter them, and truncate the output to prevent exceeding LLM context limits. If the search returns empty, fallback to the refined topic query.

### FR-4: Content Generation (Synthesis)
*   **Description:** The system must organize the search notes into a structured, engaging, and professional article draft.
*   **Behavior:** The Writer Agent must output clean Markdown formatting containing an H1 title, a brief introduction, at least two H2 subheadings, and a concluding reflection.

### FR-5: Brand Style Generation
*   **Description:** The system must choose a custom visual palette and layout typography that matches the emotional tone of the generated essay.
*   **Behavior:** The Designer Agent must output a structured configuration dictionary (JSON) defining background colors, text colors, heading/body font faces, and accent colors.

### FR-6: Front-End HTML Compilation
*   **Description:** The system must merge the Markdown essay and the JSON style properties into a single-file webpage code block.
*   **Behavior:** The Developer Agent must output valid HTML/CSS including imports for Google Fonts, CSS variable styling blocks, and semantic HTML body elements. It must wrap the essay in a premium, glassmorphic layout card with curved corners, drop shadows, and visual accent highlights.

### FR-7: Automated Quality Assurance (QA Audit)
*   **Description:** The system must verify the compiled code for layout and syntax bugs before writing files to the disk.
*   **Behavior:** The Reviewer Agent must audit the code. If bugs exist (e.g. missing tags), it must return a failure instruction list, triggering the Developer Agent to edit and repair the code (up to 3 compile attempts). If correct, it must return a PASS.

### FR-8: File Persistence & Gallery History
*   **Description:** The system must write the successfully compiled webpage to a local directory and track all previously created publication pages.
*   **Behavior:** Save completed pages as `.html` files inside a designated essays output folder. Show a clickable history list of these files on the dashboard sidebar.

### FR-9: Live Agent Execution Logs (Transparency Panel)
*   **Description:** The system must display a real-time status log showing exactly what the agents are doing behind the scenes.
*   **Behavior:** Render a collapsible execution logs window in the UI. Print logs when:
    *   Sending requests to the OpenRouter LLM (waiting states).
    *   Receiving plain text contents vs tool calling requests.
    *   Executing local web search scripts.
    *   Encountering errors or triggering compile retries.

---

## 5. Non-Functional Requirements (NFRs)

*   **Security (Path Protection):** The file-writing system must enforce path isolation. It must be impossible for the LLM to write or edit files outside the designated output directory (preventing directory traversal attacks).
*   **Performance (Rate-Limit Staggering):** To run on free API tiers, the orchestrator loop must implement minor delay pauses (sleep buffers) between sequential agent API calls to prevent HTTP 429 rate limit locks.
*   **Stability (JSON Fallbacks):** If the Designer Agent returns malformed JSON, the orchestrator must intercept the error and load a safe default color scheme to prevent the pipeline from crashing.
*   **Deployability (Zero Config Cloud Hosting):** The application must run locally and in the cloud (Streamlit Cloud) from the same codebase without modification. It must support environment secrets decoupling (reading API keys from local `.env` files or secure cloud secrets managers).
*   **License & Portability:** The software must use standard Python libraries (`urllib`) and the open-source Streamlit library to keep the codebase lightweight and easy for students to clone and run.
