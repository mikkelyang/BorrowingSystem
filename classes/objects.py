from database import ConnectionPool
from datetime import datetime, timedelta


class Persons:
    def __init__(self, first_name, last_name, person_type,
                 school_id=None, rfid_num=None, inventory_login=None, username=None, password=None, person_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.person_type = person_type
        self.school_id = school_id
        self.rfid_num = rfid_num
        self.inventory_login = inventory_login
        self.username = username
        self.password = password
        self.person_id = person_id

    def add_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''INSERT INTO persons(last_name, first_name, person_type, school_id, rfid_num)
            VALUES(%s, %s, %s, %s, %s) RETURNING person_id;''', (self.last_name, self.first_name, self.person_type,
                                                                 self.school_id, self.rfid_num))
            self.person_id = cursor.fetchone()[0]

            if self.username and self.password:
                cursor.execute('''INSERT INTO login_permission(inventory_login, username, password, person_id) 
                VALUES(%s, %s, %s, %s);''', (self.inventory_login, self.username, self.password, self.person_id))

    def update_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE persons SET last_name = %s, first_name = %s, person_type = %s,
            school_id = %s, rfid_num = %s WHERE person_id = %s''',
                           (self.last_name, self.first_name, self.person_type, self.school_id, self.rfid_num,
                            self.person_id))

    def update_login(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE login_permission SET inventory_login = %s, username = %s, password = %s
            WHERE person_id = %s''', (self.inventory_login, self.username, self.password, self.person_id))

    @classmethod
    def load_by_id(cls, person_id):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT last_name, first_name, person_type, school_id, rfid_num FROM persons
            WHERE person_id = %s''', (person_id,))
            last_name, first_name, person_type, school_id, rfid_num = cursor.fetchone()
            return cls(last_name=last_name, first_name=first_name, person_type=person_type, school_id=school_id,
                       rfid_num=rfid_num, person_id=person_id)

    @classmethod
    def load_by_name(cls, last_name, first_name):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT person_id, person_type, school_id, rfid_num FROM persons
            WHERE UPPER(last_name) = %s AND UPPER(first_name) = %s;''', (last_name.upper(), first_name.upper()))
            person_id, person_type, school_id, rfid_num = cursor.fetchone()
            return cls(last_name=last_name, first_name=first_name, person_type=person_type, school_id=school_id,
                       rfid_num=rfid_num, person_id=person_id)

    @classmethod
    def attempt_login(cls, username, password):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT password, person_id FROM login_permission WHERE UPPER(username) = %s',
                           (str(username).upper(),))
            data = cursor.fetchone()

            if data:
                db_password, person_id = data
                if db_password == password:
                    return cls.load_by_id(person_id)
                else:
                    return False
            else:
                return False


class Items:
    def __init__(self, item_name, category, item_type, brand=None, remarks=None, added_on=None, item_id=None):
        self.item_name = item_name
        self.category = category
        self.item_type = item_type
        self.brand = brand
        self.remarks = remarks
        if added_on is None:
            self.added_on = datetime.now()
        else:
            self.added_on = added_on
        self.item_id = item_id

    def add_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''INSERT INTO inventory.items(item_name, category, item_type, brand, remarks, added_on)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING item_id;''',
                           (self.item_name, self.category, self.item_type, self.brand, self.remarks, self.added_on))
            self.item_id = cursor.fetchone()[0]

    def update_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE inventory.items SET item_name = %s, category = %s, item_type = %s, brand = %s,
            remarks = %s, added_on = %s WHERE item_id = %s''',
                           self.item_name, self.category, self.item_type, self.brand, self.remarks, self.added_on,
                           self.item_id)

    @classmethod
    def load_by_id(cls, item_id):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT item_name, category, item_type, brand, remarks, added_on 
            FROM inventory.items WHERE item_id = %s;''', (item_id,))
            item_name, category, item_type, brand, remarks, added_on = cursor.fetchone()
            return cls(item_name=item_name, category=category, item_type=item_type, brand=brand, remarks=remarks,
                       added_on=added_on, item_id=item_id)

    @classmethod
    def load_by_name(cls, item_name):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT item_id, category, item_type, brand, remarks, added_on
            FROM inventory.items WHERE item_name = %s;''', (item_name,))
            item_id, category, item_type, brand, remarks, added_on = cursor.fetchone()
            return cls(item_name=item_name, category=category, item_type=item_type, brand=brand, remarks=remarks,
                       added_on=added_on, item_id=item_id)


class Units(Items):
    def __init__(self, item_id, supplier_id, serial=None, date_purchased=None, sequence=None,
                 add_remarks=None, unit_id=None, date_removed=None, remove_remarks=None, removed_by_person_id=None):
        self.item_id = item_id
        self.supplier_id = supplier_id
        self.serial = serial
        if date_purchased is None:
            self.date_purchased = date_purchased
        else:
            self.date_purchased = datetime.now()
        self.sequence = sequence
        self.add_remarks = add_remarks
        self.unit_id = unit_id

        self.date_removed = date_removed
        self.remove_remarks = remove_remarks
        self.removed_by_person_id = removed_by_person_id

        item = Items.load_by_id(self.item_id)
        super(Units, self).__init__(item_name=item.item_name, category=item.category, item_type=item.item_type,
                                    brand=item.brand, remarks=item.remarks, added_on=item.added_on,
                                    item_id=item.item_id)

    def add_to_db(self):
        if self.date_removed is None or self.remove_remarks is None or self.removed_by_person_id is None:
            with ConnectionPool() as cursor:
                if self.sequence is None:
                    cursor.execute('''SELECT MAX(sequence) FROM inventory.units WHERE item_id = %s;''', (self.item_id,))
                    data = cursor.fetchone()

                    if data:
                        self.sequence = data[0] + 1
                    else:
                        self.sequence = 1

                cursor.execute('''INSERT INTO inventory.units(item_id, date_purchased, add_remarks, serial, sequence,
                supplier_id) VALUES(%s, %s, %s, %s, %s, %s) RETURNING unit_id''',
                               (self.item_id, self.date_purchased, self.add_remarks, self.serial, self.sequence,
                                self.supplier_id))
                self.unit_id = cursor.fetchone()[0]
        else:
            raise ValueError('You are adding a unit where either removed_date, remove_remarks, '
                             'or removed_by is not null')

    def update_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE inventory.units SET item_id = %s, date_purchased = %s, add_remarks = %s,
            serial = %s, sequence = %s, supplier_id = %s, date_removed = %s, remove_remarks = %s, 
            removed_by_person_id = %s WHERE unit_id = %s''',
                           (self.item_id, self.date_purchased, self.add_remarks, self.serial, self.sequence,
                            self.supplier_id, self.date_removed, self.remove_remarks, self.removed_by_person_id,
                            self.unit_id))

    @classmethod
    def load_by_id(cls, unit_id):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT item_id, date_purchased, add_remarks, serial, sequence, supplier_id,
            date_removed, remove_remarks, removed_by_person_id WHERE unit_id = %s;''', (unit_id,))
            item_id, date_purchased, add_remarks, ser, seq, supplier_id, date_re, removed_re, removed_by = cursor.fetchone()[0]
            return cls(item_id=item_id, date_purchased=date_purchased, add_remarks=add_remarks, serial=ser,
                       sequence=seq, supplier_id=supplier_id, date_removed=date_re,
                       remove_remarks=removed_re, removed_by_person_id=removed_by, unit_id=unit_id)


class UnitPerson:
    def __init__(self, person_id, unit_id, borrow_type, borrow_date=None, borrow_remarks=None, expected_return=None,
                 return_by=None, date_return=None, return_remarks=None, verified=None, room=None, borrow_id=None):
        self.person_id = person_id
        self.unit_id = unit_id
        self.borrow_type = borrow_type
        self.borrow_remarks = borrow_remarks
        self.verified = verified
        self.room = room

        if borrow_date is None:
            self.borrow_date = datetime.now()
        else:
            self.borrow_date = borrow_date

        if expected_return is None:
            self.expected_return = datetime.now() + timedelta(days=1)
        else:
            self.expected_return = expected_return

        self.return_by = return_by
        self.date_return = date_return
        self.return_remarks = return_remarks

        self.borrow_id = borrow_id

    def add_to_db(self):
        if self.return_remarks is None or self.date_return is None or self.return_by is None:
            with ConnectionPool() as cursor:
                cursor.execute('''INSERT INTO inventory.unit_person (person_id, unit_id, borrow_date, borrow_type, 
                borrow_remarks, expected_return, verified, room) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING borrow_id;''',
                               (self.person_id, self.unit_id, self.borrow_date, self.borrow_type, self.borrow_remarks,
                                self.expected_return, self.verified, self.room))
                self.borrow_id = cursor.fetchone()[0]

        else:
            raise ValueError('You are adding a borrow transaction where either removed_date, remove_remarks, '
                             'or removed_by is not null')

    def update_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE inventory.unit_person SET person_id = %s, unit_id = %s, borrow_date = %s,
            borrow_type = %s, borrow_remarks = %s, expected_return = %s, return_by_person_id = %s, 
            date_return = %s, return_remarks = %s, verified = %s, room = %s WHERE borrow_id = %s;''',
                           (self.person_id, self.unit_id, self.borrow_date, self.borrow_type, self.borrow_remarks,
                            self.expected_return, self.return_by, self.date_return, self.return_remarks,
                            self.verified, self.borrow_id, self.room))

    @classmethod
    def load_by_id(cls, borrow_id):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT person_id, unit_id, borrow_date, borrow_type, borrow_remarks, expected_return,
            return_by_person_id, date_return, return_remarks, verified, room 
            FROM inventory.unit_person
            WHERE borrow_id = %s;''', (borrow_id,))
            person_id, unit_id, bor_date, bor_type, bor_rem, expected_ret, ret_by, date_ret, ret_remarks, verified, room = cursor.fetchone()
            return cls(person_id=person_id, unit_id=unit_id, borrow_date=bor_date, borrow_type=bor_type,
                       borrow_remarks=bor_rem, expected_return=expected_ret, return_by=ret_by, date_return=date_ret,
                       return_remarks=ret_remarks, borrow_id=borrow_id, verified=verified, room=room)

    @staticmethod
    def get_table_info():
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT last_name, first_name, item_name, borrow_date, expected_return, borrow_remarks
            FROM inventory.unit_person WHERE ''')


