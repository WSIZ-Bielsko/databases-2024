from pydantic import BaseModel


class Summit(BaseModel):
    id: int
    name: str
    altitude: float
    position_long: float
    position_lat: float


if __name__ == '__main__':
    lonelyMountain = Summit(id=1, name='Lonely Mountain', altitude=441.55, position_long=45.1234, position_lat=67.9854)

    print(lonelyMountain)
