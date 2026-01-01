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
    "2. DEPS: Identify and install necessary system-level dependencies using sudo (non-interactive) and project-level dependencies. Install all dependencies NOW.\n"
    "3. NEVER modify files in /testbed/, except for files and folders that appear in .gitignore (e.g. .venv). This means that `git status` should show no changes after running tests.\n"
    "4. SCRIPTS:\n"
    "   - Create '/scripts/setup_system.sh': Executed with sudo privileges. This script performs runtime system setup (e.g., starting database services, Redis, etc.). It should NOT install dependencies. If no runtime services are needed, create an empty script or a script that just exits 0.\n"
    "   - Create '/scripts/setup_shell.sh': When executed (sourced), this script sets up the project environment (Python virtualenv, conda, etc.). It SHOULD NOT install system-level dependencies. Use `uv` for speed or `conda` for complex environments. It must NOT require sudo rights. It should be idempotent and not reinstall everything everytime. \n"
    "   - Create '/scripts/run_tests': This script should not reference other scripts. It should be run like `git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests` on the two hashes. "
    "and execute the test suite (or a relatively large representative subset of it, but finish within maximum 10 minutes). These scripts **must remain functional** even if /testbed/ is checked out to HEAD~1.\n"
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
    "2. DEPS: Identify and install necessary system-level dependencies using sudo (non-interactive) and project-level dependencies. Only dependencies stored outside of /testbed/ will persist!"
    "If Playwright or Cypress is used, ensure browser binaries are installed via `npx playwright install` if not already present. Install all dependencies NOW.\n"
    "3. NEVER modify files in /testbed/, except for files and folders that appear in .gitignore (e.g., node_modules, .next, dist). "
    "This means that `git status` should show no changes after running tests.\n"
    "4. SCRIPTS:\n"
    "   - Create '/scripts/setup_system.sh': Executed with sudo privileges, this script performs runtime system setup (e.g., starting database services, Redis, etc.). It should NOT install dependencies. If no runtime services are needed, create an empty script or a script that just exits 0.\n"
    "   - Create '/scripts/setup_shell.sh': When sourced, this script sets up the project (and shell environment), e.g. activating virtual environment or installing dependencies. It SHOULD NOT install system-level dependencies. It must NOT require sudo rights. It should be idempotent and not reinstall everything everytime. "
    "Use `nvm` to switch Node versions if necessary and the detected package manager for installation.\n"
    "   - Create '/scripts/run_tests': This script should not reference other scripts. It should be run like `git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests` on the two hashes. "
    "and execute the test suite (or a relatively large representative subset of it, but finish within maximum 10 minutes). These scripts **must remain functional** even if /testbed/ is checked out to HEAD~1.\n"
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
    "javascript": SETUP_PROMPT_JAVASCRIPT,
    "typescript": SETUP_PROMPT_JAVASCRIPT,
}

ENVIRONMENT = """## Your Environment

You operate in a containerized, non-interactive **polyglot development environment** based on **Ubuntu 24.04**.

### **Core Runtimes**

* **Python:** Managed by `uv` (versions **3.8, 3.9, 3.10, 3.11**, see `uv python list`).
* **Node.js:** **v22.12.0** (via NVM `nvm`) with **TypeScript**, `ts-node`, and `vercel`.
* **Rust:** Full toolchain (Cargo/Rustup) in `/opt/rust`.
* **.NET:** **SDK 8.0** (LTS).
* **C/C++:** GCC, Clang, CMake, and `build-essential`.
* **Java:** OpenJDK (`default-jdk`).

### **Pre-installed Tools**

* **Testing:** **Playwright** (with Chromium and system deps).
* **System:** `git`, `curl`, `wget`, `vim`, `sudo`, and build libraries (SSL, ffi, sqlite).

### **Environment Specs**

* **User:** `benchmarker` (non-root with passwordless `sudo`).
* **Repository Directory:** `/testbed`. `/testbed` is wiped on exit.
* **Key Paths:** Tools are pre-configured in `$PATH` (Node, Rust, .NET, uv).
"""

TASK = """## Task

Configure the development environment and validation scripts for the repository located in `/testbed/`.

**Constraints:**

1. **EXPLORE:** Analyze the `/testbed/` directory to identify the primary programming language, required runtime versions (e.g., via version files or manifests), the preferred package manager, and the testing framework used.
2. **DEPS:** Identify and install necessary system-level dependencies using `sudo` (non-interactive) and all project-level dependencies. Ensure any external binaries or drivers required by the test suite (e.g., browser engines, compilers, or database headers) are installed immediately. Anything installed inside `/testbed/` will be wiped on exit!
3. **INTEGRITY:** NEVER modify files in /testbed/ directly, any changes you perform will be wiped after you exit! `/scripts/setup_shell.sh` can setup /testbed directory, however it should NOT modify versioned files in `/testbed/`, i.e. it should only modify files or folders that are explicitly ignored by the version control system (e.g., build artifacts, dependency directories, cache). `git status` must show no changes.
4. **SCRIPTS:**
* **Create `/scripts/setup_system.sh`:** Executed with `sudo` prior to running the tests, this script performs runtime system configuration (e.g., starting database services, Redis, or configuring system limits). It should **not** install packages. If no system services are required, create a script that exits 0.
* **Create `/scripts/setup_shell.sh`:** When sourced, this script configures the shell environment (e.g. activate virtual environment or set environment variables), selects the correct runtime versions, and installs project dependencies and linters. It must **NOT** require `sudo`. It must be idempotent (safe to run multiple times) and avoid redundant installations where possible. Project installations that change any files in `/testbed/` must be performed here.
* **Create `/scripts/run_tests`:** This script must be self-contained and execute the test suite (or a relatively large and representative subset that finishes in up to 15 minutes). It will be invoked as follows: `git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests`. `/scripts/run_tests` itself must NOT setup the environment, environment variables, shell or similar, it should rely on the previous scripts having been run before. `/scripts/run_tests` must only run and parse tests. It should be invoked like : `/scripts/setup_shell.sh && /scripts/run_tests` to run tests in an already setup shell.
* **Portability:** These scripts **must remain functional** even if `/testbed/` is checked out to THE previous commit (in other words: `HEAD~1`).
5. **OUTPUT:** The `/scripts/run_tests` script must output exactly one JSON line as its final `stdout` message:
`{"passed": int, "failed": int, "skipped": int, "total": int}`.
You may need to write a wrapper or use a custom test reporter to ensure this exact format is captured.
6. **VERIFICATION:** Always execute `source /scripts/setup_shell.sh && /scripts/run_tests` in a single shell command (in an environment that is clean -> `git clean -xdff` and has system services running `/scripts/setup_system.sh`) on both the current commit and `HEAD~1`. Confirm the JSON outputs accurately reflect the test results.
Your shell doesn't persist environment across shell commands.

**Note:** Multiple runtimes (Python, Node, Rust, .NET, Java) and their respective version managers are pre-installed. Any global configurations or runtime versions you install will be preserved across the session.
**Note:** You run in a non-interactive terminal; Proceed with these actions without asking for further permission. Take action and perform the installation and changes.
"""

SUMMARY = """## Final Notes
Once you have completed the task, briefly write a concise summary of the testing setup in `/scripts/SUMMARY.md` of the form:
# Summary
...
## System Dependencies
...
## PROJECT Environment
...
## Testing Framework
...
## Additional Notes
... (e.g. any obstacles or misconfigurations of the environment you encountered)
"""

BOOTSTRAP_PROMPT = ENVIRONMENT + "\n" + TASK + "\n" + SUMMARY