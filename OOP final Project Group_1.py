import time
class Manager:
    List_Manger = []
    loan_amount = float(200000000)
    password = "ramzan123"
    def __init__(self):
        self.m_name = "Ramzan Bhatti"
        self.m_address = "The White House, 1600 Pennsylvania Ave., Washington, D.C. 20500."
        self.m_ph_number = 3061243259
        self.m_email = "ramzan2020@whitehouse.gmail.com"

    def show(self):
        print(self.m_name, self.m_ph_number, self.m_email)

    @staticmethod
    def view_Reports():
        for history in Account.transaction_history:
            print(history)

class Customer:
    customers_list = []
    def __init__(self, name, contact, id):
        self.name = name
        self.contact = contact
        self.id = id

    def show_customer(self):
        return self.name, self.contact, self.id

    @staticmethod
    def add_customer():
        name = input("Enter name: ")
        try:
            contact = int(input("Enter contact number: "))
            id = int(input("Enter cnic without dashes: "))
        except ValueError:
            print("id and contact should be in integer.")
            while ValueError:
                try:
                    contact = int(input("Enter contact number: "))
                    id = int(input("Enter cnic without dashes: "))
                    break
                except ValueError:
                    print("Value error occured.")
        Customer.customers_list.append(Customer(name, contact, id))
        print("Customer Added")

