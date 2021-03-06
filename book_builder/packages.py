#! py -3
# Discover examples that don't have packages
import logging
import re
from logging import debug

import book_builder.config as config
# from book_builder.package_names import atom_package_names

logging.basicConfig(filename=__file__.split(
    '.')[0] + ".log", filemode='w', level=logging.DEBUG)

slugline = re.compile("^(//|#) .+?\.[a-z]+$", re.MULTILINE)


def unpackaged(source_dir=config.markdown_dir):
    print("Discovering examples that don't have packages ...")
    if not source_dir.exists():
        return f"Cannot find {source_dir}"
    for sourceText in source_dir.glob("[0-9][0-9]_*.md"):
        debug(f"--- {sourceText.name} ---")
        for group in re.findall("```(.*?)\n(.*?)\n```", sourceText.read_text(), re.DOTALL):
            listing = group[1].splitlines()
            title = listing[0]
            package = None
            for line in listing:
                if line.startswith("package "):
                    package = line.split()[1].strip()
            if slugline.match(title):
                debug(title)
                fpath = title.split()[1].strip()
                if package:
                    print(f"{sourceText.name}: {fpath} in package {package}")
                else:
                    print(f"{sourceText.name} : {fpath} has no package")
                # print(f"should be in package {atom_package_names[sourceText.name]}")

    return "Package check complete"


def missing_package(n, lines):
    n += 1
    while lines[n].strip() != "```":
        if lines[n].startswith("package "):
            return False
        n += 1
    else:
        return True


def contains_missing_package(lines):
    for n, line in enumerate(lines):
        if line.startswith(f"```{config.language_name}"):
            if not lines[n + 1].startswith("//"):
                continue
            if missing_package(n, lines):
                return n
    else:
        return False


# def add_next_package(lines, md_name):
#     n = contains_missing_package(lines) + 1
#     while lines[n].strip().startswith("//"):
#         n += 1
#     pckg = "package " + atom_package_names[md_name]
#     lines.insert(n, pckg)
#     # print("inserted " + lines[n])
#     if not (lines[n + 1].startswith("import") or lines[n + 1].strip() == ""):
#         lines.insert(n + 1, "")
#     return lines


# def add_packages(target_dir=config.markdown_dir):
#     print("Inserting package statements into examples that lack them")
#     if not target_dir.exists():
#         return f"Cannot find {target_dir}"
#     for md in target_dir.glob("[0-9][0-9]_*.md"):
#         lines = md.read_text().splitlines()
#         while contains_missing_package(lines):
#             print(f"missing package in {md.name}")
#             lines = add_next_package(lines, md.name)

#         md.write_text("\n".join(lines) + "\n")
#         # md.with_suffix(".txt").write_text("\n".join(lines))

#     return "Package insertion complete"
