from core.mail.outlook import Outlook

from core.html.html_parsers.clc_parser import parse_html_to_model


def get_outlook_messages():
    max_messages = 1
    outlook = Outlook()
    for message_idx, message in enumerate(outlook.scan_inbox()):
        if message_idx >= max_messages:
            break
        print(f"Subject: {message.subject}")


def parse_clc_html_template():
    # Example usage
    with open(r"app\resources\templates\message_0.html", "r") as file:
        html_content = file.read()
    # Replace with the actual HTML content
    reservation_model = parse_html_to_model(html_content)
    print(reservation_model)


if __name__ == "__main__":
    get_outlook_messages()
    parse_clc_html_template()
