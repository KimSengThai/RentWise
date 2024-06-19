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
    # This is because applicant list is different
    if heading_msg == "YOUR APPLCATION LIST" and len(properties) > 0:   
        applications = properties                            # Use application for list below, 1st loop
        properties = [app.property for app in applications]  # Use properties for detail list, 2nd loop 

    loop = True
    while loop:
        sub_heading(heading_msg)
        print("")        
        if heading_msg == "ALL PROPERTIES" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.type}, ${prop.weekly_rent}/week")
        elif heading_msg == "ALL HOUSES" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent}/week")
        elif heading_msg == "ALL APARTMENTS" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.location}, {prop.bedroom} bedroom, ${prop.weekly_rent}/week ")
        elif heading_msg == "PROPERTIES LIST BY BEDROOM" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.bedroom} bedroom {prop.type}, ${prop.weekly_rent}/week ")
        elif heading_msg == "PROPERTIES LIST BY BATHROOM" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.bathroom} bathroom {prop.type}, ${prop.weekly_rent}/week ") 
        elif heading_msg == "PROPERTIES LIST BY WEEKLY RENT" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): ${prop.weekly_rent}/week for {prop.bedroom} bedroom {prop.type}")
        elif heading_msg == "YOUR APPLCATION LIST" and len(properties) > 0:
            for app in applications:
                prop = app.property
                print(f"{prop.id} (Property ID): {prop.type} at {prop.location}, ${prop.weekly_rent}/week, status: {app.status}")
        elif heading_msg == "AVAILABLE APPLICATION" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): ${prop.weekly_rent}/week, {prop.bedroom} bedroom, {prop.bathroom} bathroom {prop.type} at {prop.location}")
        elif heading_msg == "YOUR EXISTING PROPERTIES LIST" and len(properties) > 0:
            for prop in properties:
                print(f"{prop.id} (Property ID): {prop.type} at {prop.location}, ${prop.weekly_rent}/week")
        elif heading_msg == "YOUR PROPERTIES LISTING" and len(properties) > 0:
            for agent_prop in properties:
                print(f"{agent_prop.id} (Property ID): {agent_prop.type} at {agent_prop.location}, ${agent_prop.weekly_rent}/week")
        elif heading_msg == "ALL APPLICATIONS LIST" and len(properties) > 0:
            for app in properties:
                print(f"{app.id} (Application ID): {app.applicant.name} at {app.property.location}, status: {app.status}") 
        elif heading_msg == "PROPERTIES TO ENLIST" and len(properties) > 0:
            for agent_prop in properties:
                print(f"{agent_prop.id} (Property ID): {agent_prop.type} at {agent_prop.location}, ${agent_prop.weekly_rent}/week")                                                              
        else:
            print("No properties exist...")
        print('-' * 50)

        if heading_msg == "AVAILABLE APPLICATION" and len(properties) > 0:
            print("\nPlease enter the property ID to apply for (type 'back' to go back):")
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
                        print('-' * 50)
                    else:
                        print("Please select relevant property ID!")
                except ValueError:
                    print("Invalid input. Please enter a valid property ID.")
            else:
                clear()
                loop = False
                return False
        elif heading_msg == "PROPERTIES TO ENLIST" and len(properties) > 0:
            print("\nPlease enter the property ID to enlist for (type 'back' to go back):")
            id_input = input()
            clear()
            if id_input != 'back':
                try:
                    print(Fore.GREEN + f"Enlisting For Property ID: {id_input} has been successful" + Style.RESET_ALL)
                    property_id_input = int(id_input)  # Use property_id_input
                    selected_property = [p for p in properties if p.id == property_id_input]
                    if selected_property:
                        property = selected_property[0]
                        applicants_properties = AgentProperty(property_id=property.id, agent_id=my_user_id)
                        session.add(applicants_properties)
                        session.commit()
                        print('-' * 50)
                    else:
                        print("Please select a relevant property ID!")
                except ValueError:
                    print("Invalid input. Please enter a valid property ID.")
            else:
                clear()
                return False
        elif heading_msg == "ALL APPLICATIONS LIST" and len(properties) > 0:
            print("\nPlease enter the application ID to edit the status (type 'back' to go back):")
            id_input = input()
            clear()
            if id_input.lower() != 'back':
                try:
                    print(Fore.GREEN + f"Application ID {id_input}: Status" + Style.RESET_ALL)
                    application_id = int(id_input)
                    selected_application = [p for p in properties if p.id == application_id]
                    if len(selected_application) > 0:
                        application = selected_application[0]
                        # Display current status and prompt for new status
                        print(f"Current Status: {application.status}")
                        new_status = input("Enter new status (pending/approved/rejected): ")

                        if new_status.lower() in ['pending', 'approved', 'rejected']:
                            # Update the application status
                            application.status = new_status.lower()
                            session.commit()
                            print(Fore.GREEN + f"Application ID {application_id} status updated to {new_status}." + Style.RESET_ALL)
                        else:
                            print("Invalid status entered. Please enter either 'pending', 'approved', or 'rejected'.")
                    else:
                        print("Please select relevant application ID!")
                except ValueError:
                    print("Invalid input. Please enter a valid application ID!")
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

                        # Checking if user is an agent or not
                        agent_name = session.query(Agent).filter(
                            Agent.name == my_user_id
                        ).all()
                        if agent_name:
                            owner = session.query(Owner).filter(Owner.id == property.owner_id).first()
                            applications = session.query(Application).filter(
                            Application.property_id == property.id).all()
                            print(Fore.CYAN + f"Owner Name:"  + Style.RESET_ALL)
                            print(owner.name)
                            print(Fore.CYAN + f"List of existing applications:"  + Style.RESET_ALL)
                            for application in applications:
                                applicant = session.query(Applicant).filter(Applicant.id == application.applicant_id).first()
                                if applicant:
                                    print(f"Applicant ID: {applicant.id}, Name: {applicant.name}")

                        print(Fore.CYAN + "List of available agents:" + Style.RESET_ALL)
                        agent_properties = session.query(AgentProperty).filter(
                            AgentProperty.property_id == property.id
                        ).all()
                        for agent_property in agent_properties:
                            agent = session.query(Agent).filter(Agent.id == agent_property.agent_id).first()
                            print(f"Agent ID: {agent.id}, Name: {agent.name}")
                        print('-' * 50)
                    else:
                        print("Please select relevant property ID!")
                except ValueError:
                    print("Invalid input. Please enter a valid property ID.")
            else:
                clear()
                loop = False
                return False

