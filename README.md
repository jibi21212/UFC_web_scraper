# UFC Web Scraper

A comprehensive UFC data scraping system that collects, processes, and stores detailed fighter and event information from UFC's official statistics website. The system includes fighter statistics, event details, fight performances, and automated nationality detection.

## Features

- Complete UFC fighter database scraping
- Detailed event and fight statistics collection
- Automated nationality detection using intelligent web scraping
- Comprehensive fight performance metrics
- SQLite database storage
- Robust error handling and logging
- Progress tracking and estimation

## System Components

### 1. Web Scraper (webscraper.py)
- Main scraping orchestrator
- Collects fighter profiles, event details, and fight statistics
- Handles rate limiting and error recovery
- Multi-stage processing pipeline

### 2. Data Models (ufc_dataclasses.py)
- Structured data classes for:
  - Fighter profiles
  - Career statistics
  - Fight performances
  - Event details
  - Round-by-round statistics
  - Strike analytics

### 3. Nationality Scraper (nationality_scraper.py)
- Selenium-based intelligent scraping
- Handles multiple country name variations
- Supports regional and historical names
- Built-in retry mechanism

### 4. Database Handler (ufc_save_data.py)
- SQLite database setup and management
- Structured schema for all UFC data
- Efficient data storage and retrieval
- Relationship management between entities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jibi21212/UFC_web_scraper.git
cd UFC_web_scraper
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Requirements:

- Python 3.x
- Chrome Browser
- ChromeDriver (compatible with your Chrome version)
Sufficient disk space for SQLite database

## Usage

Run the main scraper:

```bash
python webscraper.py
```

The script executes in four stages:

1. Fighter data collection
2. Event data scraping
3. Nationality detection
4. Database storage

Progress and logs are written to 'ufc_scraper.log'

## Runtime Expectaions:

The complete scraping process typically takes around 6 hours to complete, with the majority of time (approximately 4 hours) spent on the nationality detection phase. The core data scraping only takes about 2 hours.

Note: The nationality scraping logic is currently being improved, and in future updates, a pre-compiled nationality dataset will be made available to skip this time-intensive step.

Note: Runtime may vary based on:

Internet connection speed
System specifications
Server response times
Number of fighters/events at time of scraping

## Database Schema
The system uses SQLite with the following main tables:

fighters: Basic fighter information
career_stats: Fighter career statistics
events: Event details
fights: Individual fight information
fight_performance: Fighter performance in specific fights
round_stats: Round-by-round statistics
strike_stats: Detailed strike statistics
strike_breakdown: Strike type analysis

## Error Handling
The system includes:

- Comprehensive logging to 'ufc_scraper.log'
- Exception handling for network issues
- Data validation at each stage
- Progress tracking with timestamps
- Automatic retry mechanisms

## Output Files
- ufc_data.db: SQLite database containing all scraped data
- ufc_scraper.log: Detailed logging of the scraping process
- Console output: Real-time progress updates

## Acknowledgments
UFC Stats website (http://www.ufcstats.com/statistics/events/completed)
UFC community and data contributors