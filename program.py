"""
Categorical Marking System (Better)
Tejas Parmar - A00026547
Last Modified: 24 Jan 2025
"""
# Necessary Impports
import logging
import threading
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from tabulate import tabulate
from statistics import mean, median

# Configuring the logging module - TIME, DATE - LEVEL - MESSAGE
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='cms.log',
    filemode='a'
)

# Lists for possible marks
category_marks_lists = (0, 5, 15, 25, 32, 35, 38,
                        42, 45, 48, 52, 55, 58,
                        62, 65, 68, 72, 75, 78,
                        82, 85, 92, 100)

# Categories dictionary to determine category
categories = {
    "Aurum Standard": [100],
    "Upper First": [82, 85, 92],
    "First": [72, 75, 78],
    "2:1": [62, 65, 68],
    "2:2": [52, 55, 58],
    "Third": [42, 45, 48],
    "Condonable Fail": [32, 35, 38],
    "Fail": [25, 15, 5],
    "Defecit Opus": [0]
}

# Student class
class Student:
    
    # Initializing necessary attributes
    def __init__(self, student_id, name, dob, scores):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.scores = scores
        self.age = 0
        self.overall = 0
        self.rounded = 0
        self.category = ""

    # Method to calculate age
    def calculate_age(self):
        birth_date = datetime.strptime(self.dob, "%Y-%m-%d")
        today = datetime.now()
        self.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Method to calculate overall score
    def calculate_overall_score(self, weights):
        if len(self.scores) != len(weights): # Return an error if there if number of scores provided are not equals to number of weights
            raise ValueError("The number of scores and weights must match.")
        self.overall = sum(s * w for s, w in zip(self.scores, weights))

    # Method to round the score to category
    def round_to_category(self):
        closest_boundary = min(category_marks_lists, key=lambda x: abs(x - self.overall))
        self.rounded = closest_boundary
        self.category = self.determine_category(closest_boundary)

    # Method to determine category
    def determine_category(self, boundary):
        if boundary < 0 or boundary > 100:
            return 'Ungraded' # Return ungraded if out of bound
        for category, values in categories.items(): # Search for boundary in categories dictionary
            if boundary in values:
                return category # Return the category name
        return 'Ungraded' # Redundant - self check - does not make any difference

# Module Configuration Class
class ModuleConfig:
    
    # Initialize configuration list
    def __init__(self):
        self.module_configuration = {}  # e.g. {"Coursework1": 0.2, "Coursework2": 0.3, ...}

    # Middleware method to ask for custom module setup
    def setup_module(self):
        if not self.ask_for_custom_configuration(): # Ask for confirmation
            return # Return to main if no

        module_name = input("Enter module name: ")  # Redundant
        self.configure_module() # Call method to configure module

    # Method to ask for custom module config
    def ask_for_custom_configuration(self):
        while True:
            choice = input("Would you like to setup custom module configuration? (y/n): ").lower()
            if choice in ["n", "no"]:
                print("\n")
                return False
            elif choice in ["y", "yes"]:
                return True
            print("Invalid choice. Please enter 'y' or 'n'.")

    # Method to configure module
    def configure_module(self):
        while True:
            try:
                num_components = self.get_number_of_components() # get the number of component
                self.module_configuration.clear() # Clear any previous module config to avoid issues
                total_weight = self.get_component_weights(num_components) # Get component weights based on the number of components

                if abs(total_weight - 100) > 0.01: # Check if the weights add up to 100%
                    print("Weights must sum to 100%. Please try again.")
                    continue
                
                print("Module configuration complete.")
                return
            except ValueError:
                logging.error("Entered an invalid integer.")
                print("Please enter a valid integer for the number of components.")

    # Method to get the number of components
    def get_number_of_components(self):
        while True:
            try:
                num_components = int(input("How many assessment components does this module have? "))
                if num_components <= 0:
                    print("Number of components must be a positive integer.")
                    continue
                return num_components
            except ValueError:
                logging.error("Invalid number of components.")
                print("Invalid input. Please enter a valid integer.")

    # Method to get component weights
    def get_component_weights(self, num_components):
        total_weight = 0
        for i in range(num_components):
            while True:
                try:
                    comp_name = input(f"Component {i+1} name: ").strip()
                    if not comp_name:
                        print("Component name cannot be empty.")
                        continue
                    weight = float(input(f"Enter {i+1} weight (%): "))
                    if weight <= 0 or weight > 100:
                        print("Weight must be between 0 and 100.")
                        continue
                    self.module_configuration[comp_name] = weight / 100
                    total_weight += weight
                    break
                except ValueError:
                    logging.error("Invalid number of weights.")
                    print("Invalid input. Please try again.")
        return total_weight

    # Return the usual four weights if no configuration is available - helper method
    def get_weights(self):
        if self.module_configuration:
            return list(self.module_configuration.values())
        return [0.1, 0.2, 0.3, 0.4]  # default

