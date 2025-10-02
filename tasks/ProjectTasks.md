# ProjectTasks

> Canonical task list. Agents may only modify their own `owner/status/notes` fields.

- TASK: Initialize repo
  owner: RICKARD
  status: TODO
  notes: Create initial structure and docs

- TASK: Set up CI checks
  owner: BRITTAN
  status: TODO
  notes: Validate tasks/journal/notices; run tests

- TASK: Build minimal UI skeleton
  owner: OPEN
  status: DONE
  notes: List + editor + “Summarize” knapp (utan riktig AI)
Init layout
[Finish] PR #2
[Finish] Merged
[Finish] PR #2
PR #2 opened
[Finish] Merged
[Finish] Merged PR #2

- TASK: Implement file store (JSON)
  owner: Gemini CLI
  status: REVIEW
  notes: load/save, skapa data/notes.json vid behov
Auto-picked

- TASK: Mock summarize agent
  owner: OPEN
  status: DONE
  notes: returnera TL;DR + 3 highlights (hårdkodat först)
Returnera TL;DR + 3 highlights (mock)
[Finish] Bulk close by Gemini CLI

- TASK: Wire UI → mock agent
  owner: OPEN
  status: TODO
  notes: click handler som visar svar i UI

- TASK: Add basic tests (store + summarize flow)
  owner: OPEN
  status: TODO
  notes: kör i CI senare

- TASK: Delete & Rename notes
  owner: OPEN
  status: TODO
  notes: Delete action + inline rename på title

- TASK: Autosave & Save indicator
  owner: OPEN
  status: TODO
  notes: Autosave var 3s; diskret indikator i header

- TASK: Keyboard navigation & focus rings (a11y)
  owner: OPEN
  status: TODO
  notes: Piltangenter i listan; tabb-ordning; tydlig focus-stil

- TASK: Empty states & error states
  owner: OPEN
  status: TODO
  notes: Visa vänliga tomt-meddelanden; fel-fallback i UI

- TASK: Lint/Format setup (ESLint + Prettier)
  owner: OPEN
  status: TODO
  notes: Kör lokalt + i CI

- TASK: Unit tests — summarizer mock
  owner: OPEN
  status: TODO
  notes: Testa TL;DR truncation och 3 highlights ur text

- TASK: Migrate storage — localStorage → JSON filstore
  owner: OPEN
  status: TODO
  notes: Bevara schema; skriv migreringssteg

- TASK: Import/Export Markdown
  owner: OPEN
  status: TODO
  notes: Exportera note->.md; Importera .md->note

- TASK: CI — workflow_dispatch + badge
  owner: OPEN
  status: TODO
  notes: Lägg manuell Run-knapp + README-badge för Repo Checks

- TASK: Docs — user guide & screenshots
  owner: OPEN
  status: TODO
  notes: Kort användarguide; placeholder för screenshots
