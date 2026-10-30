# MarketMind AI — Autonomous Business Research Agent

MarketMind AI is an autonomous business research agent built to generate schema-validated, fully traceable market intelligence briefs for management consultancies (Verity Strategy Partners). It implements a robust, hand-crafted plan-act-observe loop, strict schema validation, deterministic tool dispatching, a 4-way claim-typing evidence store, automated quality control, and a human approval gate.

## Prerequisites & Installation
* Python 3.10+
* Virtual environment recommended.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Copy `.env.example` to `.env` and configure your OpenAI API key:
```bash
cp .env.example .env
```
Ensure your API key is project-scoped with appropriate spend limits.

## Running a Research Run
```bash
python src/main.py --scenario S1 --output-dir runs/run_01
```

## Running Evaluation
```bash
python evaluation/run_eval.py
```
