# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import gender_guesser.detector as gender

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.html_content = None

    def fetch_content(self):
        # Send an HTTP GET request to the specified URL
        response = requests.get(self.url)
        if response.status_code == 200:
            self.html_content = response.text
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            self.html_content = None

    def parse_names(self):
        if self.html_content is None:
            return []
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(self.html_content, "html.parser")
        # Find all <strong> tags with the class "name" which contain employee names
        all_employees = soup.find_all(name="strong", class_="name")
        # Extract the text from each <strong> tag and store it in a list
        return [employee.get_text(strip=True) for employee in all_employees]

class GenderGuesser:
    def __init__(self):
        self.detector = gender.Detector()

    def guess_genders(self, names):
        # Extract the first name by splitting each full name and selecting the first element
        first_names = [f.split(' ')[0] for f in names]
        # Guess the gender for each first name
        return [self.detector.get_gender(first_name) for first_name in first_names]

class GenderStats:
    def __init__(self, names, genders):
        self.names = names
        self.genders = genders

    def count_genders(self):
        male_count = sum(1 for g in self.genders if g.startswith('male'))
        female_count = sum(1 for g in self.genders if g.startswith('female'))
        return male_count, female_count

    def save_to_file(self, filename):
        with open(filename, mode="w") as file:
            for name, gender in zip(self.names, self.genders):
                file.write(f"{name}: {gender}\n")

# Define the URL of the webpage to scrape
URL = "https://brkthru.com/team/"

# Create instances of the classes and use them
scraper = WebScraper(URL)
scraper.fetch_content()
employee_names = scraper.parse_names()

if employee_names:
    guesser = GenderGuesser()
    genders = guesser.guess_genders(employee_names)

    stats = GenderStats(employee_names, genders)
    male_count, female_count = stats.count_genders()

    # Print the counts of male and female names
    print(f"Number of males: {male_count}")
    print(f"Number of females: {female_count}")

    # Save the employee names and their guessed genders to a file
    stats.save_to_file("employees_with_genders.txt")
