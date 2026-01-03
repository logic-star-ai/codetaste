ENVIRONMENT = """## Your Environment

You operate in a containerized, non-interactive **polyglot development environment** based on **Ubuntu 24.04**.

### **Core Runtimes**

* **Python:** Managed by `uv` (versions **3.8, 3.9, 3.10, 3.11**, see `uv python list`).
* **Node.js:** **v22.12.0** (via NVM `nvm`) with **TypeScript**, `ts-node`, and `vercel`.
* **Go:** **v1.23.4** (Global toolchain).
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
* **Key Paths:** Tools are pre-configured in `$PATH` (Node, Rust, .NET, Go, uv).
"""

TASK = """## Task

Configure the development environment and validation scripts for the repository located in `/testbed/`.

**Constraints:**

1. **EXPLORE:** Analyze the `/testbed/` directory to identify the primary programming language, required runtime versions (e.g., via version files or manifests), the preferred package manager, and the testing framework used.
2. **DEPS:** Identify and install necessary system-level dependencies using `sudo` (non-interactive) and all project-level dependencies. Ensure any external binaries or drivers required by the test suite (e.g., browser engines, compilers, or database headers) are installed immediately. Anything installed inside `/testbed/` will be wiped on exit!
3. **INTEGRITY:** NEVER modify files in /testbed/ directly, any changes you perform will be wiped after you exit! `/scripts/setup_shell.sh` can setup /testbed directory, however it should NOT modify versioned files in `/testbed/`, i.e. it should only modify files or folders that are explicitly ignored by the version control system (e.g., build artifacts, dependency directories, cache). `git status` must show no changes.
4. **SCRIPTS:**
* **Create `/scripts/setup_system.sh`:** 
    Executed with `sudo` prior to running the tests, this script performs runtime system configuration (e.g., starting database services, Redis, or configuring system limits). 
    It should **not** install packages. If no system services are required, create a script that exits 0.
* **Create `/scripts/setup_shell.sh`:** 
    When sourced, this script configures the shell environment for the project **and** to run tests:
        - activate virtual environment if necessary.
        - install local project dependencies and linters. 
        - set up all environment variables.
        - selects the correct runtime versions.
        - Project and dependency installations that change files in `/testbed/` MUST be performed in this script.
    It must **NOT** require `sudo`. It must be idempotent (safe to run multiple times) and avoid redundant installations. 
* **Create `/scripts/run_tests`:** This script must be self-contained and execute the test suite (or a relatively large and representative subset that finishes in up to 15 minutes). It will be invoked as follows: `git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests`. 
    `/scripts/run_tests` must NOT setup the environment, environment variables, shell or similar, it should rely on the previous scripts having been run before. `/scripts/run_tests` must only run and parse tests. It should be invoked like : `/scripts/setup_shell.sh && /scripts/run_tests` to run tests in an already setup shell. `/scripts/setup_shell.sh` sets up the environment and environment variables.
* **Portability:** These scripts **must remain functional** even if `/testbed/` is checked out to THE previous commit (in other words: `HEAD~1`). I.e. they should work on HEAD and HEAD~1 without any modifications.
5. **OUTPUT:** The `/scripts/run_tests` script must output exactly one JSON line as its final `stdout` message:
`{"passed": int, "failed": int, "skipped": int, "total": int}`. 
Where the int value corresponds to the number of tests that passed, failed, were skipped, and the total number of representative tests run.
You may need to write a wrapper or use a custom test reporter to ensure this exact format is captured.
6. **VERIFICATION:** Always execute `source /scripts/setup_shell.sh && /scripts/run_tests` in a single shell command (in an environment that is clean -> `git clean -xdff` and has system services running `/scripts/setup_system.sh`) on both the current commit and `HEAD~1`. Confirm the JSON outputs accurately reflect the test results.
Your shell doesn't persist environment across shell commands.

**Note:** Multiple runtimes (Python, Node, Rust, .NET, Java, GO) and their respective version managers are pre-installed. Any global configurations or runtime versions you install will be preserved across the session.
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
