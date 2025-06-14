import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz
import re

def get_bhd_rate():
    try:
        url = "https://www.bhd.com.do/wps/portal/bhd/bhd/personas/tasas-y-tarifas/tasas-de-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the USD rates in the table
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and 'USD' in cols[0].text:
                    buy = float(cols[1].text.strip().replace(',', ''))
                    sell = float(cols[2].text.strip().replace(',', ''))
                    return {"bank": "Banco BHD", "buy": buy, "sell": sell}
    except Exception as e:
        print(f"Error getting BHD rate: {str(e)}")
    return None

def get_banreservas_rate():
    try:
        url = "https://www.banreservas.com/personas/tasas-y-tarifas/tasas-de-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the USD rates in the table
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and 'USD' in cols[0].text:
                    buy = float(cols[1].text.strip().replace(',', ''))
                    sell = float(cols[2].text.strip().replace(',', ''))
                    return {"bank": "Banreservas", "buy": buy, "sell": sell}
    except Exception as e:
        print(f"Error getting Banreservas rate: {str(e)}")
    return None

def get_popular_rate():
    try:
        url = "https://www.popularenlinea.com/_api/web/lists/getbytitle('Tasas de Cambio')/items"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        for item in data['d']['results']:
            if 'USD' in item['Title']:
                buy = float(item['Compra'].replace(',', ''))
                sell = float(item['Venta'].replace(',', ''))
                return {"bank": "Banco Popular", "buy": buy, "sell": sell}
    except Exception as e:
        print(f"Error getting Popular rate: {str(e)}")
    return None

def get_lafise_rate():
    try:
        url = "https://www.bancolafise.com/tasas-de-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the USD rates in the table
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and 'USD' in cols[0].text:
                    buy = float(cols[1].text.strip().replace(',', ''))
                    sell = float(cols[2].text.strip().replace(',', ''))
                    return {"bank": "Banco Lafise", "buy": buy, "sell": sell}
    except Exception as e:
        print(f"Error getting Lafise rate: {str(e)}")
    return None

def get_vimenca_rate():
    try:
        url = "https://www.vimenca.com/tasas-de-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the USD rates in the table
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and 'USD' in cols[0].text:
                    buy = float(cols[1].text.strip().replace(',', ''))
                    sell = float(cols[2].text.strip().replace(',', ''))
                    return {"bank": "Banco Vimenca", "buy": buy, "sell": sell}
    except Exception as e:
        print(f"Error getting Vimenca rate: {str(e)}")
    return None

def get_santa_cruz_rate():
    try:
        url = "https://www.bancosantacruz.com.do/tasas-de-cambio"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the USD rates in the table
        table = soup.find('table', {'class': 'table'})
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3 and 'USD' in cols[0].text:
                    buy = float(cols[1].text.strip().replace(',', ''))
                    sell = float(cols[2].text.strip().replace(',', ''))
                    return {"bank": "Banco Santa Cruz", "buy": buy, "sell": sell}
    except Exception as e:
        print(f"Error getting Santa Cruz rate: {str(e)}")
    return None

def scrape_rates():
    rates = []
    
    # Get rates from each bank
    bank_functions = [
        get_bhd_rate,
        get_banreservas_rate,
        get_popular_rate,
        get_lafise_rate,
        get_vimenca_rate,
        get_santa_cruz_rate
    ]
    
    for get_rate in bank_functions:
        rate = get_rate()
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
    with open('rates.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully updated rates. Found {len(rates)} banks.")

if __name__ == "__main__":
    scrape_rates() 