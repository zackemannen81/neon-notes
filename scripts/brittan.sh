#!/usr/bin/env bash
set -euo pipefail
AGENT="${AGENT:-Brittan}"
PROJECT_INFO="docs/ProjectInformation.md"
JOURNAL="journal/DeveloperJournal.md"
TASKS="tasks/ProjectTasks.md"
CLI="tools/agent_cli.py"

now_utc() { date -u +"%Y-%m-%d %H:%M:%S UTC"; }
today() { date -u +"%Y-%m-%d"; }

append_journal () {
  local title="$1"; shift
  local lines="$*"
  if ! grep -q "## $(today)" "$JOURNAL" 2>/dev/null; then
    printf "\n## %s\n\n" "$(today)" >> "$JOURNAL"
  fi
  {
    printf "### %s — %s\n" "$AGENT" "$title"
    while IFS= read -r line; do [ -n "$line" ] && printf -- "- %s\n" "$line"; done <<< "$lines"
    printf "\n"
  } >> "$JOURNAL"
}

if [ -d .git ]; then git pull --rebase || true; fi

if [ -f "$PROJECT_INFO" ]; then
  ACTIVE=$(awk '/^## Active Notices/{flag=1;next}/^##/{flag=0}flag' "$PROJECT_INFO")
  notice_ids=$(echo "$ACTIVE" | sed -n 's/^- \(NOTICE-[0-9-]\+\):.*/\1/p')
  for nid in $notice_ids; do
    block=$(awk -v nid="$nid" '$0 ~ "- "nid":" {flag=1} flag{print} flag&&NF==0{flag=0}' "$PROJECT_INFO")
    mand=$(echo "$block" | sed -n 's/^[[:space:]]*- Mandatory: \(Yes\|No\).*/\1/p' | head -n1)
    if [ "$mand" = "Yes" ] && ! echo "$block" | grep -q "$AGENT ("; then
      python3 "$CLI" ack "$nid" --agent "$AGENT" --notes "Auto-ACK by orchestrator" || true
    fi
  done
fi

# Optionally auto-assign OPEN tasks round-robin if AUTO_ASSIGN=1
if [ "${AUTO_ASSIGN:-0}" = "1" ]; then
  agents=("OpenAI Codex CLI #1" "OpenAI Codex CLI #2" "Gemini CLI" "Claude Code (CLI)" "Cascade (Windsurf)")
  open_tasks=$(awk '/^- TASK: /{title=$0; getline; o=$0; if(o ~ /owner: OPEN/){print substr(title,9)}}' "$TASKS")
  for t in $open_tasks; do
    pick=${agents[$RANDOM % ${#agents[@]}]}
    python3 "$CLI" start "$t" --agent "$pick" --notes "Auto-assign by orchestrator" || true
  done
fi

append_journal "Orchestrator run" "$(printf "**Time:** %s\n**Notes:** Checked notices, optional auto-assign" "$(now_utc)")"
