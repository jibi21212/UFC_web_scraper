from typing import Dict, List, Optional
import ufc_dataclasses
from bs4 import BeautifulSoup
import requests
import string
import re
import logging
from datetime import datetime
import time
from nationality_scraper import update_fighters_nationality
from ufc_save_data import setup_database, save_all_data
import logging 
FIGHTERS_URL = 'http://www.ufcstats.com/statistics/fighters'

fighters_dict : Dict[str, ufc_dataclasses.Fighter] = {} 
events : ufc_dataclasses.Event = []

def convertHeight(string):
    feet, inches = string.split("'")
    return int(feet) * 12 + int(inches)



def convert_event_date(date_str):
    return datetime.strptime(date_str, '%B %d, %Y').strftime('%Y-%m-%d')

def convertDOB(dob_str):
    return datetime.strptime(dob_str, '%b %d, %Y').strftime('%Y-%m-%d')

def get_fighter_data(url):
    # Parsing logic
    response = requests.get(url)
    html_content = response.text
    fighter_soup = BeautifulSoup(html_content, 'html.parser')
    body = fighter_soup.body
    section = body.find('section', class_='b-statistics__section_details')
    div = section.find('div', class_='l-page__container')
    h2 = div.find('h2', class_="b-content__title")
    fighter_name = h2.find('span', class_='b-content__title-highlight')
    record_tag = h2.find('span', class_="b-content__title-record")
    record = record_tag.text.strip()
    record_values = record.replace("Record: ", "")
    match = re.search(r"(\d+)-(\d+)-(\d+)(?: \((\d+) NC\))?", record_values)
    if match:
        wins = int(match.group(1))
        losses = int(match.group(2))
        draws = int(match.group(3))
        no_contests = int(match.group(4)) if match.group(4) else 0
    nickname = div.p.text.strip()

    

    inner_div = div.find('div', class_='b-fight-details b-fight-details_margin-top') # From this you can go to basic stats, advanced strikes, and advanced takedowns

    basic_div = inner_div.find('div', class_='b-list__info-box b-list__info-box_style_small-width js-guide')
    basic_ul = basic_div.find('ul', class_='b-list__box-list')
    height_tag = basic_ul.select_one('li:has(i:-soup-contains("Height:"))')
    weight_tag = basic_ul.select_one('li:has(i:-soup-contains("Weight:"))')
    reach_tag = basic_ul.select_one('li:has(i:-soup-contains("Reach:"))')
    stance_tag =  basic_ul.select_one('li:has(i:-soup-contains("STANCE:"))')
    dob_tag =  basic_ul.select_one('li:has(i:-soup-contains("DOB:"))')

    height_str = height_tag.get_text(strip=True).replace('Height:', '').replace('"','')
    weight_str = weight_tag.get_text(strip=True).replace("Weight:", '').replace(" lbs.", '')
    reach_str = reach_tag.get_text(strip=True).replace("Reach:", '').replace('"','')
    stance = stance_tag.get_text(strip=True).replace('STANCE:', '')
    dob_str = dob_tag.get_text(strip=True).replace('DOB:', '')
    

    career_div = inner_div.find('div', class_= 'b-list__info-box b-list__info-box_style_middle-width js-guide clearfix')
    inner_career_div = career_div.find('div', class_='b-list__info-box-left clearfix')
    strike_ul = inner_career_div.find('ul', class_="b-list__box-list b-list__box-list_margin-top")

    slpm_tag = strike_ul.select_one('li:has(i:-soup-contains("SLpM:"))')
    str_acc_tag = strike_ul.select_one('li:has(i:-soup-contains("Str. Acc.:"))')
    sapm_tag = strike_ul.select_one('li:has(i:-soup-contains("SApM:"))')
    str_def_tag = strike_ul.select_one('li:has(i:-soup-contains("Str. Def:"))')

    slpm_str = slpm_tag.get_text(strip=True).replace('SLpM:', '')
    str_acc_str = '0.' + str_acc_tag.get_text(strip=True).replace('Str. Acc.:', '').replace('%', '')
    sapm_str = sapm_tag.get_text(strip=True).replace('SApM:', '')
    str_def_str = '0.' + str_def_tag.get_text(strip=True).replace('Str. Def:', '').replace('%', '')
    

    td_div = inner_career_div.find('div', class_='b-list__info-box-right b-list__info-box_style-margin-right')
    td_ul = td_div.find('ul', class_='b-list__box-list b-list__box-list_margin-top')

    td_avg_tag = td_ul.select_one('li:has(i:-soup-contains("TD Avg.:"))')
    td_acc_tag = td_ul.select_one('li:has(i:-soup-contains("TD Acc.:"))')
    td_def_tag = td_ul.select_one('li:has(i:-soup-contains("TD Def.:"))')
    td_sub_tag = td_ul.select_one('li:has(i:-soup-contains("Sub. Avg.:"))')

    td_avg_str = td_avg_tag.get_text(strip=True).replace('TD Avg.:', '')
    td_acc_str = '0.' + td_acc_tag.get_text(strip=True).replace('TD Acc.:', '').replace('%', '')
    td_def_str = '0.' + td_def_tag.get_text(strip=True).replace('TD Def.:', '').replace('%', '')
    td_sub_str = td_sub_tag.get_text(strip=True).replace('Sub. Avg.:', '')
    if height_str!='--':
        height = convertHeight(height_str)
    else:
        height = None

    if weight_str!='--':
        weight = int(weight_str)
    else:
        weight = None

    if reach_str!='--':
        reach = int(reach_str)
    else:
        reach = None

    if dob_str!='--':
        dob = convertDOB(dob_str)
    else:
        dob = None

    if slpm_str!='--':
        slpm = float(slpm_str)
    else:
        slpm = None

    if str_acc_str!='--':
        str_acc = float(str_acc_str)
    else:
        str_acc = None

    if sapm_str!='--':
        sapm = float(sapm_str)
    else:
        sapm = None

    if str_def_str!='--':
        str_def = float(str_def_str)
    else:
        str_def = None

    if td_avg_str!='--':
        td_avg = float(td_avg_str)
    else:
        td_avg = None

    if td_acc_str!='--':
        td_acc = float(td_acc_str)
    else:
        td_acc = None

    if td_def_str!='--':
        td_def = float(td_def_str)
    else:
        td_def = None
    
    if td_sub_str!='--':
        td_sub = float(td_sub_str)
    else:
        td_sub = None

    career_stats = ufc_dataclasses.CareerStats(
        strikes_per_minute=slpm,
        strike_accuracy=str_acc,
        strikes_absorbed_per_minute=sapm,
        strike_defense=str_def,
        takedown_average=td_avg,
        takedown_accuracy=td_acc,
        takedown_defense=td_def,
        submission_average=td_sub
    )
    
    return ufc_dataclasses.Fighter(
        name=fighter_name.get_text(strip=True),
        nickname=nickname,
        height=height,
        weight=weight,
        reach=reach,
        stance=stance,
        date_of_birth=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
        wins=wins,
        losses=losses,
        draws=draws,
        no_contests=no_contests,
        career_stats=career_stats,
        was_champion=False,  
        fight_performances=[]
    )

