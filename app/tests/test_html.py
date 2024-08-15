import pytest
from app.core.html.html_parsers import clc_parser
from app.models.reservation_models import ReservationDetails


@pytest.fixture
def clc_model() -> ReservationDetails:
    return ReservationDetails(
        clcReservationNumber="12345678",
        hotelReservationNumber="Updated 8/19",
        reservationCreatedBy="Martin, Tanner",
        status="Your Hotel Reservation Is Confirmed.",
        singles=1,
        doubles=0,
        paymentMethod="Direct Bill",
        hotelName="Holiday Inn West Covina (68155)",
        hotelAddress="3223 E Garvey Ave N, West Covina, Ca, 91791",
        hotelPhone="[626] 9668311",
        checkInDate="11-AUG-24",  # type: ignore
        checkOutDate="26-AUG-24",  # type: ignore
        primaryEmployeeNumber="Trmart",
        primaryEmployeeName="Myfirstname Mylastname",
        jobNumber="5648155",
        phase="0000",
        projectManager="Pmfirstlastname",
    )


@pytest.fixture
def clc_html_path() -> str:
    return r"app\resources\templates\message_0.html"


def test_parse_clc_html(clc_model: ReservationDetails, clc_html_path: str):
    with open(clc_html_path, "r") as file:
        html_content = file.read()

    reservation_model = clc_parser.parse_html_to_model(html_content)
    assert reservation_model.clc_reservation_number == clc_model.clc_reservation_number
    assert (
        reservation_model.hotel_reservation_number == clc_model.hotel_reservation_number
    )
    assert reservation_model.reservation_created_by == clc_model.reservation_created_by
    assert reservation_model.status == clc_model.status
    assert reservation_model.singles == clc_model.singles
    assert reservation_model.doubles == clc_model.doubles
    assert reservation_model.payment_method == clc_model.payment_method
    assert reservation_model.hotel_name == clc_model.hotel_name
    assert reservation_model.hotel_address == clc_model.hotel_address
    assert reservation_model.hotel_phone == clc_model.hotel_phone
    assert reservation_model.check_in_date == clc_model.check_in_date
    assert reservation_model.check_out_date == clc_model.check_out_date
    assert (
        reservation_model.primary_employee_number == clc_model.primary_employee_number
    )
    assert reservation_model.primary_employee_name == clc_model.primary_employee_name
    assert reservation_model.job_number == clc_model.job_number
    assert reservation_model.phase == clc_model.phase
    assert reservation_model.project_manager == clc_model.project_manager
