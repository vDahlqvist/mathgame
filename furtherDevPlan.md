# Plan: Error Handling & Crash Prevention

The application has **27 identified vulnerabilities** across 8 categories, with 18 critical issues that will definitely crash under certain conditions. This plan addresses systematic hardening through defensive programming, comprehensive error handling, and state validation.

## Steps

1. **Wrap all database operations** in try-except blocks in `db.py` (`save_score`, `get_scores`) to catch `sqlite3.Error`, handle disk-full/locked/corrupted scenarios, and initialize the scores table at application startup in `main.py` rather than on-demand.

2. **Add input validation layer** in `logic.py`.`check_answer()` to reject empty/whitespace-only answers before parsing, validate player names in `gui.py`.`show_save_score_dialog()` for length/content, and add try-except around `parse_latex()` with specific error messaging for `LaTeXParsingError`.

3. **Implement game state validation** in `logic.py`.`start_game()` to reset `current_points` and `questions_completed`, validate `current_difficulty` is not None before allowing game start, validate `selected_subjects` is not empty, and add checks in `next_question()` for valid dictionary keys before accessing `QUESTIONS`.

4. **Fix PyQt widget lifecycle issues** in `gui.py` by adding `closeEvent()` handler to stop timer on window close, checking `scoreboard_window.isVisible()` or catching `RuntimeError` in `open_scoreboard()`, and disabling submit button during `check_answer()` processing to prevent duplicate submissions.

5. **Add MathJax fallback mechanism** in `gui.py`.`update_question_display()` by detecting load failures with `loadFinished` signal handler, displaying raw LaTeX with error message when CDN unavailable, or bundling offline MathJax as alternative.

6. **Enhance math expression handling** in `logic.py`.`check_answer()` by using `sympy.simplify()` before comparison to normalize expressions like `x^2` vs `x*x`, adding special handling for ± symbols and comma-separated solutions, and wrapping comparison in try-except for symbolic math errors.

## Further Considerations

1. **Database architecture**: Should database connections use connection pooling/context managers for efficiency, or implement a persistent connection pattern? Current open/close per operation is inefficient.

2. **User feedback**: Currently errors print to console. Should there be QMessageBox dialogs for user-facing errors (invalid answers, save failures), or status bar messages, or logging to file?

3. **Testing strategy**: Should unit tests be added for error conditions, or manual testing checklist created? Consider adding test fixtures for corrupted databases, invalid LaTeX, missing files.
