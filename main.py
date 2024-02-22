from storage import Database
from service import Service
from ui import UI

DATA_FILE = "dictionary.json"

def main():
    db = Database(DATA_FILE)
    service = Service(db)
    ui = UI(service)
    ui.run()


main()
