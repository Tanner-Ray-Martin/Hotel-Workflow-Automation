from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime as dt


# Define the Pydantic model
class ReservationDetails(BaseModel):
    clc_reservation_number: Optional[str] = Field(..., alias="clcReservationNumber")
    hotel_reservation_number: Optional[str] = Field(..., alias="hotelReservationNumber")
    reservation_created_by: Optional[str] = Field(..., alias="reservationCreatedBy")
    status: str
    singles: Optional[int]
    doubles: Optional[int]
    payment_method: Optional[str] = Field(..., alias="paymentMethod")
    hotel_name: str = Field(..., alias="hotelName")
    hotel_address: str = Field(..., alias="hotelAddress")
    hotel_phone: str = Field(..., alias="hotelPhone")
    check_in_date: date = Field(..., alias="check-InDate")
    check_out_date: date = Field(..., alias="check-OutDate")
    primary_employee_number: Optional[str] = Field(..., alias="primaryEmployeeNumber")
    primary_employee_name: str = Field(..., alias="primaryEmployeeName")
    job_number: str = Field(..., alias="jobNumber")
    phase: Optional[str]
    project_manager: str = Field(..., alias="projectManager")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    @field_validator("check_in_date", "check_out_date", mode="before")
    def fix_dates(cls, v):
        if isinstance(v, str):
            return dt.strptime(v, "%d-%b-%y").date()
        return v
