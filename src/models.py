from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    isbn = db.Column(db.String(120), unique=False, nullable=False)
    author = db.Column(db.String(100), unique=False, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "isbn": self.isbn,
            "author":self.author
            
        }
    @classmethod
    def create(cls, kws):
        try:
            new_Books = cls(**kws)
            db.session.add(new_Books)
            db.session.commit()
            return new_Books
        except Exception as error:
            db.session.rollback()
            print(error)
            return None

    def update(self, book):
        if "title" in book:
            self.title = book["title"]
        if "isbn" in book:
            self.isbn = book["isbn"]
        if "author" in book:
            self.author = book["author"]

        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(error)
            return False

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            print(error)
            return False