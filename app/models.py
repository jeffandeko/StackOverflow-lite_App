from app import db


class Questions(db.Model):
    """ This is the class that will represent StackOveflow-lite question table"""

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String(0))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, users_name):
        """ The questions are initialized to start with name"""

        self.users_name = users_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Questions.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Questions: {}>".format(self.users_name)


class Answers(db.model):
    """this is the class that will represent StackOverflow-lite Answers table """
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String(0))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, users_name):
        """Initializes answers to begin with users_name"""
        self.users_name = users_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Answers.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Answers: {}>".format(self.Users_name)