class Rooms:
    def __init__(self, room_name, room_number, floor=None, in_charge=None, room_id=None):
        self.room_name = room_name
        self.room_number = room_number
        self.floor = floor
        self.in_charge = in_charge
        self.room_id = room_id

    def __repr__(self):
        return "{}: {}".format(self.room_number, self.room_name)

    def add_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''INSERT INTO rooms (room_name, room_number, floor, in_charge)
            VALUES (%s, %s, %s, %s) RETURNING room_id;''',
                           (self.room_name, self.room_number, self.floor, self.in_charge))
            self.room_id = cursor.fetchone()[0]

    def update_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE rooms SET room_name = %s, room_number = %s, floor = %s, in_charge = %s
            WHERE room_id = %s;''',
                           (self.room_name, self.room_number, self.floor, self.in_charge, self.room_id))

    @classmethod
    def load_by_id(cls, room_id):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT room_name, room_number, floor, in_charge FROM rooms WHERE room_id = %s;', (room_id,))
            room_name, room_number, floor, in_charge = cursor.fetchone()
            return cls(room_name=room_name, room_number=room_number, floor=floor, in_charge=in_charge, room_id=room_id)

    @classmethod
    def load_by_number(cls, room_number):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT room_id, room_name, floor, in_charge FROM rooms WHERE room_number = %s',
                           (room_number,))
            room_id, room_name, floor, in_charge = cursor.fetchone()
            return cls(room_name=room_name, room_number=room_number, floor=floor, in_charge=in_charge, room_id=room_id)


