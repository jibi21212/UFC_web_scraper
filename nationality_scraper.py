UFC_COUNTRIES = {
    "USA", "Brazil", "Japan", "Russia", "Canada", "United Kingdom", "Mexico",
    "South Korea", "Australia", "China", "France", "Poland", "Netherlands",
    "Germany", "Sweden", "Ireland", "New Zealand", "Peru", "Ukraine",
    "Argentina", "Georgia", "Italy", "Kazakstan", "Philippines", "South Africa",
    "Croatia", "Cuba", "Indonesia", "Lithuania", "Armenia", "India",
    "Uzbekistan", "Czech Republic", "Denmark", "Venezuela", "Iran", "Jamaica",
    "Nigeria", "Norway", "Romania", "Spain", "Finland", "Tajikistan",
    "Bosnia and Herzegovina", "Ecuador", "Serbia", "Afghanistan", "Belgium",
    "Bulgaria", "Cameroon", "Colombia", "Guam", "Moldova", "Vietnam",
    "Albania", "Angola", "Austria", "Belarus", "Bolivia", "Chile", "Congo",
    "Dominican Republic", "Iraq", "Kyrgyzstan", "Mongolia", "Morocco",
    "Panama", "Switzerland", "The Democratic Republic of Congo", "Turkey",
    "Azerbaijan", "Bahamas", "Cyprus", "El Salvador", "Estonia", "Hungary",
    "Jordan", "Palestine", "Paraguay", "Portugal", "Puerto Rico", "Singapore",
    "Slovakia", "Suriname", "Syria", "Thailand", "Uruguay", "Zimbabwe",
    "Algeria", "American Samoa", "Anguilla", "Cape Verde", "Costa Rica",
    "Egypt", "Ghana", "Greece", "Grenada", "Guyana", "Haiti", "Hong Kong",
    "Iceland", "Kurdistan", "Latvia", "Lebanon", "Liberia", "Macedonia",
    "Montenegro", "Myanmar", "Nicaragua", "Niger", "Solomon Islands",
    "Taiwan", "Trinidad and Tobago", "Tunisia", "U.S. Virgin Islands",
    "Uganda", "United Arab Emirates"
}

COUNTRY_VARIATIONS = {
    "USA": ["United States", "United States of America", "US", "U.S.A.", "U.S.", "American", "America"],
    "United Kingdom": ["UK", "Britain", "Great Britain", "England", "Scotland", "Wales", "Northern Ireland", "British"],
    "Russia": [
        "Russian Federation", 
        "Russian", 
        "USSR", 
        "Soviet Union",
        "Dagestan",  # Khabib, Islam Makhachev
        "Republic of Dagestan",
        "Chechnya",  # Many fighters from here too
        "Chechen Republic",
        "North Caucasus",
        "Ingushetia",
        "Republic of Ingushetia",
        "North Ossetia",
        "Republic of North Ossetia-Alania",
        "Siberia",
        "Buryatia",
        "Republic of Buryatia",
        "Yakutia",
        "Republic of Sakha",
    ],
    "South Korea": ["Korea", "Republic of Korea", "ROK", "Korea South"],
    "China": ["People's Republic of China", "PRC", "Chinese", "Mainland China"],
    "Netherlands": ["Holland", "Dutch"],
    "Czech Republic": ["Czechia", "Czech"],
    "Bosnia and Herzegovina": ["Bosnia", "BiH"],
    "Dominican Republic": ["DR", "Dom Rep"],
    "The Democratic Republic of Congo": ["DRC", "DR Congo", "Congo-Kinshasa"],
    "Congo": ["Republic of Congo", "Congo-Brazzaville"],
    "United Arab Emirates": ["UAE", "Emirates"],
    "U.S. Virgin Islands": ["USVI", "Virgin Islands"],
    "South Africa": ["RSA", "Republic of South Africa"],
    "New Zealand": ["NZ", "Aotearoa"],
    "Puerto Rico": ["PR"],
    "American Samoa": ["AS"],
    "Cape Verde": ["Cabo Verde"],
    "Myanmar": ["Burma"],
    "Macedonia": ["North Macedonia", "FYROM"],
    "Kurdistan": ["Iraqi Kurdistan", "Kurdish Region"],
    "Hong Kong": ["HK", "HKSAR"],
    
    # Countries that might need accent variations
    "Mexico": ["México"],
    "Peru": ["Perú"],
    "Panama": ["Panamá"],
    
    # Countries that might appear with "Republic of"
    "Georgia": ["Republic of Georgia"],
    "Armenia": ["Republic of Armenia"],
    "Moldova": ["Republic of Moldova"],
    "Belarus": ["Republic of Belarus"],
    "Azerbaijan": ["Republic of Azerbaijan"],
    
    # Countries that might appear with demonyms
    "Brazil": ["Brazilian"],
    "Japan": ["Japanese"],
    "Canada": ["Canadian"],
    "Mexico": ["Mexican"],
    "Australia": ["Australian"],
    "France": ["French"],
    "Poland": ["Polish"],
    "Germany": ["German"],
    "Sweden": ["Swedish"],
    "Ireland": ["Irish"],
    "Ukraine": ["Ukrainian"],
    "Argentina": ["Argentinian", "Argentine"],
    "Italy": ["Italian"],
    "Philippines": ["Filipino"],
    "Croatia": ["Croatian"],
    "Cuba": ["Cuban"],
    "Indonesia": ["Indonesian"],
    "Lithuania": ["Lithuanian"],
    "India": ["Indian"],
    "Venezuela": ["Venezuelan"],
    "Iran": ["Iranian", "Persian"],
    "Jamaica": ["Jamaican"],
    "Nigeria": ["Nigerian"],
    "Norway": ["Norwegian"],
    "Romania": ["Romanian"],
    "Spain": ["Spanish"],
    "Finland": ["Finnish"],
    "Serbia": ["Serbian"],
    "Belgium": ["Belgian"],
    "Bulgaria": ["Bulgarian"],
    "Cameroon": ["Cameroonian"],
    "Colombia": ["Colombian"],
    "Vietnam": ["Vietnamese"],
    "Albania": ["Albanian"],
    "Austria": ["Austrian"],
    "Chile": ["Chilean"],
    "Mongolia": ["Mongolian"],
    "Morocco": ["Moroccan"],
    "Switzerland": ["Swiss"],
    "Turkey": ["Turkish"],
    "Hungary": ["Hungarian"],
    "Portugal": ["Portuguese"],
    "Slovakia": ["Slovak"],
    "Syria": ["Syrian"],
    "Thailand": ["Thai"],
    "Uruguay": ["Uruguayan"],
    "Zimbabwe": ["Zimbabwean"],
    "Algeria": ["Algerian"],
    "Egypt": ["Egyptian"],
    "Ghana": ["Ghanaian"],
    "Greece": ["Greek"],
    "Iceland": ["Icelandic"],
    "Latvia": ["Latvian"],
    "Lebanon": ["Lebanese"],
    "Nicaragua": ["Nicaraguan"],
    "Tunisia": ["Tunisian"],
    "Uganda": ["Ugandan"],
    "Other" : ["Unlisted"]
}

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import Dict
from datetime import datetime