# Find all properties
def find_all_proeprties(username=None):
    properties = session.query(Property).all()

    return display_properties(properties, "ALL PROPERTIES", username)

def find_house(username=None):
    property_type = session.query(Property).filter(Property.type.like("House")).all()
    if property_type:
        clear()
        display_properties(property_type, f"ALL HOUSES", username)
    else:
        print(f"No houses found!")

def find_apartment(username=None):
    property_type = session.query(Property).filter(Property.type.like("Apartment")).all()
    if property_type:
        clear()
        display_properties(property_type, f"ALL APARTMENTS", username)
    else:
        print(f"No apartments found!")

def find_bedroom(username=None):
    print("\nPlease enter a bedroom number: ")
    bedroom_input = input()
    bedroom = session.query(Property).filter(Property.bedroom.like(bedroom_input)).all()
    if bedroom:
        clear()
        display_properties(bedroom, f"PROPERTIES LIST BY BEDROOM", username)
    else:
        print("No property found!")

def find_bathroom(username=None):
    print("\nPlease enter a bathroom number: ")
    bathroom_input = input()
    bathroom = session.query(Property).filter(Property.bathroom.like(bathroom_input)).all()
    if bathroom:
        clear()
        display_properties(bathroom, f"PROPERTIES LIST BY BATHROOM", username)
    else:
        print("No property found!")

