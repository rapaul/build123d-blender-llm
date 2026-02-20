## 1. Update render-and-review skill

- [x] 1.1 Read the current skill file at `.claude/commands/render-and-review.md` to understand what it currently instructs
- [x] 1.2 Update `.claude/commands/render-and-review.md` to instruct the skill to write the user-provided description to `renders/<name>/prompt.txt` using the Write tool, immediately after `render.py` exits with code 0

## 2. Verify

- [x] 2.1 Manually invoke `/render-and-review` on any existing model and confirm `renders/<name>/prompt.txt` is created with the correct content
