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
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rates = []
        # Find the table with bank rates (it's after the "Precio Dólar en bancos y agentes de cambio de Santo Domingo" heading)
        heading = soup.find('h2', string='Precio Dólar en bancos y agentes de cambio de Santo Domingo')
        if heading:
            table = heading.find_next('table')
            if table:
                rows = table.find_all('tr')[1:]  # Skip header row
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        # Get bank name from the first column
                        bank_element = cols[0].find('a')
                        bank = bank_element.text.strip() if bank_element else cols[0].text.strip()
                        
                        # Get buy and sell rates
                        buy_text = cols[1].text.strip().replace('$', '').replace('=', '').strip()
                        sell_text = cols[2].text.strip().replace('$', '').replace('=', '').strip()
                        
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
                            except ValueError:
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
        
    except Exception as e:
        print(f"Error scraping rates: {str(e)}")
        raise

if __name__ == "__main__":
    scrape_rates() 