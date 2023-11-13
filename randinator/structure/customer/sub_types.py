from typing import Optional

from isv2 import PydanticModel


class PaymentDetailsSchema(PydanticModel):
    payment_method: Optional[str] = ""
    payment_term: Optional[str] = ""


class ContactSchema(PydanticModel):
    uuid: UUID4Str
    name: str
    email: str
    fax: str
    phone: str
    phone_description: str


class AddressDetailSchema(PydanticModel):
    city: str
    country_region_id: str
    country_region_iso_code: str
    country_name: str
    description: Optional[str] = "Billing Address"
    state: Optional[str] = ""
    street: str
    street_number: Optional[str] = ""
    zip_code: str


class DimensionSchema(PydanticModel):
    key: str
    value: str


class D365DetailsSchema(PydanticModel):
    customer_group_id: str
    # finance_ref in payload maps to customer_account here
    customer_account: Optional[str] = ""
    data_area_id: str
    # name in payload maps to organization_name here
    organization_name: Optional[str] = ""
    organization_number: str
    language_id: str
    clauk_account_manager: str
    clauk_sector_dim: DimensionSchema
    clauk_vertical_dim: DimensionSchema
    clauk_segment_dim: DimensionSchema
    sales_tax_group: str
    sales_currency_code: str
