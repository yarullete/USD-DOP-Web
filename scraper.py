import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz
import re
import os

def clean_rate(rate_text):
    # Remove $, =, whitespace, newlines and take only the first number
    cleaned = re.sub(r'[^\d.]', '', rate_text.split()[0])
    return cleaned

def get_bank_rate(url, bank_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Fetching rates for {bank_name}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table with rates
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')
            if len(rows) >= 2:  # At least header and one data row
                cols = rows[1].find_all('td')  # Get first data row
                if len(cols) >= 3:
                    buy_text = cols[1].get_text().strip()
                    sell_text = cols[2].get_text().strip()
                    
                    print(f"Raw rates for {bank_name}: Buy='{buy_text}', Sell='{sell_text}'")
                    
                    # Clean the rate texts
                    buy_clean = clean_rate(buy_text)
                    sell_clean = clean_rate(sell_text)
                    
                    print(f"Cleaned rates for {bank_name}: Buy='{buy_clean}', Sell='{sell_clean}'")
                    
                    try:
                        buy = float(buy_clean)
                        sell = float(sell_clean)
                        if buy > 0 and sell > 0:
                            return {
                                "bank": bank_name,
                                "buy": buy,
                                "sell": sell
                            }
                    except ValueError as e:
                        print(f"Error converting rates for {bank_name}: {str(e)}")
        
        print(f"Could not find valid rates for {bank_name}")
        return None
        
    except Exception as e:
        print(f"Error fetching rates for {bank_name}: {str(e)}")
        return None

def scrape_rates():
    # List of banks with their URLs
    banks = [
        {
            "name": "Banco BHD",
            "url": "https://www.infodolar.com.do/precio-dolar-entidad-banco-bhd.aspx"
        },
        {
            "name": "Banreservas",
            "url": "https://www.infodolar.com.do/precio-dolar-entidad-banreservas.aspx"
        },
        {
            "name": "Banco Popular",
            "url": "https://www.infodolar.com.do/precio-dolar-entidad-banco-popular.aspx"
        },
        {
            "name": "Banco Lafise",
            "url": "https://www.infodolar.com.do/precio-dolar-entidad-banco-lafise.aspx"
        },
        {
            "name": "Banco Vimenca",
            "url": "https://www.infodolar.com.do/precio-dolar-entidad-banco-vimenca.aspx"
        },
        {
            "name": "Banco Caribe",
            "url": "https://www.infodolar.com.do/precio-dolar-entidad-banco-caribe.aspx"
        }
    ]
    
    rates = []
    for bank in banks:
        rate = get_bank_rate(bank["url"], bank["name"])
        if rate:
            rates.append(rate)
    
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
    try:
        print(f"Writing rates to rates.json...")
        print(f"Current directory: {os.getcwd()}")
        print(f"Directory contents: {os.listdir('.')}")
        
        with open('rates.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        # Verify the file was written correctly
        with open('rates.json', 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
            print(f"Verified saved data: {json.dumps(saved_data, indent=2)}")
            
        print(f"Successfully updated rates. Found {len(rates)} banks.")
        if len(rates) == 0:
            print("WARNING: No rates were found!")
        else:
            print("Updated rates for:")
            for rate in rates:
                print(f"- {rate['bank']}: Buy ${rate['buy']:.2f}, Sell ${rate['sell']:.2f}")
                
    except Exception as e:
        print(f"Error writing rates.json: {str(e)}")
        raise

if __name__ == "__main__":
    scrape_rates() 