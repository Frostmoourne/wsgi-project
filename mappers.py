import sqlite3

from models import Student, Teacher, Course, Category

connection = sqlite3.connect('patterns.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class Mapper:

    def __init__(self, connection, tablename, mapper):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = tablename
        self.mapper = mapper

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return self.mapper(*result)
        else:
            raise RecordNotFoundException(f'Запись с id={id} не найдена.')

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            item = self.mapper(name)
            item.id = id
            result.append(item)
        return result

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return Mapper(connection, 'student', Student)
        if isinstance(obj, Teacher):
            return Mapper(connection, 'teacher', Teacher)
        if isinstance(obj, Course):
            return Mapper(connection, 'course', Course)
        if isinstance(obj, Category):
            return Mapper(connection, 'category', Category)

    @staticmethod
    def get_current_mapper(name, mapper):
        return Mapper(connection, name, mapper)
