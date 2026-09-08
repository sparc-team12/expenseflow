# ExpenseFlow

Expense claim submission and approval app. Demo application for an
agentic Change Request pipeline across the SDLC.

## Stack
- Backend: FastAPI (Python), `backend/app/`
- Frontend: plain HTML + JS, `frontend/`, served by FastAPI
- Tests: pytest, `backend/tests/`

## Rules for agents

1. ALWAYS read `traceability/index.yaml` first to find relevant files.
   Never scan the repository.
2. Business rules live ONLY in `backend/app/domain/claim_rules.py`.
   Never put validation logic in `main.py` or the frontend.
3. Every rule has a comment marking its feature and acceptance criterion
   (e.g. `# AC-2: ...`). Keep these markers accurate when editing.
4. Update `traceability/index.yaml` when adding or moving a file.
5. Output diffs and patches, never whole rewritten files.
6. Do not modify files outside the impact set for the current CR.

## Commands
- Run: `cd backend && uvicorn app.main:app --reload`
- Test: `cd backend && pytest`