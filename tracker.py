#! /opt/miniconda3/bin/python3
'''
tracker is an app that maintains a list of personal
financial transactions.

It uses Object Relational Mappings (ORM)
to abstract out the database operations from the
UI/UX code.

The ORM, Category, will map SQL rows with the schema
  (rowid, category, description)
to Python Dictionaries as follows:

(5,'rent','monthly rent payments') <-->

{rowid:5,
 category:'rent',
 description:'monthly rent payments'
 }

Likewise, the ORM, Transaction will mirror the database with
columns:
amount, category, date (yyyymmdd), description

In place of SQL queries, we will have method calls.

This app will store the data in a SQLite database ~/tracker.db

Note the actual implementation of the ORM is hidden and so it
could be replaced with PostgreSQL or Pandas or straight python lists

'''

#from transactions import Transaction
from category import Category
from transaction import Transaction
import sys

transactions = Transaction('tracker.db')
category = Category('tracker.db')


# here is the menu for the tracker app

menu = '''
0. quit
1. show categories
2. add category
3. modify category
4. show transactions
5. add transaction
6. delete transaction
7. summarize transactions by date
8. summarize transactions by month
9. summarize transactions by year
10. summarize transactions by category
11. print this menu
'''

def process_choice(choice):

    if choice=='0':
        return
    elif choice=='1':
        cats = category.select_all()
        print_categories(cats)
    elif choice=='2':
        name = input("category name: ")
        desc = input("category description: ")
        cat = {'name':name, 'desc':desc}
        category.add(cat)
    elif choice=='3':
        print("modifying category")
        rowid = int(input("rowid: "))
        name = input("new category name: ")
        desc = input("new category description: ")
        cat = {'name':name, 'desc':desc}
        category.update(rowid,cat)
    elif choice=='4':
        trans = transactions.select_all()
        print_transactions(trans)
    elif choice=='5':
        amount = int(input("transaction amount: "))
        cate = input("transaction category: ")
        date = int(input("transaction date (yyyymmdd): "))
        description = input("transaction description: ")
        tran = {'amount':amount,'category':cate,'date':date,'description':description}
        transactions.add(tran)
    elif choice=='6':
        print("deleting transaction")
        rowid = int(input("rowid: "))
        transactions.delete(rowid)
    elif choice=='7':
        res = transactions.transactions_by_date()
        print_transactions_groupby_date(res)
    elif choice=='8':
        res = transactions.transactions_by_month()
        print_transactions_groupby_month(res)
    elif choice=='9':
        res = transactions.transactions_by_year()
        print_transactions_groupby_year(res)
    elif choice=='10':
        res = transactions.transactions_by_category()
        print_transactions_groupby_category(res)
    elif choice=='11':
        print_help_menu()
    else:
        print("choice",choice,"not yet implemented")

    choice = input("> ")
    return(choice)


def toplevel():
    ''' handle the user's choice '''

    ''' read the command args and process them'''
    print(menu)
    choice = input("> ")
    while choice !='0' :
        choice = process_choice(choice)
    print('bye')

#
# here are some helper functions
#

def print_transactions(items):
    ''' print the transactions '''
    if len(items)==0:
        print('no items to print')
        return
    print('\n')
    print("%-10s %-10s %-10s %-10s %-30s"%(
        'item #','amount','category','date','description'))
    print('-'*50)
    for item in items:
        values = tuple(item.values())
        print("%-10s %-10d %-10s %-10d %-30s"%values)

def print_transactions_groupby_date(items):
    ''' helper method when group by date '''
    if len(items)==0:
        print('no items to print')
        return
    print('\n')
    print("%-10s %-10s"%(
        'date','amount'))
    print('-'*50)
    for item in items:
        values = tuple(item.values())
        print("%-10s %-10d"%values)

def print_transactions_groupby_month(items):
    ''' helper method when group by month '''
    if len(items)==0:
        print('no items to print')
        return
    print('\n')
    print("%-10s %-10s"%(
        'month','amount'))
    print('-'*50)
    for item in items:
        values = tuple(item.values())
        print("%-10s %-10d"%values)

def print_transactions_groupby_year(items):
    ''' helper method when group by year '''
    if len(items)==0:
        print('no items to print')
        return
    print('\n')
    print("%-10s %-10s"%(
        'year','amount'))
    print('-'*50)
    for item in items:
        values = tuple(item.values())
        print("%-10s %-10d"%values)

def print_transactions_groupby_category(items):
    ''' helper method when group by category '''
    if len(items)==0:
        print('no items to print')
        return
    print('\n')
    print("%-10s %-10s"%(
        'category','amount'))
    print('-'*50)
    for item in items:
        values = tuple(item.values())
        print("%-10s %-10d"%values)

def print_help_menu():
    ''' print help menu '''
    print(menu)

def print_category(cat):
    print("%-3d %-10s %-30s"%(cat['rowid'],cat['name'],cat['desc']))

def print_categories(cats):
    print("%-3s %-10s %-30s"%("id","name","description"))
    print('-'*45)
    for cat in cats:
        print_category(cat)


# here is the main call!

toplevel()
