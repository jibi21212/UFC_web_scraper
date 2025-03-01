import sqlite3
from typing import Dict, List
import ufc_dataclasses

conn = sqlite3.connect('ufc_data.db')
c = conn.cursor()

def setup_database():
    c.execute('''
        CREATE TABLE IF NOT EXISTS event (
            event_id INTEGER PRIMARY KEY,
            event_title TEXT,
            date TEXT,
            location TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS fight (
            fight_id INTEGER PRIMARY KEY,
            event_name TEXT,
            date TEXT,
            title_bout INTEGER,
            method TEXT,
            round_ended INTEGER,
            time_ended INTEGER,
            referee TEXT,
            event_id INTEGER,
            FOREIGN KEY(event_id) REFERENCES event(event_id)
            )
            
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS fighters (
            fighters_id INTEGER PRIMARY KEY,
            name TEXT,
            nationality TEXT,
            nickname TEXT,
            height INTEGER,
            weight INTEGER,
            reach INTEGER,
            stance TEXT,
            date_of_birth TEXT,
            wins INTEGER,
            losses INTEGER,
            draws INTEGER,
            no_contests INTEGER,
            was_champion BOOLEAN,
            championship_bouts_won INTEGER
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS career_stats (
            stat_id INTEGER PRIMARY KEY,
            strikes_per_minute REAL,
            strike_accuracy REAL,
            strikes_absorbed_per_minute REAL,
            strike_defense REAL,
            takedown_average REAL,
            takedown_accuracy REAL,
            takedown_defense REAL,
            submission_average REAL,
            fighters_id INTEGER,
            FOREIGN KEY(fighters_id) REFERENCES fighters(fighters_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS fight_performance (
            fightp_id INTEGER PRIMARY KEY,
            fighter_name TEXT,
            fighters_id INTEGER,
            fight_id INTEGER,
            FOREIGN KEY(fighters_id) REFERENCES fighters(fighters_id),
            FOREIGN KEY(fight_id) REFERENCES fight(fight_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS strike_stats(
            strike_stats_id INTEGER PRIMARY KEY,
            landed INTEGER,
            attempted INTEGER,
            percentage REAL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS strike_breakdown (
            strike_breakdown_id INTEGER PRIMARY KEY,
            significant_strikes_id INTEGER,
            total_strikes_id INTEGER,
            head_strikes_id INTEGER,
            body_strikes_id INTEGER,
            leg_strikes_id INTEGER,
            distance_strikes_id INTEGER,
            clinch_strikes_id INTEGER,
            ground_strikes_id INTEGER,
            FOREIGN KEY(significant_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(total_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(head_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(body_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(leg_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(distance_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(clinch_strikes_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(ground_strikes_id) REFERENCES strike_stats(strike_stats_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS round_stats (
            round_id INTEGER PRIMARY KEY,
            round_number INTEGER,
            knockdowns INTEGER,
            submission_attempts INTEGER,
            reversals INTEGER,
            control_time INTEGER,
            fightp_id INTEGER,
            strike_stats_id INTEGER,
            strike_breakdown_id INTEGER,
            FOREIGN KEY(fightp_id) REFERENCES fight_performance(fightp_id),
            FOREIGN KEY(strike_stats_id) REFERENCES strike_stats(strike_stats_id),
            FOREIGN KEY(strike_breakdown_id) REFERENCES strike_breakdown(strike_breakdown_id)
            )
        ''')


def insert_event(event: ufc_dataclasses.Event):
    c.execute('''
    INSERT INTO event (event_title ,date, location)
    VALUES (?,?,?)
    ''', (
        event.title,
          event.date.strftime('%Y-%m-%d'), 
          event.location
          ))
    event_id = c.lastrowid
    conn.commit()

    return event_id

