from datetime import datetime
from app import database


def dump_datetime(value):
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


class Images(database.Model):
    __tablename__ = "Images"
    id = database.Column(database.Integer(), primary_key=True, autoincrement=True)
    imageFileName = database.Column(database.String(128), index=True, unique=True)

    def __repr__(self):
        return f"<Image id: {self.id}, filename: {self.imageFileName} >"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "imageFileName": self.imageFileName
        }


class ProcessedImages(database.Model):
    __tablename__ = "ProcessedImages"
    id = database.Column(database.Integer(), primary_key=True)
    dateUploaded = database.Column(database.DateTime(), index=True, default=datetime.utcnow)
    imageFileName = database.Column(database.String(64), index=True, unique=True)
    sizeFrom = database.Column(database.String(32), index=True)
    sizeTo = database.Column(database.String(32))
    resizeStatus = database.Column(database.String(8), index=True)
    downloadFileURL = database.Column(database.String(128), index=True, unique=True)

    def __repr__(self):
        return f"<Id: {self.id}, date uploaded: {self.dateUploaded}, download link: {self.downloadFileURL}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "dateUploaded": dump_datetime(self.dateUploaded),
            "imageFileName": self.imageFileName,
            "sizeFrom": self.sizeFrom,
            "sizeTo": self.sizeTo,
            "resizeStatus": self.resizeStatus,
            "downloadFileURL": self.downloadFileURL
        }
