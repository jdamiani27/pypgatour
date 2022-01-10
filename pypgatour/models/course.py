from typing import List
from .camel_case import CamelizedModel


class Coordinate(CamelizedModel):
    x: str
    y: str
    z: str


class HoleRound(CamelizedModel):
    round_id: str
    par: str
    distance: str
    tee: Coordinate
    pin: Coordinate
    stimp: str


class AdditionalData(CamelizedModel):
    fov: str
    lens: str
    roll: str


class Hole(CamelizedModel):
    hole_id: str
    rounds: List[HoleRound]
    rank: str
    green_camera: Coordinate
    green_target: Coordinate
    hole_camera: Coordinate
    hole_target: Coordinate
    green_additional_data: AdditionalData
    hole_additional_data: AdditionalData


class Course(CamelizedModel):
    course_id: str
    course_code: str
    is_host: bool
    par_in: str
    par_out: str
    par_total: str
    holes: List[Hole]
    msg_id: str
