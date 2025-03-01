from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class CareerStats:
    strikes_per_minute: float
    strike_accuracy: float
    strikes_absorbed_per_minute: float
    strike_defense: float
    takedown_average: float
    takedown_accuracy: float
    takedown_defense: float
    submission_average: float
    def __str__(self):
        return f"""
            strikes_per_minute: {self.strikes_per_minute}
            strike_accuracy: {self.strike_accuracy}
            strikes_absorbed_per_minute: {self.strikes_absorbed_per_minute}
            strike_defense: {self.strike_defense}
            takedown_average: {self.takedown_average}
            takedown_accuracy: {self.takedown_accuracy}
            takedown_defense: {self.takedown_defense}
            submission_average: {self.submission_average}
            """

@dataclass
class StrikeStats:
    landed: int = 0
    attempted: int = 0
    percentage: Optional[float] = 0

    def __post_init__(self):
        if self.percentage is None and self.attempted > 0:
            self.percentage = self.landed / self.attempted
    
    def __str__(self):
        return f"""Landed: {self.landed}, Attempted: {self.attempted}, Percentage: {self.percentage}"""

@dataclass
class RoundStrikeBreakdown:
    significant_strikes: StrikeStats = field(default_factory=StrikeStats)
    total_strikes: StrikeStats = field(default_factory=StrikeStats)
    head_strikes: StrikeStats = field(default_factory=StrikeStats)
    body_strikes: StrikeStats = field(default_factory=StrikeStats)
    leg_strikes: StrikeStats = field(default_factory=StrikeStats)
    distance_strikes: StrikeStats = field(default_factory=StrikeStats)
    clinch_strikes: StrikeStats = field(default_factory=StrikeStats)
    ground_strikes: StrikeStats = field(default_factory=StrikeStats)

    def __str__(self):
        return f"""
        significant_strikes {str(self.significant_strikes)}
        total_strikes {str(self.total_strikes)}
        head_strikes {str(self.head_strikes)}
        body_strikes {str(self.body_strikes)}
        leg_strikes {str(self.leg_strikes)}
        distance_strikes {str(self.distance_strikes)}
        clinch_strikes {str(self.clinch_strikes)}
        ground_strikes {str(self.ground_strikes)}
        """

@dataclass
class RoundStats:
    round_number: int
    fighter_name: str
    knockdowns: int = 0
    strike_breakdown: RoundStrikeBreakdown = field(default_factory=RoundStrikeBreakdown)
    takedowns: StrikeStats  = field(default_factory=StrikeStats)
    submission_attempts: int = 0
    reversals: int = 0
    control_time: int  = 0 # in seconds
    def __str__(self):
        return f"""
        round_number: {self.round_number}
        fighter_name: {self.fighter_name}
        knockdowns: {self.knockdowns}
        strike_breakdown: {str(self.strike_breakdown)}
        takedowns: {str(self.takedowns)}
        submission_attempts: {self.submission_attempts}
        reversals: {self.reversals}
        control_time: {self.control_time}
        """

@dataclass
class FightPerformance:
    fighter_name: str
    rounds: Dict[int, RoundStats]
    def __str__(self):
        s = ""

        for i in range(len(self.rounds)):
            s += str(self.rounds[i+1])

        return s

@dataclass
class Fighter:
    # Required parameters (no default values) first
    name: str
    stance: str
    wins: int
    losses: int
    draws: int
    no_contests: int
    career_stats: CareerStats
    
    # Optional parameters (with default values) after
    nickname: Optional[str] = None
    nationality: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    reach: Optional[int] = None
    date_of_birth: Optional[datetime] = None
    was_champion: bool = False
    championship_bouts_won: int = 0
    fight_performances: List[FightPerformance] = field(default_factory=list)
    
    def add_performance(self, performance: FightPerformance, is_title_fight: bool, is_winner: bool):
        self.fight_performances.append(performance)
        if is_winner and is_title_fight and performance.fighter_name == self.name:
            self.was_champion = True
            self.championship_bouts_won += 1

    def __str__(self):
        return f"""
        name: {self.name}
        nationality: {self.nationality}
        Champ (Present or Past) ? : {self.was_champion}
        Championship bouts won: {self.championship_bouts_won}
        nickname: {self.nickname}
        height (in inches): {self.height}
        weight (in pounds): {self.weight}
        reach (in inches): {self.reach}
        stance: {self.stance}
        date_of_birth: {self.date_of_birth}
        wins: {self.wins}
        losses: {self.losses}
        draws: {self.draws}
        no_contests: {self.no_contests}
        career_stats: {str(self.career_stats)}
        """

@dataclass
class Fight:
    event_name: str
    date: datetime
    winner: str
    loser: str
    weight_class: str
    title_bout : bool
    method: str
    round_ended: int
    time_ended: int  # in seconds
    referee: str
    fighter_1: FightPerformance
    fighter_2: FightPerformance

    def __str__(self):
        return f"""
        event_name: {self.event_name}
        date: {self.date}
        title_bout : {self.title_bout}
        winner: {self.winner}
        loser: {self.loser}
        weight_class: {self.weight_class}
        method: {self.method}
        round_ended: {self.round_ended}
        time_ended: {self.time_ended}
        referee: {self.referee}
        fighter_1: {str(self.fighter_1)}
        fighter_2: {str(self.fighter_2)}
        """

@dataclass
class Event:
    title: str
    date: datetime
    location: str
    fights: List[Fight]

    def __str__(self):
        fights = ""
        for f in self.fights:
            fights += str(f)
        return f"""
        title: {self.title}
        date: {self.date}
        location: {self.location}
        fights: {fights}"""
