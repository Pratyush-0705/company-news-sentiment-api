from pydantic import BaseModel, Field


class CompanyRequest(BaseModel):
    company: str = Field(
        ...,
        min_length=1,
        example="Tesla"
    )

    days: int = Field(
        default=90,
        ge=1,
        le=365,
        example=90
    )