class Suppliers:
    def __init__(self, name, contact, number, email, supplier_id=None):
        self.supplier_name = name
        self.contact_person = contact
        self.contact_number = number
        self.contact_email = email
        self.supplier_id = supplier_id

    def __repr__(self):
        return "{}. Contact: {}. Nunmber: {}. Email: {}.".format(self.supplier_name, self.contact_person,
                                                                 self.contact_number, self.contact_email)

    def add_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''INSERT INTO inventory.suppliers(supplier_name, contact_person,
            contact_number, contact_email) VALUES (%s, %s, %s, %s) RETURNING supplier_id;''',
                           (self.supplier_name, self.contact_person, self.contact_number, self.contact_email))
            self.supplier_id = cursor.fetchone()[0]

    def update_db(self):
        with ConnectionPool() as cursor:
            cursor.execute('''UPDATE inventory.suppliers SET supplier_name = %s, contact_person = %s, 
            contact_number = %s, contact_email = %s WHERE supplier_id = %s''',
                           (self.supplier_name, self.contact_person, self.contact_number, self.contact_email,
                            self.supplier_id))

    @classmethod
    def load_by_id(cls, supplier_id):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT supplier_name, contact_person, contact_number,contact_email
            FROM inventory.suppliers WHERE supplier_id = %s;''',
                           (supplier_id,))

            supplier_name, contact_person, contact_number, contact_email = cursor.fetchone()
            return cls(name=supplier_name, contact=contact_person, number=contact_number, email=contact_email,
                       supplier_id=supplier_id)

    @classmethod
    def load_by_name(cls, supplier_name):
        with ConnectionPool() as cursor:
            cursor.execute('''SELECT supplier_id, contact_person, contact_number,contact_email 
            FROM inventory.suppliers WHERE supplier_name = %s;''',
                           (supplier_name,))
            supplier_id, contact_person, contact_number, contact_email = cursor.fetchone()
            return cls(name=supplier_name, contact=contact_person, number=contact_number, email=contact_email,
                       supplier_id=supplier_id)
