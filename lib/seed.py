from env import session
from random import randint, sample
from models import Property, Applicant, Application, Agent, AgentProperty, Owner

properties_data = [
    {
        'id': 1,
        'bedroom': 3,
        'bathroom': 2,
        'type': 'Apartment',
        'location': '1234 Elm Street, Sydney NSW 2000',
        'weekly_rent': 750,
        'owner_id': 1
    },
    {
        'id': 2,
        'bedroom': 4,
        'bathroom': 3,
        'type': 'House',
        'location': '5678 Oak Avenue, Melbourne VIC 3000',
        'weekly_rent': 600,
        'owner_id': 2
    },
    {
        'id': 3,
        'bedroom': 2,
        'bathroom': 1,
        'type': 'House',
        'location': '9102 Pine Lane, Brisbane QLD 4000',
        'weekly_rent': 800,
        'owner_id': 3
    },
    {
        'id': 4,
        'bedroom': 5,
        'bathroom': 2,
        'type': 'House',
        'location': '1113 Maple Road, Perth WA 6000',
        'weekly_rent': 950,
        'owner_id': 4
    },
    {
        'id': 5,
        'bedroom': 1,
        'bathroom': 1,
        'type': 'Apartment',
        'location': '1415 Cedar Street, Adelaide SA 5000',
        'weekly_rent': 400,
        'owner_id': 5
    },
        {
        'id': 6,
        'bedroom': 2,
        'bathroom': 1,
        'type': 'Apartment',
        'location': '2425 Willow Street, Sydney NSW 2000',
        'weekly_rent': 620,
        'owner_id': 1
    },
    {
        'id': 7,
        'bedroom': 3,
        'bathroom': 2,
        'type': 'Apartment',
        'location': '3321 Acacia Avenue, Melbourne VIC 3000',
        'weekly_rent': 700,
        'owner_id': 2
    },
    {
        'id': 8,
        'bedroom': 4,
        'bathroom': 3,
        'type': 'House',
        'location': '4218 Palm Drive, Brisbane QLD 4000',
        'weekly_rent': 850,
        'owner_id': 4
    },
    {
        'id': 9,
        'bedroom': 1,
        'bathroom': 1,
        'type': 'Apartment',
        'location': '5536 Oakwood Boulevard, Perth WA 6000',
        'weekly_rent': 450,
        'owner_id': 4
    },
    {
        'id': 10,
        'bedroom': 5,
        'bathroom': 4,
        'type': 'House',
        'location': '6827 Maple Circle, Adelaide SA 5000',
        'weekly_rent': 1200,
        'owner_id': 5
    }
]


applicant_data = [
    {'name': 'Olivia Smith',
        'phone_number': '0412 345 678'
    },
    {
        'name': 'Jack Johnson',
        'phone_number': '0401 234 567'
    },
    {
        'name': 'Amelia Brown',
        'phone_number': '0423 456 789'
    },
    {
        'name': 'Liam Williams',
        'phone_number': '0432 567 890'
    },
    {
        'name': 'Ava Jones',
        'phone_number': '0443 678 901'
    },
    {
        'name': 'Henry Davis',
        'phone_number': '0456 789 012'
    },
    {
        'name': 'Isabella Miller',
        'phone_number': '0467 890 123'
    },
    {
        'name': 'Thomas Wilson',
        'phone_number': '0478 901 234'
    },
    {
        'name': 'Sophia Moore',
        'phone_number': '0489 012 345'
    },
    {
        'name': 'James Taylor',
        'phone_number': '0490 123 456'
    }
]

agent_data = [
    {'name': 'Jackson Anderson'},
    {'name': 'Sophie Carter'},
    {'name': 'Oliver Edwards'},
    {'name': 'Amelia Lewis'},
    {'name': 'Isaac Young'}
]

owner_data = [
    {'name': 'Liam Taylor'},
    {'name': 'Olivia Johnson'},
    {'name': 'Ava Brown'},
    {'name': 'Lucas White'},
    {'name': 'Sophia Davis'}
]

# adding agents
def create_agents(agent_data):
    for agent in agent_data:
        new_agent = Agent(**agent)
        session.add(new_agent)
    session.commit()

# adding applicants
def create_applicants(applicant_data):
    for aplicant in applicant_data:
        new_applicant = Applicant(**aplicant)
        session.add(new_applicant)
    session.commit()

# adding owner
def create_owner(owner_data):
    for owner in owner_data:
        new_owner = Owner(**owner)
        session.add(new_owner)
    session.commit()

# adding properties
def create_properties(properties_data):
    for proerty_data in properties_data:
        new_property = Property(**proerty_data)
        session.add(new_property)
    session.commit()

# adding agent_properties, 2 foreign keys
def create_agent_properties():
    properties = session.query(Property).all()                  #get all row from Property table to a list
    agents = session.query(Agent).all()                         #get all row from Agent table to a list

    for property in properties:                                 
        random_num = randint(1, randint(1,4))          #get random number from 1 to 4, nested approach can create non-uniform distributions
        
        agent_sample = sample(agents, random_num)      #select random list of agents (1 to 4), this will be put in a loop below

        for agent in agent_sample:
            agent_properties = AgentProperty(property_id =property.id, agent_id=agent.id)
            session.add(agent_properties)
        
    session.commit()                                    #loop ensure property can have many applicants, 1 to many relationship

# adding applications, 2 foreign keys
def create_applications():
    applicants = session.query(Applicant).all()                  
    properties = session.query(Property).all()                         

    for property in properties:                                 
        random_num = randint(1, randint(1,4))          
        
        applicant_sample = sample(applicants, random_num)    

        for applicant in applicant_sample:
            applicants_properties = Application(property_id =property.id, applicant_id=applicant.id, status="pending")
            session.add(applicants_properties)
        
    session.commit()

# Delete all records from the data, do this to delete existing data and replacing it with new
def delete_all():
    session.query(Property).delete()
    session.query(Owner).delete()
    session.query(Applicant).delete()
    session.query(Application).delete()
    session.query(Agent).delete()
    session.query(AgentProperty).delete()

if __name__ == "__main__":
    delete_all()

    create_agents(agent_data)
    create_owner(owner_data)
    create_applicants(applicant_data)
    create_properties(properties_data)
    create_agent_properties()
    create_applications()

    print("✅ Seeding complete...")