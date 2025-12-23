SUMMARY_PROMPT = (
    "Once you have completed the task, briefly write a concise summary of the testing setup in "
    "`/scripts/SUMMARY.md` of the form: # Summary \n...\n## System Dependencies \n...\n## PROJECT "
    "Environment \n...\n## Testing Framework \n...\n## Additional Notes"
)

SETUP_PROMPT_PYTHON = (
    "You are working inside a containerized Linux environment with sudo privileges.\n"
    "Task: Configure the Python environment and validation scripts for the repository in /testbed/.\n"
    "Constraints:\n"
    "1. EXPLORE: Analyze the /testbed/ directory to identify the required Python version, system dependencies, and testing framework. CI files may provide hints.\n"
    "2. DEPS: Identify and install necessary system-level dependencies using sudo (non-interactive) and project-level dependencies. \n"
    "3. NEVER modify files in /testbed/, except for files and folders that appear in .gitignore (e.g. .venv). This means that `git status` should show no changes after running tests.\n"
    "4. SCRIPTS:\n"
    "   - Create '/scripts/setup_env.sh': When executed, this script sets up the entire project environment. It SHOULD NOT install system-level dependencies. Use `uv` for speed or `conda` for complex environments.\n"
    "   - Create '/scripts/run_tests': Source '/scripts/setup_env.sh' and executes the test suite. These scripts must remain functional even if /testbed/ is checked out to HEAD~1.\n"
    "5. OUTPUT: The '/scripts/run_tests' script must output a single JSON line as its final stdout: "
    '{"passed": int, "failed": int, "skipped": int, "total": int}. Ensure no logs appear after this JSON object.\n'
    "6. VERIFICATION: Execute '/scripts/run_tests' on both the current commit and HEAD~1; confirm the JSON outputs match the actual test results. Proceed without asking for permission.\n\n"
    "Note: Use `uv` or `conda` to install the right Python distribution. Versions 3.8 through 3.13 are pre-cached. Any dependencies or python environments that you install globally are preserved.\n"
) + "\n" + SUMMARY_PROMPT

SETUP_PROMPT_JAVASCRIPT = (
    "You are working inside a containerized Linux environment with sudo privileges.\n"
    "Task: Configure the JavaScript/TypeScript environment and validation scripts for the repository in /testbed/.\n"
    "Constraints:\n"
    "1. EXPLORE: Analyze the /testbed/ directory to identify the required Node.js version (check .nvmrc or package.json), "
    "the preferred package manager (npm, pnpm, yarn, or bun), and the testing framework (Jest, Vitest, Playwright, etc.).\n"
    "2. DEPS: Identify and install necessary system-level dependencies using sudo (non-interactive) and project-level dependencies. "
    "If Playwright or Cypress is used, ensure browser binaries are installed via `npx playwright install` if not already present.\n"
    "3. NEVER modify files in /testbed/, except for files and folders that appear in .gitignore (e.g., node_modules, .next, dist). "
    "This means that `git status` should show no changes after running tests.\n"
    "4. SCRIPTS:\n"
    "   - Create '/scripts/setup_env.sh': When executed, this script sets up the entire project environment. It SHOULD NOT install system-level dependencies. "
    "Use `nvm` to switch Node versions if necessary and the detected package manager for installation.\n"
    "   - Create '/scripts/run_tests': Source '/scripts/setup_env.sh' and executes the test suite. "
    "These scripts must remain functional even if /testbed/ is checked out to HEAD~1.\n"
    "5. OUTPUT: The '/scripts/run_tests' script must output a single JSON line as its final stdout: "
    '{"passed": int, "failed": int, "skipped": int, "total": int}. '
    "You may need to write a small wrapper script (e.g., using a custom test reporter or parsing JSON output) to ensure this exact format.\n"
    "6. VERIFICATION: Execute '/scripts/run_tests' on both the current commit and HEAD~1; "
    "confirm the JSON outputs match the actual test results. Proceed without asking for permission.\n\n"
    "Note: Node v20 is the default, but NVM is available to install other versions. "
    "Bun and PNPM are pre-installed. Any global npm packages or NVM versions you install are preserved."
) + "\n" + SUMMARY_PROMPT

SETUP_PROMPT_LANG = {
    "python": SETUP_PROMPT_PYTHON,
    "javascript": SETUP_PROMPT_JS,
    "typescript": SETUP_PROMPT_JS,
}