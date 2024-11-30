import csv
import io
import logging

from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

logger = logging.getLogger(__name__)


class Gedcom2CSV:
    def __init__(self):
        self.gedcom_parser = Parser()
        self.fieldnames = [
            "id",
            "name",
            "name variations",
            "gender",
            "birth date",
            "birth place",
            "death date",
            "place of death",
            "title",
        ]

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
        logger.info(f"Converting GEDCOM file {gedcom_file} into a CSV file")

        out = io.StringIO()

        self.gedcom_parser.parse_file(gedcom_file)

        root_child_elements = self.gedcom_parser.get_root_child_elements()

        writer = csv.DictWriter(out, fieldnames=self.fieldnames, lineterminator="\n")
        writer.writeheader()

        for element in root_child_elements:
            if isinstance(element, IndividualElement):
                name = element.get_name()
                if name[0] == "Unnamed":
                    continue

                def process_name(name: str) -> str | None:
                    name_elements = name.split("/")
                    if name_elements:
                        return " ".join(
                            [ne.strip() for ne in filter(None, name_elements)]
                        )
                    return None

                # alternate names are the other names attached to an individual (so we skip the first one)
                alternate_names = [
                    process_name(n) for n in ((element.get_all_names() or [])[1:])
                ]
                record_id = element.get_pointer().replace("@", "").lower()
                gender = element.get_gender()
                birth_data = element.get_birth_data()
                death_data = element.get_death_data()
                titles = self._get_titles(element)
                titles_str = ",".join(filter(None, titles))

                item = {
                    "id": record_id,
                    "name": " ".join(filter(None, name)),
                    "name variations": ",".join(filter(None, alternate_names or [])),
                    "gender": gender,
                    "birth date": self._formatGedcomDate(birth_data[0]),
                    "birth place": birth_data[1]
                    if birth_data[1] and birth_data[1].strip()
                    else None,
                    "death date": self._formatGedcomDate(death_data[0]),
                    "place of death": death_data[1]
                    if death_data[1] and death_data[1].strip()
                    else None,
                    "title": titles_str if titles_str and titles_str.strip() else None,
                }

                writer.writerow(item)

        return out.getvalue()
