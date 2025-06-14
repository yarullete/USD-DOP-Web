import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz

def scrape_rates():
    url = "https://www.infodolar.com.do/precio-dolar-provincia-santo-domingo.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print("Fetching page from InfoDolar.com.do...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # List of banks we want to track
        target_banks = [
            "Banco BHD",
            "Banreservas",
            "Banco Popular",
            "Banco Lafise",
            "Banco Vimenca",
            "Banco Santa Cruz"
        ]
        
        rates = []
        print("Looking for rates table...")
        
        # Find all tables with class 'cotizaciones'
        tables = soup.find_all('table', class_='cotizaciones')
        print(f"Found {len(tables)} tables with class 'cotizaciones'")
        
        for table in tables:
            rows = table.find_all('tr')
            print(f"Processing table with {len(rows)} rows")
            
            for row in rows:
                # Skip header rows
                if row.find('th'):
                    continue
                    
                # Get bank name from the first column
                bank_cell = row.find('td', class_='colNombre')
                if bank_cell:
                    bank = bank_cell.find('span', class_='nombre').get_text().strip()
                    print(f"Found bank: '{bank}'")
                    
                    # Only process if it's one of our target banks
                    if bank in target_banks:
                        # Get buy and sell rates
                        buy_cell = row.find('td', class_='colCompraVenta')
                        sell_cell = buy_cell.find_next('td', class_='colCompraVenta') if buy_cell else None
                        
                        if buy_cell and sell_cell:
                            buy_text = buy_cell.get_text().strip().replace('$', '').replace('=', '').strip()
                            sell_text = sell_cell.get_text().strip().replace('$', '').replace('=', '').strip()
                            print(f"Rates for {bank}: Buy='{buy_text}', Sell='{sell_text}'")
                            
                            # Only add if both buy and sell rates are present and valid
                            if buy_text and sell_text and buy_text != '0.00' and sell_text != '0.00':
                                try:
                                    buy = float(buy_text)
                                    sell = float(sell_text)
                                    if buy > 0 and sell > 0:  # Additional validation
                                        rates.append({
                                            "bank": bank,
                                            "buy": buy,
                                            "sell": sell
                                        })
                                        print(f"Added rates for {bank}")
                                except ValueError as e:
                                    print(f"Error converting rates for {bank}: {str(e)}")
                                    continue
        
        # Sort rates by bank name
        rates.sort(key=lambda x: x['bank'])
        
        # Get current time in Dominican Republic timezone
        dominican_tz = pytz.timezone('America/Santo_Domingo')
        current_time = datetime.now(dominican_tz)
        
        data = {
            "last_updated": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "rates": rates
        }
        
        # Write to rates.json
        with open('rates.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully updated rates. Found {len(rates)} banks.")
        if len(rates) == 0:
            print("WARNING: No rates were found!")
            print("Available banks found:")
            for table in tables:
                for row in table.find_all('tr'):
                    bank_cell = row.find('td', class_='colNombre')
                    if bank_cell:
                        bank = bank_cell.find('span', class_='nombre').get_text().strip()
                        if bank:
                            print(f"- {bank}")
        
    except Exception as e:
        print(f"Error scraping rates: {str(e)}")
        raise

if __name__ == "__main__":
    scrape_rates() 