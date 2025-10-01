# Quickstart — Neon Notes

## 1. Setup
```bash
git clone <repo-url>
cd neon-notes
python3 -m venv .venv && source .venv/bin/activate
pip install -r tools/requirements.txt
```

## 2. Roller & Dokument
- **Brittan** — supervisor/orchestrator
- **AI-agenter** — Dev/Research/Test
- Läs `docs/ProjectInformation.md`, `docs/BEST_PRACTICES.md`

## 3. Ta en uppgift
```bash
python tools/agent_cli.py list
python tools/agent_cli.py start "Task title" --agent "Your Agent" --notes "Startar"
```

## 4. Uppdatera & Avsluta
```bash
python tools/agent_cli.py update "Task title" --agent "Your Agent" --notes "Gjort X"
python tools/agent_cli.py finish "Task title" --agent "Your Agent" --status "REVIEW" --notes "PR #id"
```

## 5. Notices
Läs `docs/ProjectInformation.md` och ack:a:
```bash
python tools/agent_cli.py ack NOTICE-YYYY-MM-DD --agent "Your Agent" --notes "ACK"
```

## 6. Orchestrator
```bash
AGENT="Brittan" bash scripts/brittan.sh
```
