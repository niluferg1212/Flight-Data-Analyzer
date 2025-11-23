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
    with open("results.txt", 'a') as f:
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


def horizontal_histogram(hour_counts, airline_name, airport_name, year):
    win = GraphWin(f'Departures by hour for {airline_name} from {airport_name}', 800, 550)
    win.setBackground('lightgray')

    left_margin = 150
    top_margin = 50
    bar_height = 25
    spacing = 10

    if not hour_counts:
        print(f'Warning: No flights found for {airline_name}. Histogram can not be drawn.')
        win.close()
        return
    
    max_count = max(hour_counts.values())
    
    if max_count == 0:
        print(f'Warning: No flights found for {airline_name} between 00:00 to 11.59. Histogram can not be drawn.')
        win.close()
        return

    scale =  500 / max_count

    title = Text(Point(400, 30), f'Departures by hour for {airline_name} from {airport_name} {year}')
    title.setSize(17)
    title.setStyle('bold')
    title.draw(win)

    y = top_margin

    total_flights = sum(hour_counts.values())

    for hour in range(12):
        count = hour_counts.get(hour, 0)
        bar_length = count * scale

        rect = Rectangle(
            Point(left_margin, y),
            Point(left_margin + bar_length, y + bar_height)
            )
        rect.setFill('teal')
        rect.draw(win)

        hour_label = Text(Point(left_margin - 40, y + bar_height/2), f'{hour:02d}:00')
        hour_label.draw(win)

        if count > 0:
            count_label = Text(Point(left_margin + bar_length + 10, y + bar_height/2), str(count))
            count_label.draw(win)
            
        y += bar_height + spacing

    x_label = Text(Point(400, 520), "Hours from 00:00 to 12:00")
    x_label.setSize(12)
    x_label.draw(win)

    total_label = Text(Point(400, 490), f"Total flights shown: {total_flights}")
    total_label.setStyle("bold")
    total_label.setSize(12)
    total_label.draw(win)

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
        hour_counts_dict = {}
        for row in data_list:
            if row[1][:2].upper() == airline_code.upper(): 
                try:
                    # Scheduled Departure Time (index 2)
                    time_str = row[2] 
                    hour = int(time_str.split(':')[0]) # Saat kısmını al (Örn: '08:45' -> 8)
                    
                    if 0 <= hour <= 11:
                        # Eğer saat 0-11 arasındaysa, ilgili indeksi artır
                        hour_counts_dict[hour] = hour_counts_dict.get(hour, 0) + 1
                        
                except (ValueError, IndexError):
                    pass # Hatalı saat formatlarını yoksay
                
        airline_name = airline_valid[airline_code]
        airport_name = airport_valid[airport_code]
                
        horizontal_histogram(hour_counts_dict, airline_name, airport_name, selected_year)

        again = input("Do you want to select a new data file? Y/N: ").upper()
        if again == "N":
            print("Thank you for using the Flight Data Analyzer.")
            break

if __name__ == "__main__":
    main()
    
#************************************************************************************************************
