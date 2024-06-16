from env import session, clear
from models import Property, Applicant, Application, Agent, AgentProperty, Owner
from colorama import Fore, Style, init

# global variable use to track logged-in user
logged_user = None

# heading for commandline
def heading(text):
    border_char = "⭐"
    key_char= "🔑"
    house_char = "🏠📋🏠"
    width = 45 

    print(border_char * width)
    print(key_char * width)
    print(border_char * width)
    print()
    print(f"{' ' * 15}{house_char * 2}{' ' * 5}{text}{' ' * 5}{house_char * 2}")
    print()
    print(border_char * width)
    print(key_char * width)
    print(border_char * width)

def sub_heading(text):
    border_char = "⭐"
    house_char = "🏠📋🏠"
    smiley_char = "😊"
    width = 45 

    print(border_char * width)
    print()
    print(f"{' ' * 15}{house_char * 2}{' ' * 5}{text}{smiley_char}{' ' * 5}{house_char * 2}")
    print()
    print(border_char * width)

# propmt yes or no for commandline
def handle_yes_no(message):
    returned_val = True
    while True:
        print(message)
        choice = input()

        if choice.lower() == "yes" or choice.lower() == "y":
            returned_val = True
            break
        elif choice.lower() == "no" or choice.lower() == "n":
            returned_val = False
            clear()
            break
        else:
            print("Invalid input")
    return returned_val

# Displays a list of properties and allows the user to view more details or go back to the main menu.
def display_properties(properties, heading_msg):
    loop = True
    while loop:
        sub_heading(heading_msg)

        if heading_msg == "ALL PROPERTIES" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id}: {prop.location}, {prop.type}, ${prop.weekly_rent} per week")
        elif heading_msg == "ALL HOUSES" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id}: {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent} per week")
        elif heading_msg == "ALL APARTMENTS" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id}: {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent} per week ")                
        else:
            print("No properties exist...")
        print('-' * 30)

        print("\nPlease enter the property ID to view more details (type 'back' to go back):")
        id_input = input()
        clear()
        if id_input.lower() != 'back':
            try:

                print(Fore.RED + "Selected Property Details:" + Style.RESET_ALL)
                property_id = int(id_input)
                selected_property = [p for p in properties if p.id == property_id]

                if len(selected_property) > 0:
                    property = selected_property[0]
                    print(f"{property.location.upper()}")
                    print(f"Property Types: {property.type}")
                    print(f"Bedroom Number: {property.bedroom}")
                    print(f"Bathroom Number: {property.bathroom}")
                    print(f"Weekly Rent: {property.weekly_rent}")

                    print("List of available agents:")
                    agent_properties = session.query(AgentProperty).filter(
                        AgentProperty.property_id == property.id
                    ).all()
                    for agent_property in agent_properties:
                        agent = session.query(Agent).filter(Agent.id == agent_property.agent_id).first()
                        print(Fore.CYAN + f"Agent ID: {agent.id}, Name: {agent.name}" + Style.RESET_ALL)
                    print('-' * 30)
                else:
                    print("Please select relevant property ID!")
            except ValueError:
                print("Invalid input. Please enter a valid property ID.")
        else:
            clear()
            loop = False
            return False

# Find all properties
def find_all_proeprties():
    properties = session.query(Property).all()

    return display_properties(properties, "ALL PROPERTIES")

def find_house():
    property_type = session.query(Property).filter(Property.type.like("House")).all()
    if property_type:
        clear()
        display_properties(property_type, f"ALL HOUSES")
    else:
        print(f"No houses found!")

def find_apartment():
    property_type = session.query(Property).filter(Property.type.like("Apartment")).all()
    if property_type:
        clear()
        display_properties(property_type, f"ALL APARTMENTS")
    else:
        print(f"No apartments found!")

def find_bedroom():
    print("\nPlease enter a bedroom number:")
    bedroom_input = input()

    bedroom = session.query(Property).filter(Property.bedroom.like(bedroom_input)).first()

    if bedroom:
        clear()
        display_properties(bedroom.movies, f"MOVIES UNDER {genre.name.upper()}")
    else:
        print("No genre found!")

