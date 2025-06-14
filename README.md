# USD to DOP Exchange Rates

A web application that displays current USD to DOP (Dominican Peso) exchange rates from various banks in the Dominican Republic. The rates are automatically updated daily at 8:00 AM Dominican Republic time.

## Features

- Real-time display of exchange rates from multiple Dominican banks
- Daily automatic updates at 8:00 AM (Dominican Republic time)
- Clean and responsive design
- Mobile-friendly interface

## How it Works

1. The application uses a GitHub Action to scrape exchange rates from InfoDolar.com.do
2. The rates are stored in a JSON file
3. The web interface displays the rates in a clean, easy-to-read format
4. The page automatically refreshes every 5 minutes to show the latest rates

## Setup

1. Fork this repository
2. Enable GitHub Pages in your repository settings:
   - Go to Settings > Pages
   - Select the main branch as the source
   - Save the settings

The site will be available at `https://[your-username].github.io/[repository-name]`

## Local Development

To run the scraper locally:

1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the scraper:
   ```bash
   python scraper.py
   ```

## License

MIT License
