import logging

from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

logger = logging.getLogger(__name__)


class Gedcom2CSV:
    def __init__(self):
        self.gedcom_parser = Parser()

    @staticmethod
    def _formatGedcomDate(date_string: str) -> str:
        return (
            date_string.lower()
            .replace("abt abt", "abt")
            .replace("abt", "ca.")
            .replace("bef bef", "bef")
            .replace("bef ", "before ")
            .replace("aft aft", "aft")
            .replace("aft ", "after")
            .replace("bet", "")
            .replace("and", "-")
            .replace("jan", "Jan")
            .replace("feb", "Feb")
            .replace("mar", "Mar")
            .replace("apr", "Apr")
            .replace("may", "May")
            .replace("jun", "Jun")
            .replace("jul", "Jul")
            .replace("aug", "Aug")
            .replace("sep", "Sep")
            .replace("oct", "Oct")
            .replace("nov", "Nov")
            .replace("dec", "Dec")
        )

    @staticmethod
    def _get_titles(element: IndividualElement) -> list[str]:
        titles = []

        for child in element.get_child_elements() or []:
            if child.get_tag() in ["NOBI", "NPFX", "TITL"]:
                titles.append(child.get_value())

        return titles

    def convert_to_csv(self, gedcom_file: str) -> str:
        logger.info(f"Converting GEDCOM file {gedcom_file} into a CSV graph")

        self.gedcom_parser.parse_file(gedcom_file)

        root_child_elements = self.gedcom_parser.get_root_child_elements()

        outfile_contents = []

        outfile_contents.append(
            ",".join(
                [
                    "id",
                    "name",
                    "gender",
                    "birth date",
                    "birth place",
                    "death date",
                    "place of death",
                    "title",
                ]
            )
        )

        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                row = []
                name = element.get_name()
                if name[0] == "Unnamed":
                    continue

                record_id = element.get_pointer().replace("@", "").lower()

                row.append(record_id)
                row.append(" ".join(filter(None, name)))

                gender = element.get_gender()

                row.append(gender)

                birth_data = element.get_birth_data()

                row.append(self._formatGedcomDate(birth_data[0]))
                if birth_data[1] and birth_data[1].strip():
                    row.append(format('"%s"' % birth_data[1]))
                else:
                    row.append("")

                death_data = element.get_death_data()

                row.append(self._formatGedcomDate(death_data[0]))
                if death_data[1] and death_data[1].strip():
                    row.append(format('"%s"' % death_data[1]))
                else:
                    row.append("")

                titles = self._get_titles(element)
                titles_str = ",".join(filter(None, titles))
                if titles_str and titles_str.strip():
                    row.append(format('"%s"' % titles_str))
                else:
                    row.append("")

                outfile_contents.append(",".join(row))

        return "\n".join(outfile_contents)