# CMS Class
class CategoricalMarkingSystem:
    
    # Initializing required data
    def __init__(self):
        self.students_data = {}
        self.module_config = ModuleConfig()

    # Main method of class
    def run(self):
        print("----- Welcome to the Categorical Marking System -----")
        print("\tMade by Tejas Parmar - A00026547\n")
        self.module_config.setup_module() # Ask for module config
        self.ask_for_mode() # Ask for mode

        if not self.students_data: # Exit if no data exists
            print("No data is provided. Exiting the program.")
            return

        # Displaying and saving data
        self.display_and_save_data()
        
        # Option to show analytics and student distribution
        while(True):
            choice = input("\nWould you like to view score analytics & student distribution? (y/n): ").lower()
            if choice in ["y", "yes"]:
                self.show_analytics()
                break
            elif choice in ["n", "no"]:
                break
            else:
                print("Invalid choice. Please try again.")
        
        # Option to send emails to students
        while(True):
            choice = input("\nWould you like to send notifications to failing students? (y/n): ").lower()
            if choice in ["y", "yes"]:
                self.notify_failing_students()
                return
            elif choice in ["n", "no"]:
                return
            else:
                print("Invalid choice. Please try again.")

    # Ask for mode
    def ask_for_mode(self):
        while True:
            print("\nEnter 1 to input information manually.")
            print("Enter 2 to read and input information from a file.\n")

            try:
                mode = int(input("Enter your choice (1/2): "))
                if mode not in [1, 2]:
                    print("Invalid choice. Please enter 1 or 2.")
                    continue
                if mode == 1:
                    print("\nNow, let's enter student information and grades.")
                    self.collect_student_data()
                elif mode == 2:
                    filename = input("Enter the filename/path to file: ") # ask for path to file or filename
                    self.advanced(filename)
                break
            except ValueError:
                logging.error("Invalid mode selected.")
                print("Please enter a valid integer (1 or 2).")

    # Method to collect student data
    def collect_student_data(self):
        weights = self.module_config.get_weights() # Get weights from helper function
        while True:
            try: # Enter all the student information (manual part)
                student_id = self.validate_input('id', "\nEnter Student ID (2-digit) (or 'end' to finish): ")
                if student_id.lower() == 'end':
                    break

                if student_id in self.students_data:
                    print("\nStudent ID already exists. Please try again.")
                    continue

                name = self.validate_input('name', "Enter student name: ")
                dob = self.validate_input('dob', 'Enter date of birth (YYYY-MM-DD): ')
                scores = self.collect_scores()

                stu = Student(student_id, name, dob, scores) # Create student object based on information
                stu.calculate_age() # calculate age
                stu.calculate_overall_score(weights) # calculate overall scre
                stu.round_to_category() # round to category

                self.students_data[student_id] = stu
                logging.info(f"Collected data for student ID {student_id}")

                if len(self.students_data) >= 3: # End taking information if studnets are equal to three
                    break
            except ValueError:
                logging.error("Invalid student information.")
                print("Invalid data. Please try again.")
                continue

    # Method to collect scores
    def collect_scores(self):
        scores = []
        if self.module_config.module_configuration: # Collect scores as per the module config if it is available
            print("Module configuration is available.")
            for component in self.module_config.module_configuration:
                score = self.validate_input('score', f"Enter score for {component}: ")
                scores.append(score)
        else: # Enter scores for the four usual cworksS
            for i in range(4):
                score = self.validate_input('score', f"Enter score for Coursework {i+1}: ")
                scores.append(score)
        return scores

    # Method for advanced mode
    def advanced(self, filename):
        self.students_data.clear()
        weights = self.module_config.get_weights()

        try: # Open given file name
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logging.error("File not found error occurred.")
            print(f"File {filename} not found")
            return
        
        # Sub-function to process a chuck of the data
        def process_chunk(chunk, thread_id):
            total = len(chunk)
            for i, line in enumerate(chunk, 1): # for line in each chunk
                stu = self.process_each_line(line, thread_id) # proess each line
                if stu:
                    stu.calculate_age()
                    stu.calculate_overall_score(weights)
                    stu.round_to_category()

                    # Combine both threats
                    lock.acquire()
                    try: # Check for duplicates
                        if stu.student_id not in self.students_data:
                            self.students_data[stu.student_id] = stu
                    finally: # Release threads
                        lock.release()
                if thread_id == 1:  # Only show progress from one thread
                    print(f"\rProgress: {i}/{total} records processed", end="")
                        
        # Calculate midpoint of the number of lines
        mid_point = len(lines) // 2
        chunk1 = lines[:mid_point] # Distribute between chunk 1 & 2
        chunk2 = lines[mid_point:]

        # Get a lock pointer for threading
        lock = threading.Lock()
        
        # Initialize two threads both responsible for processing each chunk
        t1 = threading.Thread(target=process_chunk, args=(chunk1, 1))
        t2 = threading.Thread(target=process_chunk, args=(chunk2, 2))

        # Start threads
        t1.start()
        t2.start()
        
        # Join threads
        t1.join()
        t2.join()

    # Method to process each line.
    def process_each_line(self, line, thread_id):
        try: # Strip each part of line by commas
            parts = line.strip().split(',')
        
            # Get expected number of scores from module config
            expected_scores = (len(self.module_config.module_configuration) if self.module_config.module_configuration else 4)
        
            # Check if total parts match expected format
            expected_parts = 3 + expected_scores  # id, name, dob + scores
            if len(parts) != expected_parts:
                logging.warning(f"Thread {thread_id}: Invalid number of parts. Expected {expected_parts}, got {len(parts)}")
                if thread_id == 1:
                    print(f"Skipping invalid data: File contains {len(parts)-3} scores but module requires {expected_scores}")
                return None
            
            student_id, name, dob = parts[:3]
            scores = [float(score) for score in parts[3:7]]

            # Validate all fields
            try:
                self.validate_id(student_id)
                self.validate_name(name)
                self.validate_dob(dob)
                for sc in scores:
                    self.validate_score(str(sc))
            except ValueError as e:
                logging.warning(f"Thread {thread_id}: Validation error - {e}")
                if thread_id == 1:
                    print(f"Skipping invalid data: {e}")
                return None

            if student_id in self.students_data:
                logging.warning(f"Thread {thread_id}: Duplicate ID {student_id}")
                if thread_id == 1:
                    print(f"Skipping duplicate student ID: {student_id}")
                return None

            return Student(student_id, name, dob, scores)
        
        except Exception as e:
            logging.error(f"Thread {thread_id}: Unexpected error - {e}")
            if thread_id == 1:
                print("Skipping invalid data.")
            return None

    def validate_input(self, input_type, prompt):
        """Generic input validation method that handles different types of inputs."""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("Input cannot be empty. Please try again.")
                    continue

                if input_type == 'id':
                    return self.validate_id(user_input)
                elif input_type == 'name':
                    return self.validate_name(user_input)
                elif input_type == 'dob':
                    return self.validate_dob(user_input)
                elif input_type == 'score':
                    return self.validate_score(user_input)
                else:
                    raise ValueError(f"Invalid input type: {input_type}")
                    
            except ValueError as e:
                logging.error(f"Validation error for {input_type}: {str(e)}")
                print(f"Invalid input: {str(e)}. Please try again.")
            except Exception as e:
                logging.error(f"Unexpected error during {input_type} validation: {str(e)}")
                print("An unexpected error occurred. Please try again.")
    
    # Validation Functions
    def validate_id(self, user_input):
        if user_input.lower() == 'end':
            return user_input

        stripped_id = user_input.lstrip('0')
        if not stripped_id:
            stripped_id = '0'

        if not stripped_id.isdigit() or int(stripped_id) > 99:
            raise ValueError("ID must be a 2-digit number.")

        return user_input.zfill(2)

    def validate_name(self, user_input):
        if not all(c.isalpha() or c.isspace() for c in user_input):
            raise ValueError("Name should contain only letters and spaces.")
        return user_input

    def validate_dob(self, user_input):
        datetime.strptime(user_input, '%Y-%m-%d')
        return user_input

    def validate_score(self, user_input):
        score = float(user_input)
        if not 0 <= score <= 100:
            raise ValueError("Score must be between 0 and 100")
        return score

    # Function to display data
    def display_and_save_data(self):
        table_data = []
        headers = ["UID", "Name", "D.o.B", "Age", "Raw Score", "Rounded Score", "Category"]

        # for each id in sorted id dict
        for sid in sorted(self.students_data.keys()):
            stu = self.students_data[sid]
            table_data.append([
                stu.student_id,
                stu.name,
                stu.dob,
                stu.age,
                f"{stu.overall:.4f}",
                stu.rounded,
                stu.category
            ])

        print("\nStudent Summary: ")
        print(tabulate(table_data, headers=headers))
        # self.save_to_file(table_data, headers)
        self.save_to_file()
        logging.info("Data displayed and saved")

    # def save_to_file(self, table_data, headers):
    # Function to save information to csv file
    def save_to_file(self):
        with open('./students.csv', 'w', newline='') as f:
            writer = csv.writer(f) # Initialize file pointer
            writer.writerow(['ID', 'Name', 'DOB', 'Age', 'Overall', 'Rounded', 'Category']) # Header row
            for stu in self.students_data.values(): # Write datas
                writer.writerow([stu.student_id, stu.name, stu.dob, stu.age,
                               f"{stu.overall:.2f}", stu.rounded, stu.category])
        print("\nResults exported to students.csv\n")
        # with open('./students.txt', "w") as f:
        #     f.write(tabulate(table_data, headers=headers))
        # logging.info("Data saved to students.txt")
    
    # Function to show analytics - min, max, mean, median
    def show_analytics(self):
        if not self.students_data:
            print("No student data available.")
            return

        all_overalls = [stu.overall for stu in self.students_data.values()]
        min_score = min(all_overalls)
        max_score = max(all_overalls)
        avg_score = mean(all_overalls)
        med_score = median(all_overalls)
        
        print("\n--- Analytics Summary ---")        
        print(f"Lowest score: {min_score:.2f}")
        print(f"Highest score: {max_score:.2f}")
        print(f"Average score: {avg_score:.2f}")
        print(f"Median score: {med_score:.2f}")
        
        # Calculate students in each category
        category_count = {}
        for stu in self.students_data.values():
            category_count[stu.category] = category_count.get(stu.category, 0) + 1

        # Show category distribution
        print("\n--- Category Distribution ---")
        for cat, cnt in category_count.items():
            print(f"{cat}: {cnt} student(s)")
    
    # Function to notify failing studnets
    def notify_failing_students(self):
        
        # Initialize SMTP configuration
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = input("Enter your email: ")
        password = input("Enter your email password: ")
        
        try: # Establish a connection with smtp server
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, password)
            
            # check for students with fail and d. opus
            for sid, student in self.students_data.items():
                if student.category in ["Fail", "Defecit Opus"]:
                    
                    # Initialize message/email structure
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = f"{student.name}@domain"
                    msg['Subject'] = "Important: Course Performance Update"
                    
                    body = f"""Dear {student.name} - {sid},
                    This is to inform you about your current academic standing.
                    Your overall score is {student.overall:.2f}
                    Category: {student.category}
                    
                    Please contact your module leader for support.
                    """
                    
                    msg.attach(MIMEText(body, 'plain'))
                    server.send_message(msg)
                    print(f"Notification sent to {student.name}")
                    logging.info("Message sent to failing and defecit opus students.")
            server.quit()
            print("All notifications sent successfully")
            
        except Exception as e:
            print(f"Error sending notifications: {e}")

def main():
    cms = CategoricalMarkingSystem()
    cms.run()

if __name__ == "__main__":
    main()