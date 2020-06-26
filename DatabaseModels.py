from datetime import datetime
from app import database


class Images(database.Model):
    __tablename__ = "Images"
    id = database.Column(database.Integer(), primary_key=True, autoincrement=True)
    imageFileName = database.Column(database.String(128), index=True, unique=True)

    def __repr__(self):
        return f"<Image id: {self.id}, filename: {self.imageFileName} >"


class ProcessedImages(database.Model):
    __tablename__ = "ProcessedImages"
    id = database.Column(database.Integer(), primary_key=True)
    dateUploaded = database.Column(database.DateTime(), index=True, default=datetime.utcnow)
    imageFileName = database.Column(database.String(64), index=True, unique=True)
    sizeFrom = database.Column(database.String(32), index=True)
    sizeTo = database.Column(database.String(32))
    resizeStatus = database.Column(database.String(8), index=True)
    downloadFileURL = database.Column(database.String(128), index=True, unique=True)