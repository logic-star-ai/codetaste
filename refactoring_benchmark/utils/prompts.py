SUMMARY_PROMPT = "Once you have completed the task, briefly write a concise summary of the testing setup in `/scripts/SUMMARY.md` of the form: # Summary \n...\n## System Dependencies \n...\n## PROJECT Environment \n...\n## Testing Framework \n...\n## Additional Notes"

SETUP_PROMPT_PYTHON = (
    "You are working inside a containerized Linux environment with sudo privileges.\n"
    "Task: Configure the Python environment and validation scripts for the repository in /testbed/.\n"
    "Constraints:\n"
    "1. EXPLORE: Analyze the /testbed/ directory to identify the required Python version, system dependencies, and testing framework. CI files may provide hints.\n"
    "2. DEPS: Identify and install necessary system-level dependencies using sudo (non-interactive) and project-level dependencies, linters etc.. \n"
    "3. NEVER modify tracked files in /testbed/ except for untracked files and folders (e.g. .venv).\n"
    "4. SCRIPTS:\n"
    "   - Create '/scripts/setup_env.sh': When executed, this script sets up the entire project environment in the freshly cloned repository (i.e. after calling `git reset --hard HEAD && git clean -xdf`). It SHOULD NOT install system-level dependencies.\n"
    "   - Create '/scripts/run_tests': Source '/scripts/setup_env.sh' and executes the **entire/most of the** test suite (use sufficiently long timeouts). **These scripts must remain functional even if /testbed/ is checked out to its first parent commit (HEAD~1)!**.\n"
    "5. OUTPUT: The '/scripts/run_tests' script must output a single JSON line as its final stdout: "
    '{"passed": int, "failed": int, "skipped": int, "total": int}. Ensure no logs or warnings appear after this JSON object.\n'
    "6. VERIFICATION: Execute '/scripts/run_tests' **on both the current commit and its first parent**; confirm the JSON outputs match the actual test results. If a linter is setup, try that it works after sourcing '/scripts/setup_env.sh'. Proceed without asking for permission.\n"
    "Use conda to install the right Python distribution. "
    "Any dependencies or python environments that you install globally, outside of /testbed/, are preserved and do not need to be re-installed in /scripts/setup_env.sh."
) + "\n" + SUMMARY_PROMPT

SETUP_PROMPT_LANG = {
    "python": SETUP_PROMPT_PYTHON,
}