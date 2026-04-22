# Pulling Updated Tests & Fixes Into Your Repository

The template repository has been updated with important bug fixes and complete test suites for all four tasks. If you've already cloned your assignment repo, follow these steps to pull the changes in.

## Step 1 — Open a terminal in your repo folder

```bash
cd ~/repos/YOUR-ASSIGNMENT-REPO
```

## Step 2 — Add the template repo as a remote (one-time only)

```bash
git remote add template https://github.com/beeteetoo/COM5413_Student_Main.git
```

If you get `fatal: remote template already exists`, that's fine — skip to Step 3.

## Step 3 — Pull the updates

```bash
git fetch template
git merge template/main --allow-unrelated-histories -m "Merge upstream template fixes"
```

## Step 4 — Install any new dependencies

```bash
pip3 install -r requirements.txt
```

This adds `pyftpdlib`, which is needed by the Task 3 test suite.

## Step 5 — Verify everything works

```bash
python3 -m pytest field_tests/ --tb=short
```

You should see **50 tests collected**. Tests for tasks you haven't started yet will fail — that's expected.

---

## What changed?

- Test suites for **all four tasks** are now available (not just Task 1)
- Fixed a bug where correct implementations could fail the deduplication test
- Fixed a bug where using `input` as a variable/parameter name was incorrectly flagged
- `README.md` now uses `python3` / `pip3` (correct for Kali)
- `setup_benji_protocol.sh` removed (not needed)

---

## If you get merge conflicts

If you've edited files outside your task's toolkit folder (e.g. test files), you may see conflicts. Resolve them by keeping the **template** version of any file in `field_tests/`:

```bash
git checkout template/main -- field_tests/
git add field_tests/
git commit -m "Resolve conflicts: keep upstream test files"
```
