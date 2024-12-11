import os

from gedcom.element.individual import IndividualElement

from gedcom2csv.transformer import Gedcom2CSV


def test_convert_gedcom_to_csv(test_data_dir):
    expected_file_name = os.path.join(test_data_dir, "expected.csv")
    with open(expected_file_name, "r") as ef:
        expected_csv_string = ef.read()

    test_file_name = os.path.join(test_data_dir, "test.ged")
    transformer = Gedcom2CSV()
    csv_string = transformer.convert_to_csv(test_file_name)

    assert expected_csv_string == csv_string


def test_get_titles():
    element = IndividualElement(level=0, pointer="@I5@", tag="INDI", value="")
    name = element.new_child_element(tag="NAME", value="First /Last/")
    element.new_child_element(tag="SEX", value="M")
    name.new_child_element(tag="GIVN", value="First")
    name.new_child_element(tag="SURN", value="Last")
    name.new_child_element(tag="NPFX", value="Lord of This and That")
    print(f"gedcom string: {element.to_gedcom_string(True)}")

    all_titles = Gedcom2CSV._get_titles(element)
    assert len(all_titles) == 1

    element = IndividualElement(level=0, pointer="@I6@", tag="INDI", value="")
    element.new_child_element(tag="NAME", value="First /Last/")
    element.new_child_element(tag="SEX", value="M")
    element.new_child_element(tag="GIVN", value="First")
    element.new_child_element(tag="SURN", value="Last")
    element.new_child_element(tag="NPFX", value="Lord of This and That")

    all_titles = Gedcom2CSV._get_titles(element)
    assert len(all_titles) == 1
