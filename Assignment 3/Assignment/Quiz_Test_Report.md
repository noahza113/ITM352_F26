# Quiz Login and Gameplay Test Report

**Date:** November 18, 2026  
**Result:** PASS — 4 tests run, 0 failures, 0 errors  
**Method:** Flask test client submitted the same forms used by the website. Test accounts and scores were written to temporary JSON files and removed after each test.

## Test results

| Test | Result | What was checked |
|---|---|---|
| `test_registration_login_and_input_validation` | PASS | Rejected a short username and password, registered an account, confirmed the password was not saved as plain text, rejected a duplicate account and incorrect password, and accepted the correct login. |
| `test_login_required_category_validation_and_question_display` | PASS | Redirected a logged-out user away from starting a quiz, rejected an invalid category, and displayed five Geography questions with four valid answer options. |
| `test_hint_and_invalid_answer` | PASS | Displayed a hint and rejected an invalid answer without recording a response. |
| `test_full_quiz_feedback_score_and_saved_history` | PASS | Completed five questions with four correct and one incorrect, checked both feedback messages, verified a duplicate answer was not counted, displayed the 4/5 result and missed-question review, and confirmed the score appeared in saved score history. |

## Hint limit follow-up

After adding the one-hint-per-quiz limit, an additional focused check passed:

| Test | Result | What was checked |
|---|---|---|
| `test_one_hint_per_quiz` | PASS | Showed the hint once, rejected a second request, and confirmed the limit remained in effect on the next question. |

This follow-up also used temporary account and score files.

## Summary

The original four integration checks and the hint-limit follow-up passed. The quiz score was saved in a temporary `scores.json` file during the full-quiz check and appeared in the home-page score history. No test accounts or scores were added to the app's local data files.
