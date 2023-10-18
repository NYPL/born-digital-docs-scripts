import nox

versions = ["3.8", "3.9", "3.10", "3.11"]

@nox.session(python=versions)
def py_tests(session):
    session.install(".")

    for v in versions:
        session.run("pytest")

@nox.session(python=versions)
def lint(session):
    session.install("flake8")
    session.run("flake8")