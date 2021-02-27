import mysql.connector as mysql

class servicesdb:
    def __init__(self):
        self.connector = None
        self.dbcursor = None
        self.connect_database()
        self.create_table()
    
    def connect_database(self):
        self.connector = mysql.connect(host='127.0.0.1', user='root', password='Urmil@2000')

        self.dbcursor = self.connector.cursor()
        self.dbcursor.execute('CREATE DATABASE IF NOT EXISTS MegaTradeFair')
        self.dbcursor.execute('USE MegaTradeFair')

    def create_table(self):
        self.dbcursor.execute(''' CREATE TABLE IF NOT EXISTS Country(
        Id INT NOT NULL AUTO_INCREMENT,
        Country_name VARCHAR(30),
        PRIMARY KEY (id)
        );''')

        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS State(
            Id INT NOT NULL AUTO_INCREMENT,
            State_name VARCHAR(30),
            Country_id INT,
            PRIMARY KEY (id),
            FOREIGN KEY (country_id) REFERENCES Country(id) ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Industry(
            Id INT NOT NULL AUTO_INCREMENT,
            Industry_name VARCHAR(40),
            PRIMARY KEY (id)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Venue(
            Id INT NOT NULL AUTO_INCREMENT,
            City VARCHAR(40),
            Address VARCHAR(200),
            Country_id INT,
            State_id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Country_id) REFERENCES Country(Id) ON UPDATE CASCADE,
            FOREIGN KEY (State_id) REFERENCES State(Id) ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Event(
            Id INT NOT NULL AUTO_INCREMENT,
            Name VARCHAR(50),
            BookingStartDate DATETIME NOT NULL,
            StartDate DATETIME NOT NULL,
            EndDate DATETIME NOT NULL,
            Venue_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Venue_Id) REFERENCES Venue(Id) ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Stall(
            Id INT NOT NULL AUTO_INCREMENT,
            StallNo INT NOT NULL,
            Price FLOAT NOT NULL,
            StallSize INT,
            IsBooked BIT NOT NULL,
            Event_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Visitor(
            Id INT NOT NULL AUTO_INCREMENT,
            FirstName VARCHAR(20),
            LastName VARCHAR(20),
            Address VARCHAR(200),
            Pincode INT NOT NULL,
            MobileNo VARCHAR(10) NOT NULL,
            EmailId VARCHAR(40) NOT NULL,
            DateOfBirth DATETIME,
            Gender BIT NOT NULL,
            PRIMARY KEY (Id)
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Exhibitor(
            Id INT NOT NULL AUTO_INCREMENT,
            Name VARCHAR(30),
            EmailId VARCHAR(40),
            PhoneNo VARCHAR(10),
            CompanyName VARCHAR(20),
            CompanyDescription VARCHAR(50),
            Address VARCHAR(200),
            Pincode INT NOT NULL,
            Industry_Id INT,
            Country_Id INT,
            State_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Industry_Id) REFERENCES Industry(Id) ON UPDATE CASCADE,
            FOREIGN KEY (Country_Id) REFERENCES Country(Id) ON UPDATE CASCADE,
            FOREIGN KEY (State_Id) REFERENCES State(Id) ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS Booking(
            Id INT NOT NULL AUTO_INCREMENT,
            BookingDate DATETIME NOT NULL,
            TotalAmount FLOAT NOT NULL,
            Event_Id INT,
            Exhibitor_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON UPDATE CASCADE,
            FOREIGN KEY (Exhibitor_Id) REFERENCES Exhibitor(Id) ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS BookingStallMap(
            Id INT NOT NULL AUTO_INCREMENT,
            Booking_Id INT,
            Event_Id INT,
            Stall_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON UPDATE CASCADE,
            FOREIGN KEY (Stall_Id) REFERENCES Stall(Id) ON UPDATE CASCADE,
            FOREIGN KEY (Booking_Id) REFERENCES Booking(Id) ON UPDATE CASCADE
        ); ''')

        self.dbcursor.execute('''CREATE TABLE if NOT EXISTS MegaConusmerCard(
            Id INT NOT NULL AUTO_INCREMENT,
            Spend INT NOT NULL,
            SpendDate DATETIME NOT NULL,
            PaymentMode VARCHAR(15),
            
            Event_Id INT,
            Booking_Id INT,
            Visitor_Id INT,
            PRIMARY KEY (Id),
            FOREIGN KEY (Event_Id) REFERENCES Event(Id) ON UPDATE CASCADE,
            FOREIGN KEY (Booking_Id) REFERENCES Booking(Id) ON UPDATE CASCADE,
            FOREIGN KEY (Visitor_Id) REFERENCES Visitor(Id) ON UPDATE CASCADE	
        );''')

        self.connector.commit()

    def add_record(self, table_name, input_data):
        keys = list(input_data.keys())
        
        #Preparing Query
        table_data, table_values = '(', ' VALUES ('
        for i, x in enumerate(keys):
            if i != len(keys)-1:
                table_values += f'%({x})s, '
                table_data += f'{x}, '
            else:
                table_values += f'%({x})s)'
                table_data += f'{x})'

        add_query = (f'INSERT INTO {table_name} ' + table_data + table_values)

        #Execute Query
        try:
            self.dbcursor.execute(add_query, input_data)
            self.connector.commit()
        except Exception as e:
            print(e)

    def fetch_records(self, table_name):
        select_query = (f'SELECT * FROM {table_name}')

        self.dbcursor.execute(select_query)
        records = self.dbcursor.fetchall()
        return records
