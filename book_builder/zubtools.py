"""
Random automation subtools
"""
from pathlib import Path
import os
import re
import sys
from itertools import filterfalse
from pprint import pprint
import book_builder.config as config


def check_for_notes(md, lines):
    notes = False
    for line in lines:
        if line.startswith("+ Notes:") and len(line) > len("+ Notes:"):
            print(f"{md.stem}: [{line}]")
            os.system(f"{config.md_editor} {md}:6:10")
            notes = True
    return notes


def remove_checkboxes():
    def determine(line):
        return (
            line.strip().endswith("] Ready for Review") or
            line.strip().endswith("] Tech Checked") or
            line.startswith("+ Notes:")
        )
    for md in config.markdown_dir.glob("*.md"):
        lines = md.read_text().splitlines()
        if check_for_notes(md, lines):
            return "Notes need changing to {{}}"
        lines[:] = filterfalse(determine, lines)
        text = re.sub('\n{2,}','\n\n', "\n".join(lines))
        md.write_text(text + "\n")