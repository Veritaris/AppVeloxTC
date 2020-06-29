from datetime import datetime
from app import database


def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Images(database.Model):
    __tablename__ = "Images"
    id = database.Column(database.Integer(), primary_key=True, autoincrement=True)
    deleteImagePassword = database.Column(database.String(16), unique=True)

    def __repr__(self):
        return f"<Image id: {self.id}>"

    @property
    def serialize(self):
        return {
            "id": self.id
        }


class ProcessedImages(database.Model):
    __tablename__ = "ProcessedImages"
    id = database.Column(database.Integer(), primary_key=True, unique=True)
    dateUploaded = database.Column(database.DateTime(), default=datetime.utcnow)
    imageFileName = database.Column(database.String(64), unique=True)
    sizeFrom = database.Column(database.String(32))
    sizeTo = database.Column(database.String(32))
    resizeStatus = database.Column(database.String(8))

    def __repr__(self):
        return f"<Id: {self.id}, date uploaded: {self.dateUploaded}, " \
               f"download link: /static/resizedImages/{self.imageFileName}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "dateUploaded": dump_datetime(self.dateUploaded),
            "imageFileName": self.imageFileName,
            "sizeFrom": self.sizeFrom,
            "sizeTo": self.sizeTo,
            "resizeStatus": self.resizeStatus,
            "downloadFileURL": f"/static/resizedImages/{self.imageFileName}>"
        }
