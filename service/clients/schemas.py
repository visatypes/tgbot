from pydantic import BaseModel


class Country(BaseModel):
    uid: int
    name: str
    desc: str


class Visa(BaseModel):
    uid: int
    country_id: int
    name: str
    desc: str

    @property
    def display(self) -> str:
        return f'{self.name} \n{self.desc}'