def populate_fighters_dict():
    for char in string.ascii_lowercase:
        url = f"{FIGHTERS_URL}?char={char}"

def get_fighter_urls(url, limit=None):
    
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        body = soup.find('body', class_='b-page')
        tbody = body.tbody
        processed_count = 0
        for tr in tbody.find_all('tr', class_='b-statistics__table-row'):
            if limit and processed_count >= limit:
                break

            link = tr.find('td').find('a')
            if link:
                try:
                    fighter = get_fighter_data(link.get('href'))
                    fighters_dict[fighter.name] = fighter
                    print(f"Added fighter to dictionary: {fighter.name}")
                except Exception as e:
                    print(f"Error processing fighter {link.text}: {str(e)}")
                    continue
        
    except Exception as e:
        print(f"Error fetching fighters from {url}: {str(e)}")
        return []


def parse_strike_data(strike_str: str) -> Optional[ufc_dataclasses.StrikeStats]:
    if strike_str == '---' or strike_str == '--':
        return ufc_dataclasses.StrikeStats()
    if ' of ' in strike_str:
        landed, attempted = map(int, strike_str.split(' of '))
        return ufc_dataclasses.StrikeStats(landed=landed, attempted=attempted)
    return ufc_dataclasses.StrikeStats()

def parse_percentage(pct_str: str) -> Optional[float]:
    if pct_str == '---':
        return None
    return float('0.' + pct_str.replace('%', ''))

