from faker import Faker
from random import choice, randint, uniform

def get_address():
    cities = {
        "Agryz": "422233",
        "Almetyevsk": "423403",
        "Arsk": "422000",
        "Aznakayevo": "423330",
        "Bavly": "423930",
        "Bugulma": "423230",
        "Buinsk": "422430",
        "Chistopol": "422951",
        "Innopolis": "420500",
        "Kazan": "420000",
        "Laishevo": "422610",
        "Leninogorsk": "423250",
        "Mamadysh": "422190",
        "Mendeleyevsk": "423650",
        "Menzelinsk": "423700",
        "Naberezhnye Chelny": "423800",
        "Nizhnekamsk": "423570",
        "Nurlat": "423030",
        "Tetyushi": "422370",
        "Yelabuga": "423600",
        "Zainsk": "423520",
        "Zelenodolsk": "422540"
    }
    streets = ['50 Let Pobedy', 'Agadullina', 'Avtodorozhnaya', 'Belinskogo', 'Chaykovskogo', 'Devonskaya', 'Farrakhova', 'Gagarina', 'Gogolya', 'Gubkina', 'Karla Marksa', 'Krupskoy', 'Kutuzova', 'Leningradskaya', 'Lermontova', 'Mendeleyeva', 'Murzina', 'Pervomayskaya', 'Promyshlennaya', 'Rabochaya', 'Shashina', 'Shevchenko', 'Suvorova', 'Sverdlova', 'Tukaya', 'Yasnaya', 'Zavarykina', 'Zhukovskogo']
    maxHouseNum = 70
    maxAppartmentNum = 120
    city = choice(list(cities.keys()))
    address = {
        "Country": "Russia",
        "City": city,
        "ZipCode": cities[city],
        "Street": choice(streets),
        "House": randint(1, maxHouseNum),
        "Appartment": randint(1, maxAppartmentNum)
    }
    return address

def get_birth_date():
    minBirthYear = 1970
    maxBirthYear = 2005
    # date in format YYYY-MM-DD
    birthDate = str(randint(minBirthYear, maxBirthYear)) + '-'
    birthDate += str(randint(1, 13)).zfill(2) + '-'
    birthDate += str(randint(1, 29)).zfill(2)
    return birthDate

def get_designation():
    designations = ["Allergist", "Anesthesiologist", "Cardiologist", "Dermatologist", "Endocrinologist", "Family Physician", "Gastroenterologist", "Hematologist", "Internist", "Nephrologist", "Neurologist", "Ophthalmologist", "Osteopath", "Otolaryngologist", "Physiatrist", "Psychiatrist", "Rheumatologist", "Urologist"]
    return choice(designations)

def get_doctor_type():
    types = ["Trainee", "Visiting", "Permanent"]
    return choice(types)

def get_history():
    educations = ["University of Arkansas (UAMS) Nursing", "University of Tennessee College of Dentistry", "Morehouse School of Medicine", "Medical College of Georgia", "Maulana Azad Medical College", "University of Arkansas for Medical Sciences", "Lady Hardinge Medical College, India", "Tehran University of Medical Sciences", "Aga Khan Medical College", "Tufts University School of Medicine", "University of Iowa College of Medicine", "University of the East, Philippines"]
    experience = randint(2, 15)
    history = "Education: " + choice(educations) + "\n"
    history += "Experience: " + str(experience) + " years of practice"
    return history

def get_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    passwordLength = randint(6, 12)
    password = ''
    for i in range(passwordLength):
        password += choice(chars)
    return password

def get_patient_height():
    return randint(150, 195)

def get_patient_weight():
    return round(uniform(40, 90), 1)

def get_phone_number():
    numbers = '1234567890'
    codes = ['843', '903', '904', '905', '908', '912', '917', '919', '927', '929', '937', '939', '950', '951', '960', '967', '962', '965', '987', '996', '999']
    phone = "+7" + '-' + choice(codes) + '-'
    for i in range(3):
        phone += choice(numbers)
    phone += '-'
    for i in range(2):
        phone += choice(numbers)
    phone += '-'
    for i in range(2):
        phone += choice(numbers)
    return phone

def get_profile():
    fake = Faker('en_US')
    return fake.simple_profile()

def get_salary(type):
    if type == 'doctor':
        return randint(60000, 100000) // 1000 * 1000
    elif type == 'nurse' or type == 'laboratorist':
        return randint(30000, 55000) // 1000 * 1000
    else:
        return randint(15000, 25000) // 1000 * 1000

def get_username(name, collection, createdCollection):
    splittedName = name.split()
    if len(splittedName) > 1:
        username = splittedName[0][0].lower() + '.' + splittedName[1].lower()
    elif len(splittedName) == 1:
        username = splittedName[0]
    else:
        username = "user"
    i = 2
    existingUsernames = [i['_key'] for i in collection.fetchAll()] + [i['_key'] for i in createdCollection]
    tempUsername = username
    while tempUsername in existingUsernames:
        tempUsername = username + str(i)
        i += 1
    return tempUsername

def get_verification_link():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    verificationLink = ''
    numberOfSymbols = 20
    for i in range(numberOfSymbols):
        verificationLink += choice(chars)
    return verificationLink


