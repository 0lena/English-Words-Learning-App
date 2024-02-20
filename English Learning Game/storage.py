import csv

def item_from_list(l):
    if len(l) != 4:
        raise RuntimeError("invalid number of items")

    item = DictItem(l[0], l[1], l[2], l[3])
    item.validate_input()
    return item

class DictItem:

    def __init__(self, topic, word, meaning, pos):
        self.topic = topic.strip().lower()
        self.word = word.strip().lower()
        self.meaning = meaning.strip()
        self.pos = pos.strip().lower()

    def validate_input(self):
        if self.topic == "" or self.word == "" or self.meaning == "" or self.pos == "":
            raise RuntimeError("All fields are required!")


    def to_list(self):
        return [self.topic, self.word, self.meaning, self.pos]

class Dictionary:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        dict_list = []
        with open(self.filename) as csvfile:
            reader = csv.reader(csvfile)
            line = 0
            for row in reader:
                line += 1
                try:
                    dict_list.append(item_from_list(row))
                except RuntimeError as exc:
                    print(f"Error in line {line}: {exc}")
        return dict_list

    def write(self, dlist):
        with open(self.filename, "w") as csvfile:
            writer = csv.writer(csvfile)
            for item in dlist:
                writer.writerow(item.to_list())

