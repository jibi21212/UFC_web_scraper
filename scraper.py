import string
from bs4 import BeautifulSoup
import requests

# Function to extract specific fighter data based on the label
def extract_fighter_data(fighter_soup, label):
    data = fighter_soup.find('i', string=lambda text: text and label in text)
    if data:
        parent_li = data.find_parent('li')
        if parent_li:
            value = parent_li.get_text(strip=True).replace(f'{label}', '').strip()
            return value
    return 'N/A'

# Function to scrape match history from the fighter profile page
def scrape_match_history(fighter_soup, fighter_name):
    history = []
    # Locate the match history table rows
    match_history_table = fighter_soup.select('tbody.b-fight-details__table-body tr')

    for match in match_history_table:
        # Check if 'loss' exists in the <i class="b-flag__text"> element
        flag_text_element = match.select_one('i.b-flag__text')
        is_win = flag_text_element.get_text(strip=True).lower() if flag_text_element else 'N/A'
        # Extract opponent's name (the second fighter in the opponent list)
        opponent_elements = match.select('td.l-page_align_left p.b-fight-details__table-text a.b-link')
        opponent = opponent_elements[1].get_text(strip=True) if len(opponent_elements) > 1 else 'N/A'

        # Extract all 'p' elements with the class 'b-fight-details__table-text'
        method_elements = match.select('td.b-fight-details__table-col.l-page_align_left p.b-fight-details__table-text')

        if method_elements:
            # The method of victory (like "U-DEC", "KO") will be in the second-last 'p'
            method = method_elements[-2].get_text(strip=True)

            # If the method is "SUB", the last 'p' will contain specific submission details (like "Guillotine Choke")
            if len(method_elements) > 1 and method == "SUB":
                method += f" ({method_elements[-1].get_text(strip=True)})"
        else:
            method = 'N/A'


        history.append({
            'Opponent': opponent,
            'Result': is_win,
            'Method': method
        })

    return history

def scrape_fighter_profile(fighter_url):
    fighter_response = requests.get(fighter_url)
    fighter_soup = BeautifulSoup(fighter_response.content, 'html.parser')

    # Scraping fighter's name
    name = fighter_soup.select_one('span.b-content__title-highlight')
    if name:
        name = name.get_text(strip=True)
    else:
        print(f"Name not found at {fighter_url}. Skipping...")
        return None  # Skip if no name is found

    # Scrape fighter's height, weight, reach, stance, and DOB
    height = extract_fighter_data(fighter_soup, "Height:")
    weight = extract_fighter_data(fighter_soup, "Weight:")
    reach = extract_fighter_data(fighter_soup, "Reach:")
    stance = extract_fighter_data(fighter_soup, "STANCE:")
    dob = extract_fighter_data(fighter_soup, "DOB:")

    # Extract data from the left side (SLpM, Str. Acc., SApM, Str. Def.)
    career_stats_left = fighter_soup.select_one('.b-list__info-box-left .b-list__box-list')
    if career_stats_left:
        slpm = extract_fighter_data(career_stats_left, "SLpM:")
        str_acc = extract_fighter_data(career_stats_left, "Str. Acc.:")
        sapm = extract_fighter_data(career_stats_left, "SApM:")
        str_def = extract_fighter_data(career_stats_left, "Str. Def:")
    else:
        slpm = str_acc = sapm = str_def = 'N/A'

    # Extract data from the right side (TD Avg., TD Acc., TD Def., Sub. Avg.)
    career_stats_right = fighter_soup.select_one('.b-list__info-box-right .b-list__box-list')
    if career_stats_right:
        td_avg = extract_fighter_data(career_stats_right, "TD Avg.:")
        td_acc = extract_fighter_data(career_stats_right, "TD Acc.:")
        td_def = extract_fighter_data(career_stats_right, "TD Def.:")
        sub_avg = extract_fighter_data(career_stats_right, "Sub. Avg.:")
    else:
        td_avg = td_acc = td_def = sub_avg = 'N/A'

    # Scrape match history
    match_history = scrape_match_history(fighter_soup, name)

    # Print or save the scraped fighter details
    print(f"""
    Name: {name}
    Height: {height}
    Weight: {weight}
    Reach: {reach}
    Stance: {stance}
    DOB: {dob}
    SLpM: {slpm}
    Str. Acc.: {str_acc}
    SApM: {sapm}
    Str. Def.: {str_def}
    TD Avg.: {td_avg}
    TD Acc.: {td_acc}
    TD Def.: {td_def}
    Sub. Avg.: {sub_avg}
    Match History:
    """)

    for match in match_history:
        if match['Opponent']!='N/A':
            print(f"{name} vs {match['Opponent']} : {match['Result']} by {match['Method']}")
    print("-" * 40)

# Keep track of already scraped fighter URLs to avoid duplication
visited_fighter_urls = set()

# Loop through each letter of the alphabet and scrape fighter profiles
for alphabet in string.ascii_lowercase:
    url = f"http://www.ufcstats.com/statistics/fighters?char={alphabet}&page=all"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all fighter names and links
    fighters = soup.find_all('a', class_='b-link b-link_style_black')

    print(f"Fighters whose last name starts with {alphabet.upper()}:")
    
    # Loop through each fighter
    for fighter in fighters:
        fighter_name = fighter.get_text().strip()
        fighter_url = fighter['href']  # Extract the fighter's personal page link

        # Check if this URL has already been visited
        if fighter_url in visited_fighter_urls:
            continue  # Skip duplicates

        # Add the URL to the visited set
        visited_fighter_urls.add(fighter_url)

        # Ensure we're accessing a new fighter profile each time
        print(f"Accessing profile page for {fighter_name}: {fighter_url}")
        scrape_fighter_profile(fighter_url)

    print("-" * 40)  # Separator between letters
