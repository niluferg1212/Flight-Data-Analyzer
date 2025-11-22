"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w2144848
 4. Date: 23.11.2025
****************************************************************************

"""
from graphics import *
import csv
import math

data_list = []   # data_list An empty list to load and hold data from csv file

def load_csv(CSV_chosen):
    """
    This function loads any csv file by name (set by the variable 'selected_data_file') into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            data_list.append(row)

airport_valid = {
    'LHR': 'London Heathrow',
    'MAD': 'Madrid  Adolfo Suárez-Barajas',
    'CDG': 'Charles De Gaulle Internationa (Paris)',
    'IST': 'Istanbul Airport International',
    'AMS': 'Amsterdam Schipol',
    'LIS': 'Lisbon Portela',
    'FRA': 'Frankfurt Main',
    'FCO': 'Rome Fiumicino',
    'MUC': 'Munich International',
    'BCN': 'Barcelona International'}

airline_valid = {
    'BA': 'British Airways',
    'AF': 'Air France',
    'AY': 'Finnair',
    'KL': 'KLM',
    'SK': 'Scandinavian Airlines',
    'TP': 'TAP Air Portugal',
    'TK': 'Turkish Airlines',
    'W6': 'Wizz Air',
    'U2': 'easyJet',
    'FR': 'Ryanair',
    'A3': 'Aegean Airlines',
    'SN': 'Brussels Airlines',
    'EK': 'Emirates',
    'QR': 'Qatar Airways',
    'IB': 'Iberia',
    'LH': 'Lufthansa'}

def city_code():
    valid_codes = list(airport_valid.keys())
    while True:
        code = input('Please enter a three-letter city code: ').upper()
        if len(code) != 3:
            print('Wrong code length - please enter a three-letter city code.')
            continue
        elif code not in valid_codes:
            print('Unavailable city code - please enter a valid city code.')
            continue
        return code

def year():
    while True:
        user_input = input('Please enter the year requiredd in the format YYYY: ')
        if not user_input.isdigit() or len(user_input) != 4:
            print('Wrong data type - please enter a four-digit year value.')
            continue

        year_range = int(user_input)
        if year_range < 2000 or year_range > 2025:
            print('Out of range - please enter a value from 2000 to 2025.')
            continue
        return year_range

def get_airline_code():
    valid_codes = list(airline_valid.keys())

    while True:
        code = input('Enter a two-character Airline code to plot a histogram: ').upper()
        if len(code) != 2:
            print('Wrong code length - please enter a tow-letter airline code.')
            continue

        if code not in valid_codes:
            print('Unavailable Airline code please try again.')
            continue
        return code
    
def load_csv_dynamic(airport_code, year):
    selected_data_file = airport_code.upper() + str(year) + '.csv' #File name creating 

    try: #Catches the error (Error handling)
        with open(selected_data_file, 'r') as file: #'with open' closes automatically 
            csvreader = csv.reader(file) #csv.reader reads csv file row by row
            header = next(csvreader) #reads and skips the header row
            return [row for row in csvreader] #converts list all remainings
    except FileNotFoundError: 
        print(f'{selected_data_file} not found. Please try again. ')
        return None

def analyse_data(data_list):
    total_flights = 0
    terminal2_flights = 0
    short_flights = 0
    air_france_flights = 0
    temp_below_15 = 0
    ba_count = 0
    delayed_af = 0
    rain_hours = 0
    destination_counts = {} #makes a dictionary to store the counts for each destinations

    for flight in data_list:
        total_flights += 1
        
        if flight[8] == '2': # 2. Terminal 2 flights (index 8)
            terminal2_flights += 1

        try: 
            distance = int(flight[5])  # 3. Distance miles (index 5)
            if distance < 600:
                short_flights += 1
        except ValueError:
             pass

        airline = flight[1][:2].upper() # 4. Air France flights & 8. Delayed AF check
        if airline == 'AF':
            air_france_flights += 1
            if flight[3] > flight[2]: # Delay check (ActualDep > ScheduledDep)
                delayed_af += 1

        weather = flight[10] # 5. Temperature < 15°C (index 10)
        temp_str = weather.split('°')[0] if '°' in weather else '999'
        try:
            temperature = int(temp_str)
        except ValueError:
            temperature = 999 
            
        if temperature < 15:
            temp_below_15 += 1

        if airline == 'BA': # 6 & 7. British Airways count
            ba_count += 1

        if 'rain' in weather.lower(): # 9. Rain hours
            rain_hours += 1

        dest_code = flight[4] # 10. Destination counts (index 4)
        destination_counts[dest_code] = destination_counts.get(dest_code, 0) + 1

        # Calculations
    british_airways_percentage = (ba_count / total_flights) * 100 if total_flights > 0 else 0
    air_france_delayed_percentage = (delayed_af / air_france_flights) * 100 if air_france_flights > 0 else 0
    average_ba_per_hour = ba_count / 12  # Assuming 12 hours

    # 10. Least common destinations (Full names required for output)
    least_common_names = []
    if destination_counts:
        min_count = min(destination_counts.values())
        least_common_codes = [dest for dest, count in destination_counts.items() if count == min_count]
        for code in least_common_codes:
            least_common_names.append(airport_valid.get(code, code)) 
    
    outcomes = {
        'total_flights': total_flights,
        'terminal2_flights': terminal2_flights,
        'short_flights': short_flights,
        'air_france_flights': air_france_flights,
        'temp_below_15': temp_below_15,
        'british_airways_percentage': british_airways_percentage,
        'air_france_delayed_percentage': air_france_delayed_percentage,
        'average_ba_per_hour': average_ba_per_hour,
        'rain_hours': rain_hours,
        'least_common_destinations': least_common_names
    }
    return outcomes

