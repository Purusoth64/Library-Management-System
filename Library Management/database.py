import psycopg2 as pg
from tabulate import tabulate as t

#make a connection with postgres database
try:
  connection=pg.connect(host='localhost',
                      port=5432,
                      database='target_hub',
                      user='postgres',
                      password='spDurai@64')

  cur=connection.cursor()
except pg.OperationalError as e:
    print(f"Error connecting to the database: {e}")

def close_conn():
    try:
        connection.commit()
        cur.close()
        connection.close()
    except pg.Error as e:
        print(f"Error closing the connection: {e}")

def add_book(book_id,book_name,author_name,published_year,ratings):
    try:
        sql=f'''insert into library values({book_id},'{book_name}','{author_name}',
                                        '{published_year}',{ratings});'''
        cur.execute(sql)
        print('Book Details Added sucessfully into library table')
    except pg.Error as e:
        print(f"Error adding book details: {e}")


def view_details():
    try:
        cur.execute('select * from library;')
        view_data = cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        print(t(view_data,headers=headers,tablefmt='pipe'))
    except pg.Error as e:
        print(f"Error adding book details: {e}")

def update_book(column_name,value,book_id):
    try:
        cur.execute(f"SELECT book_id FROM library WHERE book_id = {book_id};")
        res = cur.fetchone()

        if res:
            update = f"UPDATE library SET {column_name} = '{value}' WHERE book_id = {book_id};"
            cur.execute(update)
            print('Book Details Updated Successfully')
        else:
            print('You Entered Wrong Book_ID. Please Check The Table')
    except pg.Error as e:
        print(f"Error adding book details: {e}")

def del_book(book_id):

    try:
        # Check if the book_id exists in the library table
        cur.execute(f"SELECT book_id FROM library WHERE book_id = {book_id};")
        res = cur.fetchone()

        if res:
            delete = f"DELETE FROM library WHERE book_id = {book_id};"
            cur.execute(delete)
            print('Book Details Deleted Successfully')
        else:
            print('The Book_ID does not exist in the table. Please check the value.')
    except pg.Error as e:
        print(f"Error deleting book details: {e}")


def search_book(book_name):
    try:
        book = cur.execute(f"select book_name from library where book_name='{book_name}';")
        name = cur.fetchone()
        cur.execute(f"select * from library where book_name='{book_name}'");
        search=cur.fetchall()
        headers = [desc[0] for desc in cur.description]
        if name:
            print(t(search,headers=headers,tablefmt='pipe'))
        else:
            print("Please Enter Correct Book Name ")
    except pg.Error as e:
        print(f"Error adding book details: {e}")

def del_details():
    try:
        truncate='Truncate table Library;'
        cur.execute(truncate)
        print('All Book Details Deleted Sucessfully')
    except pg.Error as e:
        print(f"Error adding book details: {e}")

e_s = '😀'
e_b = '📚'
print("\t\t\t\t\t\t\t\t",e_s,e_b,e_b,e_s,"Welcome To Library",e_s,e_b,e_b,e_s)
print("Please Select Your Option\n1.Add Book Details\n2.Display All Books\n3.Delete Book Details")
print("4.Update Book Details\n5.Search Book Details\n6.Delete All Books")
user_ip=int(input('Enter Your Option : '))

if user_ip==1:
    book_id=int(input('Enter Your Book Number : '))
    book_name=input('Ente Your Book Name : ')
    author_name=input('Enter Author Name  : ')
    published_year=input('Enter The Year Of Published : ')
    ratings=int(input('Rating Of The Book : '))
    add_book(book_id,book_name,author_name,published_year,ratings)

elif user_ip==2:
    view_details()

elif user_ip==3:
    book_id = int(input('Enter Your Book Id : '))
    del_book(book_id)

elif user_ip==4:
    column_name = input('Enter Column Name You Want To Change : ')
    value=input('Enter The Value You Want To Change : ')
    book_id=(input('Enter Your Book Id or Book Name: '))
    update_book(column_name, value, book_id)

elif user_ip==5:
    book_name = input('Enter Your Book Name : ')
    search_book(book_name)

elif user_ip==6:
    del_details()

else:
    print('This Is Not A Valid Input')
close_conn()