from abc import ABC, abstractmethod
class Account(ABC):
    List_Account = []
    transaction_history = []
    def __init__(self, acc_holder, uname, password, acc_type, balance = 0):
        self.acc_holder = acc_holder
        self.uname = uname
        self.password = password
        self.balance = balance
        self.acc_type = acc_type
        self.acc_number = self.acc_holder.contact

    def overdraft(self):
        try:
            amount=float(input("Enter amount to be deposited: "))
        except ValueError:
            print("Amount should be in integer or float")
            while ValueError:
                try:
                    amount=float(input("Enter amount to be deposited: "))
                    break
                except ValueError:
                    print("Value error occured.")
        withdrawl = []
        withdrawl.append(self.acc_holder.id)
        t = time.time()
        withdrawl.append(f"Withdrawn at {time.ctime(t)}")
        if amount <= self.balance:
            self.balance = self.balance - amount
            withdrawl.append(f"Amount withdrawn {amount}")
            Account.transaction_history.append(withdrawl)
            print(f"Amount withdrawn is {amount}")
        elif amount > self.balance:
            overdraft = -1 * (self.balance - amount)
            over_amount = self.credit_limit + self.balance
            self.balance = 0
            if overdraft <= self.credit_limit:
                Manager.loan_amount -= overdraft
                withdrawl.append(f"Amount withdrawn is {amount}")
                Loan.loanTakers.append(Loan(self.acc_holder, self.uname, self.password, self.acc_type, self.balance, overdraft, time.ctime(t)))
                print(f"Overdraft is given to you of amount {overdraft}")
                Account.transaction_history.append(withdrawl)
            else:
                Manager.loan_amount -= self.credit_limit
                withdrawl.append(f"Amount withdrawn is {over_amount} with overdraft of {overdraft}")
                Loan.loanTakers.append(Loan(self.acc_holder, self.uname, self.password, self.acc_type, self.balance, self.credit_limit, time.ctime(t)))
                print(f"Overdrawn amount is {self.credit_limit}")
                Account.transaction_history.append(withdrawl)

    def delete_account(self):
        personal_accounts = []
        for account in Account.List_Account:
            if account.acc_holder.id == self.acc_holder.id:
                personal_accounts.append(account)
        if len(personal_accounts) > 1:
            if personal_accounts[0].acc_type == "CheckingAccount":
                check = personal_accounts[0]
            else:
                check = personal_accounts[1]
            if personal_accounts[1].acc_type == "SavingAccount":
                save = personal_accounts[1]
            else:
                save = personal_accounts[0]
            for p_account in personal_accounts:
                p_account.show_account()
            select = input("Enter S for Saving account, C for Checking account: ")
            while select != "s" and select != "S" and select != "c" and select != "C":
                select = input("Enter S for Saving account, C for Checking account: ")
            if select == "s" or select == "S":
                for account_1 in Account.List_Account:
                    if account_1.acc_holder.id == save.acc_holder.id and account_1.acc_type == save.acc_type:
                        Account.List_Account.remove(account_1)
            elif select == "c" or select == "C":
                for account_1 in Account.List_Account:
                    if account_1.acc_holder.id == check.acc_holder.id and account_1.acc_type == check.acc_type:
                        Account.List_Account.remove(account_1)
        else:
            for account in Account.List_Account:
                if account.acc_holder.id == self.acc_holder.id:
                    for customer in Customer.customers_list:
                        if customer.id == self.acc_holder.id:
                            Customer.customers_list.remove(customer)
                    Account.List_Account.remove(account)

    def return_loan(self):
        for taker in Loan.loanTakers:
            if taker.acc_holder.id == self.acc_holder.id:
                loan_return = []
                loan_return.append(taker.acc_holder.id)
                t = time.time()
                loan_return.append(f"Return time {time.ctime(t)}")
                return_amount = (taker.principle_amount * taker.interest_rate) + taker.principle_amount
                taker.principle_amount = (taker.principle_amount * taker.interest_rate) + taker.principle_amount
                print(f"Amount you have to return is {taker.principle_amount}")
                try:
                    amount = float(input("Enter amount you want to return: "))
                except ValueError:
                    print("Amount should be in integer or float")
                    while ValueError:
                        try:
                            amount = float(input("Enter amount you want to return: "))
                            break
                        except ValueError:
                            print("Value error occured.")
                if return_amount > amount:
                    Manager.loan_amount += amount
                    taker.principle_amount = taker.principle_amount - amount
                    loan_return.append(f"Loan Returned {amount}")
                    print(f"You have retured {amount} and you still have to pay {taker.principle_amount}")
                    Account.transaction_history.append(loan_return)
                elif return_amount < amount:
                    extra_amount = amount - return_amount
                    Manager.loan_amount += return_amount
                    self.balance += extra_amount
                    taker.principle_amount = 0
                    print(f"You have returned your loan. And updated balance is {self.balance}")
                    loan_return.append(f"Loan Returned {amount}")
                    Account.transaction_history.append(loan_return)
                    Loan.loanTakers.remove(taker)
                else:
                    Manager.loan_amount += return_amount
                    taker.principle_amount = 0
                    print(f"You have returned your loan")
                    Loan.loanTakers.remove(taker)
                    loan_return.append(f"Loan Returned {amount}")
                    Account.transaction_history.append(loan_return)
            else:
                print("You have no loan to return")

    def create_account(self):
        print(f"Your account is created successful with username {self.uname} and password {self.password}. Now login for further operations.")

    def login(self):
        try:
            id = int(input("Enter your CNIC: "))
        except ValueError:
            print("id should be in integer.")
            while ValueError:
                try:
                    id = int(input("Enter your CNIC: "))
                    break
                except ValueError:
                    print("Value error occured.")
        password = input("Enter your account password: ")
        if password == self.password and id == self.acc_holder.id:
            print("You have successfully logged in :) !")
        else:
            print("Invalid username or password.")
            return False

    def deposit(self):
        deposit = []
        deposit.append(self.acc_holder.id)
        try:
            amount = float(input("Enter amount to be deposited: "))
        except ValueError:
            print("Amount should be in integer or float")
            while ValueError:
                try:
                    amount=float(input("Enter amount to be deposited: "))
                    break
                except ValueError:
                    print("ValueError.Enter amount in float or in integer.")
        self.balance += amount
        t = time.time()
        deposit.append(f"Deposit time {time.ctime(t)}")
        deposit.append(f"Deposited Amount {amount}")
        Account.transaction_history.append(deposit)
        print(f"Your have made a deposit of {amount}. Successfully added to your account")

    def view_history(self):
        for history in Account.transaction_history:
            if self.acc_holder.id == history[0]:
                print(history)
            else:
                print("Dear customer, No Transaction history to show. Please make transactions! ")

    def show_account(self):
        print(self.acc_holder.show_customer(), self.uname, self.password, self.acc_type)

    @abstractmethod
    def withdraw(self):
        pass

    def balanceEnquiry(self):
        print(self.acc_holder.name, "\t", self.acc_number, "\t", self.balance)

class Checking_Account(Account):
    def __init__(self, acc_holder, uname, password, balance = 0, credit_limit = 150000, acc_type = "CheckingAccount"):
        super().__init__(acc_holder, password, uname, acc_type, balance)
        self.credit_limit = credit_limit

    def withdraw(self):
        withdrawl = []
        withdrawl.append(self.acc_holder.id)
        try:
            amount=float(input("Enter amount to be withdrawn: "))
        except ValueError:
            print("Amount should be in integer or float")
            while ValueError:
                try:
                    amount=float(input("Enter amount to be withdrawn: "))
                    break
                except ValueError:
                    print("ValueError.Enter amount in float or in integer.")
        if amount <= self.balance:
            self.balance = self.balance - amount
            withdrawl.append(f"Withdrawn Amount {amount}")
            t = time.time()
            withdrawl.append(time.ctime(t))
            print(f"Amount withdrawn is {amount}")
            Account.transaction_history.append(withdrawl)
        else:
            print("Amount entered is greater than the current balance! And you are given an overdraft within the credit limit")
            self.overdraft()


