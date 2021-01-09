import json

def write_json(data, filename='db.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 
 

def create_user(name, passw, debt, owed):
    with open ("db.json", "r+") as db:
        db = json.load(db)

    users = db["users"]

    user = {name:{
        "id": id,
        "pass": passw,
        "debt": debt,
        "owed": owed,
    }}

    users.update(user)

    write_json(db)


class User():
    
    id_counter = 1
    usernames = []

    def __init__(self, username = str, password = str):
        if username in User.usernames:
            raise ValueError("Username already in use.")
        self.username = username
        self.password = password
        self.debt = 0
        self.owed = 0
        self.id = self.id_counter
        self.network = []
        User.id_counter += 1 
        User.usernames.append(username)

    def add_to_network(self, user2):
        # checks if users are already in the same network:
        for i in self.network:
            if i[0] == user2.id:
                    return print("Users already have a connection.")

        # creates new interaction between users
        else:
            a = Interaction(user2.id, self.id)
            self.network.append((user2.id, a))
            user2.network.append((self.id, a))

    def add_debt(self, amount, user2):
        self.add_to_network(user2)

        for contact in self.network:
            if contact[0] == user2.id:
                interaction = contact[1]

        interaction.add_transfer(self.id, amount)
        user2.owed += amount
        self.debt += amount

    def print_debt(self):
        print("Total debt of: " )

    def data(self):
        print("Username: {}\n Password: {}\n Id: {}".format(self.username, self.password, self.id))

    def print_network(self):
        print(self.network)

    def interaction_data(self, user2):
        for contact in self.network:
            if contact[0] == user2.id:
                interaction = contact[1]

        print(interaction.balance)
        interaction.state(self.id)

        
class Interaction(User):
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2
        self.balance = 0

    def add_transfer(self, user, amount):
        if user == self.user1:
            self.balance += amount
        else:
            self.balance -= amount

    def state(self, user):
        if user == self.user1:
            if self.balance > 0:
                print("You owe {} to user {}".format(-self.balance, self.user2))            
            else:
                print("User {} owes you {}".format(self.user2, self.balance))

        else:
            if self.balance < 0:
                print("You owe {} to user {}".format(-self.balance, self.user1))

            else:
                print("User {} owes you {}".format(self.user1, self.balance))

jer = User("jer", "yo")
pedro = User("pedro", "yo")
tiago = User("judsadsas", "fffff")

create_user("Jer", "lol", "90","99")
