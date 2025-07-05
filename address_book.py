from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self._validate(value)
        super().__init__(value)

    def _validate(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits")


class Birthday(Field):
    def __init__(self, value):
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date_value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        bday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str},birthday: {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        end_date = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value  # це вже datetime.date
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= end_date:
                    congrats_date = birthday_this_year

                    if congrats_date.weekday() == 5:  # Субота
                        congrats_date += timedelta(days=2)
                    elif congrats_date.weekday() == 6:  # Неділя
                        congrats_date += timedelta(days=1)

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congrats_date.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays

        
def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments."
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except Exception as e:
            return f"Unexpected error: {e}"
    return wrapper


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        return "Invalid command. Usage: add-birthday [name] [birthday]"
    name, bday = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(bday)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    if record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"{name} has no birthday set."


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    lines = [f"{item['name']}: {item['congratulation_date']}" for item in upcoming]
    return "\n".join(lines)


@input_error
def add_contact(args, book):
    if len(args) < 2:
        return "Invalid command. Usage: add [name] [phone]"
    name, phone = args[0], args[1]
    record = book.find(name)
    try:
        if record:
            record.add_phone(phone)
            return f"Phone added to existing contact {name}."
        else:
            new_record = Record(name)
            new_record.add_phone(phone)
            book.add_record(new_record)
            return f"Contact {name} added."
    except ValueError as e:
        return str(e)


@input_error
def change_contact(args, book):
    if len(args) != 3:
        return "Invalid command. Usage: change [name] [old_phone] [new_phone]"
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    if record.edit_phone(old_phone, new_phone):
        return "Phone updated."
    return "Old phone not found."


@input_error
def show_phone(args, book):
    if len(args) != 2:
        return "Invalid command. Usage: phone [name] [phone]"
    name, phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    found = record.find_phone(phone)
    if found:
        return f"{name}: {found.value}"
    return "Phone not found."


@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def delete_contact(args, book):
    if len(args) != 1:
        return "Invalid command. Usage: delete [name]"
    name = args[0]
    if book.delete(name):
        return f"Contact {name} deleted."
    return "Contact not found."
