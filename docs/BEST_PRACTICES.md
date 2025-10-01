# BEST_PRACTICES.md (Evergreen)

Detta dokument gäller för **alla** projekt. Fyll bara i projektspecifika filer (Overview/Tasks) när ni startar nytt.

## 1) Revisionshantering (Git)
- **Branch-strategi**
  - `main`: produktionsredo
  - `develop`: integration/test
  - `feature/*`: nya features
  - `release/*`: releaseförberedelser
  - `hotfix/*`: akuta fixar mot `main`
- **Conventional Commits**: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`
- **Pull Requests**
  - Små, fokuserade, minst 1 review
  - Länka till task i `tasks/ProjectTasks.md`
  - Beskriv *vad* och *varför*

## 2) Testning
- Enhetstester för kärnmoduler
- Integrationstester för kritiska flöden
- Körs lokalt & i CI för alla PRs
- Mät test-täckning (rimlig nivå > 70% i kärnan)

## 3) Felhantering & Loggning
- Logga alltid fel med tid, modul, task
- **NEEDS_INFO** när oklart underlag
- **BLOCKED** när extern beroende hindrar
- Inga tysta fel; kasta/logga och faila tidigt
- UI: visa snälla fel (fallbacks hellre än krascher)

## 4) Källkodskontroll & Stil
- Följ `docs/CODE_STYLE.md`
- Lint/format lokalt + i CI
- Ingen direkt push till `main`
- Journal-uppdatering för större ändringar

## 5) Struktur
```
/docs                – styrdokument (overview/roadmap/devplan/quickstart/best_practices/...)
/tasks               – ProjectTasks.md (enda sanningen för tasks)
/journal             – DeveloperJournal.md (append-only) + DEVLOG.md (snapshots)
/tools               – agent_cli.py + utils
/scripts             – brittan.sh (orkestrator) + setup hjälpare
/configs             – project.yaml + policies
/src                 – källkod
/.github/workflows   – CI/CD
```
- Alla styrdokument är versionerade i Git
- Journal är verkligheten; allt arbete syns där

## 6) CI/CD
- Validera: tasks-format, journal finns, notices finns
- Blockera merge vid:
  - mandatory notice utan ACK
  - lint/test-fel
  - ogiltig task-status
- Bygg/test/deploy på `develop`/`main`

## 7) Agentflöde (Daglig rutin)
1. `git pull`
2. Läs `docs/ProjectInformation.md` (NOTICES)
3. Ta task (`owner: OPEN`) → `agent_cli.py start`
4. Jobba, logga `update` ofta
5. `finish` → `REVIEW` eller `DONE` med PR-länk
6. Ack:a NOTICES vid behov: `agent_cli.py ack ...`
7. Håll `journal/DeveloperJournal.md` uppdaterad

## 8) Säkerhet & Sekretess
- Lägg aldrig in hemligheter i repo
- Använd `.env`/secrets för CI
- Sanera loggar och journal från känslig data

## 9) Dokumentation
- `PROJECT_OVERVIEW.md`: vision, mål, arkitektur (projektunik)
- `ROADMAP.md`, `DEVELOPMENTPLAN.md`: faser & sprintar
- `QUICKSTART.md`: för nya medlemmar
- Uppdatera docs vid större process-ändringar (lägg NOTICE)