def get_fight_data(url:str, event_date: datetime):
    try:
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        section = soup.find('section', class_='b-statistics__section_details')
        div = section.find('div', class_='b-fight-details')
        div_fighters = div.find('div', class_='b-fight-details__persons clearfix')


        loser_div = div_fighters.select_one('div:has(i:-soup-contains("L"))')
        loser = loser_div.select_one('h3.b-fight-details__person-name a').get_text(strip=True)
        winner_div = div_fighters.select_one('div:has(i:-soup-contains("W"))')
        winner = winner_div.select_one('h3.b-fight-details__person-name a').get_text(strip=True)

        winner_fighter = fighters_dict.get(winner)
        loser_fighter = fighters_dict.get(loser)
        weight_class = div.find('div', class_='b-fight-details__fight').find('i', class_='b-fight-details__fight-title').get_text(strip=True)
        is_title_fight = "Title" in weight_class



        method = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item_first').get_text(strip=True).replace('Method:', '')
        rnd = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item_first').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Round:', '')
        time = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Time:', '')
        time_format = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Time format:', '')
        total_rounds = int(time_format[0])
        referee = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Referee:', '')
        details = div.find('div', class_='b-fight-details__content').find('p', class_='b-fight-details__text').find_next('p', class_='b-fight-details__text').get_text(strip=True).replace('Details:', '')

        table = div.find('table', class_='b-fight-details__table js-fight-table')
        table_rounds = table.find('tbody')
        theads = table_rounds.findAll('thead') # These are nothing but the round numbers and not the stats
        trs = table_rounds.findAll('tr')

        totals_stat = {
            0: 'name', 
            1: 'kd', 
            2: 'sig_str',
            3: 'sig_str_pct',
            4: 'total_str',
            5: 'td',
            6: 'td_pct', 
            7: 'sub_att', 
            8: 'rev',
            9: 'ctrl'
            }

        sig_strike_stats = {
            0: 'name',
            1: 'sig_str',
            2: 'sig_str_pct', 
            3: 'head',
            4: 'body',
            5: 'leg',
            6: 'distance',
            7: 'clinch',
            8: 'ground'
            }

        # Create RoundStrikeBreakdown for each round
        def create_round_strike_breakdown(round_data):
            return ufc_dataclasses.RoundStrikeBreakdown(
                significant_strikes=parse_strike_data(round_data['sig_str']),
                total_strikes=parse_strike_data(round_data['total_str']),
                head_strikes=parse_strike_data(round_data['head']),
                body_strikes=parse_strike_data(round_data['body']),
                leg_strikes=parse_strike_data(round_data['leg']),
                distance_strikes=parse_strike_data(round_data['distance']),
                clinch_strikes=parse_strike_data(round_data['clinch']),
                ground_strikes=parse_strike_data(round_data['ground'])
            )

        # Create RoundStats for each round
        def create_round_stats(round_data, round_number, fighter_name):
            return ufc_dataclasses.RoundStats(
                round_number=round_number,
                fighter_name=fighter_name,
                knockdowns=int(round_data['kd']) if round_data['kd'] != '---' else 0,
                strike_breakdown=create_round_strike_breakdown(round_data),
                takedowns=parse_strike_data(round_data['td']),
                submission_attempts=int(round_data['sub_att']) if round_data['sub_att'] != '---' else 0,
                reversals=int(round_data['rev']) if round_data['rev'] != '---' else 0,
                control_time=int(round_data['ctrl'].split(':')[0]) * 60 + int(round_data['ctrl'].split(':')[1]) if round_data['ctrl'] != '---' else 0
            )

        fighter_1_rounds_data = {}
        fighter_2_rounds_data = {}

        # Collect round data
        for j, tr in enumerate(trs):
            tds = tr.findAll('td')
            round_number = j + 1

            fighter_1_round_data = {}
            fighter_2_round_data = {}

            for i, td in enumerate(tds):
                ps = td.findAll('p')
                stat_name = totals_stat[i]

                if len(ps) >= 2:
                    fighter_1_round_data[stat_name] = ps[0].get_text(strip=True)
                    fighter_2_round_data[stat_name] = ps[1].get_text(strip=True)

            fighter_1_rounds_data[round_number] = fighter_1_round_data
            fighter_2_rounds_data[round_number] = fighter_2_round_data

        # Collect significant strike data
        sig_strike_stats_div = div.find('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section')
        tbody_sig = sig_strike_stats_div.find('tbody')
        trs_sig = tbody_sig.findAll('tr')

        # Add significant strike data to round data
        for j, tr in enumerate(trs_sig):
            round_number = j + 1
            tds = tr.findAll('td')

            for i, td in enumerate(tds):
                ps = td.findAll('p')
                stat_name = sig_strike_stats[i]

                if len(ps) >= 2:
                    fighter_1_rounds_data[round_number][stat_name] = ps[0].get_text(strip=True)
                    fighter_2_rounds_data[round_number][stat_name] = ps[1].get_text(strip=True)

        # Create FightPerformance objects
        fighter_1_performance = ufc_dataclasses.FightPerformance(
            fighter_name=winner,
            rounds={i: create_round_stats(fighter_1_rounds_data[i], i, winner) 
                    for i in range(1, len(trs) + 1)}
        )

        fighter_2_performance = ufc_dataclasses.FightPerformance(
            fighter_name=loser,
            rounds={i: create_round_stats(fighter_2_rounds_data[i], i, loser) 
                    for i in range(1, len(trs) + 1)}
        )
        
        if winner_fighter:
            winner_fighter.add_performance(fighter_1_performance, is_title_fight, True)

        if loser_fighter:
            loser_fighter.add_performance(fighter_2_performance, is_title_fight, False)
        
        # Create and return Fight object
        return ufc_dataclasses.Fight(
            event_name=section.find('h2', class_='b-content__title').get_text(strip=True),
            date=event_date,
            title_bout=is_title_fight,
            winner=winner,
            loser=loser,
            weight_class=weight_class,
            method=method,
            round_ended=int(rnd) if rnd != '---' else 0,
            time_ended=int(time.split(':')[0]) * 60 + int(time.split(':')[1]) if time != '---' else 0,
            referee=referee,
            fighter_1=fighter_1_performance,
            fighter_2=fighter_2_performance
        )
    except requests.RequestException as e:
        logging.error(f"Error fetching URL {url}: {str(e)}")
        return None
    except ValueError as e:
        logging.error(f"Error parsing data from {url}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error processing {url}: {str(e)}")
        return None
    


