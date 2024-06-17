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
def display_properties(properties, heading_msg, my_user_id=None):
    
    if heading_msg == "YOUR APPLCATION LIST" and len(properties) > 0:   # This is because applicant list is different
        applications = properties                            # Use application for list below, 1st loop
        properties = [app.property for app in applications]  # Use properties for detail list, 2nd loop 

    loop = True
    while loop:
        sub_heading(heading_msg)
        print("")        
        if heading_msg == "ALL PROPERTIES" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.type}, ${prop.weekly_rent} per week")
        elif heading_msg == "ALL HOUSES" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent} per week")
        elif heading_msg == "ALL APARTMENTS" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent} per week ")
        elif heading_msg == "PROPERTIES LIST BY BEDROOM" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.bedroom} bedroom {prop.type} at {prop.location}, ${prop.weekly_rent} per week ")
        elif heading_msg == "PROPERTIES LIST BY BATHROOM" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.bathroom} bathroom {prop.type} at {prop.location}, ${prop.weekly_rent} per week ") 
        elif heading_msg == "PROPERTIES LIST BY WEEKLY RENT" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): ${prop.weekly_rent} per week for {prop.bedroom} bedroom {prop.type} at {prop.location}, ")
        elif heading_msg == "YOUR APPLCATION LIST" and len(properties) > 0:
            for app in applications:
                prop = app.property
                print(f"{prop.id} (Property ID): {prop.bedroom} bedroom at {prop.location}, ${prop.weekly_rent} per week, status: {app.status}")
        elif heading_msg == "AVAILABLE APPLICATION" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): ${prop.weekly_rent}/week, {prop.bedroom} bedroom, {prop.bathroom} bathroom {prop.type} at {prop.location}")
        elif heading_msg == "YOUR EXISTING PROPERTIES LIST" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent} per week")                             
        else:
            print("No properties exist...")
        print('-' * 50)

        if heading_msg == "AVAILABLE APPLICATION" and len(properties) > 0:
            print("\nPlease enter the property ID to apply (type 'back' to go back):")
            id_input = input()
            clear()
            if id_input.lower() != 'back':
                try:
                    print(Fore.GREEN + f"Application For Property ID: {id_input} Submitted" + Style.RESET_ALL)
                    property_id = int(id_input)
                    selected_property = [p for p in properties if p.id == property_id]
                    if len(selected_property) > 0:
                        property = selected_property[0]
                        applicants_properties = Application(property_id = property.id, applicant_id = my_user_id, status="pending")
                        session.add(applicants_properties)
                        session.commit()
                        print('-' * 30)
                    else:
                        print("Please select relevant property ID!")
                except ValueError:
                    print("Invalid input. Please enter a valid property ID.")
            else:
                clear()
                loop = False
                return False
        else:
            print("\nPlease enter the property ID to view more details (type 'back' to go back):")
            id_input = input()
            clear()
            if id_input.lower() != 'back':
                try:
                    print(Fore.GREEN + "Selected Property Details:" + Style.RESET_ALL)
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
    print("\nPlease enter a bedroom number: ")
    bedroom_input = input()
    bedroom = session.query(Property).filter(Property.bedroom.like(bedroom_input)).all()
    if bedroom:
        clear()
        display_properties(bedroom, f"PROPERTIES LIST BY BEDROOM")
    else:
        print("No property found!")

def find_bathroom():
    print("\nPlease enter a bathroom number: ")
    bathroom_input = input()
    bathroom = session.query(Property).filter(Property.bathroom.like(bathroom_input)).all()
    if bathroom:
        clear()
        display_properties(bathroom, f"PROPERTIES LIST BY BATHROOM")
    else:
        print("No property found!")

def find_rent():
    print("\nPlease enter weekly rent price: ")
    rent_input = input()
    weekly_rent = session.query(Property).filter(Property.weekly_rent.like(rent_input)).all()
    if weekly_rent:
        clear()
        display_properties(weekly_rent, f"PROPERTIES LIST BY WEEKLY RENT")
    else:
        print("No property found!")

# For applicants to apply for applications
def apply_for_new_applications(username):
    # Fetch the current user
    my_user = session.query(Applicant).filter(Applicant.name == username).first()
    if not my_user:
        print("User not found.")
        return

    # Get property IDs that the user has applied for
    applied_properties_ids = session.query(Application.property_id).filter(Application.applicant_id == my_user.id).all()
    applied_properties_ids = [prop_id[0] for prop_id in applied_properties_ids]  # Flatten the list of tuples

    # Query properties that are not in the applied properties list
    applications_list = session.query(Property).filter(Property.id.notin_(applied_properties_ids)).all()

    # Display the available applications
    if applications_list:
        clear()
        display_properties(applications_list, "AVAILABLE APPLICATION", my_user.id)
    else:
        print("No available applications found!")

