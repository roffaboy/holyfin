#!/usr/bin/env python3
"""Checks theme.css against a Jellyfin web client. Standard library only.

    tools/check.py <jellyfin-web-dir> [--update-baseline]

What it checks:
  1. The stylesheet itself: balanced braces, every var(--x) is defined, corners only from the radii of
     HolyArrs (--r-*), no fixed Jellyfin blue.
  2. Drift: every class the theme styles still exists in that Jellyfin version.
  3. New blue: Jellyfin has not gained more fixed blue than the theme was made against
     (tools/blue-baseline.json; refresh it with --update-baseline after a version you have looked at).

Exit code 0 when all is well, 1 when something needs a look. The report goes to stdout and, in
GitHub Actions, to the job summary.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEME = ROOT / "theme.css"
BASELINE = ROOT / "tools" / "blue-baseline.json"
ALLOW = ROOT / "tools" / "allow-missing.txt"
BLUES = ["#00a4dc", "#03a9f4", "#0288d1"]


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def own_checks(css):
    """Problems in the stylesheet itself."""
    problems = []
    if css.count("{") != css.count("}"):
        problems.append("braces are not balanced")
    if css.count("(") != css.count(")"):
        problems.append("parentheses are not balanced")
    defined = set(re.findall(r"(--[\w-]+)\s*:", css))
    for name in sorted(set(re.findall(r"var\((--[\w-]+)", css)) - defined):
        if not name.startswith("--jf-"):
            problems.append(f"var({name}) is used but never defined")
    for value in re.findall(r"border-radius\s*:\s*([^;]+);", css):
        v = value.strip().replace("!important", "").strip()
        if v not in ("0", "inherit") and not re.fullmatch(r"var\(--r-(sm|btn|card|panel|modal|pill)\)", v):
            problems.append(f"border-radius: {value.strip()} (use one of the radii --r-sm, --r-btn, --r-card, --r-panel, --r-modal, --r-pill)")
    for blue in BLUES:
        if blue in css.lower():
            problems.append(f"{blue} is written in the theme (use the accent)")
    return problems


def classes_in(css):
    """The class names in the selectors of the theme (not in declarations, keyframes or at-rules)."""
    names = set()
    for match in re.finditer(r"([^{}]+)\{", css):
        selector = match.group(1).strip()
        if selector.startswith("@") or re.fullmatch(r"(from|to|\d+%)(\s*,\s*(from|to|\d+%))*", selector):
            continue
        # a selector list can follow an at-rule block, so take the part after the last ';' or '}'
        selector = re.split(r"[;}]", selector)[-1]
        names.update(re.findall(r"\.(-?[A-Za-z_][\w-]*)", selector))
    return names


def load_bundle(web_dir):
    """All identifiers in the CSS and JS of the web client, and the CSS text for the blue count."""
    identifiers, css_text = set(), []
    for path in Path(web_dir).rglob("*"):
        if path.suffix not in (".css", ".js", ".html"):
            continue
        text = path.read_text(errors="ignore")
        identifiers.update(re.findall(r"[A-Za-z_][\w-]*", text))
        # The blue count looks at what the dark theme loads: the other themes (light, blueradiance,
        # ...) are not used here.
        parts = path.relative_to(web_dir).parts
        other_theme = parts[0] == "themes" and len(parts) > 1 and parts[1] not in ("dark", "_base")
        if path.suffix == ".css" and not other_theme:
            css_text.append(text)
    return identifiers, "\n".join(css_text)


def exists(name, identifiers):
    """A class exists when the bundle mentions it. MUI builds 'MuiButton-root' from two strings."""
    if name in identifiers:
        return True
    mui = re.fullmatch(r"(Mui[A-Za-z]+)-([A-Za-z0-9-]+)", name)
    if mui:
        return mui.group(1) in identifiers and mui.group(2) in identifiers
    state = re.fullmatch(r"Mui-([A-Za-z]+)", name)
    if state:
        return state.group(1) in identifiers
    return False


def count_blue(text):
    return {blue: len(re.findall(re.escape(blue), text, flags=re.I)) for blue in BLUES}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not Path(args[0]).is_dir():
        sys.exit(__doc__)
    update = "--update-baseline" in sys.argv
    css = strip_comments(THEME.read_text())
    lines, failed = [], False

    problems = own_checks(css)
    lines.append("## The stylesheet")
    lines += [f"- {p}" for p in problems] or ["- fine"]
    failed |= bool(problems)

    identifiers, css_text = load_bundle(args[0])
    allowed = set(ALLOW.read_text().split()) if ALLOW.exists() else set()
    missing = sorted(n for n in classes_in(css) if not exists(n, identifiers) and n not in allowed)
    lines.append("\n## Classes that Jellyfin no longer has")
    lines += [f"- .{n}" for n in missing] or ["- none"]
    failed |= bool(missing)

    blue = count_blue(css_text)
    if update:
        BASELINE.write_text(json.dumps(blue, indent=2) + "\n")
        lines.append(f"\n## Blue baseline\n- updated: {blue}")
    else:
        base = json.loads(BASELINE.read_text()) if BASELINE.exists() else {}
        more = {k: (base.get(k, 0), v) for k, v in blue.items() if v > base.get(k, 0)}
        lines.append("\n## New fixed blue in Jellyfin's stylesheets")
        lines += [f"- {k}: {old} before, {new} now" for k, (old, new) in more.items()] or ["- none"]
        failed |= bool(more)

    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).write_text(report + "\n")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
