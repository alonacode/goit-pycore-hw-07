from address_book import AddressBook, Record

if __name__ == "__main__":

    # Test OOP
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("7.07.1990")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")
    book.delete("Jane")

    print("\nПісля видалення Jane:")
    for name, record in book.data.items():
        print(record)

    print("\n Upcoming birthdays:")
    for item in book.get_upcoming_birthdays():
        print(f"{item['name']}: {item['congratulation_date']}")