def save_results(airport_code, year, outcomes):
    airport_name = airport_valid[airport_code]
    with open("results.txt", 'w') as f:
        f.write("*" * 50 + "\n")
        f.write(f"Flight Data Analysis for {airport_name} {year}\n")
        f.write("*" * 50 + "\n")
        f.write(f"Total flights from this airport: {outcomes['total_flights']}\n")
        f.write(f"Flights departing Terminal Two: {outcomes['terminal2_flights']}\n")
        f.write(f"Departures on flights under 600 miles: {outcomes['short_flights']}\n")
        f.write(f"Air France flights: {outcomes['air_france_flights']}\n")
        f.write(f"Flights departing in temperatures below 15°C: {outcomes['temp_below_15']}\n")
        f.write(f"Average British Airways flights per hour: {round(outcomes['average_ba_per_hour'],2)}\n")
        f.write(f"British Airways percentage of departures: {round(outcomes['british_airways_percentage'],2)}%\n")
        f.write(f"Air France delayed percentage: {round(outcomes['air_france_delayed_percentage'],2)}%\n")
        f.write(f"Hours with rain: {outcomes['rain_hours']}\n")

        least_common = outcomes['least_common_destinations']
        if len(least_common) == 1:
            f.write(f"Least common destination: {least_common[0]}\n")
        else:
            f.write(f"Least common destinations: {least_common}\n")
        f.write("\n")

    print("Results saved to results.txt")



    # 1. Total number of departure flights
    total_flights = len(data_list)

    # 2. Terminal 2 flights
    terminal2_count = sum(1 for row in data_list if row[8] == "2")

    # 3. Flights under 600 miles
    under_600 = sum(1 for row in data_list if int(row[5]) < 600)

    # 4. Air France flights
    air_france_total = sum(1 for row in data_list if row[1].startswith("AF"))

    # 5. Temperature < 15°C (WeatherConditions like “18°C clear”)
    def get_temp(row):
        temp_str = row[10].split()[0]     # "18°C"
        return int(temp_str.replace("°C", ""))

    temp_under_15 = sum(1 for row in data_list if get_temp(row) < 15)

    # 6. Average British Airways flights per hour (BA*** flight numbers)
    ba_total = sum(1 for row in data_list if row[1].startswith("BA"))
    avg_ba_per_hour = round(ba_total / 12, 2)

    # 7. % of total departures that are British Airways
    percent_ba = round((ba_total / total_flights) * 100, 2)

    # 8. % Air France flights delayed (delay = ActualDep > ScheduledDep)
    def delayed(row):
        return row[3] > row[2]  # string compare works: "00:27" > "00:12"

    af_delayed = sum(1 for row in data_list if row[1].startswith("AF") and delayed(row))
    percent_af_delayed = round((af_delayed / air_france_total) * 100, 2) if air_france_total else 0

    # 9. Rain hours — check if “rain” exists in WeatherConditions
    rain_hours = sum(1 for row in data_list if "rain" in row[10].lower())

    # 10. Least common destinations
    dest_counts = {}
    for row in data_list:
        dest = row[4]
        dest_counts[dest] = dest_counts.get(dest, 0) + 1

    min_count = min(dest_counts.values())
    least_common_destinations = [d for d, c in dest_counts.items() if c == min_count]

def plot_histogram(data_list, airline_valid, airport_valid, selected_year):
    hours = []
    for row in data_list:  
        # row list olduğu için indeksle erişiyoruz
        if row[1][:2].upper() == airline_valid.upper():  
            try:
                time_str = row[2]  # Scheduled Departure Time
                hour = int(time_str.split(':')[0]) 
                if 0 <= hour <= 11:
                    hours.append(hour)
            except (ValueError, IndexError):
                pass

    if len(hours) == 0:
        print("No flights found for this airline.")
        return

    # Histogram sayımları
    hour_counts = {}
    for h in hours:
        hour_counts[h] = hour_counts.get(h, 0) + 1

    # Grafik penceresi
    win = GraphWin(f"Histogram for {airline_valid}", 600, 400)
    win.master.lift()

    max_height = max(hour_counts.values())
    bar_width = 500 / len(hour_counts)

    x = 50
    for h, count in sorted(hour_counts.items()):
        height = (count / max_height) * 300
        
        bar = Rectangle(Point(x, 350), Point(x + bar_width, 350 - height))
        bar.setFill("blue")
        bar.draw(win)

        # Hour label
        label = Text(Point(x + bar_width/2, 360), str(h))
        label.draw(win)

        # Count label
        count_label = Text(Point(x + bar_width/2, 350 - height - 10), str(count))
        count_label.draw(win)

        x += bar_width

    # Title
    title = Text(Point(300, 20),
                 f"{airline_valid} Flights per Hour - {airport_valid} {selected_year}")
    title.draw(win)

    try:
        win.getMouse()
    except GraphicsError:
        pass
    finally:
        win.close()

