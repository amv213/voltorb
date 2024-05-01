import nox

nox.options.envdir = ".cache/nox"
nox.options.default_venv_backend = "uv"

# all external utility tools used by the nox sessions
BUILD_TOOLS = ["build"]
COVERAGE_TOOLS = [
    "coverage[toml]",
    "coverage-badge",
    "setuptools",
]  # setuptools required with uv as coverage-badge imports pkg_resources
FORMATTING_TOOLS = ["ruff~=0.4.0"]
LINTING_TOOLS = FORMATTING_TOOLS
LOCKFILE_TOOLS = ["pip-tools>=7.0.0"]
TYPING_TOOLS = ["mypy"]

LOCKFILE_PATH = "pylock.txt"

COVERAGE_REPORTS_DIR = "artefacts/reports/coverage"
TEST_REPORTS_DIR = "artefacts/reports"


@nox.session
def dist_build(session: nox.Session) -> None:
    """Builds distributions (sdist and wheel).

    Examples:
        nox -s dist_build
    """

    session.run("rm", "-rf", "dist", external=True)
    session.install(*BUILD_TOOLS)
    session.run("python", "-m", "build")


@nox.session
def formatting_check(session: nox.Session) -> None:
    """Checks codebase formatting.

    Examples:
        nox -s formatting_check
    """
    session.install(*FORMATTING_TOOLS)
    session.run("ruff", "check", "--select", "I")
    session.run("ruff", "format", "--check", *session.posargs)


@nox.session
def formatting_fix(session: nox.Session) -> None:
    """Fixes codebase formatting.

    Examples:
        nox -s formatting_fix
    """
    session.install(*FORMATTING_TOOLS)
    session.run("ruff", "check", "--select", "I", "--fix")
    session.run("ruff", "format", *session.posargs)


@nox.session
def linting_check(session: nox.Session) -> None:
    """Checks codebase lint quality.

    Examples:
        nox -s linting_check
    """
    session.install(*LINTING_TOOLS)
    session.run("ruff", "check", *session.posargs)


@nox.session
def linting_fix(session: nox.Session) -> None:
    """Fixes codebase lint quality where possible.

    Examples:
        nox -s linting_fix
    """
    session.install(*LINTING_TOOLS)
    session.run("ruff", "--fix", *session.posargs)


@nox.session
def typing_check(session: nox.Session) -> None:
    """Checks codebase static typing.

    Examples:
        nox -s typing_check
    """
    session.install(".[tests]", *TYPING_TOOLS, "--constraint", LOCKFILE_PATH)
    session.run("mypy", *session.posargs)


@nox.session
def dependencies_pin(session: nox.Session) -> None:
    """Generates a package dependencies' lockfile.

    Examples:
        nox -s dependencies_pin
    """
    session.install(*LOCKFILE_TOOLS)

    session.run(
        "pip-compile",
        "--verbose",
        "--strip-extras",
        "--no-emit-index-url",
        "--no-emit-trusted-host",
        "pyproject.toml",
        "-o",
        LOCKFILE_PATH,
        "--upgrade",
        env={"CUSTOM_COMPILE_COMMAND": f"nox -s {session.name}"},
    )
    session.log(f"Lockfile generated at {LOCKFILE_PATH!r} ✨")


@nox.session
def tests_run(session: nox.Session) -> None:
    """Runs tests and doctests.

    Examples:
        nox -s tests_run
    """

    # Run tests
    session.install(".[tests]", "--constraint", LOCKFILE_PATH)

    doctests_target_dir = "src/"
    tests_target_dir = "tests/"

    coverage_datafile_path = f"{COVERAGE_REPORTS_DIR}/.coverage"
    junitxml_path = f"{TEST_REPORTS_DIR}/.junitxml.xml"

    session.run(
        "coverage",
        "run",
        f"--data-file={coverage_datafile_path}",
        "-m",
        "pytest",
        f"--junitxml={junitxml_path}",
        doctests_target_dir,
        tests_target_dir,
        *session.posargs,
    )

    session.notify("coverage_report")


@nox.session
def coverage_report(session: nox.Session) -> None:
    """Generates coverage reports.

    This session is usually triggered following a pytest coverage session generating
    the coverage data files to build the reports on.

    Examples:
        nox -s coverage_report
    """

    session.install(*COVERAGE_TOOLS)

    # Output coverage reports in same folder (for convenience)
    data_file = f"{COVERAGE_REPORTS_DIR}/.coverage"
    session.run("coverage", "report", "--data-file", data_file)
    session.run(
        "coverage",
        "html",
        "--data-file",
        data_file,
        "-d",
        f"{COVERAGE_REPORTS_DIR}/html",
    )
    session.run(
        "coverage",
        "xml",
        "--data-file",
        data_file,
        "-o",
        f"{COVERAGE_REPORTS_DIR}/coverage.xml",
    )
    session.run(
        "coverage",
        "json",
        "--data-file",
        data_file,
        "-o",
        f"{COVERAGE_REPORTS_DIR}/coverage.json",
    )

    session.notify("coverage_build_badge")


@nox.session
def coverage_build_badge(session: nox.Session) -> None:
    """Generates a coverage badge.

    This session is usually triggered following a pytest coverage session generating
    the coverage data files for which to build the badge.

    Examples:
        nox -s coverage_build_badge
    """

    # coverage-badge only works from the same directory where the .coverage
    # data file is located.
    session.chdir(COVERAGE_REPORTS_DIR)

    badge_filename = "coverage.svg"

    # cleanup old badge
    session.run("rm", "-rf", badge_filename, external=True)

    session.install(*COVERAGE_TOOLS)
    session.run("coverage-badge", "-o", badge_filename)