# For applicants and their applications
def user_existing_application(username):
    user_id = session.query(Applicant).filter(Applicant.name == username).first()
    applications_list = session.query(Application).filter(Application.applicant_id.like(user_id.id)).all()
    if applications_list:
        clear()
        display_properties(applications_list, f"YOUR APPLCATION LIST")
    else:
        print(f"No applications found!")

# For owners to view their own properties
def owner_existing_property(username):
    user_id = session.query(Owner).filter(Owner.name == username).first()
    property_list = session.query(Property).filter(Property.owner_id.like(user_id.id)).all()
    if property_list:
        clear()
        display_properties(property_list, f"YOUR EXISTING PROPERTIES LIST")
    else:
        print(f"No property found!")

# For agent to add new property
def add_property(username):
    property_location = input("Enter Property Location: ")
    bedroom_number = input("Enter Bedroom Number: ")
    bathroom_number = input("Enter Bathroom Number: ")
    property_type = input("Enter Property Type: ")
    property_rent = input("Enter Weekly Rent: ")
    owner_name = input("Enter Owner Name (CASE SENSITIVE): ")
    # Check if owner exists, if not, add new owner
    owner = session.query(Owner).filter(Owner.name == owner_name).first()
    if not owner:
        choice = handle_yes_no(f'{owner_name} does not exist. Do you want to register {owner_name} (yes/no)?')
        if choice:
            new_owner = Owner(name=owner_name)
            session.add(new_owner)
            session.commit()
            owner = new_owner
            print("\nNew owner registered successfully!")
        else:
            return False
    else:
        print(f"Owner {owner_name} found, proceeding with property registration.")

    properties_data = {'bedroom': int(bedroom_number),'bathroom': int(bathroom_number),'type': property_type,'location': property_location, 'weekly_rent': int(property_rent), 'owner_id': owner.id}

    new_property = Property(**properties_data)
    session.add(new_property)
    session.commit()

    my_agent_id = session.query(Agent).filter(Agent.name == username).first()
    new_property_id = session.query(Property).filter(Property.location == property_location).first()

    agent_properties = AgentProperty(property_id =new_property_id.id, agent_id=my_agent_id.id)
    session.add(agent_properties)
    session.commit()

    print(f"Property at {property_location} successfully added and assigned to agent {username}.") 

# For agent to delete new property
def delete_property():
    pass

# For agent to edit new property
def edit_property():
    pass

# For agent to view property
def list_agent_property():
    pass

# Main Menu selection
def main_menu():
    print("\nType the following:")
    print("\nAgent       - If you're an agent (1)")
    print("Applicant   - If you're an applicant looking for renting (2)")
    print("Owner       - If you're an owner (3)")
    print('Quit        - Terminate The Program (4)')
    return input("\nEnter your choice: ")

# Greeding the user and 
def greet():
    clear()
    heading("Welcome to RentWise App!")

def login(username, role):
    if role == 'agent':
        while True:
            user = session.query(Agent).filter(Agent.name == username).first()
            if not user:
                print("Agent name not found, please try again or type 'back' to go back")
                username = input("Please enter your fullname (CASE SENSITIVE): ")
                if username.lower() == 'back':
                    return False
            else:
                break
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
    elif role == 'owner':
        while True:
            user = session.query(Owner).filter(Owner.name == username).first()
            if not user:
                print("Owner name not found, please try again or type 'back' to go back")
                username = input("Please enter your fullname (CASE SENSITIVE): ")
                if username.lower() == 'back':
                    return False
            else:
                break          
    global logged_user
    logged_user = user

def applicant_menu(username):
    heading("MAIN MENU")
    print(f"Hi {username} 👋")
    print("\nType the following:")
    print("\nMyApp     - List of your existing applications (1)")
    print("NewApp    - Apply for a new applications (2)") 
    print("All       - Display all properties (3)")
    print("House     - List of houses (4)")
    print("Apartment - List of apartments (5)")
    print("Bedroom   - Search properties by bedroom number (6)")
    print("Bathroom  - Search properties by bathroom number (7)")
    print("Rent      - Search properties by weekly rent (8)")
    print('Back      - Go back (9)')
    return input("\nPlease enter you menu choice: ")

