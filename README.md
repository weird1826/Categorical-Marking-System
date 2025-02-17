# Categorical Marking System
## Documentation
### Overview
A python-based grading system that processes student data, calculates
scores, and categorizes academic performance.
### Core Classes
#### `Student` Class
```python
class Student:
 """
 Represents a student with their academic information and

 Attributes:
 student_id (str): 2-digit unique identifier
 name (str): Student's full name
 dob (str): Date of birth in YYYY-MM-DD format
 scores (list): List of assessment scores
 age (int): Calculated age
 overall (float): Weighted average score
 rounded (int): Score rounded to nearest category
 category (str): Academic performance category
 """
```
#### `ModuleConfig` Class
```python
class ModuleConfig:
 """
Categorical Marking System 2
 Handles module assessment configuration.

 Attributes:
 module_configuration (dict): Maps assessment componen

 Methods:
 setup_module(): Interactive module setup
 get_weights(): Returns assessment weights (default or
 """
```
#### `CategoricalMarkingSystem` Class
```python
class CategoricalMarkingSystem:
 """
 Main system class handling all operations.

 Key Features:
 - Manual/File-based data input
 - Multi-threaded file processing
 - Data validation
 - Analytics generation
 - Email notifications
 - CSV export
 """
```
#### Constants
```python
# Available mark boundaries
category_marks_lists = (0, 5, 15, ..., 92, 100)
# Grade categories and their corresponding marks
categories = {
 "Aurum Standard": [100],
 "Upper First": [82, 85, 92],
 # ...
}
```
## Key Features
### Data Input Methods
- Manual Entry
- Text-file import with multi-threaded processing
### Validation System
- Student ID (2 digits)
- Name (alphabetic)
- Date of Birth (YYYY-MM-DD)
- Scores 0100
### Analytics
- Min/Max Scores
- Mean/Median Calculation
- Category Distribution
### Output
- Console Display
- CSV export
- Email notifications for failing students
### Technical Requirements
- Dependencies:
  - `tabulate`
  - `statistics`
  - `smtp`
### Error Handling
- Input validation
- File processing errors
- Email sending exceptions
- Thread synchronization
### Logging
- Configured to log to `cms.log` file
- Records timestamps, error levels, messages
## Email Configuration Steps - Using a personal account
### SMTP setup - Gmail
1. Enable 2FA
2. Go to Google Account Security
3. Select "App Passwords"
4. Generate new app password for "Mail"
5. Save the 16-character password
6. Make sure to save the 16 character password securely somewhere. It is a
special type of password which allows applications to log into your
google account directly without any additional authentication steps.

- The process similar in case of a Microsoft Account.
### Code Configuration
#### SMTP Settings
```python
smtp_server = "smtp.gmail.com" # or microsoft server domain
port = 587
sender_email = "your-email@gmail.com"
password = "your-16-digit-app-password"
```
## Email Configuration steps if you are using an organizational account
- If you are using an organizational account, you need to ask your
administrator to generate an app password.
# Personal Recommendations
- Make an visually appealing GUI using libraries like tkinter to further improve accessibility.
- Using libraries like Flask to create a web-application based platform which can be hosted locally on university intranet.
- Making the use-case broader by giving students, teachers and third-party, access to this program.
- Implement secure authentication for admin, students, teachers, and thirdparty using cryptographic algorithms and authorization using well-defined access-control lists.
- Changing the file input from a text file to a comparatively well-organized file source such as a spreadsheet while also adding options to export to a wide range of formats.
- Along with exporting/importing of a file, establish a connection with a segregate university student database and another connection to this programs relational database, in order to make information flow more uniform, which makes the program well-established for commercial usage.