def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Add user agent to make it look more like a regular browser
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Ignore certificate errors and disable logging
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)  # Set page load timeout
        return driver
    except Exception as e:
        print(f"Error setting up ChromeDriver: {str(e)}")
        raise

def get_fighter_nationality(fighter_name: str, driver) -> str:
    try:
        search_query = f"UFC fighter {fighter_name} nationality wiki"
        driver.get("https://www.google.com")
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        results = driver.find_elements(By.CLASS_NAME, "g")
        search_text = " ".join([result.text.lower() for result in results[:3]])
        
        print(f"\nSearch text found:\n{search_text}\n")
        
        for country in UFC_COUNTRIES:
            country_lower = country.lower()
            patterns = [
                f"is a {country_lower}",
                f"is an {country_lower}",
                f"{country_lower} professional mixed martial artist",
                f"represents {country_lower}",
                f"fighting out of {country_lower}",
                f"nationality: {country_lower}",
                f"nationality {country_lower}"
            ]
            
            for pattern in patterns:
                if pattern in search_text:
                    print(f"Found match with pattern: '{pattern}'")
                    return country
            
            # Check variations
            if country in COUNTRY_VARIATIONS:
                for variation in COUNTRY_VARIATIONS[country]:
                    variation_lower = variation.lower()
                    variation_patterns = [
                        f"is a {variation_lower}",
                        f"is an {variation_lower}",
                        f"{variation_lower} professional mixed martial artist",
                        f"represents {variation_lower}",
                        f"fighting out of {variation_lower}",
                        f"nationality: {variation_lower}",
                        f"nationality {variation_lower}"
                    ]
                    
                    for pattern in variation_patterns:
                        if pattern in search_text:
                            print(f"Found variation match with pattern: '{pattern}'")
                            return country
        
        print(f"No country found in search results for {fighter_name}")
        return "Unlisted"
        
    except Exception as e:
        print(f"Error getting nationality for {fighter_name}: {str(e)}")
        return "Unlisted"



def update_fighters_nationality(fighters_dict: Dict, save_interval: int = 50) -> Dict:
    """
    Update nationality for all fighters in the dictionary using one browser instance.
    
    Args:
        fighters_dict: Dictionary of fighter objects
        save_interval: How often to print progress
    """
    driver = setup_driver()
    total_fighters = len(fighters_dict)
    processed = 0
    start_time = datetime.now()
    
    try:
        print(f"Starting nationality updates for {total_fighters} fighters...")
        
        for name, fighter in fighters_dict.items():
            try:
                nationality = get_fighter_nationality(name, driver)
                fighter.nationality = nationality
                processed += 1
                
                # Progress tracking
                if processed % save_interval == 0:
                    elapsed = datetime.now() - start_time
                    avg_time = elapsed.total_seconds() / processed
                    remaining = (total_fighters - processed) * avg_time
                    
                    print(f"\nProgress: {processed}/{total_fighters} ({(processed/total_fighters)*100:.1f}%)")
                    print(f"Time elapsed: {elapsed}")
                    print(f"Estimated time remaining: {remaining:.0f} seconds")
                    print(f"Last processed: {name} -> {nationality}")
                
                # Add delay between requests
                time.sleep(2)
                
            except Exception as e:
                print(f"\nError processing {name}: {e}")
                continue
    
    except Exception as e:
        print(f"\nFatal error: {e}")
    
    finally:
        print("\nClosing browser...")
        driver.quit()
        
    print(f"\nProcessing complete. Updated {processed} fighters.")
    return fighters_dict



def test_nationalities():
    driver = None
    try:
        print("Setting up ChromeDriver...")
        driver = setup_driver()
        '''"Khabib Nurmagomedov",
            "Israel Adesanya",
            "Francis Ngannou",
            "Conor McGregor",
            "Alexander Volkanovski",
            "Petr Yan"'''
        test_fighters = [
            
            "Dustin Poirier",
            "Robert Whittaker",
        ]
        
        for fighter in test_fighters:
            print(f"\nSearching nationality for {fighter}...")
            try:
                nationality = get_fighter_nationality(fighter, driver)
                print(f"{fighter}: {nationality}")
                time.sleep(2)
            except Exception as e:
                print(f"Error processing {fighter}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Fatal error in test: {str(e)}")
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

