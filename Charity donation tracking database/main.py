import sqlite3 as db
def create_tables():
    conn = db.connect("charity.db")
    cursor = conn.cursor()

    # Donors Table stores information about people donating money
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Donors (
            DonorID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT,
            BusinessName TEXT,
            Postcode TEXT,
            HouseNumber TEXT,
            PhoneNumber TEXT
        )
    ''')

    # Events Table   stores charity event details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            EventID INTEGER PRIMARY KEY AUTOINCREMENT,
            EventName TEXT,
            RoomInfo TEXT,
            BookingDateTime TEXT,
            Cost REAL
        )
    ''')

    # Volunteers Table stores information about volunteers helping with events
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Volunteers (
            VolunteerID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Role TEXT,
            EventID INTEGER,
            FOREIGN KEY (EventID) REFERENCES Events(EventID)
        )
    ''')

    # Donations Table stores information about donations made by donors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Donations (
            DonationID INTEGER PRIMARY KEY AUTOINCREMENT,
            Amount REAL,
            Date TEXT,
            GiftAid BOOLEAN,
            Notes TEXT,
            DonorID INTEGER,
            EventID INTEGER,
            VolunteerID INTEGER,
            FOREIGN KEY (DonorID) REFERENCES Donors(DonorID),
            FOREIGN KEY (EventID) REFERENCES Events(EventID),
            FOREIGN KEY (VolunteerID) REFERENCES Volunteers(VolunteerID)
        )
    ''')

    #Users Table stores information about users (admins) who can manage the system
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT UNIQUE,
            Password TEXT
        )
    ''')

    conn.commit()
    conn.close()



# Basic User Management (for admins)
def add_user(username, password):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
        print("User added successfully.")
    except db.IntegrityError:
        print("Username already exists.")
    conn.commit()
    conn.close()


# Add a new donor
def add_donor(first, last, business, postcode, house, phone):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Donors (FirstName, LastName, BusinessName, Postcode, HouseNumber, PhoneNumber)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (first, last, business, postcode, house, phone))
    conn.commit()
    conn.close()



# Add a new donation
def add_donation(amount, date, gift_aid, notes, donor_id, event_id, volunteer_id):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Donations (Amount, Date, GiftAid, Notes, DonorID, EventID, VolunteerID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (amount, date, gift_aid, notes, donor_id, event_id, volunteer_id))
    conn.commit()
    conn.close()


# Prevent donor deletion if they have donations
def delete_donor(donor_id):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donations WHERE DonorID = ?", (donor_id,))
    if cursor.fetchall():
        print(" Cannot delete donor: donations exist.")
    else:
        cursor.execute("DELETE FROM Donors WHERE DonorID = ?", (donor_id,))
        print(" Donor deleted.")
    conn.commit()
    conn.close()



# Prevent event deletion if donations exist
def delete_event(event_id):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donations WHERE EventID = ?", (event_id,))
    if cursor.fetchall():
        print(" Cannot delete event: donations exist.")
    else:
        cursor.execute("DELETE FROM Events WHERE EventID = ?", (event_id,))
        print(" Event deleted.")
    conn.commit()
    conn.close()



# Search Donations
def search_donations_by_donor(donor_id):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donations WHERE DonorID = ?", (donor_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def search_donations_by_event(event_id):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donations WHERE EventID = ?", (event_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def search_donations_by_volunteer(volunteer_id):
    conn = db.connect("charity.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Donations WHERE VolunteerID = ?", (volunteer_id,))
    results = cursor.fetchall()
    conn.close()
    return results



# Simple interactive menu
def menu():
    create_tables()
    while True:
        print("\n🟦 Charity Donation Tracker Menu")
        print("1. Add Donor")
        print("2. Add Donation")
        print("3. Delete Donor")
        print("4. Delete Event")
        print("5. Search Donations by Donor")
        print("6. Search Donations by Event")
        print("7. Search Donations by Volunteer")
        print("8. Add User (Admin)")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            fn = input("First Name: ")
            ln = input("Last Name: ")
            bname = input("Business Name: ")
            pc = input("Postcode: ")
            hn = input("House Number: ")
            phone = input("Phone Number: ")
            add_donor(fn, ln, bname, pc, hn, phone)

        elif choice == "2":
            amt = float(input("Donation Amount: "))
            date = input("Donation Date (YYYY-MM-DD): ")
            gift = input("Gift Aid (True/False): ").lower() == "true"
            notes = input("Notes: ")
            donor = int(input("Donor ID: "))
            event = int(input("Event ID: "))
            vol = int(input("Volunteer ID: "))
            add_donation(amt, date, gift, notes, donor, event, vol)

        elif choice == "3":
            donor_id = int(input("Donor ID to delete: "))
            delete_donor(donor_id)

        elif choice == "4":
            event_id = int(input("Event ID to delete: "))
            delete_event(event_id)

        elif choice == "5":
            donor_id = int(input("Enter Donor ID: "))
            results = search_donations_by_donor(donor_id)
            for row in results:
                print(row)

        elif choice == "6":
            event_id = int(input("Enter Event ID: "))
            results = search_donations_by_event(event_id)
            for row in results:
                print(row)

        elif choice == "7":
            volunteer_id = int(input("Enter Volunteer ID: "))
            results = search_donations_by_volunteer(volunteer_id)
            for row in results:
                print(row)



        elif choice == "8":
            username = input("Enter new username: ")
            password = input("Enter password: ")
            add_user(username, password)

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")

# Run the full system
if __name__ == "__main__":
    menu()
