# README for the AI Conversational Health Analytics Project

/Introduction/
The project described here involves the development of a prototype conversational agent that enables users to explore health data from connected devices using natural language, without ever making a diagnosis or providing medical advice.

This project was carried out as part of a work placement. It combines data analysis, rigorous validation of interactions with the language model, and a conversational interface connected to a local LLM via Ollama. Following the steps below will help you set up the environment, run the project and understand how it works.

/Setting everything up/
Step 1: Software to download before starting the project

- Python 3.10 or later
- Visual Studio Code, or any coding environment of your choice
- The following Python libraries: LangGraph, pydantic, pandas, numpy, matplotlib, streamlit, openai, pytest
- To download the libraries, use the following command in the terminal: ‘pip install langgraph pydantic pandas numpy matplotlib streamlit openai pytest’

Step 2: Download the project files from this repository 
- "Clone this repository, or download it as a ZIP and extract it:" #A voir comment je le rends

Step 3: Connect to the language model (Ollama)
- If you are not connected to the LifeSTech wifi you need to use a VPN following the instructions in the link "(https://pages.lst.tfo.upm.es/it/services/lst/vpn/)"
- If you are connected to the LifeSTech wifi, you can run the project directly

Step 4 : Run the project

- Open the terminal and navigate to the project directory
- Run the following command to : 'streamlit run app.py' it will open a webpage with the AI assistant
- You can now chat with the AI assistant and ask it questions about health data
- If wanted, it is also possible to run the project in the terminal using the command 'python main.py'
 

/How It Works/
The user asks a question in plain language. The language model decides which tool(s), among 18 available, it needs to call to answer each tool queries the real data of a given participant. The final answer is always built from the tools' actual results, never invented.

Here is a scheme of the process:

User question
      │
      ▼
┌───────────────┐      ┌───────────────────────────┐
│ assistant.py   │─────▶│ 18 tools (tools/)           │
│ (LLM + loop)   │      │ validated in/out by pydantic│
└───────────────┘      └───────────────────────────┘
      │                              │
      ▼                              ▼
 Final answer            Analysis functions (pandas)
                          steps.py, sleep.py, heart_rate.py,
                          activity.py, wellness.py, injury.py,
                          srpe.py, analytics.py, correlations.py,
                          charts.py, reporting.py
                                      │
                                      ▼
                                PMData (JSON/CSV files)

Each tool's input and output are validated with pydantic (tools/base.py, tools/outputs.py, tools/definitions.py) before being registered in tools/registry.py, which both assistant.py and the test suite rely on.

/Project Structure/

├── PMData/                  # dataset (not versioned)
├── config.py                # configuration (paths, model, Ollama endpoint)
├── loader.py                # PMData file loading
├── steps.py, sleep.py, heart_rate.py, activity.py,
│   wellness.py, injury.py, srpe.py                # per-domain analysis
├── analytics.py              # comparisons, trends, recommendations
├── correlations.py           # correlations between metrics
├── charts.py                 # chart generation
├── reporting.py               # reports combining several domains
├── tools/                    # pydantic schemas + the 18-tool registry
│   ├── base.py
│   ├── outputs.py
│   ├── definitions.py
│   └── registry.py
├── prompts.py                 # assistant's system prompt
├── assistant.py                # HealthAssistant class (LLM + tools)
├── main.py                     # command-line interface
└── app.py                      # Streamlit interface

/Design choices/
Four decisions were deliberately left open and settled during the project:
- Dataset: PMData, chosen for being small and clean, over the richer but heavier LifeSnaps.
- Model: local, via Ollama (gpt-oss:20b), rather than a proprietary API, as a trade-off between the confidentiality of health data and tool-calling quality (gpt-oss being specifically trained for tool use).
- Tool granularity: 18 specific tools rather than a handful of generic ones, chosen from a 30 questions golden dataset rather than arbitrarily.
- What "correct" means: for single-answer questions (a number, a comparison), the reference is the direct pandas computation. For open-ended questions (correlations, advice), "correct" means an answer faithful to the tools actually called, without overreaching causal language ("causes" instead of "is associated with") and without invented numbers.


/Know limitations of the project/
- Single tool round-trip per question. The assistant can call one or several tools at once, but cannot make a second tool call that depends on the result of the first. A question requiring sequential, multi-step reasoning won't be fully handled.
- No dedicated routing step. Unlike an architecture with upfront classification (out-of-scope / general knowledge / data query), the assistant relies on the system prompt to refuse out-of-scope questions (diet, alcohol, hydration) rather than on a guaranteed deterministic rule.
- get_most_active_day and get_highest_calorie_day look across a participant's entire history, not a specific period ("this week"), so a question phrased that way is answered over all available data instead.
- Participants with no data at all: a few aggregation functions (get_average_wake_up_time, get_most_active_day, get_highest_calorie_day) don't handle a completely empty participant gracefully (not encountered with PMData's 16 real participants, but worth keeping in mind).
