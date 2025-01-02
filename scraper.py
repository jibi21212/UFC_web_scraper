from bs4 import BeautifulSoup
import requests
import string
import re
# SO FAR: This script works for all FIGHTERS, but not for all FIGHTS/BOUTS, need to figure out how to get the data for all fights
FIGHTERS_URL = 'http://www.ufcstats.com/statistics/fighters'


def convertHeight(string):
    feet, inches = string.split("'")
    return int(feet) * 12 + int(inches)

from datetime import datetime



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

    '''
    print("Fighter Name: " + fighter_name.text.strip())
    if nickname:
        print(nickname)
    print(f'height_str: {height_str}\nweight_str: {weight_str}\nreach_str: {reach_str}\nstance: {stance}\ndob_str: {dob_str}')
    print(f'slpm_str: {slpm_str}\nstr_acc_str: {str_acc_str}\nsapm_str: {sapm_str}\nstr_def_str: {str_def_str}')
    print(f'td_avg_str: {td_avg_str}\ntd_acc_str : {td_acc_str }\ntd_def_str: {td_def_str}\ntd_sub_str: {td_sub_str}')
    '''
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

    return {
        'fighter_name': fighter_name.get_text(strip=True),
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'NC': no_contests,
        'nickname': nickname,
        'height': height,
        'weight': weight,
        'reach': reach,
        'stance': stance,
        'dob': dob, 
        'SLpM': slpm,
        'Strike Accuracy': str_acc, 
        'SApM': sapm, 
        'Strike Defense': str_def, 
        'Takedown Average': td_avg,
        'Takedown Accuracy': td_acc, 
        'Takedown Defense': td_def, 
        'Submission Average': td_sub 
    }

    

def get_fighter_urls(url):

    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    body = soup.find('body', class_= 'b-page')
    tbody = body.tbody
    for tr in tbody.find_all('tr', class_='b-statistics__table-row'):
        link = tr.find('td').find('a')
        if link:
            # print(f'Fighter: {link.text}, link: {link.get('href')}') # -> Works perfectly
            print(get_fighter_data(link.get('href')))


