import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
import random
import string
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        print("START FUNCTION CREATE TABLES")

        if purge:
            self.query("DROP TABLE IF EXISTS skills")
            self.query("DROP TABLE IF EXISTS experiences")
            self.query("DROP TABLE IF EXISTS positions")
            self.query("DROP TABLE IF EXISTS institutions")
            self.query("DROP TABLE IF EXISTS feedback")

            """
            self.query("DROP TABLE IF EXISTS hash")
            self.query("DROP TABLE IF EXISTS wallet")
            self.query("DROP TABLE IF EXISTS transactions")
            self.query("DROP TABLE IF EXISTS blockchain")
            self.query("DROP TABLE IF EXISTS nft")
            self.query("DROP TABLE IF EXISTS users")
            """

        sql_lst = ["institutions.sql", "positions.sql", "experiences.sql", "skills.sql"]
        csv_lst = ["institutions.csv", "positions.csv", "experiences.csv", "skills.csv"]
        
        for i in range(len(sql_lst)):
            with open(data_path+"create_tables/"+sql_lst[i], 'r') as sqlfile:
                data = sqlfile.read()
                self.query(data.strip())

                with open(data_path+"initial_data/"+csv_lst[i], 'r') as csvfile:
                    csvdata = csvfile.read().split('\n')   # Split it into a list by newline
                    cols = csvdata[0].replace('"', '')     # inst_id,type,name,department,address,city,state,zip
                    for j in range(1, len(csvdata)):
                        self.query("INSERT INTO " + sql_lst[i][:-4] + " (" + cols + ") VALUES (" + csvdata[j] + ")")

                        """EXAMPLE: "INSERT INTO institutions (inst_id,type,name,department,address,city,state,zip) 
                        VALUES (1,Academia,Michigan State University,Computer Science,NULL,East Lansing,Michigan,48823)
                        """
        # Creating feedback table
        with open(data_path+"create_tables/feedback.sql", 'r') as feedbacksql:
            fdata = feedbacksql.read()
            self.query(fdata.strip())
        # Creating users table
        with open(data_path+"create_tables/users.sql", 'r') as usersql:
            fdata = usersql.read()
            self.query(fdata.strip())
        # Creating wallet table
        with open(data_path+"create_tables/nft.sql", 'r') as usersql:
            fdata = usersql.read()
            self.query(fdata.strip())
        with open(data_path+"create_tables/wallet.sql", 'r') as usersql:
            fdata = usersql.read()
            self.query(fdata.strip())
        # Creating blockchain table
        with open(data_path+"create_tables/blockchain.sql", 'r') as usersql:
            fdata = usersql.read()
            self.query(fdata.strip())
        # Creating nft table
        # Creating transaction table
        with open(data_path+"create_tables/transactions.sql", 'r') as usersql:
            fdata = usersql.read()
            self.query(fdata.strip())
        # Creating transaction table
        with open(data_path+"create_tables/hash.sql", 'r') as usersql:
            fdata = usersql.read()
            self.query(fdata.strip())
        

        print("DONE WITH CREATE TABLES")



    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):

        if table[-4:] == '.sql':    # This checks if it has ".sql" at the end and removes it if it does
            table = table[:-4]

        cols = ",".join(columns)        # ["inst_id", "type"] -> "inst_id,type"
        with open('flask_app/database/' + table + ".sql", 'w') as sqlfile:
            # This loop makes a values string for every first item of each list, then every second item of each list, etc
            values = ''
            i = 0
            j = 0
            while True:
                if j == len(parameters[0]):
                    break
                values += '"' + parameters[i][j] + '",'
                i += 1
                if i == len(parameters):
                    values = values[:-1]
                    print("INSERT INTO " + table + " (" + cols + ") VALUES (" + values + ")")
                    self.query("INSERT INTO " + table + " (" + cols + ") VALUES (" + values + ")")

                    i = 0
                    j += 1

    def getResumeData(self):
        print("GETTING RESUME DATA")
        finaldata = {}

        inst_data = self.query("SELECT * FROM institutions")

        # FIRST CREATING THE INSITUTION DATA
        for i in range(len(inst_data)):
            data = {}
            for k, v in inst_data[i].items():
                if k == 'inst_id':
                    finaldata[i+1] = None
                else:
                    data[k] = v
 
            finaldata[i+1] = data
            finaldata[i+1]['positions'] = {}

            # CREATING THE POSITION DATA INSIDE THE INSTITUTION DATA
            pos_dic = {}
            pos_id = None
            pos_data = self.query("SELECT * FROM positions WHERE inst_id=" + str(i+1))
            for j in range(len(pos_data)):
                for pk, pv in pos_data[j].items():
                    if pk == 'position_id':
                        finaldata[i+1]['positions'][pv] = {}
                        pos_id = pv
                    elif pk == 'inst_id':
                        continue
                    else:
                        pos_dic[pk] = pv

                pos_dic['experiences'] = {}
                finaldata[i+1]['positions'][pos_id] = pos_dic

                # CREATING THE EXPERIENCE DATA INSIDE THE POSITION DATA
                exp_dic = {}
                exp_id = None
                exp_data = self.query("SELECT * FROM experiences WHERE position_id=" + str(i+1))
                for x in range(len(exp_data)):
                    for ek, ev in exp_data[x].items():
                        if ek == 'position_id':
                            finaldata[i+1]['positions'][pos_id]['experiences'][ev] = {}
                            exp_id = ev
                        elif ek == 'experience_id':
                            continue
                        else:
                            exp_dic[ek] = ev
                    
                    exp_dic['skills'] = {}
                    #print(exp_dic)
                    finaldata[i+1]['positions'][pos_id]['experiences'][exp_id] = exp_dic

                    # CREATING THE SKILLS DATA INSIDE THE EXPERIENCE DATA
                    skills_dic = {}
                    skills_id = None
                    skills_data = self.query("SELECT * FROM skills WHERE experience_id=" + str(i+1))
                    for y in range(len(skills_data)):
                        for sk, sv in skills_data[y].items():
                            if sk == 'experience_id':
                                finaldata[i+1]['positions'][pos_id]['experiences'][exp_id]['skills'][sv] = {}
                                skills_id = sv
                            elif sk == 'skill_id':
                                continue
                            else:
                                print("SKkkkkkkkkkkkk:", sk)
                                skills_dic[sk] = sv
                        
                        finaldata[i+1]['positions'][pos_id]['experiences'][exp_id]['skills'][skills_id] = skills_dic

                

        print("RETURNING GETRESUMEDATA")
        return finaldata

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        


        all_emails = self.query("SELECT email FROM users")
        failure = False
        # Checks to see if email already in table
        for item in all_emails:
            if item['email'] == email:
                failure = True
                break
        
        if failure:
            return {'failure': 0}
        
        password = self.onewayEncrypt(password)

        key = self.generateKey()
        self.insertRows("users.sql", ["role", "email", "password", "user_key"], [[role], [email], [password], [key]])

        new_id = self.query("SELECT user_id FROM users")[-1]['user_id']

        self.insertRows("wallet", ['user_key', 'user_id', 'tokens'], [[key], [str(new_id)], ['10']])

        return {'success': 1}

    def authenticate(self, email='me@email.com', password='password', signin=False):
    
        all_users = self.query("SELECT email, password FROM users")

        if signin:
            for user in all_users:
                if user["email"] == email:
                    return True
        else:

            print("Authenticating:", email, self.onewayEncrypt(password))

            
            for user in all_users:
                if user["email"] == email and user["password"] == self.onewayEncrypt(password):
                    return True

        return False



    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


    
    def generateKey(self):
        return "".join(random.choices(string.ascii_letters, k=20))
    
    def get_id_from_email(self, email):

        users = (self.query('SELECT * from users'))

        id_insert = None

        for item in users:
            if item['email'] == email:
                id_insert = str(item['user_id'])
                break
        
        return id_insert
    
    def get_key_from_id(self, id):
        print("ID:", id)
        wallet = self.query("SELECT user_key FROM wallet WHERE user_id = " + str(id))

        print("WALLET:", self.query("SELECT * FROM wallet"))

        return wallet[0]['user_key']
    
    def get_key_from_email(self, email):
        id = self.get_id_from_email(email)

        print("GKFE ID:", id)

        return self.get_key_from_id(id)

