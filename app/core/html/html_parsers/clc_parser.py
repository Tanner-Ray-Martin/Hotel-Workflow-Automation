from bs4 import BeautifulSoup
from models.reservation_models import ReservationDetails

BAD_TEXT_IS = ["", "Hotel"]
BAD_TEXT_CONTAINS = ["Thank You For Choosing", "This Message", " Policy: "]
BAD_TEXT_STARTS_WITH = ["At "]


def is_valid_column_text(text):
    valid = True
    for bad_text in BAD_TEXT_CONTAINS:
        if bad_text in text:
            valid = False
            break
    for bad_text in BAD_TEXT_STARTS_WITH:
        if text.startswith(bad_text):
            valid = False
            break
    for bad_text in BAD_TEXT_IS:
        if text == bad_text:
            valid = False
            break
    return valid


def is_valid_columns(columns):
    return len(columns) > 1


def clean_text(text: str):
    text = text.strip()
    if text.endswith(":"):
        text = text[:-1]
    return text.title()


def fix_columns_or_none(new_columns: list[str | None]):
    if not is_valid_columns(new_columns):
        return None
    if len(new_columns) == 1:
        new_columns.append(None)
    return new_columns


def large_row_to_many(columns):
    new_columns = []
    for column in columns:
        if "Your Hotel Reservation" in column:
            new_columns.append(["Status", column])
        elif "Singles" in column and "Doubles" in column:
            column = column.replace(",", "")
            singles = column.split("Singles")[0].strip()
            column = column.split("Singles")[1].strip()
            doubles = column.split("Doubles")[0].strip()
            new_columns.append(["Singles", singles])
            new_columns.append(["Doubles", doubles])
        elif "(" in column and column.endswith(")"):
            new_columns.append(["Hotel Name", column])

        elif column.count(",") > 2:
            new_columns.append(["Hotel Address", column])
        elif "]" in column and column.startswith("["):
            new_columns.append(["Hotel Phone", column])
    if len(new_columns) == 0:
        new_columns.append(columns)
    return new_columns


def parse_html_to_model(html):
    row_replacements = [
        (
            "<br>",
            "</span></b></p></td><td><p><b><span style='font-size:9.0pt;font-family:\"Arial\",sans-serif;color:black'>",
        )
    ]
    for replacte_this, with_this in row_replacements:
        html = html.replace(replacte_this, with_this)
    soup = BeautifulSoup(html, "html.parser")

    # Initialize a dictionary to store the scraped data
    reservation_info = {}

    # Find all rows in the table
    rows = soup.find_all("tr")

    # Extract the relevant information from the rows
    for row in rows:
        columns = row.find_all("td")
        new_columns = [
            clean_text(column.text)
            for column in columns
            if is_valid_column_text(clean_text(column.text))
        ]

        new_columns = fix_columns_or_none(new_columns)

        # Skip empty rows
        if not new_columns:
            continue

        for new_columns in large_row_to_many(new_columns):
            key = new_columns[0]
            value = new_columns[1]
            key = key.replace(" ", "")
            key = key[0].lower() + key[1:]
            reservation_info[key] = value
    return ReservationDetails(**reservation_info)
