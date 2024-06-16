from sqlalchemy import Column, String, Integer,Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.associationproxy import association_proxy 

Base = declarative_base()

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer(), primary_key=True)
    bedroom = Column(Integer())
    bathroom = Column(Integer())
    type = Column(String())
    location = Column(String())
    weekly_rent = Column(Integer())
    owner_id= Column(Integer(), ForeignKey('owners.id'))

    applications = relationship('Application', back_populates='property')
    applicants = association_proxy('applications', 'applicant', creator=lambda a: Application(applicant=a))

    agent_properties = relationship('AgentProperty', back_populates='property')
    agents = association_proxy('agent_properties', 'agent', creator=lambda a: AgentProperty(agent=a))

    owner = relationship('Owner', back_populates='properties')

    def __repr__(self):
        return f"{self.id}: {self.location}, {self.type}"

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    phone_number = Column(String())

    applications = relationship('Application', back_populates='applicant')
    properties = association_proxy('applications', 'property', creator=lambda p: Application(property=p))

    def __repr__(self):
        return f"{self.id}: Name: {self.name}, Contact Detail: {self.phone_number}"

# Joint Model
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer(), primary_key=True)
    applicant_id = Column(Integer(), ForeignKey('applicants.id'))
    property_id = Column(Integer(), ForeignKey('properties.id'))
    status = Column(String())

    property = relationship('Property', back_populates='applications')
    applicant = relationship('Applicant', back_populates='applications')

    def __repr__(self):
        return f"{self.applicant.name} application to {self.property.location} is {self.status}"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    agent_properties = relationship('AgentProperty', back_populates='agent')
    properties = association_proxy('agent_properties', 'property', creator=lambda p: AgentProperty(property=p))

    def __repr__(self):
        return f"Agent(id={self.id}, name='{self.name}')"

# Joint Model
class AgentProperty(Base):
    __tablename__ = "agent_properties"
    
    id = Column(Integer(), primary_key=True)
    property_id = Column(Integer(), ForeignKey('properties.id'))
    agent_id = Column(Integer(), ForeignKey('agents.id'))

    property = relationship('Property', back_populates='agent_properties')
    agent = relationship('Agent', back_populates='agent_properties')

    def __str__(self):
        return f"Agent ID: {self.agent_id}, Property ID: {self.property_id}"

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer(), primary_key=True)
    name = Column(String())    

    # one (owner) to many (poperties) relationships
    properties = relationship('Property', back_populates='owner')

    def __repr__(self):
        return f"Owner(id={self.id}, name='{self.name}')"
