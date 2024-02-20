from storage import Dictionary
from service import Service
from ui import UI

DATA_FILE = "dictionary.csv"

def main():
    dictionary = Dictionary(DATA_FILE)
    service = Service(dictionary)
    ui = UI(service)
    ui.run()


main()
