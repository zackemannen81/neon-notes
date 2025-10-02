# Project Overview — Neon Notes

## Vision
Snabb, minimal anteckningsapp där du kan skriva/ladda upp text och få en 1-klicks AI-sammanfattning (TL;DR + highlights).

## Slutmål (MVP)
- Lista + editor för anteckningar
- Filbaserad lagring (JSON)
- Knapp “Summarize” → mockad agent som svarar med TL;DR + 3 highlights
- CI-checks och tydlig agentprocess (journal, notices, ACK)

## Systemkarta & Komponenter
- **Frontend (HTML/TS eller enkel React senare):**
  - Vy: lista av anteckningar, editorpanel, “Summarize”-knapp
  - Tillgänglighet: tabb-ordning, labels, aria-live för svar
- **FileStore (JSON):** `data/notes.json`
  - Schema `Note`:
    ```json
    {
      "id": "uuid",
      "title": "string",
      "body": "string",
      "createdAt": "ISO-8601",
      "updatedAt": "ISO-8601",
      "summary": { "tldr": "string", "highlights": ["string"] }
    }
    ```
- **SummarizeAgent (mock v1):**
  - **Input:** `{ "body": string }`
  - **Output:** `{ "tldr": string, "highlights": string[] }`
  - Implementation: ren JS-funktion (ingen nätverkskall i MVP)
- **Orchestrator:** `scripts/brittan.sh` (auto-ACK notices, valfri auto-assign)
- **Agent-CLI:** `tools/agent_cli.py` (list/start/update/finish/ack)
- **Dokumentation:** `/docs` (Overview, Roadmap, DevPlan, Quickstart, Best Practices)
- **CI/CD:** `.github/workflows/` (validerar tasks/journal/notices)

## Användarflöde (MVP)
1. Skapa/öppna anteckning → skriv i editor.
2. **Save** uppdaterar `data/notes.json`.
3. **Summarize** kör mock-agent → visar `tldr` + 3 highlights under editorn.
4. Journal uppdateras av respektive agent via CLI.

## Status & Process
- Tillåtna status: `TODO | IN_PROGRESS | REVIEW | DONE | BLOCKED | NEEDS_INFO`
- **Tasks:** enda sanningen i `tasks/ProjectTasks.md`
- **Journal:** append-only i `journal/DeveloperJournal.md`
- **Notices:** `docs/ProjectInformation.md` (ACK krävs för Mandatory)

## Icke-funktionella krav
- Node LTS (20.11), lint/format i CI
- Snabb Undo/Redo där relevant (stretch)
- A11y: tydlig fokusmarkering, tangentbordsstöd
- Prestanda: responsiv UI på låg hårdvara

## Stretch Goals
- Taggar & sök
- Export/Import (Markdown/ZIP)
- PWA/offline
- Riktig LLM-summarizer bakom feature-flag