def display_histogram(flight_counts, airline_valid, airport_valid, year):
    """
    Display a horizontal histogram of flight counts per hour.
    
    flight_counts: list of 12 integers representing flights in hours 0-11
    airline_name: full airline name (string)
    airport_name: full airport name (string)
    year: year of data (string/int)
    """
    
    win_width = 700
    win_height = 400
    margin = 50
    
    # Create window
    win = GraphWin("Flight Histogram", win_width, win_height)
    win.setBackground("white")
    
    # Scaling
    max_count = max(flight_counts) or 1  # avoid division by zero
    bar_width = (win_width - 2*margin) / len(flight_counts)
    scale = (win_height - 2*margin) / max_count
    
    # Draw bars
    for i, count in enumerate(flight_counts):
        x1 = margin + i*bar_width
        x2 = margin + (i+1)*bar_width - 5
        y1 = win_height - margin
        y2 = y1 - count*scale
        rect = Rectangle(Point(x1, y2), Point(x2, y1))
        rect.setFill("skyblue")
        rect.draw(win)
        
        # Draw flight count above bar
        Text(Point((x1+x2)/2, y2-10), str(count)).draw(win)
        
        # Draw hour label below bar
        Text(Point((x1+x2)/2, y1+10), str(i)).draw(win)
    
    # Title
    title = Text(Point(win_width/2, margin/2), f"{airline_valid} Flights at {airport_name} ({year})")
    title.setFace("helvetica")
    title.setStyle("bold")
    title.setSize(14)
    title.draw(win)
    
    # Y-axis label
    Text(Point(margin/2, win_height/2), "Flights").draw(win)
    
    # Wait for user click to close
    try:
        win.getMouse()
    except GraphicsError:
        pass
    finally:
        win.close()

def main():
    print("Welcome to the Flight Data Analyzer!")
    
    while True:
        global data_list
        data_list = []

        airport_code = city_code()
        selected_year = year()

        data_list = load_csv_dynamic(airport_code, selected_year)

        if data_list is None:
            continue

        # Verileri analiz et
        outcomes = analyse_data(data_list)
        
        print("*" * 80)
        print(f"File {airport_code}{selected_year}.csv selected - Planes departing {airport_valid[airport_code]} {selected_year}")
        print("*" * 80)
        print(f"The total number of flights from this airport was {outcomes['total_flights']}")
        print(f"The total number of flights departing Terminal Two was {outcomes['terminal2_flights']}")
        print(f"The total number of departures on flights under 600 miles was {outcomes['short_flights']}")
        print(f"There were {outcomes['air_france_flights']} Air France flights from this airport")
        print(f"There were {outcomes['temp_below_15']} flights departing in temperatures below 15 degrees")
        print(f"There was an average of {round(outcomes['average_ba_per_hour'],2)} British Airways flights per hour from this airport")
        print(f"British Airways planes made up {round(outcomes['british_airways_percentage'],2)}% of all departures")
        print(f"{round(outcomes['air_france_delayed_percentage'],2)}% of Air France departures were delayed")
        print(f"There were {outcomes['rain_hours']} hours in which rain fell")

        # Least common destinations - beginner-friendly cümle
        least_common = outcomes['least_common_destinations']

        if len(least_common) == 1:
            print("The least common destination is " + least_common[0])
        else:
            print(f"The least common destinations are {least_common}")
            
        save_results(airport_code, selected_year, outcomes)

        # Airline code for histogram
        airline_code = get_airline_code()
        plot_histogram(data_list, airline_code, airport_code, selected_year)

        again = input("Do you want to select a new data file? Y/N: ").upper()
        if again == "N":
            print("Thank you for using the Flight Data Analyzer.")
            break

if __name__ == "__main__":
    main()
    
#************************************************************************************************************


selected_data_file="CDG2021.csv" #hard coded csv name to be replaced with your dynamically created filename
load_csv(selected_data_file)     #calls the function "load_csv" sending the variable 'selected_data_file" as a parameter

#Some Example code queries to be replaced with those required by the brief. Compare these outputs to the supplied CSV files

print (f"The current file name is {selected_data_file}")
print ("")
print (f"First row of data_list is data_list[0] -> {data_list[0]}")
print ("")
print (f"Second item of the first row is flight number, data_list[0][1]      -> {data_list[0][1]}")
print ("")
print (f"Third item of the second row is scheduled depature, data_list[1][2] -> {data_list[1][2]}")

  






