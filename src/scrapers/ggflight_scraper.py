# Import necessary libraries
import pandas as pd
import datetime
import time

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
# Crawl data by selenium
def scrape(flight_df, departure_city, arrival_city, departure_date, travel_class, max_retries=5):   
    """
    This function scrapes flight data from Google Flights using Selenium.

    Input:
        flight_df: pd.DataFrame - The DataFrame to store scraped flight data.
        departure_city: str - The IATA code of the departure city.
        arrival_city: str - The IATA code of the arrival city.
        departure_date: str - The departure date in the format "YYYY-MM-DD".
        travel_class: str - The travel class (e.g., "Economy", "Business").
        max_retries: int - The maximum number of retries for scraping.
    Output:
        pd.DataFrame - The DataFrame containing the scraped flight data.
    """

    retries = 0
    
    # Check dataframe is exsist
    if flight_df is None:
        flight_df = pd.DataFrame(columns=['timestamp',
                                          'id_departure', 'id_arrival',
                                          'departure_datetime', 'arrival_datetime',
                                          'airline_name', 'travel_class', 'is_nonstop',
                                          'price'])
    
    while retries < max_retries:        
        web = f"https://www.google.com/travel/flights?q=One-way%20Flights%20to%20{arrival_city}%20from%20{departure_city}%20on%20{departure_date}%20oneway%20{travel_class}"
        # driver = webdriver.Chrome()
        # --- Cấu hình cho Docker Environment ---
        options = Options()
        options.add_argument('--headless') # Chạy ẩn không cần giao diện
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")

        # Thay vì webdriver.Chrome(), ta dùng webdriver.Remote
        # 'selenium' là tên service trong docker-compose, port 4444 là mặc định
        try:
            driver = webdriver.Remote(
                command_executor='http://selenium:4444/wd/hub',
                options=options
            )
        except Exception as e:
            print(f"Không thể kết nối tới Selenium Container: {e}")
            return None
        # --- [CHANGE END] ---

        driver.get(web)
        # driver.maximize_window()
        
        flight_entries = driver.find_elements(By.CSS_SELECTOR, 'div.yR1fYc')
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                is_nonstop = True if is_nonstop == "Nonstop" else False
                price = price[1:] # Remove currency symbol
                # Loại bỏ dấu phẩy và chuyển đổi sang int
                price = price.replace(",", "")
                                
                # Insert data to dataframe
                data_dict = {'timestamp': current_date,
                            'id_departure': departure_city, 'id_arrival': arrival_city,
                            'departure_datetime': departure_time, 'arrival_datetime': arrival_time,
                            'airline_name': airline, 'travel_class': travel_class, 'is_nonstop': is_nonstop,
                            'price': price}
                flight_df.loc[len(flight_df)] = data_dict
                count_flights += 1
            except Exception as e:
                # print(e)
                continue
                
        driver.quit()
        
        if count_flights:
            return flight_df
            
        retries += 1
        time.sleep(2)
    
    print(f"Scraping failed for {departure_city} to {arrival_city} on {departure_date} in {travel_class} class after {max_retries} retries.")
    return None

def GGFlightScraper(flight_df, departure_city, arrival_city, start_date, end_date, travel_class) -> pd.DataFrame:
    """
    This function performs multiple scraping operations over a range of dates and cities.

    Input:
        flight_df: pd.DataFrame - The DataFrame to store scraped flight data.
        departure_city: list - A list of IATA codes for departure cities.
        arrival_city: list - A list of IATA codes for arrival cities.
        start_date: str - The start date in the format "YYYY-MM-DD".
        end_date: str - The end date in the format "YYYY-MM-DD".
        travel_class: list - A list of travel classes (e.g., ["Economy", "Business"]).
    Output:
        pd.DataFrame - The DataFrame containing the scraped flight data.
    """
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
        flight_df = pd.DataFrame(columns=['timestamp',
                                          'id_departure', 'id_arrival',
                                          'departure_datetime', 'arrival_datetime',
                                          'airline_name', 'travel_class', 'is_nonstop',
                                          'price'])
    for dd in departure_date:
        for index in range(len(departure_city)):
            for tc in travel_class:
                if departure_city[index] == arrival_city[index]:
                    print("Departure city and arrival city must be different!")
                    continue
                flight_df = scrape(flight_df, departure_city[index], arrival_city[index], dd, tc)
                
    return flight_df