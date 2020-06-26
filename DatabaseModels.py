from datetime import datetime
from app import database


class Images(database.Model):
    __tablename__ = "Images"
    id = database.Column(database.Integer, primary_key=True)
    dateUploaded = database.Column(database.Date, index=True, unique=True, default=datetime.utcnow)
    imageFileName = database.Column(database.String(128), index=True, unique=True)
    sizeFrom = database.Column(database.String(32), index=True, unique=True)
    sizeTo = database.Column(database.String(32))
    resizeStatus = database.Column(database.String(8), index=True, unique=False)

    def __repr__(self):
        return '<Upload date: {}>'.format(self.dateUploaded)
