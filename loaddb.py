# this import section is based off of load_data.py

import sys
import csv
import os
from database import Base,Accounts,Customers,Users,CustomerLog,Transactions # tables defined in database
from sqlalchemy import create_engine # this function creates a connection to the database 
from sqlalchemy.orm import scoped_session, sessionmaker # function that helps manage querying the database
from flask_bcrypt import Bcrypt # handles password hashing - do have one password in customers table
from flask import Flask
from faker import Faker

app = Flask(__name__)
engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine # binds the tables in the database to the engine 
db = scoped_session(sessionmaker(bind=engine)) #related to "thread-safe" database sessions
bcrypt = Bcrypt(app)

#Initialize faker 
fake = Faker()

def accounts(number_of_rows):

    for _ in range(number_of_rows):

        # users table
        id = fake.numerify(text='C#########') #primary key #should start with a C based on the example #not sure how to make this increment 
        name = fake.name() 
        user_type = fake.random_element(elements=('admin','user', 'super user', 'guest', 'teller','cashier'))
        password = fake.password() # is using bcrypt for hash necessary - old script has: bcrypt.generate_password_hash(passw).decode('utf-8')
            
        db.execute("INSERT INTO users (id,name,user_type,password) VALUES (:i,:n,:t,:p)", {"i": id,"n": name,"t": user_type,"p": password}) 
        db.commit() #saves the transaction

        # customers table
        cust_id = fake.unique.numerify(text='0##') # does this has to increment in order? #primary key
        cust_ssn_id = fake.unique.lexify(text='??######') # has to be unique so starts with two letters then digits
        name = fake.name()
        address = fake.street_name()
        age = fake.randint(18, 105)
        state = fake.state()
        city = fake.city()
        status = fake.random_element(elements=('Inactive','Active'))
        
        db.execute("INSERT INTO customers (cust_id,cust_ssn_id,name,address,age,state,city,status) VALUES (:i,:u,:n,:a,:g,:s,:c,:t)", {"i": cust_id, "u": cust_ssn_id, "n": name, "a": address, "g": age, "s": state, "c": city, "t": status})
        db.commit()
        #do all these variables in VALUES have to be different -- in each table?

        # customerlog table
        log_id = fake.numerify(text='#')
        cust_ida = cust_id #from Customers table - saved it as a different variable
        log_message = fake.random_element(elements=('Logged in.','Logged out.','Money withdrawn.','Money deposited.','Account created.','Account deleted.'))
        time_stamp = fake.date_time_this_decade()
        
        db.execute("INSERT INTO customerlog (log_id,cust_id,log_message,time_stamp) VALUES (:l,:c,:m,:t)", {"l": log_id,"c":cust_ida,"m":log_message ,"t": time_stamp})
        db.commit()

        # accounts
        acc_id = fake.numerify(text='#') #primary key
        acc_type = fake.random_element(elements=('Savings','Checkings','Student Checkings'))
        balance = fake.random_int(0,100000)
        cust_idb = cust_id #from Customers table  - saved it as a different variable
        status = fake.random_element(elements=('Inactive','Active'))
        message = fake.random_element(elements=('Overdrawn','Negative','Good Status')) #not sure what should be put here
        last_update = fake.date_time_this_decade()

        db.execute("INSERT INTO customers (acc_id,acc_type,balance,cust_id,status,message,last_update) VALUES (:i,:a,:b,:c,:s,:m,:l)", {"i": acc_id, "a": acc_type, "b": balance, "c":cust_idb, "s": status, "m": message, "l": last_update})
        db.commit()

        # transactions
        trans_id = fake.numerify(text='###')
        acc_id = acc_id # from Accounts table
        trans_message = fake.random_element(elements=('Deposit','Withdrawal'))
        amount = fake.random_int(0,10000)
        time_stamp = fake.date_time_this_decade()

        db.execute("INSERT INTO transactions (trans_id,acc_id,trans_message, amount, time_stamp) VALUES (:t,:a,:r,:m,:s)", {"t": trans_id, "a": acc_id, "r": trans_message, "m": amount, "s": time_stamp})
        db.commit()
    
if __name__ == "__main__": #this executes if the script is run directly vs being imported into another script
    number_of_rows = 1
    accounts(number_of_rows)
