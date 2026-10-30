# Multi-Agent AI Fact-Checking System

A multi-agent AI application that investigates factual claims through an adversarial debate workflow. Built using **Python, LangGraph, and Google Gemini**, the system uses specialized AI agents to gather supporting and contradicting evidence before generating a final verdict.

The project explores how multi-agent collaboration, web search integration, and structured LLM reasoning can support a more transparent fact-checking process.

### Live Demo

🌐 **[Try the Application](https://multi-agent-debate-fact-checker-vnmicvsdui8f3zdn8a5pce.streamlit.app/)**

## How It Works

The system follows a structured multi-agent workflow:

1. **Claim Parser Agent** – Extracts the main verifiable claim from user input.
2. **Defense Agent** – Searches the web for evidence supporting the claim.
3. **Prosecutor Agent** – Independently searches for evidence challenging the claim.
4. **Judge Agent** – Evaluates both agents' findings and generates a final verdict with an explanation, confidence score, and relevant sources.

The Defense and Prosecutor agents execute in parallel using LangGraph. If the Judge returns an uncertain verdict, the workflow can retry the investigation once.

### Workflow Architecture

```text
                   User Input
                       |
                       v
                Claim Parser
                       |
              +--------+--------+
              |                 |
              v                 v
         Defense Agent    Prosecutor Agent
              |                 |
         Web Search         Web Search
              |                 |
              +--------+--------+
                       |
                       v
                  Judge Agent
                       |
              +--------+--------+
              |                 |
           Verdict          Uncertain
              |                 |
              v                 v
          Final Result     Retry Investigation
                                |
                                v
                           Final Result
```

## Key Features

- **Multi-Agent Investigation:** Separate agents investigate supporting and contradicting evidence.
- **Parallel Execution:** LangGraph coordinates simultaneous agent execution.
- **Web Search Integration:** Agents retrieve relevant information using DuckDuckGo Search.
- **Structured Verdicts:** True, False, or Uncertain, with explanations and confidence scores.
- **Evidence Transparency:** Displays relevant sources and agent findings.
- **Conditional Retry:** Supports an additional investigation attempt for uncertain verdicts.
- **LangSmith Observability:** Traces agent execution, LLM calls, and workflow performance.
- **Interactive Interface:** Streamlit application for submitting claims and reviewing results.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Google Gemini API | LLM reasoning and structured responses |
| LangGraph | Multi-agent workflow orchestration |
| LangSmith | Tracing and observability |
| DuckDuckGo Search | Web evidence retrieval |
| Pydantic | Structured output validation |
| Streamlit | Web application interface |

## Project Structure

```text
MultiAgentDebateCheck_LangGraph/
├── src/
│   ├── claim_parser.py
│   ├── debate_agents.py
│   ├── judge_agent.py
│   ├── search_tool.py
│   └── langgraph_fact_checker.py
├── app.py
├── requirements.txt
└── .gitignore
```

## Example

**Input Claim:**

> Penguins can fly.

**Expected Verdict:** False

The Defense and Prosecutor agents investigate the claim from opposing perspectives. The Judge evaluates their findings and returns a structured verdict with an explanation and relevant sources.

Actual results may vary depending on the retrieved evidence and model responses.

## Limitations and Future Improvements

- Web evidence is primarily retrieved from search-result snippets rather than full webpage content.
- The Judge relies on LLM-based evidence evaluation rather than a deterministic source-reliability scoring algorithm.
- Confidence scores are model-generated and are not statistically calibrated.
- Verdict accuracy has not yet been established through a formal benchmark evaluation.

## Learning Outcomes

Through this project, I gained practical experience in:

- Designing and coordinating multiple AI agents
- Building parallel workflows with LangGraph
- Integrating LLMs with external search tools
- Generating structured outputs using Pydantic
- Monitoring agent workflows using LangSmith
- Deploying an interactive AI application with Streamlit
---
