import arrow
# import click

from cartaro.model.log_entry import LogEntry
import cartaro.controller.base as base

log_entries = base.create_controller("log_entries", LogEntry)

# ------------------------------------------------------------------------------
# CLI Commands
# ------------------------------------------------------------------------------
@log_entries.cli.command('weekly-report')
def weekly_report():
    week_start = arrow.get().to("local").floor("week").int_timestamp
    entries = LogEntry.find(
        sort_by="logged_at",
        logged_at=f"gte:{week_start}",
    )

    # codex --full-auto workspace-write exec "summarize my weekly report in weekly.txt and save to weekly-report.txt"
    for entry in entries:
        tags = [str(tag) for tag in entry.tags]
        print("---------------------------------------------------------------")
        print(f"""Subject: {entry.subject}
Category: {entry.category}
Date: {entry.logged_at.format("MMM DD YYYY")}
Tags: {','.join(tags)}
{entry.content}
""")
        print("---------------------------------------------------------------")
