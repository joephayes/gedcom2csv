import os

from gedcom2csv.transformer import Gedcom2CSV


def test_convert_gedcom_to_csv(test_data_dir):
    expected_file_name = os.path.join(test_data_dir, "expected.csv")
    with open(expected_file_name, "r") as ef:
        expected_csv_string = ef.read()

    test_file_name = os.path.join(test_data_dir, "test.ged")
    transformer = Gedcom2CSV()
    csv_string = transformer.convert_to_csv(test_file_name)

    assert expected_csv_string == csv_string
