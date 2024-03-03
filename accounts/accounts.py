from web3_utils import *


class Account():
    def __init__(self):
        self.name = ''
        self.key = ''
        self.address = ''
        self.proxy = ''


Accounts = []


f = open('accounts\\accounts.txt', 'r')
lines = f.readlines()


for line in lines:
    if line[0] == '#':
        continue

    splitted = line.split(',')
    if len(splitted) != 7:
        continue

    account = Account()
    account.name = splitted[0]
    account.key = splitted[1]
    account.address = get_address(account.key)
    account.proxy = splitted[1]

    Accounts.append(account)


f.close()