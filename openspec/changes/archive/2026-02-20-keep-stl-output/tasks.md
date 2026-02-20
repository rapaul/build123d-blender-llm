## 1. Update render.py

- [x] 1.1 Replace `tempfile.NamedTemporaryFile` creation with a fixed path: `renders/<change-name>/model.stl`
- [x] 1.2 Remove the `finally` block (or any other cleanup) that deletes the STL file
- [x] 1.3 Verify the output directory is created before the STL export (it should already be, but confirm ordering)

## 2. Verify

- [x] 2.1 Run `uv run python render.py <model.py> <change-name>` and confirm `renders/<change-name>/model.stl` exists after completion
- [x] 2.2 Confirm all four render images are still produced correctly
- [x] 2.3 Confirm re-running overwrites the STL without error
