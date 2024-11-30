# gedcom2csv

Reads a GEDCOM file and outputs basic information about individuals in CSV format

### prerequisites
 * python 3.12+


### development

#### create and activate venv
```bash
$ python -m venv --prompt gedcom2csv venv
$ source venv/bin/activate
(gedcom2csv) $ pip install --upgrade pip
```

### install dev dependencies
```bash
(gedcom2csv) $ pip install -e '.[dev]'
```

### testing

see [tests](gedcom2csv/tests/README.md)

### Running

1.  Get GEDCOM file
    ```bash
    $ aws s3 cp s3://nsp-datafiles/nsp.ged ./data
    ```

4. Run GEDCOM to csv converter script

    ```bash
    $ ./scripts/gedcom2csv.sh ./data/nsp.ged ./output/nsp.csv
    ```