def get_fight_data(url):
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

    weight_class = div.find('div', class_='b-fight-details__fight').find('i', class_='b-fight-details__fight-title').get_text(strip=True)
    method = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item_first').get_text(strip=True).replace('Method:', '')
    rnd = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item_first').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Round:', '')
    time = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Time:', '')
    time_format = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Time format:', '')
    total_rounds = int(time_format[0])
    referee = div.find('div', class_='b-fight-details__content').find('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').find_next('i', class_='b-fight-details__text-item').get_text(strip=True).replace('Referee:', '')
    details = div.find('div', class_='b-fight-details__content').find('p', class_='b-fight-details__text').find_next('p', class_='b-fight-details__text').get_text(strip=True).replace('Details:', '')

    table = div.find('table', class_='b-fight-details__table js-fight-table')
    table_rounds = table.find('tbody')
    # print(f'Winner: {winner}\nLoser: {loser}\nWeight Class: {weight_class}\nMethod: {method}\nRound: {rnd}\nTime: {time}\nTime Format: {time_format}\nTotal Rounds: {total_rounds}\nReferee: {referee}\nDetails: {details}')
    theads = table_rounds.findAll('thead') # These are nothing but the round numbers and not the stats
    trs = table_rounds.findAll('tr')

    totals_stat = {
        0: 'name', # Dont need to convert
        1: 'kd', # Need to convert -> int if not '---' else None 
        2: 'sig_str', # Need to conver into float if not '---' or '0 of 0' else None
        3: 'sig_str_pct', # Need to convert to float if not '---' else None
        4: 'total_str', # Need to convert to float if not '---' else None -> Have 2 things, one how many strikes thrown, how many landed
        5: 'td', # Need to convert to float if not '---' else None -> Have 2 things, one how many attempted, how many landed
        6: 'td_pct', # Conver to float if not '---' else None
        7: 'sub_att', # Convert to int if not '---' else None
        8: 'rev', # Convert to int if not '---' else None
        9: 'ctrl' # Convert to int if not '---' else None -> in seconds
        }

    sig_strike_stats = { # All of these should be percentages
        0: 'name', # Dont need to convert
        1: 'sig_str', # Need to convert -> float if not '---' else None
        2: 'sig_str_pct', 
        3: 'head',
        4: 'body',
        5: 'leg',
        6: 'distance',
        7: 'clinch',
        8: 'ground'
        }


    


    # print(trs[0].prettify())
    fight_data = {
        'metadata': {
            'winner': winner, # Dont need to conver
            'loser': loser, # Dont need to convert
            'weight_class': weight_class, # Dont need to convert
            'method': method, # Dont need to convert
            'round': rnd, # Need to convert -> int if not '---' else None -> Done
            'time': time, # Need to convert -> int if not '---' else None -> Done
            'time_format': time_format, # Dont need to convert
            'total_rounds': total_rounds, # Need to convert -> int if not '---' else None -> Done
            'referee': referee, # Dont need to convert
            'details': details, # Dont need to convert
            'score': {}
        },
        'fighter_1_stats': {
            'totals': {},
            'sig_strike': {}
        },
        'fighter_2_stats': {
            'totals': {},
            'sig_strike': {}
        }
    }
    

    def convert_data(data, rounds):
        # BESIDES THE JUDGES + SCORES, EVERYTHING ELSE IS DONE
        if data['metadata']['round'] != '---':
            data['metadata']['round'] = int(data['metadata']['round'])
        else:
            None

        if data['metadata']['total_rounds'] != '---':
            data['metadata']['total_rounds'] = int(data['metadata']['total_rounds'])
        else:
            None

        if data['metadata']['time'] != '---':
            time_in_seconds = data['metadata']['time'].split(':')
            data['metadata']['time'] = int(time_in_seconds[0]) * 60 + int(time_in_seconds[1])
        else:
             data['metadata']['time'] = None

        if data['metadata']['method'] == 'Decision - Split' or data['metadata']['method'] == 'Decision - Unanimous':
            
            pattern = r"([a-zA-Z]+(?: [a-zA-Z]+)?)\s*(\d+)\s*-\s*(\d+)"
            # Find all matches for judges and scores
            details = data['metadata']['details']
            matches = re.findall(pattern, details)

            # Prepare a structured output
            judges_scores = []

            for match in matches:
                judge_name = match[0]
                score1 = int(match[1])
                score2 = int(match[2])

                # Append each judge and their scores as a dictionary
                judges_scores.append({
                    "judge": judge_name,
                    "score_1": score1,
                    "score_2": score2,
                })

            # Add judges and scores to your metadata or process them as needed
            data['metadata']['details'] = judges_scores

        
        if data['metadata']['total_rounds'] != '---':
            data['metadata']['total_rounds'] = int(data['metadata']['total_rounds'])
        else:
             data['metadata']['total_rounds'] = None
        
        # make a for loop iterating through every rounds stats

        for j in range(rounds):
            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]] != '---':
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]] = int(data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]])
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]] != '---':
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]] = int(data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]])
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[1]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[2]] != '---':
                sig_str = data['fighter_1_stats']['totals']['round'][j+1][totals_stat[2]].split(' of ')
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[2]] = {'landed': int(sig_str[0]), 'attempted': int(sig_str[1])}
            else:
                 data['fighter_1_stats']['totals']['round'][j+1][totals_stat[2]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[2]] != '---':
                sig_str = data['fighter_2_stats']['totals']['round'][j+1][totals_stat[2]].split(' of ')
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[2]] = {'landed': int(sig_str[0]), 'attempted': int(sig_str[1])}
            else:
                 data['fighter_2_stats']['totals']['round'][j+1][totals_stat[2]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[3]] != '---':
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[3]] = float('0.' + data['fighter_1_stats']['totals']['round'][j+1][totals_stat[3]].replace('%', ''))
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[3]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[3]] != '---':
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[3]] = float('0.' + data['fighter_2_stats']['totals']['round'][j+1][totals_stat[3]].replace('%', ''))
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[3]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[4]] != '---':
                x = data['fighter_1_stats']['totals']['round'][j+1][totals_stat[4]].split(' of ')
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[4]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[4]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[4]] != '---':
                x = data['fighter_2_stats']['totals']['round'][j+1][totals_stat[4]].split(' of ')
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[4]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[4]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[5]] != '---':
                x = data['fighter_1_stats']['totals']['round'][j+1][totals_stat[5]].split(' of ')
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[5]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[5]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[5]] != '---':
                x = data['fighter_2_stats']['totals']['round'][j+1][totals_stat[5]].split(' of ')
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[5]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[5]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[6]] != '---':
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[6]] = float('0.' + data['fighter_1_stats']['totals']['round'][j+1][totals_stat[6]].replace('%', ''))    
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[6]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[6]] != '---':
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[6]] = float('0.' + data['fighter_2_stats']['totals']['round'][j+1][totals_stat[6]].replace('%', ''))
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[6]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[7]] != '---':
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[7]] = int(data['fighter_1_stats']['totals']['round'][j+1][totals_stat[7]])
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[7]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[7]] != '---':
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[7]] = int(data['fighter_2_stats']['totals']['round'][j+1][totals_stat[7]])
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[7]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[8]] != '---':
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[8]] = int(data['fighter_1_stats']['totals']['round'][j+1][totals_stat[8]])
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[8]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[8]] != '---':
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[8]] = int(data['fighter_2_stats']['totals']['round'][j+1][totals_stat[8]])
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[8]] = None

            if data['fighter_1_stats']['totals']['round'][j+1][totals_stat[9]] != '---':
                time_in_seconds = data['fighter_1_stats']['totals']['round'][j+1][totals_stat[9]].split(':')
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[9]] = int(time_in_seconds[0]) * 60 + int(time_in_seconds[1])
            else:
                data['fighter_1_stats']['totals']['round'][j+1][totals_stat[9]] = None

            if data['fighter_2_stats']['totals']['round'][j+1][totals_stat[9]] != '---':
                time_in_seconds = data['fighter_2_stats']['totals']['round'][j+1][totals_stat[9]].split(':')
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[9]] = int(time_in_seconds[0]) * 60 + int(time_in_seconds[1])
            else:
                data['fighter_2_stats']['totals']['round'][j+1][totals_stat[9]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[1]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]] != '---':
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]] = float('0.' + data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]].replace('%', ''))
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]] != '---':
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]] = float('0.' + data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]].replace('%', ''))
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[2]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[3]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[4]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[5]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[6]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[7]] = None

            if data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]] != '---':
                x = data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]].split(' of ')
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]] = None

            if data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]] != '---':
                x = data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]].split(' of ')
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]] = {'landed': int(x[0]), 'attempted': int(x[1])}
            else:
                data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[8]] = None

        return data

    fight_data['fighter_1_stats']['totals']['round'] = {}
    fight_data['fighter_2_stats']['totals']['round'] = {}
    for j, tr in enumerate(trs):
        tds = tr.findAll('td')

        fight_data['fighter_1_stats']['totals']['round'][j+1] = {}
        fight_data['fighter_2_stats']['totals']['round'][j+1] = {}

        for i, td in enumerate(tds):
            ps = td.findAll('p')

            for k, p in enumerate(ps):
                if k == 0:
                    fight_data['fighter_1_stats']['totals']['round'][j+1][totals_stat[i]] = p.get_text(strip=True)
                else:
                    fight_data['fighter_2_stats']['totals']['round'][j+1][totals_stat[i]] = p.get_text(strip=True)





    sig_strike_stats_div = div.find('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section').find_next('section', class_='b-fight-details__section js-fight-section')
    tbody_sig = sig_strike_stats_div.find('tbody')
    trs_sig = tbody_sig.findAll('tr')

    fight_data['fighter_1_stats']['sig_strike']['round'] = {}
    fight_data['fighter_2_stats']['sig_strike']['round'] = {}
    for j, tr in enumerate(trs_sig):
        tds = tr.findAll('td')

        fight_data['fighter_1_stats']['sig_strike']['round'][j+1] = {}
        fight_data['fighter_2_stats']['sig_strike']['round'][j+1] = {}

        for i, td in enumerate(tds):
            ps = td.findAll('p')

            for k, p in enumerate(ps):
                if k == 0:
                    fight_data['fighter_1_stats']['sig_strike']['round'][j+1][sig_strike_stats[i]] = p.get_text(strip=True)
                else:
                    fight_data['fighter_2_stats']['sig_strike']['round'][j+1][sig_strike_stats[i]] = p.get_text(strip=True)
    

    
    return convert_data(fight_data, len(trs))
    