def find_rent(username=None):
    print("\nPlease enter weekly rent price: ")
    rent_input = input()
    weekly_rent = session.query(Property).filter(Property.weekly_rent.like(rent_input)).all()
    if weekly_rent:
        clear()
        display_properties(weekly_rent, f"PROPERTIES LIST BY WEEKLY RENT", username)
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
    print("Enter the following property details (type 'back' to go back):")

    property_location = input("Enter Property Location: ")
    if 'back' in property_location:
        clear()
        return False
           
    bedroom_number = input("Enter Bedroom Number: ")
    if 'back' in bedroom_number:
        clear()
        return False

    bathroom_number = input("Enter Bathroom Number: ")
    if 'back' in bathroom_number:
        clear()
        return False
    
    property_type = input("Enter Property Type: ")
    if 'back' in property_type:
        clear()
        return False
    
    property_rent = input("Enter Weekly Rent: ")
    if 'back' in property_rent:
        clear()
        return False
    
    owner_name = input("Enter Owner Name (CASE SENSITIVE): ")
    if 'back' in owner_name:
        clear()
        return False
    # Check if owner exists, if not, add new owner
    owner = session.query(Owner).filter(Owner.name == owner_name).first()

    if not owner:
        choice = handle_yes_no(f'{owner_name} does not exist. Do you want to register {owner_name} (yes/no)?')
        if choice:
            new_owner = Owner(name=owner_name)
            session.add(new_owner)
            session.commit()
            owner = new_owner
            print(Fore.GREEN + "\nNew owner registered successfully!"  + Style.RESET_ALL)
        else:
            print(Fore.RED + "Adding Property Has Been Cancel!" + Style.RESET_ALL)
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

# For agent to edit new property applicant, list of all applicants
def edit_property_application(username):
    # Find the agent by username
    agent = session.query(Agent).filter(Agent.name == username).first()
    if not agent:
        print(f"No agent found with name {username}")
        return

    # Get the properties the agent manages
    agent_properties = session.query(AgentProperty).filter(AgentProperty.agent_id == agent.id).all()
    if not agent_properties:
        print(f"No properties found for agent {username}")
        return

    # Get the property IDs managed by the agent
    property_ids = [ap.property_id for ap in agent_properties]

    # Query applications for those properties
    applications = session.query(Application).filter(Application.property_id.in_(property_ids)).all()

    if applications:
        clear()
        display_properties(applications, "ALL APPLICATIONS LIST")
    else:
        print(f"No applications found!")


# For agent to view their own property listing
def list_agent_property(username):
    # Fetching the agent by username
    my_agent = session.query(Agent).filter(Agent.name == username).first()

    # Querying for properties managed by the agent
    property_list = session.query(AgentProperty).filter(AgentProperty.agent_id == my_agent.id).all()

    # Extracting properties from the agent's property list
    properties = [ap.property for ap in property_list]

    # Displaying the list of properties
    if properties:
        clear()
        display_properties(properties, "YOUR PROPERTIES LISTING", logged_user.name)
    else:
        print(f"{username} has no property listings.")

def enlist(username):
    my_agent = session.query(Agent).filter(Agent.name == username).first()
    associated_property_ids = session.query(AgentProperty.property_id).filter(AgentProperty.agent_id == my_agent.id).all()
    associated_property_ids = [pid[0] for pid in associated_property_ids] 
    properties_not_with_agent = session.query(Property).filter(Property.id.notin_(associated_property_ids)).all()
    if properties_not_with_agent:
        clear()
        display_properties(properties_not_with_agent, "PROPERTIES TO ENLIST", my_agent.id)
    else:
        print(f"{logged_user.name} has no property listings.")   

# Main Menu selection
def main_menu():
    print("\nType the following:")
    print("\nAgent or 1         - If you're an agent")
    print("Applicant or 2     - If you're an applicant looking for renting")
    print('Quit or 3          - Terminate The Program')
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
                print(Fore.RED + "Agent name not found, please try again or type 'back' to go back"  + Style.RESET_ALL)
                username = input("Please enter your fullname (CASE SENSITIVE): ")
                if username.lower() == 'back':
                    return False
            else:
                break
    elif role == 'applicant':
        user = session.query(Applicant).filter(Applicant.name == username).first()
        if not user:
            while True:
                phone_number = input(Fore.RED + f'{username} does not exist. Please type your phone number (10 digits) or "back" : ' + Style.RESET_ALL)
                if phone_number.isdigit() and len(phone_number) == 10:
                    break
                elif phone_number.lower() == 'back':
                    return False
                else:
                    print(Fore.RED + "Invalid phone number or input. Please enter a 10-digit phone number." + Style.RESET_ALL)
            user = Applicant(name=username, phone_number=phone_number)
            session.add(user)
            session.commit()
    global logged_user
    logged_user = user          

