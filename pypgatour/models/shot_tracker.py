from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union
from .camel_case import CamelizedModel
from pydantic import Field, validator


# TODO: Verify if there are other non-required fields
class PlayerHoleMax(CamelizedModel):
    hole_id: str


class RoundSelector(CamelizedModel):
    hide_round_selector: bool
    round_list_items: List[str]


class PlayerData(CamelizedModel):
    show_player: bool
    player_id: str
    player_last_name: str
    player_first_name: str
    player_index: Optional[int] = None
    country: Optional[str] = None
    player_short_name: Optional[str] = None
    hide_dot: Optional[bool] = None
    hide_sponsor: Optional[bool] = None
    hide_flag: Optional[bool] = None


class PlayersData(CamelizedModel):
    team_name: Optional[str]
    players: List[PlayerData]


class ShotTrackerDataPicklePlayerHolePlayerShots(CamelizedModel):
    time: str
    shot_id: int
    distance: int
    cup: bool
    putt: Optional[int]
    t: str
    prv: str
    asc: str
    left: int
    to: str
    from_: str
    x: float
    y: float
    z: float
    shottext: str

    class Config(CamelizedModel.Config):
        fields = {
            'from_': 'from'
        }


class ShotTrackerDataPicklePlayerHolePlayer(CamelizedModel):
    player_id: str
    shots: List[ShotTrackerDataPicklePlayerHolePlayerShots]
  

class ShotTrackerDataPicklePlayerHole(CamelizedModel):
    hole_id: str
    players: List[ShotTrackerDataPicklePlayerHolePlayer]


class ShotTrackerDataPickle(CamelizedModel):
    is_member: bool
    short_name: str
    last_name: str
    first_name: str
    player_name_add_ons: str
    players_holes: List[ShotTrackerDataPicklePlayerHole]


class ShotTrackerDataDetailsHole(CamelizedModel):
    hole_id: str
    par: str
    distance: str
    rank: str


class ShotTrackerDataDetails(CamelizedModel):
    hide_rank: bool
    holes: List[ShotTrackerDataDetailsHole]


class ShotTrackerDataButtons(CamelizedModel):
    hide_player_mode: bool


class ShotTrackerDataLegendPlayerNames(CamelizedModel):
    dot: str


class ShotTrackerDataLegend(CamelizedModel):
    hide_legend: bool
    player_names: List[ShotTrackerDataLegendPlayerNames]


class ShotTrackerData(CamelizedModel):
    hide_round_selector: bool
    round_id: str
    pickle: ShotTrackerDataPickle
    details: ShotTrackerDataDetails
    buttons: ShotTrackerDataButtons
    legend: ShotTrackerDataLegend


class ScoreCardPageLineHoleNumber(CamelizedModel):
    hole_number: str


class ScoreCardPageLineHole(CamelizedModel):
    line_type: Literal["hole"]
    holes: List[ScoreCardPageLineHoleNumber]
    hide_in_out_total_line: bool
    in_out: str
    total: str


class ScoreCardPageLinePar(CamelizedModel):
    line_type: Literal["par"]
    hide_in_out_total_line: bool
    holes: List[str]
    in_out: str
    total: str


class ScoreCardPageLinePlayerDataHole(CamelizedModel):
    difference: int
    status: str
    score: str


class ScoreCardPageLinePlayerData(CamelizedModel):
    line_type: Literal["playerData"]
    holes: List[ScoreCardPageLinePlayerDataHole]
    in_out: str
    total: str


class ScoreCardPageLineStatus(CamelizedModel):
    line_type: Literal["status"]
    holes: List[str]
    in_out: str
    total: str


ScoreCardPageLine = Annotated[
    Union[ScoreCardPageLineHole, ScoreCardPageLinePar, ScoreCardPageLinePlayerData, ScoreCardPageLineStatus],
    Field(discriminator="line_type"),
]


class ScoreCardPage(CamelizedModel):
    lines: List[ScoreCardPageLine]
    is_first_page: bool
    page_index: int
    is_last_page: bool



class ScoreCards(CamelizedModel):
    hide_foot_notes: bool
    pages: List[ScoreCardPage]


class PlayByPlayHoleShot(CamelizedModel):
    show_player_color: bool
    shot_text: str


class PlayByPlayHole(CamelizedModel):
    hole_id: int
    shots: List[PlayByPlayHoleShot]


class PlayByPlay(CamelizedModel):
    holes: List[PlayByPlayHole]


class StatisticsBlockStatData(CamelizedModel):
    stat_id: str
    round_value: str
    event_value: str
    event_average: str


class StatisticsBlockStat(CamelizedModel):
    type: Literal["stat"]
    data: List[StatisticsBlockStatData]


class StatisticsBlockParPerformanceData(CamelizedModel):
    more_bogey: int
    double_bogey: int
    bogey: int
    par: int
    birdie: int
    eagle: int
    double_eagle: int
    total: int
    more_bogey_percent: int
    double_bogey_percent: int
    bogey_percent: int
    birdie_percent: int
    eagle_percent: int
    double_eagle_percent: int
    par_percent: int


class StatisticsBlockParPerformance(CamelizedModel):
    type: Literal["parPerformance"]
    data: StatisticsBlockParPerformanceData


# TODO: Make this work with dynamic fields somehow
class StatisticsBlocks(CamelizedModel):
    stat: StatisticsBlockStat
    par_performance: StatisticsBlockParPerformance
    blocks: List[str]

    @validator("blocks", pre=True, whole=True)
    def snake_case_blocks(cls, values):
        new_values = []

        for value in values:
            new_value = ""
            for character in value:
                if character.isupper():
                    new_value += "_"
                new_value += character.lower()
            new_values.append(new_value)

        return new_values


class Statistics(CamelizedModel):
    statistics_blocks: StatisticsBlocks


class ShotTracker(CamelizedModel):
    round_complete: bool
    row_id: str
    round_id: str
    group_id: str
    tournament_round_id: str
    player_holes_max: List[PlayerHoleMax]
    number_of_holes: int
    starting_hole_id: str
    format: str
    last_hole_index: int
    course_id: str
    round_selector: RoundSelector
    players_data: PlayersData
    shot_tracker: ShotTrackerData 
    score_cards: ScoreCards
    play_by_play: PlayByPlay 
    statistics: Statistics
    msg_id: str
    last_updated: datetime
    generated_time: Optional[datetime]
