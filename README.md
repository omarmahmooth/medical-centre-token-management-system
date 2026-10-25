# Medical Centre Token Management System (MCTMS)

## Project Overview

The Medical Centre Token Management System (MCTMS) is a command-line application developed using Python.

The project demonstrates how a simple patient queue management system can be implemented using Python functions, lists, dictionaries, input validation, and JSON file handling.

It allows an administrator to register patients, manage the waiting queue, call patients, and search for patient records.

## Features

* **Administrator Login:** Protects access to the main menu using administrator credentials.
* **Patient Registration:** Registers patients with a name, unique patient ID, age, and automatically generated token number.
* **Duplicate ID Prevention:** Checks whether a patient ID already exists before registering a new patient.
* **Queue Management:** Displays a patient's position in the waiting queue and estimates waiting time.
* **Patient Calling:** Calls the next waiting patient and updates the patient's status.
* **Queue Reordering:** Moves a patient to the end of the waiting queue if they have not arrived.
* **Patient Record Search:** Searches for patient records using a name or patient ID.
* **JSON Data Storage:** Stores patient records in a JSON file so that data can be loaded when the application restarts.
* **Input Validation:** Handles several invalid inputs to help prevent errors during execution.

## Technologies Used

* Python
* JSON
* Built-in Python modules: `json` and `os`
* Visual Studio Code (development environment)

## Project Structure

```text
MCTMS/
├── medical_center.py
├── admin.json
├── patients.json
└── README.md
```

* `medical_center.py`: Contains the application logic.
* `admin.json`: Stores administrator credentials.
* `patients.json`: Stores patient records.
* `README.md`: Documents the project.

The JSON files are created or populated as required by the application and its configuration.

## Requirements

* Python 3
* A code editor or terminal capable of running Python scripts

## How to Run

1. Install Python 3 if it is not already installed.

2. Download or clone the project repository.

3. Open the project folder in a terminal or Visual Studio Code.

4. Ensure that the required administrator configuration exists in `admin.json` and follows the structure expected by the application.

5. Run the application using:

   ```bash
   python medical_center.py
   ```

6. Enter the configured administrator credentials.

7. Select an option from the main menu to use the application.

Depending on your system, you may need to use `python3` instead of `python`.

## Data Storage

Patient records are stored in `patients.json` using JSON format.

The application loads existing patient records when it starts and saves changes when patients are registered or their queue status is updated.

## Learning Objectives

This project was developed to practise:

* Python functions and control flow
* Lists and dictionaries
* Loops and conditional statements
* Input validation and exception handling
* File handling
* JSON serialization and deserialization
* Basic authentication
* Queue management logic
* Breaking a program into reusable functions

## Future Improvements

Potential improvements include:

* A graphical user interface
* A database such as SQLite
* Stronger authentication and password hashing
* More comprehensive error handling
* Automated unit tests
* Patient record editing and deletion
* More detailed queue and appointment management

## Disclaimer

This is an educational project intended for learning and demonstration purposes. It is not designed for use with real patient information or as a production medical system.
