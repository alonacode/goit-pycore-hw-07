from address_book import AddressBook, parse_input, add_contact, change_contact, show_phone, show_all, delete_contact, \
    add_birthday, show_birthday, birthdays


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        cmd, args = parse_input(user_input)

        if cmd in ("exit", "close"):
            print("Good bye!")
            break
        elif cmd == "hello":
            print("How can I help you?")
        elif cmd == "add":
            print(add_contact(args, book))
        elif cmd == "change":
            print(change_contact(args, book))
        elif cmd == "phone":
            print(show_phone(args, book))
        elif cmd == "all":
            print(show_all(book))
        elif cmd == "add-birthday":
            print(add_birthday(args, book))
        elif cmd == "show-birthday":
            print(show_birthday(args, book))
        elif cmd == "birthdays":
            print(birthdays(args, book))
        elif cmd == "delete":
            print(delete_contact(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()