def applicant_menu():
    heading("MAIN MENU")
    print(f"Hi {logged_user.name} 👋")
    print("\nType the following:")
    print("\nMyApp or 1     - List of your existing applications")
    print("NewApp or 2    - Apply for a new applications") 
    print("All or 3       - Display all properties")
    print("House or 4     - List of houses")
    print("Apartment or 5 - List of apartments")
    print("Bedroom or 6   - Search properties by bedroom number")
    print("Bathroom or 7  - Search properties by bathroom number")
    print("Rent or 8      - Search properties by weekly rent")
    print('Back or 9      - Go back')
    return input("\nPlease enter you menu choice: ")

def agent_menu():
    heading("MAIN MENU")
    print(f"Hi {logged_user.name} 👋")
    print("\nType the following:")
    print("\nAdd or 1       - Add New Properties")
    print("Edit or 2      - Edit Existing Property Applications Status")
    print("MyItem or 3    - Your properties listing")
    print("Enlist or 4    - Enlist to existing properties")             
    print("All or 5       - Display all properties")
    print("House or 6     - List of houses")
    print("Apartment or 7 - List of apartments")
    print("Bedroom or 8   - Search properties by bedroom number")
    print("Bathroom or 9  - Search properties by bathroom number")
    print("Rent or 10     - Search properties by weekly rent")
    print('Back or 11     - Go back')
    return input("\nPlease enter you menu choice: ")

def agent():
    clear()
    sub_heading("Agent Login")
    username = input("\nPlease enter your fullname (CASE SENSITIVE): ")
    if login(username, 'agent') == False:
        return False
    clear()
    innerloop = True
    while innerloop:
        choice = agent_menu()
        if choice.lower() == 'add' or choice == '1':
            clear()
            add_property(logged_user.name)
        elif choice.lower()  == 'edit' or choice == '2':
            clear()
            edit_property_application(logged_user.name)
        elif choice.lower()  == 'myitem' or choice == '3':
            clear()
            list_agent_property(logged_user.name)
        elif choice.lower()  == 'enlist' or choice == '4':
            clear()
            enlist(logged_user.name)            
        elif choice.lower()  == 'all' or choice == '5':
            clear()
            find_all_proeprties(logged_user.name)
        elif choice.lower()  == 'house' or choice == '6':
            clear()
            find_house(logged_user.name)
        elif choice.lower()  == 'apartment' or choice == '7':
            clear()
            find_apartment(logged_user.name)
        elif choice.lower()  == 'bedroom' or choice == '8':
            clear()
            find_bedroom(logged_user.name)
        elif choice.lower()  == 'bathroom' or choice == '9':
            clear()
            find_bathroom(logged_user.name)
        elif choice.lower()  == 'rent' or choice == '10':
            clear()
            find_rent(logged_user.name)                            
        elif choice.lower() == 'exit' or choice.lower() == 'quit' or choice.lower() == 'back' or choice == '11':
            innerloop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using RentWise. Goodbye!")

def applicant():
    clear()
    sub_heading("Applicant Login")
    username = input("\nPlease enter your fullname (CASE SENSITIVE): ")
    if login(username, 'applicant') == False:
        return False
    clear()
    innerloop = True
    while innerloop:
        choice = applicant_menu()
        if choice.lower() == 'myapp' or choice == '1':
            clear()
            user_existing_application(logged_user.name)
        elif choice.lower()  == 'newapp' or choice == '2':
            clear()
            apply_for_new_applications(logged_user.name)
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
        elif choice == 'quit' or choice.lower() == 'exit' or choice.lower() == 'back'  or choice == '3':
            loop = False
        else:
            print("Invalid input. Please try again!")
    print("Thank you for using the RentWise App. Goodbye!")

# Ensures that the start() function is called only when the script is executed directly.
if __name__ == "__main__":
    start()