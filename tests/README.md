# testing 🧪

## running the testsuite 🔬

* create a venv for gedcom2csv if you don't already have one:

```bash
# clone the repo
some_local_dir $ git clone git@github.com:joephayes/gedcom2csv.git
some_local_dir $ cd gedcom2csv

# create venv if it doesn't already exist
gedcom2csv $ python -m venv --prompt gedcom2csv venv
gedcom2csv $ source venv/bin/activate
(gedcom2csv) gedcom2csv $ pip install --upgrade pip --quiet
(gedcom2csv) gedcom2csv $ pip install -e '.[dev]' --quiet
```

* to run tests in you IDE, e.g. VSCode:

```bash
# launch VSCode from the project root dir
(gedcom2csv) gedcom2csv $ code .

then in VSCode:

    * View -> Command Palette... -> Configure: Python Tests
    * select pytest
    * select tests as the directory containing tests
    * click on the beaker icon to open the test explorer
    * debug/run tests from there
```

* to run them in your current venv:
```bash
(gedcom2csv) gedcom2csv $ pytest
```

* to run the tests in a clean environment:
```bash
(gedcom2csv) gedcom2csv $ tox
```
this will also run the mypy type-checker, check code coverage, and generate a coverage report in `coverage_report_html/index.html`