def find_bathroom():
    pass

def find_rent():
    pass
    
# Main Menu selection
def main_menu():
    print("\nType the following")
    print("1            - If you're an agent")
    print("2            - If you're an applicant looking for renting")
    print("3            - If you're an owner")
    print('4            - Terminate The Program')
    return input("\nEnter your choice: ")

# Greeding the user and 
def greet():
    clear()
    heading("Welcome to RentWise App!")

def login(username, role):

    if role == 'agent':
        # user = session.query(Agent).filter(Agent.name == username).first()
        pass
        
    elif role == 'applicant':
        user = session.query(Applicant).filter(Applicant.name == username).first()

        if not user:

            while True:
                phone_number = input(f'{username} does not exist. Please type your phone number to register or quit to go back: ')
                if phone_number.isdigit() and len(phone_number) == 10:
                    break
                elif phone_number.lower() == 'quit':
                    return False
                else:
                    print("Invalid phone number or input. Please enter a 10-digit phone number.")

            user = Applicant(name=username, phone_number=phone_number)
            session.add(user)
            session.commit()
            print("You have successfully registered to this app!")
        else:
            print(f"Welcome back, {user.name}!")
            print()

    elif role == 'owner':
        pass
        # user = session.query(Owner).filter(Applicant.name == username).first() 

        # if not user:
        #     choice = handle_yes_no("\nOwner name not found, do you want to try again (yes/no)?")
        # need to put a loop
        # if choice:
        #     pass
        # else:
        #     pass
                      
    global logged_user
    logged_user = user

def applicant_menu(username):
    heading("MAIN MENU")
    print(f"Hi {username} 👋")
    print("\nType the following")
    print("1        - List of your existing applications")
    print("2        - Apply for a new applications") 
    print("3        - Display All Properties")
    print("4        - List of Houses")
    print("5        - List of Apartments")
    print("6        - Search Properties By Bedroom Number")
    print("7        - Search Properties By Bathroom Number")
    print("8        - Search Properties By Weekly Rent")
    print('9        - Go Back')
    return input("\nPlease enter you menu choice: ")

def agent():
    clear()
    sub_heading("Agent Login")
    print()
    username = input("Please enter your fullname (CASE SENSITIVE): ")
    login(username, 'agent')

def applicant():
    clear()
    sub_heading("Applicant Login")
    print()
    username = input("Please enter your fullname (CASE SENSITIVE): ")
    login(username, 'applicant')
    clear()
    innerloop = True
    while innerloop:
        choice = applicant_menu(username)
        if choice.lower() == 'all' or choice == '3':
            clear()
            find_all_proeprties()
        elif choice.lower() == 'house' or choice == '4':
            clear()
            find_house()
        elif choice.lower() == 'apartment' or choice == '5':
            clear()
            find_apartment()
        elif choice.lower() == 'bedroom' or choice == '6':
            clear()
            find_bedroom()
        elif choice.lower() == 'bathroom' or choice == '7':
            clear()
            find_bathroom()
        elif choice.lower() == 'rent' or choice == '8':
            clear()
            find_rent()                            
        elif choice.lower() == 'exit' or choice.lower() == 'quit' or choice == '9':
            innerloop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using RentWise. Goodbye!")

def owner():
    clear()
    sub_heading("Owner Login")
    print()
    username = input("Please enter your fullname (CASE SENSITIVE): ")
    login(username, 'owner')

# Starts the application and displays the main menu in a loop.
def start():
    loop = True
    while loop:
        greet()
        choice = main_menu()
        if choice == 'agent' or choice == '1':
            agent()
            clear()
        elif choice == 'applicant' or choice == '2':
            applicant()
            clear()
        elif choice == 'owner' or choice == '3':
            owner()
            clear()
        elif choice == 'quit' or choice.lower() == 'exit' or choice == '4':
            loop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using the RentWise App. Goodbye!")

# Ensures that the start() function is called only when the script is executed directly.
if __name__ == "__main__":
    start()