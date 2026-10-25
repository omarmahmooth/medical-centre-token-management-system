import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ADMIN_FILE = os.path.join(BASE_DIR, "admin.json")
PATIENTS_FILE = os.path.join(BASE_DIR, "patients.json")


queue = []

if os.path.exists(PATIENTS_FILE):
    try:
        with open(PATIENTS_FILE, 'r', encoding='utf-8') as patient_file:
            loaded_data = json.load(patient_file)

        if not isinstance(loaded_data, list):
            raise ValueError("Patient data must be a JSON list.")

        if not all(isinstance(patient, dict) for patient in loaded_data):
            raise ValueError("Patient records must be JSON objects.")

        queue = loaded_data

    except (json.JSONDecodeError, ValueError, OSError) as error:
        print(f"Error loading patient data: {error}")
        print("Please check the patient data file before continuing.")
        raise SystemExit(1) from error


def admin_login():

    if not os.path.exists(ADMIN_FILE):
        print("Error: ADMIN_FILE was not found.")
        return False

    try:
        with open(ADMIN_FILE, 'r', encoding='utf-8') as admin_file:
            book = json.load(admin_file)

    except json.JSONDecodeError:
        print("Error: ADMIN_FILE contains invalid JSON.")
        return False

    except OSError as error:
        print(f"Error reading administrator file: {error}")
        return False

    if not isinstance(book, list):
        print("Error: Invalid administrator data!")
        return False

    if not all(isinstance(admin, dict) for admin in book):
        print("Error: Invalid administrator record!")
        return False

    try_count = 0
    while try_count < 3:
        admin_id = input('\nEnter admin user ID: ').strip().replace(" ", "")
        admin_pswd = input('\nPassword: ').strip()

        for admin in book:
            json_id = str(admin.get("Admin", "")).strip()
            json_pwd = str(admin.get("Password", "")).strip()
            if json_id == admin_id and json_pwd == admin_pswd:
                print('\nLogin successful')
                return True
        print('Incorrect user name or password!')
        try_count += 1
    print('Maximum login attempts exceeded!')
    return False


def register_patient():

    while True:
        patient_name = input('\nEnter patient name: ',).strip()
        if patient_name:
            break
        print('\nPatient name cannot be empty!')

    while True:
        try:
            patient_id = int(input('\nEnter patient id: '))

            if patient_id <= 0:
                print('Patient ID must be a positive number.')
                continue

            id_exists = any(patient['ID'] == patient_id for patient in queue)

            if id_exists:
                print('Patient ID already exists! Please enter a unique ID.\n')
                continue

            break

        except ValueError:
            print('\nInvalid id. Please enter only numbers.')

    while True:
        try:
            patient_age = int(input('\nEnter patient age: '))

            if 0 <= patient_age <= 120:
                break

            print('\nPlease enter an age between 0 and 120.')

        except ValueError:
            print('\nInvalid age. Please enter a whole number.')

    if queue:
        token_num = max(patient['Token'] for patient in queue) + 1

    else:
        token_num = 1

    new_patient = {'Name': patient_name, 'ID': patient_id,
                   'Age': patient_age, 'Token': token_num, 'Status': 'waiting'}
    queue.append(new_patient)

    with open(PATIENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=4)
        print('\n' + f'Patient {patient_name} registered successfully!\n')

    print(f'Patient\'s Token Number: {token_num}\n')


def view_queue():

    waiting_queue = [
        patient for patient in queue
        if patient['Status'] == 'waiting'
    ]

    try:
        srch_token = int(
            input('\n' + 'Enter token number to search for patient: '))
    except ValueError:
        print('\nIncorrect entry!, Please check the ID\n')
        return

    found = None
    for position, patient in enumerate(waiting_queue, start=1):
        if patient['Token'] == srch_token:
            print(f'\nPosition in queue: {position}')
            print(
                f'Estimated waiting time: '
                f'{(position-1)*10} minutes'
            )
            found = True
            break

    if not found:
        print('Patient not found in the queue!')


def call_next():

    next_patient = None
    for patient in queue:
        if patient.get('Status') == 'waiting':
            next_patient = patient
            break

    if not next_patient:
        print('No patients in the waiting queue.\n')
        return

    print(
        f"\nCalling patient: {next_patient['Name']}, "
        f"Token Number: {next_patient['Token']}\n")

    while True:
        prompt = input('\nHas the patient arrived? (y/n): ').strip().lower()

        if prompt in ('y', 'n'):
            break
        else:
            print('Invalid entry, Please enter "y" or "n"\n')

    if prompt == 'y':
        print(f'Patient {next_patient["Name"]} has arrived.\n')
        next_patient['Status'] = 'called'

    elif prompt == 'n':
        print(f'Patient {next_patient["Name"]} has not arrived.\n')
        next_patient['Status'] = 'waiting'
        for index, item in enumerate(queue):
            if item['Token'] == next_patient['Token']:
                moved_patient = queue.pop(index)
                queue.append(moved_patient)
                break

    with open(PATIENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=4)


def search_record():
    prompt = input(
        'Select search method: \n1. Search by Name \n2. Search by ID \n')
    srch_key = None
    srch_value = None
    try:
        if prompt == '1':
            srch_value = input('Enter patient name:\n').strip().casefold()
            srch_key = 'Name'

        elif prompt == '2':
            srch_value = int(input('Enter patient ID:\n'))
            srch_key = 'ID'

        else:
            print('Invalid option. Please select 1 or 2.')
            return

    except ValueError:
        print('Invalid entry. Please check your input.')
        return

    found = False
    for patient in queue:
        if srch_key == 'Name':
            match = patient.get('Name', '').strip().casefold() == srch_value
        else:
            match = patient.get('ID') == srch_value

        if match:
            print('\n---------- Patient Record Found ----------')
            print(json.dumps(patient, indent=4))
            found = True
            break
    if not found:
        print(f'\nThe patient with the {srch_key}: {srch_value} was not found')


def menu():
    print('\n\n-------  WELCOME TO THE MAIN MENU  -------\n\n')

    while True:
        print('\n1.Register \n2.View queue \n3.Called next patient \n4.Search patient record \n5.Logout\n')

        try:
            option = int(input('Select a function to continue: '))
            if option == 1:
                register_patient()
            elif option == 2:
                view_queue()
            elif option == 3:
                call_next()
            elif option == 4:
                search_record()
            elif option == 5:
                print('\n\n------------LOGGING OUT! THANK YOU------------')
                return
            else:
                print('Invalid option, Please select 1 to 5.')
        except ValueError:
            print('\nInvalid option entry!, Please select 1 to 5\n')


if admin_login():
    menu()
else:
    print('Access denied!')
