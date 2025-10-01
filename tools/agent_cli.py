#!/usr/bin/env python3
import argparse, datetime, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TASKS = BASE / "tasks" / "ProjectTasks.md"
JOURNAL = BASE / "journal" / "DeveloperJournal.md"
PROJECT_INFO = BASE / "docs" / "ProjectInformation.md"

def now_utc():
    import datetime
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def read_tasks():
    if not TASKS.exists():
        return []
    text = TASKS.read_text()
    blocks = re.findall(r"- TASK:\s*(.+?)\n\s*owner:\s*(.+?)\n\s*status:\s*(.+?)\n\s*notes:\s*(.*?)(?:\n\n|$)", text, flags=re.S)
    tasks = []
    for title, owner, status, notes in blocks:
        tasks.append(dict(title=title.strip(), owner=owner.strip(), status=status.strip(), notes=notes.strip()))
    return tasks

def write_tasks(tasks):
    out = ["# ProjectTasks", "", "> Canonical task list. Agents may only modify their own `owner/status/notes` fields.", ""]
    for t in tasks:
        out.append(f"- TASK: {t['title']}")
        out.append(f"  owner: {t['owner']}")
        out.append(f"  status: {t['status']}")
        out.append(f"  notes: {t.get('notes','')}")
        out.append("")
    TASKS.write_text("\n".join(out))

def ensure_journal_date():
    today = __import__('datetime').datetime.utcnow().strftime("%Y-%m-%d")
    txt = JOURNAL.read_text() if JOURNAL.exists() else "# Developer Journal\n\n"
    if f"## {today}" not in txt:
        txt += f"\n## {today}\n\n"
        JOURNAL.write_text(txt)

def append_journal(agent, title, content_lines):
    ensure_journal_date()
    with open(JOURNAL, "a") as f:
        f.write(f"### {agent} — {title}\n")
        for line in content_lines:
            f.write(f"- {line}\n")
        f.write("\n")

def find_task(tasks, title):
    for t in tasks:
        if t["title"].lower() == title.lower():
            return t
    return None

def cmd_list(args):
    for t in read_tasks():
        print(f"- {t['title']} | owner: {t['owner']} | status: {t['status']}")

def cmd_start(args):
    tasks = read_tasks()
    t = find_task(tasks, args.title)
    if not t: sys.exit("ERROR: Task not found.")
    if t["owner"] != "OPEN" and not args.force:
        sys.exit(f"ERROR: Task already owned by {t['owner']} (use --force).")
    t["owner"] = args.agent
    t["status"] = "IN_PROGRESS"
    if args.notes:
        t["notes"] = (t.get("notes","") + ("\n" if t.get("notes") else "") + args.notes).strip()
    write_tasks(tasks)
    append_journal(args.agent, f"Started: {t['title']}", [f"**Time:** {now_utc()}", f"**Notes:** {args.notes or '—'}"])
    print("OK: started")

def cmd_update(args):
    tasks = read_tasks()
    t = find_task(tasks, args.title)
    if not t: sys.exit("ERROR: Task not found.")
    if args.notes:
        t["notes"] = (t.get("notes","") + ("\n" if t.get("notes") else "") + args.notes).strip()
    write_tasks(tasks)
    append_journal(args.agent, f"Update: {t['title']}", [f"**Time:** {now_utc()}", f"**Update:** {args.notes or '—'}"])
    print("OK: updated")

def cmd_finish(args):
    tasks = read_tasks()
    t = find_task(tasks, args.title)
    if not t: sys.exit("ERROR: Task not found.")
    t["status"] = args.status or "DONE"
    t["owner"] = "OPEN" if t["status"] == "DONE" else args.agent
    if args.notes:
        t["notes"] = (t.get("notes","") + ("\n" if t.get("notes") else "") + f"[Finish] {args.notes}").strip()
    write_tasks(tasks)
    append_journal(args.agent, f"Finished: {t['title']}", [f"**Time:** {now_utc()}", f"**Status:** {t['status']}", f"**Notes:** {args.notes or '—'}"])
    print("OK: finished")

def cmd_ack(args):
    if not PROJECT_INFO.exists():
        sys.exit("ERROR: docs/ProjectInformation.md missing.")
    text = PROJECT_INFO.read_text()
    import re
    pattern = rf"(- {re.escape(args.notice_id)}:.*?Acknowledged by:\s*)(.*?)(\n\n|$)"
    m = re.search(pattern, text, flags=re.S)
    if not m: sys.exit("ERROR: Notice not found.")
    pre, ack_block, tail_sep = m.groups()
    ack_lines = [line.strip() for line in ack_block.strip().splitlines() if line.strip()]
    agent_line = f"  - {args.agent} ({now_utc()})"
    if not any(args.agent in l for l in ack_lines):
        ack_lines.append(agent_line)
    new_ack = "\\n".join(ack_lines) + "\\n"
    new_text = text[:m.start(2)] + new_ack + text[m.end(2):]
    PROJECT_INFO.write_text(new_text)
    append_journal(args.agent, f"ACK: {args.notice_id}", [f"**Time:** {now_utc()}", f"**Notes:** {args.notes or '—'}"])
    print("OK: acknowledged")

def main():
    import argparse
    p = argparse.ArgumentParser(description="LLM Multi-Agent Task & Journal CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--agent", required=True, help="Agent name")

    sp = sub.add_parser("list", help="List tasks")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("start", parents=[common], help="Start a task")
    sp.add_argument("title"), sp.add_argument("--notes", default=""), sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_start)

    sp = sub.add_parser("update", parents=[common], help="Update a task")
    sp.add_argument("title"), sp.add_argument("--notes", default="")
    sp.set_defaults(func=cmd_update)

    sp = sub.add_parser("finish", parents=[common], help="Finish/close a task")
    sp.add_argument("title"), sp.add_argument("--status", choices=["DONE","REVIEW","BLOCKED","NEEDS_INFO","N/A","Not functional"], default=None)
    sp.add_argument("--notes", default="")
    sp.set_defaults(func=cmd_finish)

    sp = sub.add_parser("ack", parents=[common], help="Acknowledge a NOTICE")
    sp.add_argument("notice_id"), sp.add_argument("--notes", default="")
    sp.set_defaults(func=cmd_ack)

    args = p.parse_args(); args.func(args)

if __name__ == "__main__":
    main()
