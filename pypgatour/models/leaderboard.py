from .camel_case import CamelizedModel
from datetime import datetime
from pydantic import Field
from typing import Annotated, Dict, List, Optional, Union, Literal


class CutLine(CamelizedModel):
    show_cut_line: bool
    cut_count: Optional[int]  # TODO: verify type
    cut_line_score: str
    show_projected: bool
    projected_count: Optional[int]  # TODO: verify type
    paid_players_making_cut: Optional[int]  # TODO: verify type


class Header(CamelizedModel):
    last_updated: datetime
    generated_utc: Optional[datetime] = None
    show_round_title: bool
    hide_tee_times_local: bool


class PlayoffHoleNumber(CamelizedModel):
    type: Literal["holeNumber"]
    holes: List[str]


class PlayoffCourseHole(CamelizedModel):
    type: Literal["courseHole"]
    holes: List[str]


class PlayoffPar(CamelizedModel):
    type: Literal["par"]
    holes: List[Union[int, str]]


class PlayoffPlayer(CamelizedModel):
    type: Literal["player"]
    title: str
    status: str
    holes: List[str]


PlayoffRow = Annotated[
    Union[PlayoffHoleNumber, PlayoffCourseHole, PlayoffPar, PlayoffPlayer],
    Field(discriminator="type"),
]


class Playoff(CamelizedModel):
    playoff_present: bool
    playoff_rows: List[PlayoffRow]


class PositionMovement(CamelizedModel):
    value: str
    direction: Optional[str]


class Round(CamelizedModel):
    title: str
    strokes: str


class Ranks(CamelizedModel):
    money_rank: str
    schwab_rank: str
    rank: str
    points_rank: str
    cup_rank: str


class PlayerNames(CamelizedModel):
    is_member: bool
    short_name: str
    last_name: str
    first_name: str
    player_name_add_ons: str


class Row(CamelizedModel):
    is_active: bool
    index: int
    status: str
    round_complete: bool
    row_id: str
    player_id: str
    group_id: str
    tournament_round_id: str
    player_round_id: str
    current_hole_id: str
    can_open_drawer: bool
    starting_hole_id: str
    position_current: str
    wyndham_winner: bool
    show_tee_time: bool
    position_movement: PositionMovement
    total: str
    thru: str
    tee_time: Optional[str]  # TODO: verify type
    round: str
    rounds: List[Round]
    strokes: str
    original_sort_index: int
    country: str
    projected_ranks: Ranks
    start_ranks: Ranks
    shottext: Optional[str]  # TODO: verify type
    ocqs: bool
    course_id: str
    courses_by_rounds: Dict[str, str]
    player_names: PlayerNames


class Leaderboard(CamelizedModel):
    format: str
    tournament_round_id: int
    rounds_for_table_header: List[str]
    cut_lines: List[CutLine]
    header: Header
    scoring_type: str
    playoff: Playoff
    rows: List[Row]
