from pyArango.connection import *
from _sha512 import sha512
from json import dump
from generator import *

def get_password_hash(password):
    return sha512(password.encode()).digest().hex()

def get_user_types():
    types = {
        "doctor": 'D',
        "patient": 'P',
        "nurse": 'N',
        "receptionist": 'R',
        "pharmacist": 'H',
        "accountant": 'A',
        "laboratorist": 'L'
    }
    return types

def admin_initialization(db):
    # Admin initialization
    query = """
            INSERT @admin INTO Credential
        """
    db.AQLQuery(query, bindVars={
        'admin': {'_key': 'root', 'PasswordHash': get_password_hash("root")}
    })

def user_types_initialization(db):
    query = """
            LET data = @types
            FOR d IN data
                INSERT d INTO UserType
        """
    userTypes = get_user_types()
    db.AQLQuery(query, bindVars={
        'types': [{'_key': userTypes[i], 'type': i} for i in userTypes.keys()]
    })

def addresses_initialization(db):
    addresses = []
    for i in range(totalUserNumber):
        addresses.append(get_address())
    query = """
        LET data = @addresses
        FOR d IN data
            INSERT d INTO Address
    """
    db.AQLQuery(query, bindVars={
        'addresses': addresses
    })
    return addresses

def credentials_initialization(db):
    credentialsCollection = db['Credential']
    credentials = []
    profiles = []
    passwords = []
    for user in USERS.keys():
        for i in range(USERS[user]):
            profiles.append(get_profile())
            username = get_username(profiles[-1]['name'], credentialsCollection, credentials)
            profiles[-1]['username'] = username
            password = get_password()
            passwordHash = get_password_hash(password)
            credentials.append({
                '_key': username,
                'PasswordHash': passwordHash
            })
            passwords.append({'login': username, 'password': password})
    query = """
        LET data = @credentials
        FOR d IN data
            INSERT d INTO Credential
    """
    db.AQLQuery(query, bindVars={'credentials': credentials})
    with open("passwords", 'w') as file:
        for credential in passwords:
            file.write(str(credential) + ',' + '\n')
    return profiles

def users_initialization(db, profiles, addresses):
    query = """
        LET data = @addresses
        FOR address IN Address
            FOR d IN data
                FILTER address.City == d.City
                FILTER address.Street == d.Street
                FILTER address.House == d.House
                FILTER address.Appartment == d.Appartment
                RETURN {_key: address._key}
    """
    queryResult = db.AQLQuery(query, rawResults=True, bindVars={"addresses": addresses})
    addressKeys = [i['_key'] for i in queryResult]

    index = 0
    usersInfo = []
    for user in USERS.keys():
        for i in range(USERS[user]):
            usersInfo.append({
                '_key': profiles[index]['username'],
                'Name': profiles[index]['name'],
                'Phone': get_phone_number(),
                'Email': profiles[index]['mail'],
                'IsVerified': True,
                'VerificationLink': get_verification_link(),
                'AddressKey': addressKeys[index],
                'BirthDate': get_birth_date(),
                'Gender': profiles[index]['sex'],
                'PhotoLink': "http://seephotos.com",
                'UserType': get_user_types()[user]
            })
            if user == 'patient':
                usersInfo[-1]['Height'] = get_patient_height()
                usersInfo[-1]['Weight'] = get_patient_weight()
            else:
                usersInfo[-1]['Salary'] = get_salary(user)
                usersInfo[-1]['History'] = get_history()

            if user == 'doctor':
                usersInfo[-1]['Designation'] = get_designation()
                usersInfo[-1]['DoctorType'] = get_doctor_type()

            index += 1
    query = """
    LET data = @users
    FOR d IN data
        INSERT d INTO User
    """
    db.AQLQuery(query, bindVars={'users': usersInfo})

def rooms_initialization(db):

    return

def main():
    conn = Connection(arangoURL="http://95.213.191.243:8529", username="root")

    # Database initialization
    if not conn.hasDatabase(name=DB_NAME):
        db = conn.createDatabase(name=DB_NAME)
    else:
        db = conn[DB_NAME]

    # Clear the database
    db.dropAllCollections()
    db.reload()

    # Create all needed collections
    db.createCollection(name="Credential")
    db.createCollection(name="User")
    db.createCollection(name="Address")
    db.createCollection(name="UserType")

    admin_initialization(db)

    user_types_initialization(db)

    addresses = addresses_initialization(db)

    profiles = credentials_initialization(db)

    users_initialization(db, profiles, addresses)

    rooms_initialization(db)

DB_NAME = 'test'

ROOMS_NUMBER = 20

USERS = {
    "doctor": 10,
    "patient": 100,
    "nurse": 20,
    "receptionist": 2,
    "pharmacist": 2,
    "accountant": 2,
    "laboratorist": 4
}

totalUserNumber = sum(USERS.values())

if __name__ == '__main__':
    main()