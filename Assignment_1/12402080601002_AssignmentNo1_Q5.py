'''
Problem Statement: Design an OOP-based settlement engine with Account, Transaction and Bank classes. The engine must support
deposit, withdraw and transfer operations, maintain transaction history, prevent overdraft, and rollback an entire batch if any transaction
in the batch fails. Use custom exceptions and suitable getters/setters or properties.
'''

class InsufficientBalanceError(Exception):
    pass


class AccountNotFoundError(Exception):
    pass


class Account:

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")

        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Invalid amount")

        if amount > self.balance:
            raise InsufficientBalanceError()

        self.balance -= amount


class Transaction:

    def __init__(self, transaction_type, account, amount, to_account=None):
        self.transaction_type = transaction_type
        self.account = account
        self.amount = amount
        self.to_account = to_account


class Bank:

    def __init__(self):
        self.accounts = {}
        self.history = []

    def add_account(self, account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError()

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)
        account.deposit(amount)

        self.history.append(
            Transaction("DEPOSIT", account_id, amount)
        )

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)
        account.withdraw(amount)

        self.history.append(
            Transaction("WITHDRAW", account_id, amount)
        )

    def transfer(self, from_account, to_account, amount):
        source = self.get_account(from_account)
        destination = self.get_account(to_account)

        source.withdraw(amount)
        destination.deposit(amount)

        self.history.append(
            Transaction("TRANSFER", from_account, amount, to_account)
        )


n = int(input())

bank = Bank()

for i in range(n):
    account_id, balance = input().split()
    bank.add_account(Account(account_id, int(balance)))

q = int(input())

batch_number = 0
batch_accounts = None
batch_active = False

for i in range(q):

    parts = input().split()
    operation = parts[0]

    if operation == "BATCH_BEGIN":
        batch_number += 1
        batch_active = True
        batch_accounts = {}

        for account_id in bank.accounts:
            batch_accounts[account_id] = bank.accounts[account_id].balance

    elif operation == "BATCH_END":
        batch_active = False
        batch_accounts = None

    else:

        try:

            if operation == "DEPOSIT":
                bank.deposit(parts[1], int(parts[2]))

            elif operation == "WITHDRAW":
                bank.withdraw(parts[1], int(parts[2]))

            elif operation == "TRANSFER":
                bank.transfer(parts[1], parts[2], int(parts[3]))

        except Exception:

            if batch_active:

                for account_id in batch_accounts:
                    bank.accounts[account_id].balance = batch_accounts[account_id]

                print("FAILED", batch_number)

                batch_active = False
                batch_accounts = None

for account_id in sorted(bank.accounts):
    print(account_id, bank.accounts[account_id].balance)