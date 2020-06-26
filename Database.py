from datetime import datetime
from app import database


class AllImages(database.Model):
    imageID = database.Column(database.Integer, primary_key=True)
    resizedImageLink = database.Column(database.String(120), index=True, unique=True)
    image = database.relationship("Image")

    def __repr__(self):
        return '<Link: {}>'.format(self.resizedImageLink)


class Image(database.Model):
    id = database.Column(database.Integer, database.ForeignKey("allimages.imageID"), primary_key=True)
    dateUploaded = database.Column(database.Date, index=True, unique=True, default=datetime.utcnow)
    sizeFrom = database.Column(database.String(32), index=True, unique=True)
    sizeTo = database.Column(database.String(32))
    resizeStatus = database.Column(database.String(8), index=True, unique=False)

    def __repr__(self):
        return '<Upload date: {}>'.format(self.dateUploaded)