class Saving_Account(Account):
    def __init__(self, acc_holder, uname, password, balance = 0, interest_rate = 0.05, acc_type = "SavingAccount"):
        super().__init__(acc_holder, uname, password, acc_type, balance)
        self.interest_rate = interest_rate
        self.debit_Limit = float(100000)
    
    def withdraw(self):
        withdrawl = []
        try:
            amount=float(input("Enter amount to be withdrawn: "))
        except ValueError:
            print("Amount should be in integer or float")
            while ValueError:
                try:
                    amount=float(input("Enter amount to be withdrawn: "))
                    break
                except ValueError:
                    print("ValueError.Enter amount in float or in integer.")
        withdrawl.append(self.acc_holder.id)
        t = time.time()
        withdrawl.append(f"Withdraw time {time.ctime(t)}")
        while amount > self.debit_Limit:
            print(f"You are exceeding the debit limit. Please withdraw within limit {self.debit_Limit}")
            amount = float(input("Re-enter amount to withdraw: "))
        
        if amount <= self.balance:
            self.balance = self.balance - amount
            withdrawl.append(f"Withdrawn Amount {amount}")
            Account.transaction_history.append(withdrawl)
            print(f"Amount withdrawn is {amount} and your new balance is {self.balance}")
        elif amount > self.balance:
            while amount > self.balance:
                print("Amount entered is greater than the current balance! Enter the amount within the current balance: ")
                try:
                    amount = float(input("Enter amount to be withdrawn: "))
                except ValueError:
                    print("Amount should be in integer or float")
                    while ValueError:
                        try:
                            amount = float(input("Enter amount to be withdrawn: "))
                            break
                        except ValueError:
                            print("ValueError.Enter amount in float or in integer.")
            self.balance = self.balance - amount
            withdrawl.append(time.ctime(t))
            withdrawl.append(f"Withdrawn Amount {amount}")
            Account.transaction_history.append(withdrawl)
            print(f"Amount is withdrawn successfully. Amount withdrawn is {amount}")
    
    def needLoan(self):
        loan_taken = []
        try:
            income = float(input("What is your total monthly income?"))
            amount = float(input("What amount of loan you wanna take? "))
            loan_taken.append(self.acc_holder.id)
        except ValueError:
            print("Amount and income should be in integer or float")
            while ValueError:
                try:
                    income=float(input("What is your total monthly income?"))
                    amount=float(input("What amount of loan you wanna take? "))
                    break
                except ValueError:
                    print("ValueError.Enter amount in float or in integer.")
        t = time.time()
        loan_taken.append(f"Loan taken at {time.ctime(t)}")
        if income * Loan.loan_duration >= amount:
            Manager.loan_amount -= amount
            t = time.time()
            Loan.loanTakers.append(Loan(self.acc_holder, self.uname, self.password, self.acc_type, self.balance, amount, time.ctime(t)))
            print("Loan is given to you! ", amount)
            loan_taken.append(f"Loan taken {amount}")
            Account.transaction_history.append(loan_taken)
        else:
            print("You are not eligible for loan! ")


    def deposit(self):
        deposit = []
        deposit.append(self.acc_holder.id)
        try:
            amount=float(input("Enter amount to be deposited: "))
        except ValueError:
            print("Amount should be in integer or float")
            while ValueError:
                try:
                    amount=float(input("Enter amount to be deposited: "))
                    break
                except ValueError:
                    print("ValueError.Enter amount in float or in integer.")
        self.balance += amount
        t = time.time()
        import datetime as DT 
        today = DT.date.today()
        next_month = today + DT.timedelta(days=30) 
        interest_Amount = amount*self.interest_rate
        deposit.append(f"Deposit time {time.ctime(t)}")
        deposit.append(f"Deposited Amount {amount}")
        Account.transaction_history.append(deposit)
        print(f"Your have made a deposit of {amount}. Successfully added to your account")
        print("You will be given interest of this amount", interest_Amount, " as interest on", next_month)

class Loan(Account):
    loanTakers = []
    loan_duration = 6
    def __init__(self, acc_holder, uname, password, acc_type, balance, principle_amount, time):
        super().__init__(acc_holder, uname, password, acc_type, balance=balance)
        self.principle_amount = float(principle_amount)
        self.interest_rate = 0.2
        self.takenTime = time

    def withdraw(self):
        pass
manager = Manager()