def get_event_data(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    section = soup.find('section', class_='b-statistics__section_details')
    title = section.find('h2', class_='b-content__title').find('span', class_='b-content__title-highlight').get_text(strip=True)

    div_date = section.find('div', class_='b-list__info-box b-list__info-box_style_large-width')
    date_str = div_date.select_one('li:has(i:-soup-contains("Date:"))').get_text(strip=True).replace('Date:', '') # -> Need seperate date converter
    location_str = div_date.select_one('li:has(i:-soup-contains("Location:"))').get_text(strip=True).replace('Location:', '')

    tbody = section.find('tbody')
    print(f'Event: {title}\nDate: {date_str}\nLocation: {location_str}')
    for tr in tbody.find_all('tr', class_='b-fight-details__table-row b-fight-details__table-row__hover js-fight-details-click'):
        link = tr.find('td').find('a')
        if link:
            # print(f'Fighter: {link.text}, link: {link.get('href')}') # -> Works perfectly
            print(get_fight_data(link.get('href')))

def get_event_urls():
    response = requests.get('http://www.ufcstats.com/statistics/events/completed?page=all')
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    div = soup.find('div', class_='b-statistics__inner')
    table = div.find('table', class_='b-statistics__table-events')
    tbody = table.find('tbody')

    for tr in tbody.find_all('tr', class_='b-statistics__table-row'):
        link = tr.find('a')
        if link:
            print(get_event_data(link.get('href')))
    

def get_urls():
    for char in string.ascii_lowercase:
        # print(FIGHTERS_URL + f'?char={char}&page=all') -> This gives all URLs as intended, good for use
        # print(f'Scraping for fighters whose names start with {char.upper()}')
        get_fighter_urls(FIGHTERS_URL + f'?char={char}&page=all')

