from pydantic import BaseModel


def to_camel(string: str) -> str:
    camel = "".join(word.capitalize() for word in string.split("_"))
    camel = camel[0].lower() + camel[1:]
    return camel


class CamelizedModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
