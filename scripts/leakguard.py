#!/usr/bin/env python3
"""Leak guard: block banned terms and unexpected identities.

Banned terms live only as "<length> <sha256(lowercase term)>" lines in
.githooks/banned.sha256; the allowed author/committer email lives only as a
sha256 in .githooks/allowed_email.sha256. Findings report a location, never
the matched text.

Usage:
  leakguard.py --staged            check added lines of the staged diff + identity
  leakguard.py --message FILE      check a commit message file
  leakguard.py --range REVS...     check each commit in range: message, diff, identities
  leakguard.py --text LABEL        check stdin text (branch name, PR title/body)
  leakguard.py --tree              check every tracked file in the working tree
  leakguard.py --self-test
"""
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED = os.path.join(ROOT, ".githooks", "banned.sha256")
ALLOWED = os.path.join(ROOT, ".githooks", "allowed_email.sha256")


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_banned(path=BANNED):
    table = {}
    with open(path) as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and not line.startswith("#"):
                table.setdefault(int(parts[0]), set()).add(parts[1].lower())
    return table


def hits(text, table):
    low = text.lower()
    for n, hashes in table.items():
        for i in range(len(low) - n + 1):
            if sha(low[i:i + n]) in hashes:
                return True
    return False


def scan_lines(label, lines, table, out):
    """lines: iterable of (lineno, text)."""
    for no, text in lines:
        if hits(text, table):
            out.append("%s:%s: banned term" % (label, no))


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          errors="replace").stdout


def allowed_hash():
    with open(ALLOWED) as f:
        return f.read().split()[0].lower()


def check_email(label, email, out):
    if sha(email.strip().lower()) != allowed_hash():
        out.append("%s: author email not allowed; set user.email in this repo" % label)


def ident_email(var):
    m = re.search(r"<([^>]*)>", git("var", var))
    return m.group(1) if m else ""


def added_lines(diff):
    """Yield (file:line, text) for '+' lines of a unified diff."""
    path, no = "?", 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            p = line[4:]
            path = p[2:] if p.startswith("b/") else p
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            no = int(m.group(1)) if m else 0
        elif line.startswith("+"):
            yield path, no, line[1:]
            no += 1
        elif not line.startswith("-") and not line.startswith("\\"):
            no += 1


def scan_diff(prefix, diff, table, out):
    for path, no, text in added_lines(diff):
        if hits(text, table):
            out.append("%s%s:%d: banned term" % (prefix, path, no))
    # file paths themselves
    for line in diff.splitlines():
        if line.startswith("+++ b/") and hits(line[6:], table):
            out.append("%s%s: banned term in file path" % (prefix, "(path)"))


def cmd_staged(table, out):
    check_email("author", ident_email("GIT_AUTHOR_IDENT"), out)
    check_email("committer", ident_email("GIT_COMMITTER_IDENT"), out)
    scan_diff("", git("diff", "--cached", "-U0", "--no-color", "--no-ext-diff"), table, out)


def cmd_message(path, table, out):
    with open(path, errors="replace") as f:
        lines = [(i, l) for i, l in enumerate(f, 1) if not l.startswith("#")]
    scan_lines("commit message", lines, table, out)


def cmd_range(revs, table, out):
    for c in git("rev-list", "--reverse", *revs).split():
        short = c[:10]
        meta = git("show", "-s", "--format=%ae%n%ce", c).splitlines()
        check_email("commit %s author" % short, meta[0], out)
        check_email("commit %s committer" % short, meta[1], out)
        msg = git("show", "-s", "--format=%B", c)
        scan_lines("commit %s message" % short, enumerate(msg.splitlines(), 1), table, out)
        diff = git("show", "--format=", "-U0", "--no-color", "--no-ext-diff", c)
        scan_diff("commit %s " % short, diff, table, out)


def cmd_text(label, table, out):
    scan_lines(label, enumerate(sys.stdin.read().splitlines(), 1), table, out)


def cmd_tree(table, out):
    for path in git("ls-files", "-z").split("\0"):
        if not path:
            continue
        if hits(path, table):
            out.append("%s: banned term in file path" % path)
        try:
            with open(os.path.join(ROOT, path), errors="replace") as f:
                scan_lines(path, enumerate(f, 1), table, out)
        except (IsADirectoryError, FileNotFoundError):
            pass


def self_test():
    # Test term built at runtime so it never appears in this file.
    term = "".join(chr(c) for c in (113, 117, 105, 120, 111, 116, 105, 99))
    other = "tset"[::-1] + "-only"
    table = {len(term): {sha(term)}, len(other): {sha(other)}}
    cases = [
        ("inside dotted id", "com.%s.app" % term.upper(), True),
        ("inside longer word", "pre%ssuffix" % term, True),
        ("inside url", "https://%s.example/x" % term.capitalize(), True),
        ("second term", "a %s b" % other.upper(), True),
        ("negative control", "nothing to see here: quixote, tic", False),
    ]
    ok = True
    for name, text, want in cases:
        got = hits(text, table)
        print("%s %s" % ("ok  " if got == want else "FAIL", name))
        ok &= got == want
    diff = "+++ b/x.txt\n@@ -0,0 +1,2 @@\n+clean\n+has %s\n" % term
    out = []
    scan_diff("", diff, table, out)
    good = out == ["x.txt:2: banned term"] and term not in out[0]
    print("%s diff reports file:line only" % ("ok  " if good else "FAIL"))
    ok &= good
    load_banned()  # real list parses
    print("self-test %s" % ("passed" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[0] == "--self-test":
        return self_test()
    table, out = load_banned(), []
    mode = argv[0]
    if mode == "--staged":
        cmd_staged(table, out)
    elif mode == "--message":
        cmd_message(argv[1], table, out)
    elif mode == "--range":
        cmd_range(argv[1:], table, out)
    elif mode == "--text":
        cmd_text(argv[1], table, out)
    elif mode == "--tree":
        cmd_tree(table, out)
    else:
        print(__doc__)
        return 2
    for line in out:
        print("leakguard: " + line, file=sys.stderr)
    if out:
        print("leakguard: %d finding(s); commit/push blocked" % len(out), file=sys.stderr)
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
