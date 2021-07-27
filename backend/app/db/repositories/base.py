from databases import Database

# simple class needed only to keep a reference to our database connection. In the future we can add functionality for common db actions, but we'll keep it lightweight for now
class BaseRepository:
    def __init__(self, db: Database) -> None:
        self.db = db