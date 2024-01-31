import nox

versions = ["3.8", "3.9", "3.10", "3.11"]

@nox.session(python=versions)
def test(session):
    session.install(".")
    
    for v in versions:
        session.run("pytest")

@nox.session(python=versions)
def format(session):
    #install code formatters
    session.install("black", "isort")
    #run code formatters
    session.run("black","src","tests")
    session.run("isort","src","tests")

@nox.session(python=versions[-1])
def lint(session):
    #install linter
    session.install("flake8")
    #run linter
    session.run("flake8")