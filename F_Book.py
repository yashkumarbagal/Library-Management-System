import json
import os
from datetime import datetime, timedelta



def read_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

available=0
def login():
 
    print("usernamr:yash   password:yash" )
    username = input("Enter username:")
    password = input("Enter password:")

    
    if  username=="yash" and  password=="yash":
        print("Login successful ")
        return True

    print("Invalid login ")
    return False



class Book:

    # add book
    def add_book(self):
        books = read_json("books.json")

        
        book_id       =int(input("Id (int):"))
        book_title    =    input("Title :")
        book_author   =    input("Author:")
        book_subject  =    input("Subject:")
        book_isbn     =int(input("isbn (int)     :"))
        book_price    =float(input("Price (float) :"))
        
        books.append({"book_id":book_id,
                      "book_title":book_title,
                      "book_author":book_author,
                      "book_price":book_price,
                      "book_subject":book_subject,
                      "book_isbn":book_isbn})

        write_json("books.json", books)
        print("Book added ")
        global available
        available+=1



class Copy:

    # add copy
    def add_copy(self):
        copies = read_json("copies.json")

        copy_id = input("Copy ID: ")
        book_id = input("Book ID: ")
        rack = input("Rack: ")

        copies.append({
            "copy_id": copy_id,
            "book_id": book_id,
            "rack": rack,
            "status": "available"
        })

        write_json("copies.json", copies)
        print("Copy added  ")


class Member:

    def add_member(self):
        members = read_json("members.json")

        member_id = input("Member ID: ")
        name = input("Name: ")
        membership=bool(input("Membership Paid(T/F):"))

        members.append({
            "member_id": member_id,
            "name": name,
            "paid": membership
        })

        write_json("members.json", members)
        print("Member added  ")



class Issue:

    def issue_book(self):
        member_id = input("Member ID: ")
        book_id = input("Book ID: ")

        members = read_json("members.json")
        copies = read_json("copies.json")
        issues = read_json("issues.json")

        
        valid = False
        for m in members:
            if m["member_id"] == member_id and m["paid"]:
                valid = True

        if not valid:
            print("Member not allowed ")
            return

        # copy check
        for c in copies:
            if c["book_id"] == book_id and c["status"] == "available":

                c["status"] = "issued"

                issue_date = datetime.now()
                due_date = issue_date + timedelta(days=7)

                issues.append({
                    "issue_id": len(issues) + 1,
                    "copy_id": c["copy_id"],
                    "member_id": member_id,
                    "issue_date": str(issue_date.date()),
                    "due_date": str(due_date.date()),
                    "return_date": None,
                    "fine": 0
                })

                write_json("copies.json", copies)
                write_json("issues.json", issues)

                print("Book issued ")
                return

        print("No copy available ")


class Return:

    def return_book(self):
        copy_id = input("Enter Copy ID: ")

        issues = read_json("issues.json")
        copies = read_json("copies.json")

        for i in issues:
            if i["copy_id"] == copy_id and i["return_date"] is None:

                due = datetime.strptime(i["due_date"], "%Y-%m-%d")
                today = datetime.now()

                delay = (today - due).days
                fine = 0

                if delay > 0:
                    fine = delay * 5

                i["return_date"] = str(today.date())
                i["fine"] = fine

              
                for c in copies:
                    if c["copy_id"] == copy_id:
                        c["status"] = "available"

                write_json("issues.json", issues)
                write_json("copies.json", copies)

                print("Returned  Fine =", fine)
                return

        print("Record not found ")



class Search:

    
    def search_book(self):
        book_id = input("Enter Book ID: ")

        books = read_json("books.json")
        copies = read_json("copies.json")

        
        found = False
        for b in books:
            if b["book_id"] == book_id:
                print("\nBook Found:")
                print(b)
                found = True
            
        if not found:
            print("Book not found ")
            return

        # check copies
        available = 0
        total = 0

        for c in copies:
            if c["book_id"] == book_id:
                total += 1
                if c["status"] == "available":
                    available += 1

        print(f"Total Copies: {total}")
        print(f"Available Copies: {available}")

        if available > 0:
            print(" Book is available")
        else:
            print(" Book is NOT available")

class Report:

   
    def issued_books(self):
        issues = read_json("issues.json")

        print("\nIssued Books:")
        for i in issues:
            if i["return_date"] is None:
                print(i)

    
    def overdue_books(self):
        issues = read_json("issues.json")
        today = datetime.now()

        print("\nOverdue Books:")
        for i in issues:
            if i["return_date"] is None:
                due = datetime.strptime(i["due_date"], "%Y-%m-%d")
                if today > due:
                    print(i)

  
    def paid_members(self):
        members = read_json("members.json")

        print("\nPaid Members:")
        for m in members:
            if m["paid"]==True:
                print(m)
        print("\nUN-Paid Members:")
        for m in members:
            if m["paid"]==False:
                print(m)
   
    def total_fine(self):
        issues = read_json("issues.json")

        total = 0
        for i in issues:
            total += i["fine"]

        print("\nTotal Fine Collected =", total)


def main():
    if not login():
        return

    else:
        while True:
            print("\n===== LIBRARY MENU =====")
            print("1. Add Book")
            print("2. Add Copy")
            print("3. Add Member")
            print("4. Issue Book")
            print("5. Return Book")
            print("6. search Book")
            print("7. Report of Issued Book")   
            print("8. Report of Show Overdue")
            print("9. Report of Paid Members")
            print("10. Report of Total Fine")
            print("11. Exit")
            
            print("="*80)
            
            choice = input("Enter choice: ")
            
            if choice == "1":
                Book().add_book()
            elif choice == "2":
                Copy().add_copy()
            elif choice == "3":
                Member().add_member()
            elif choice == "4":
                Issue().issue_book()
            elif choice == "5":
                Return().return_book()
            elif choice == "6":
                Search().search_book()
            elif choice == "7":
                Report().issued_books()
            elif choice == "8":
                Report().overdue_books()
            elif choice == "9":
                Report().paid_members()
            elif choice == "10":
                Report().total_fine()
            elif choice == "11":
                break
            else:
                print("Invalid choice ")
            print('='* 80)
            



main()
