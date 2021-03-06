import os.path
import yaml
import random
import datetime
from sqlalchemy import text, create_engine, MetaData, select
from sqlalchemy import Table, Column, String, Float, Integer
from sqlalchemy.orm import registry, Session
from sqlalchemy.orm import declarative_base
import pandas as pd
import plotly.express as px
import numpy as np

yamlfilepath = os.path.expanduser('~\\yamlfiles\\information.yaml')
with open(yamlfilepath) as f:
    login = yaml.load(f, Loader=yaml.FullLoader)

address = f'postgresql://{login["user"]}:{login["pw"]}@localhost:{login["port"]}/{login["db"]}'
engine = create_engine(address)
metadata_obj = MetaData()
Base = declarative_base()

age = Table(
    "age",
    metadata_obj,
    Column('age', String(30), primary_key=True),
    Column('rate', Float)
)

sex = Table(
    "sex",
    metadata_obj,
    Column('sex', String(30), primary_key=True),
    Column('rate', Float)
)

lastname = Table(
    "lastname",
    metadata_obj,
    Column('lastname', String(30), primary_key=True),
    Column('rate', Float)
)

firstname = Table(
    "firstname",
    metadata_obj,
    Column('firstname', String(30), primary_key=True),
    Column('rate', Float)
)


class Age(Base):
    __tablename__ = 'age'
    age = Column(String(30), primary_key=True)
    rate = Column(Float)


class Sex(Base):
    __tablename__ = 'sex'
    sex = Column(String(30), primary_key=True)
    rate = Column(Float)


class LastName(Base):
    __tablename__ = 'lastname'
    lastname = Column(String(30), primary_key=True)
    rate = Column(Float)


class FirstName(Base):
    __tablename__ = 'firstname'
    firstname = Column(String(30), primary_key=True)
    rate = Column(Float)


customer = Table(
    "customer",
    metadata_obj,
    Column('cid', Integer, primary_key=True),
    Column('lastname', String(30)),
    Column('firstname', String(30)),
    Column('sex', String(30)),
    Column('dateofbirth', String(30)),
    Column('subdate', String(30))
)


class Customer(Base):
    __tablename__ = 'customer'
    cid = Column(Integer, primary_key=True)
    lastname = Column(String(30))
    firstname = Column(String(30))
    sex = Column(String(30))
    dateofbirth = Column(String(30))
    subdate = Column(String(30))


metadata_obj.create_all(engine)


def DateOfBirth(age):
    #??????????????? ???????????? ??????
    #?????? ??????
    age_int = age[:age.find('???')]
    dt_now = datetime.datetime.now()
    years = int(dt_now.year) - int(age_int)

    #???????????? ??????
    str_datetime = f"{str(years)}-01-01"
    dt_datetime = datetime.datetime.strptime(str_datetime, '%Y-%m-%d').date()
    date = round(np.random.uniform(1, 365, 1)[0])
    return dt_datetime + datetime.timedelta(days=date)


def CreateCustomer(subscription, cnt):
    session = Session(engine)
    for i in range(cnt):
        #?????? ????????? ?????? ??????
        agedata = pd.read_sql(select(Age), engine)
        age = agedata['age'].values.tolist()
        age_rate = agedata['rate'].values.tolist()
        age_in = random.choices(age, weights=age_rate)

        #????????????
        dateofb = str(DateOfBirth(age_in[0]))

        #?????? ????????? ?????? ??????
        sexdata = pd.read_sql(select(Sex), engine)
        sex = sexdata['sex'].values.tolist()
        sex_rate = sexdata['rate'].values.tolist()
        sex_in = random.choices(sex, weights=sex_rate)

        #??? ????????? ?????? ??????
        lastnamedata = pd.read_sql(select(LastName), engine)
        lastname = lastnamedata['lastname'].values.tolist()
        last_rate = lastnamedata['rate'].values.tolist()
        lastname_in = random.choices(lastname, weights=last_rate)

        #?????? ????????? ?????? ??????
        firstnamedata = pd.read_sql(select(FirstName), engine)
        firstname = firstnamedata['firstname'].values.tolist()
        first_rate = firstnamedata['rate'].values.tolist()
        firstname_in = random.choices(firstname, weights=first_rate)

        #???????????? ??????
        for a, b, c in zip(lastname_in, firstname_in, sex_in):
            session.merge(Customer(lastname=a, firstname=b, sex=c, dateofbirth=dateofb, subdate=subscription))

    session.flush()
    session.commit()
    session.close()