def owner_menu(username):
    heading("MAIN MENU")
    print(f"Hi {username} 👋")
    print("\nType the following:")
    print("\nMyProp    - List of your existing properties (1)") 
    print("All       - Display all properties (2)")
    print("House     - List of houses (3)")
    print("Apartment - List of apartments (4)")
    print("Bedroom   - Search properties by bedroom number (5)")
    print("Bathroom  - Search properties by bathroom number (6)")
    print("Rent      - Search properties by weekly rent (7)")
    print('Back      - Go back (8)')
    return input("\nPlease enter you menu choice: ")

def agent_menu(username):
    heading("MAIN MENU")
    print(f"Hi {username} 👋")
    print("\nType the following:")
    print("\nAdd       - Add New Properties (1)")
    print("Delete    - Delete Existing Properties (2)")
    print("Edit      - Edit Existing Properties (3)")
    print("MyItem    - Your properties listing (4)")             
    print("All       - Display all properties (5)")
    print("House     - List of houses (6)")
    print("Apartment - List of apartments (7)")
    print("Bedroom   - Search properties by bedroom number (8)")
    print("Bathroom  - Search properties by bathroom number (9)")
    print("Rent      - Search properties by weekly rent (10)")
    print('Back      - Go back (11)')
    return input("\nPlease enter you menu choice: ")

def agent():
    clear()
    sub_heading("Agent Login")
    print()
    username = input("Please enter your fullname (CASE SENSITIVE): ")
    login(username, 'agent')
    clear()
    innerloop = True
    while innerloop:
        choice = owner_menu(username)
        if choice.lower() == 'add' or choice == '1':
            clear()
            add_property(username)
        elif choice.lower()  == 'delete' or choice == '2':
            clear()
            delete_property()
        elif choice.lower()  == 'edit' or choice == '3':
            clear()
            edit_property()
        elif choice.lower()  == 'myitem' or choice == '4':
            clear()
            list_agent_property()
        elif choice.lower()  == 'all' or choice == '5':
            clear()
            find_all_proeprties()
            # Do it how u did it last time, with list of applicants and owner in details sections. 
            # pass in paremter of agent
        elif choice.lower()  == 'house' or choice == '6':
            clear()
            find_house()
        elif choice.lower()  == 'apartment' or choice == '7':
            clear()
            find_apartment()
        elif choice.lower()  == 'bedroom' or choice == '8':
            clear()
            find_bedroom()
        elif choice.lower()  == 'bathroom' or choice == '9':
            clear()
            find_bathroom()
        elif choice.lower()  == 'rent' or choice == '10':
            clear()
            find_rent()                            
        elif choice.lower() == 'exit' or choice.lower() == 'quit' or choice.lower() == 'back' or choice == '11':
            innerloop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using RentWise. Goodbye!")

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
        if choice.lower() == 'myapp' or choice == '1':
            clear()
            user_existing_application(username)
        elif choice.lower()  == 'newapp' or choice == '2':
            clear()
            apply_for_new_applications(username)
        elif choice.lower()  == 'all' or choice == '3':
            clear()
            find_all_proeprties()
        elif choice.lower()  == 'house' or choice == '4':
            clear()
            find_house()
        elif choice.lower()  == 'apartment' or choice == '5':
            clear()
            find_apartment()
        elif choice.lower()  == 'bedroom' or choice == '6':
            clear()
            find_bedroom()
        elif choice.lower()  == 'bathroom' or choice == '7':
            clear()
            find_bathroom()
        elif choice.lower()  == 'rent' or choice == '8':
            clear()
            find_rent()                            
        elif choice.lower() == 'exit' or choice.lower() == 'quit' or choice.lower() == 'back' or choice == '9':
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
    clear()
    innerloop = True
    while innerloop:
        choice = owner_menu(username)
        if choice.lower() == 'myprop' or choice == '1':
            clear()
            owner_existing_property(username)
        elif choice.lower()  == 'all' or choice == '2':
            clear()
            find_all_proeprties()
        elif choice.lower()  == 'house' or choice == '3':
            clear()
            find_house()
        elif choice.lower()  == 'apartment' or choice == '4':
            clear()
            find_apartment()
        elif choice.lower()  == 'bedroom' or choice == '5':
            clear()
            find_bedroom()
        elif choice.lower()  == 'bathroom' or choice == '6':
            clear()
            find_bathroom()
        elif choice.lower()  == 'rent' or choice == '7':
            clear()
            find_rent()                            
        elif choice.lower() == 'exit' or choice.lower() == 'quit' or choice.lower() == 'back' or choice == '8':
            innerloop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using RentWise. Goodbye!")


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
        elif choice == 'quit' or choice.lower() == 'exit' or choice.lower() == 'back'  or choice == '4':
            loop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using the RentWise App. Goodbye!")

# Ensures that the start() function is called only when the script is executed directly.
if __name__ == "__main__":
    start()