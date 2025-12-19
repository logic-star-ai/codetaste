SETUP_PROMPT_PYTHON = (
    "Task: Configure the Python environment and validation scripts for the repository in /testbed/.\n"
    "Constraints:\n"
    "1. SYSTEM DEPS: Explore the repository and ci files. Identify and install necessary system-level dependencies using sudo (non-interactive) and project-level dependencies. \n"
    "2. NEVER modify tracked files in /testbed/ except for untracked files and folders (e.g. .venv).\n"
    "3. SCRIPTS:\n"
    "   - Create '/scripts/setup_env.sh': When executed, this script sets up the entire project environment in the freshly cloned repository. (i.e. after calling `git reset --hard HEAD && git clean -fd`). It SHOULD NOT install system-level dependencies.\n"
    "   - Create '/scripts/run_tests': Source '/scripts/setup_env.sh' and executes the test suite.\n"
    "4. OUTPUT: The '/scripts/run_tests' script must output a single JSON line as its final stdout: "
    '{"passed": int, "failed": int, "skipped": int, "total": int}. Ensure no logs or warnings appear after this JSON object.\n'
    "5. VERIFICATION: Execute '/scripts/run_tests' and confirm the JSON output matches the actual test results. Proceed without asking for permission.\n"
    "Use conda to install the right Python distribution."
)
