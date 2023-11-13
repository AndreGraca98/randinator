

from typing import Optional

from isv2 import PydanticModel
from isv2.structure.customer.sub_types import PaymentDetailsSchema
from isv2.structure.meta import Meta
from pydantic import Field


class Customer(PydanticModel):

    meta: Meta
    customer_uuid: str
    name: str
    finance_ref: str
    on_hold: Optional[bool] = False
    messages: Optional[list[str]] = Field(default_factory=list)
    payment_details: PaymentDetailsSchema
    primary_contact_id: UUID4Str
    contacts: list[ContactSchema]
    address_details: AddressDetailSchema
    d365_details: D365DetailsSchema

    @property
    def billing_address(self):