def get_event_data(url,limit_fights=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get event details
        section = soup.find('section', class_='b-statistics__section_details')
        title = section.find('h2', class_='b-content__title').find('span', class_='b-content__title-highlight').get_text(strip=True)

        div_date = section.find('div', class_='b-list__info-box b-list__info-box_style_large-width')
        date_str = div_date.select_one('li:has(i:-soup-contains("Date:"))').get_text(strip=True).replace('Date:', '').strip()
        location_str = div_date.select_one('li:has(i:-soup-contains("Location:"))').get_text(strip=True).replace('Location:', '').strip()
        
        # Convert date string to datetime
        event_date = datetime.strptime(date_str, '%B %d, %Y')
        
        # Get all fights
        fights = []
        tbody = section.find('tbody')
        
        for tr in tbody.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click'):
            if limit_fights and len(fights) >= limit_fights:
                break
            link = tr.find('td').find('a')
            if link:
                fight = get_fight_data(link.get('href'), event_date)  # Pass the event_date
                if fight:
                    fights.append(fight)
                else:
                    logging.warning(f"Failed to get fight data from {link.get('href')}")

        if not fights:
            logging.warning(f"No fights found for event: {title}")
            return None

        return ufc_dataclasses.Event(
            title=title,
            date=event_date,
            location=location_str,
            fights=fights
        )

    except requests.RequestException as e:
        logging.error(f"Error fetching event URL {url}: {str(e)}")
        return None
    except ValueError as e:
        logging.error(f"Error parsing event data from {url}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error processing event {url}: {str(e)}")
        return None

def get_event_urls(limit=None) -> List[ufc_dataclasses.Event]:
    base_url = 'http://www.ufcstats.com/statistics/events/completed?page=all'
    
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        div = soup.find('div', class_='b-statistics__inner')
        table = div.find('table', class_='b-statistics__table-events')
        tbody = table.find('tbody')

        total_events = len(tbody.find_all('tr', class_='b-statistics__table-row'))
        logging.info(f"Found {total_events} events to process")

        for i, tr in enumerate(tbody.find_all('tr', class_='b-statistics__table-row'), 1):
            if limit and len(events) >= limit:
                break
            link = tr.find('a')
            if link:
                event_url = link.get('href')
                logging.info(f"Processing event {i}/{total_events}: {event_url}")
                
                try:
                    event = get_event_data(event_url)
                    if event:
                        events.append(event)
                        logging.info(f"Successfully processed event: {event.title}")
                    else:
                        logging.warning(f"Failed to process event: {event_url}")
                except Exception as e:
                    logging.error(f"Error processing event {event_url}: {str(e)}")
                    continue

        logging.info(f"Successfully processed {len(events)} out of {total_events} events")
        return events

    except requests.RequestException as e:
        logging.error(f"Error fetching events list: {str(e)}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return []
    

def get_urls():
    all_fighters = []
    total_letters = len(string.ascii_lowercase)
    
    try:
        for i, char in enumerate(string.ascii_lowercase, 1):
            url = f"{FIGHTERS_URL}?char={char}&page=all"
            logging.info(f"Processing fighters starting with '{char.upper()}' ({i}/{total_letters})")
            
            try:
                # Fighters per letter
                get_fighter_urls(url)
                logging.info(f"Successfully processed fighters for letter {char.upper()}")
                logging.info(f"Current total fighters in dictionary: {len(fighters_dict)}")
                # Delay
                time.sleep(1)
                
            except Exception as e:
                logging.error(f"Error processing letter {char.upper()}: {str(e)}")
                continue
        
        logging.info(f"Total fighters processed: {len(all_fighters)}")
        return all_fighters
        
    except Exception as e:
        logging.error(f"Unexpected error in get_urls: {str(e)}")
        return []
    
   
if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Starting scraping at {start_time}")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ufc_scraper.log'),
            logging.StreamHandler()
        ]
    )

    try:
        # Stage 1: Scrape all fighter data
        print("\nStage 1: Scraping fighter data...")
        get_urls()  # This populates fighters_dict
        print(f"Completed Stage 1: Scraped {len(fighters_dict)} fighters")
        print(f"Time elapsed: {datetime.now() - start_time}")

        # Stage 2: Scrape all event data
        print("\nStage 2: Scraping event data...")
        events = get_event_urls()
        print(f"Completed Stage 2: Scraped {len(events)} events")
        print(f"Time elapsed: {datetime.now() - start_time}")

        # Stage 3: Update nationalities using Selenium
        print("\nStage 3: Updating fighter nationalities...")
        fighters_dict = update_fighters_nationality(fighters_dict)
        print("Completed Stage 3: Updated fighter nationalities")
        print(f"Time elapsed: {datetime.now() - start_time}")

        # Stage 4: Save everything to database
        print("\nStage 4: Saving to database...")
        setup_database()
        save_all_data(events, fighters_dict)
        print("Completed Stage 4: All data saved to database")

        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"\nAll stages completed successfully!")
        print(f"Total time: {total_time}")
        print(f"Started at: {start_time}")
        print(f"Finished at: {end_time}")

    except Exception as e:
        print(f"Error during processing: {e}")
        logging.error(f"Error during processing: {e}")
    finally:
        print("\nScript finished")