print("Welcome ! to our Bank.You are on the right way. And our manager is", end=" ")
manager.show()
while True:
    start1 = input("Enter C to create account: ")
    while start1 != "c" and start1 != "C":
        start1 = input("Enter first C to create account and then proceed: ")
    a = input("Enter S for saving account, C for checking account: ")
    while a != "s" and a != "S" and a != "c" and a != "C":
        a = input("Enter S for saving account, C for checking account: ")
    Customer.add_customer()
    try:
        id = int(input("Re-Enter your CNIC or confirm CNIC: "))
    except ValueError:
        print("id should be in integer")
        while ValueError:
            try:
                id = int(input("Re-Enter your CNIC or confirm CNIC: "))
                break
            except ValueError:
                print("Value error occured.")
    if a == "s" or a == "S":
        for customer in Customer.customers_list:
            if customer.id == id:
                uname = input("Enter username: ")
                count = 0
                while count < 8:
                    password = input("Enter password of at least 8 characters: ")
                    count = len(password)
                Account.List_Account.append(Saving_Account(customer, uname, password))
                for account in Account.List_Account:
                    if account.password == password and account.acc_holder.id == id:
                        account.create_account()
                        print("Account Created")
                        while account.login() is False:
                            pass
    elif a == "c" or a == "C":
        for customer in Customer.customers_list:
            if customer.id == id:
                uname = input("Enter username: ")
                count = 0
            while count < 8:
                password = input("Enter password of at least 8 characters: ")
                count = len(password)
            Account.List_Account.append(Checking_Account(customer, uname, password))
            for account in Account.List_Account:
                if account.password == password and account.acc_holder.id == id:
                    account.create_account()
                    print("Account Created")
                    while account.login() is False:
                        pass
    while True:
        start = input("Enter:\nC to create account:\nD to deposit:\nW to withdraw:\nB to enquire balance\nV to view history\nL to take loan\nR to return loan \nE to exit: ")
        if start == "c" or start == "C":
            a = input("Enter S for saving account, C for checking account: ")
            while a != "s" and a != "S" and a != "c" and a != "C":
                a = input("Enter S for saving account, C for checking account: ")
            try:
                id = int(input("Re-Enter your CNIC or confirm CNIC: "))
            except ValueError:
                print("id should be in integer or float")
                while ValueError:
                    try:
                        id = int(input("Re-Enter your CNIC or confirm CNIC: "))
                        break
                    except ValueError:
                        print("Value error occured.")
            if a == "s" or a == "S":
                for customer in Customer.customers_list:
                    if customer.id == id:
                        uname = input("Enter username: ")
                        count = 0
                        while count < 8:
                            password = input("Enter password of at least 8 characters: ")
                            count = len(password)
                        Account.List_Account.append(Saving_Account(customer, uname, password))
                        for account in Account.List_Account:
                            if account.password == password and account.acc_holder.id == id:
                                account.create_account()
                        # while account.login() is False:
                        #     pass
                    else:
                        print("Enter valid CNIC")
            elif a == "c" or a == "C":
                for customer in Customer.customers_list:
                    if customer.id == id:
                        uname = input("Enter username: ")
                        count = 0
                        while count < 8:
                            password = input("Enter password of at least 8 characters: ")
                            count = len(password)
                        Account.List_Account.append(Checking_Account(customer, uname, password))
                        for account in Account.List_Account:
                            if account.password == password and account.acc_holder.id == id:
                                account.create_account()
                                # while account.login() is False:
                                #     pass
                    else:
                        print("Enter valid CNIC")
        elif start == "d" or start == "D":
            account.deposit()
        elif start == "w" or start == "W":
            account.withdraw()
        elif start == "h" or start == "H":
            account.view_history()
        elif start == "b" or start == "B":
            account.balanceEnquiry()
        elif start == "v" or start == "V":
            account.view_history()
        elif start == "l" or start == "L":
           if account.acc_type == "SavingAccount":
               account.needLoan()
        elif start == "r" or start == "R":
            if account.acc_type == "SavingAccount":
                account.return_loan()
            else:
               print("Only saving account holders can take loan. So you are not eligible")
        elif start == "e" or start == "E":
            print("Thanks for coming to our bank! Have a nice day! ")
            m = input("If you are manager and want to view transaction history then enter your credentials\nEnter Y if yes\nEnter N if no: ")
            if m == "Y" or m == "y":
                password = input("Enter password: ")
                while Manager.password != password:
                    password = input("Enter valid password: ")
                Manager.view_Reports()
                condition = input("Enter Y if you want to close the bank: ")
                if condition == 'Y' or condition == "y":
                    exit()
                else:
                    break
                
            else:
                condition = input("Enter Y if you want to close the bank: ")
                if condition == 'Y' or condition == "y":
                    exit()
                else:
                    break
        else:
            print("Enter valid input")