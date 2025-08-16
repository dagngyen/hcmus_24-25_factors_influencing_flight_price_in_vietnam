# Import necessary libraries
import pandas as pd
import datetime
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By

def convert_datetime(date, time_str) -> str:
    """
    This function converts a time string to a 24-hour format datetime string.
    
    Input:
        date: str - The date string in the format "YYYY-MM-DD"
        time_str: str - The time string in the format "HH:MM AM/PM"
        
    Output:
        str - The datetime string in the format "YYYY-MM-DD HH:MM"
    """
    if time_str == "" or time_str is None:
        return None
    date_str = date
    if "+1" in time_str:
        time_str = time_str[:-2]
        date_str = (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Check if the time_str contains "AM"
    in_time = datetime.datetime.strptime(time_str.strip(), "%I:%M %p")
    out_time = datetime.datetime.strftime(in_time, "%H:%M")
    
    return f"{date_str} {out_time}"

# Crawl data by selenium
def scrape(flight_df, departure_city, arrival_city, departure_date, travel_class, max_retries=5):    
    retries = 0
    
    # Check dataframe is exsist
    if flight_df is None:
        flight_df = pd.DataFrame(columns=['scrape_date',
                                     'id_departure', 'id_arrival',
                                     'departure_datetime', 'arrival_datetime',
                                     'airline', 'travel_class', 'is_nonstop',
                                     'price'])
    
    while retries < max_retries:        
        web = f"https://www.google.com/travel/flights?q=One-way%20Flights%20to%20{arrival_city}%20from%20{departure_city}%20on%20{departure_date}%20oneway%20{travel_class}"
        driver = webdriver.Chrome()
        driver.get(web)
        driver.maximize_window()
        
        flight_entries = driver.find_elements(By.CSS_SELECTOR, 'div.yR1fYc')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        data_dict = {}
        count_flights = 0
        for entry in flight_entries:
            try:              
                departure_time = entry.find_element(By.CSS_SELECTOR, "span[aria-label^='Departure time:']").text
                arrival_time = entry.find_element(By.CSS_SELECTOR, "span[aria-label^='Arrival time:']").text
                airline = entry.find_element(By.CSS_SELECTOR, '.sSHqwe.tPgKwe.ogfYpf > span').text
                is_nonstop = entry.find_element(By.CLASS_NAME, 'rGRiKd').get_property('textContent')
                price = entry.find_element(By.CSS_SELECTOR, '.YMlIz.FpEdX > span').text
                
                departure_time = convert_datetime(departure_date, departure_time)
                arrival_time = convert_datetime(departure_date, arrival_time)
                if departure_time == None or arrival_time == None or price == 'Price unavailable':
                    # continue
                    break
                price = price[1:] # Remove currency symbol
                # Loại bỏ dấu phẩy và chuyển đổi sang int
                price = price.replace(",", "")
                                
                # Insert data to dataframe
                data_dict = {'scrape_date': current_date,
                            'id_departure': departure_city, 'id_arrival': arrival_city,
                            'departure_datetime': departure_time, 'arrival_datetime': arrival_time,
                            'airline': airline, 'travel_class': travel_class, 'is_nonstop': is_nonstop,
                            'price': price}
                flight_df.loc[len(flight_df)] = data_dict
                count_flights += 1
            except Exception as e:
                # print(e)
                continue
                
        driver.quit()
        
        if count_flights:
            break
            
        retries += 1
        time.sleep(2)
            
    return flight_df

def multi_scrape(flight_df, departure_city, arrival_city, start_date, end_date, travel_class) -> pd.DataFrame:
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if end_date < start_date:
        print("Start date was greater than end date, end date will be set to start date!")
        end_date = start_date
    if end_date < current_date:
        print("End date must be greater than current date!")
        return flight_df
    if start_date < current_date:
        print("Start date will be set to current date!")
        start_date = (datetime.datetime.strptime(current_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    departure_date = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d').tolist()
    
    # Check dataframe is exsist
    if flight_df is None:
        flight_df = pd.DataFrame(columns=['scrape_date',
                                     'id_departure', 'id_arrival',
                                     'departure_datetime', 'arrival_datetime',
                                     'airline', 'travel_class', 'is_nonstop',
                                     'price'])
    for dd in departure_date:
        for index in range(len(departure_city)):
            for tc in travel_class:
                if departure_city[index] == arrival_city[index]:
                    print("Departure city and arrival city must be different!")
                    continue
                flight_df = scrape(flight_df, departure_city[index], arrival_city[index], dd, tc)
                
    return flight_df