def insert_fight(fight: ufc_dataclasses.Fight, event_id: int): 
    # Probably look into how the datetime object for fight.date needs to be handled
    c.execute('''
        INSERT INTO fight (
              event_name, date, title_bout, method, round_ended,
              time_ended, referee, event_id
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            fight.event_name, fight.date.strftime('%Y-%m-%d'), fight.title_bout,
            fight.method, fight.round_ended, fight.time_ended,
            fight.referee, event_id
        ))
    fight_id = c.lastrowid
    conn.commit()
    return fight_id

def insert_fighter(fighter: ufc_dataclasses.Fighter):
    c.execute('''
        INSERT INTO fighters (
            name, nationality, nickname, height, weight,
            reach, stance, date_of_birth, wins, losses,
            draws, no_contests, was_champion, championship_bouts_won
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        fighter.name, fighter.nationality, fighter.nickname,
        fighter.height, fighter.weight, fighter.reach,
        fighter.stance, 
        fighter.date_of_birth.strftime('%Y-%m-%d') if fighter.date_of_birth else None, 
        fighter.wins,
        fighter.losses, fighter.draws, fighter.no_contests,
        fighter.was_champion, fighter.championship_bouts_won
    ))
    fighters_id = c.lastrowid

    c.execute('''
        INSERT INTO career_stats (
            strikes_per_minute, strike_accuracy,
            strikes_absorbed_per_minute, strike_defense,
            takedown_average, takedown_accuracy,
            takedown_defense, submission_average,
            fighters_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        fighter.career_stats.strikes_per_minute,
        fighter.career_stats.strike_accuracy,
        fighter.career_stats.strikes_absorbed_per_minute,
        fighter.career_stats.strike_defense,
        fighter.career_stats.takedown_average,
        fighter.career_stats.takedown_accuracy,
        fighter.career_stats.takedown_defense,
        fighter.career_stats.submission_average,
        fighters_id
    ))

    conn.commit()
    return fighters_id

def insert_fight_performance(performance: ufc_dataclasses.FightPerformance, fighters_id: int, fight_id: int):
    c.execute('''
        INSERT INTO fight_performance (
            fighter_name, fighters_id, fight_id
        ) VALUES (?, ?, ?)
    ''', (
        performance.fighter_name,
        fighters_id,
        fight_id
    ))
    fightp_id = c.lastrowid
    conn.commit()
    return fightp_id

def insert_strike_stats(strike_stats: ufc_dataclasses.StrikeStats):
    c.execute('''
        INSERT INTO strike_stats (
            landed, attempted, percentage  
        ) VALUES (?, ?, ?)
    ''', (
        strike_stats.landed,
        strike_stats.attempted,
        strike_stats.percentage
    ))
    strike_stats_id = c.lastrowid
    conn.commit()
    return strike_stats_id

def insert_strike_breakdown(strike_breakdown : ufc_dataclasses.RoundStrikeBreakdown):
    significant_strikes_id = insert_strike_stats(strike_breakdown.significant_strikes)
    total_strikes_id = insert_strike_stats(strike_breakdown.total_strikes)
    head_strikes_id = insert_strike_stats(strike_breakdown.head_strikes)
    body_strikes_id = insert_strike_stats(strike_breakdown.body_strikes)
    leg_strikes_id = insert_strike_stats(strike_breakdown.leg_strikes)
    distance_strikes_id = insert_strike_stats(strike_breakdown.distance_strikes)
    clinch_strikes_id = insert_strike_stats(strike_breakdown.clinch_strikes)
    ground_strikes_id = insert_strike_stats(strike_breakdown.ground_strikes)

    c.execute('''
        INSERT INTO strike_breakdown (
            significant_strikes_id, total_strikes_id,
            head_strikes_id, body_strikes_id, leg_strikes_id,
            distance_strikes_id, clinch_strikes_id, ground_strikes_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        significant_strikes_id, total_strikes_id,
        head_strikes_id, body_strikes_id, leg_strikes_id,
        distance_strikes_id, clinch_strikes_id, ground_strikes_id
    ))
    strike_breakdown_id = c.lastrowid
    conn.commit()
    return strike_breakdown_id

def insert_round_stats(round_stats: ufc_dataclasses.RoundStats, fightp_id: int):
    
    strike_stats_id = insert_strike_stats(round_stats.takedowns)

    strike_breakdown_id = insert_strike_breakdown(round_stats.strike_breakdown)

    c.execute('''
        INSERT INTO round_stats (
            round_number, knockdowns,
            submission_attempts, reversals, control_time,
            fightp_id, strike_stats_id, strike_breakdown_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        round_stats.round_number,
        round_stats.knockdowns,
        round_stats.submission_attempts,
        round_stats.reversals,
        round_stats.control_time,
        fightp_id,
        strike_stats_id,
        strike_breakdown_id
    ))

    round_id = c.lastrowid
    conn.commit()
    return round_id

def save_all_data(events: List[ufc_dataclasses.Event], fighters_dict: Dict[str, ufc_dataclasses.Fighter]):
    try:
        print("\nSaving fighters...")
        fighters_count = len(fighters_dict)
        for i, fighter in enumerate(fighters_dict.values(), 1):
            try:
                insert_fighter(fighter)
                if i % 10 == 0:  # Progress update every 10 fighters
                    print(f"Processed {i}/{fighters_count} fighters")
            except Exception as e:
                print(f"Error saving fighter {fighter.name}: {e}")
                continue
        print("\nSaving events & fights...")
        events_count = len(events)
        for i, event in enumerate(events, 1):
            try:
                event_id = insert_event(event)
                print(f"\nProcessing event {i}/{events_count}: {event.title}")
                for fight in event.fights:
                    try:
                        # Save fight
                        fight_id = insert_fight(fight, event_id)

                        # Get fighter IDs from database
                        c.execute("SELECT fighters_id FROM fighters WHERE name = ?", 
                                (fight.fighter_1.fighter_name,))
                        fighter_1_id = c.fetchone()[0]

                        c.execute("SELECT fighters_id FROM fighters WHERE name = ?", 
                                (fight.fighter_2.fighter_name,))
                        fighter_2_id = c.fetchone()[0]

                        # Save fight performances and their rounds
                        fightp_1_id = insert_fight_performance(fight.fighter_1, 
                                                             fighter_1_id, fight_id)

                        # Save rounds for fighter 1
                        for round_num, round_stats in fight.fighter_1.rounds.items():
                            insert_round_stats(round_stats, fightp_1_id)

                        # Save fighter 2's performance and rounds
                        fightp_2_id = insert_fight_performance(fight.fighter_2, 
                                                             fighter_2_id, fight_id)

                        # Save rounds for fighter 2
                        for round_num, round_stats in fight.fighter_2.rounds.items():
                            insert_round_stats(round_stats, fightp_2_id)

                        print(f"Saved fight: {fight.fighter_1.fighter_name} vs {fight.fighter_2.fighter_name}")

                    except Exception as e:
                        print(f"Error saving fight {fight.fighter_1.fighter_name} vs {fight.fighter_2.fighter_name}: {e}")
                        continue
            except Exception as e:
                print(f"Error saving event {event.title}: {e}")
                continue

        print("\nData saving compelted!")
    except Exception as e:
        print(f"Fatal error during save: {e}")
        conn.rollback()
        raise
    finally:
        print("\nSave operation finished")


# Whole database was saved succesfully
# However, it seems the nationality scraper was not that good
# I need to write a script to update the entries in my data base with a more sophisticated nationality scraper
# In short: Create an sqlite script that updates queries -> Calls improved nationality scraper -> Update each query