import json

class DictItem:

    def __init__(self, topic, word, meaning, pos):
        self.topic = topic.strip().lower()
        self.word = word.strip().lower()
        self.meaning = meaning.strip()
        self.pos = pos.strip().lower()

    def validate_input(self):
        if self.topic == "" or self.word == "" or self.meaning == "" or self.pos == "":
            raise RuntimeError("All fields are required!")

#Creates and returns an instance of DictItem using data from a dictionary d
def item_from_dict(d):
    return DictItem(d["topic"], d["word"], d["meaning"], d["pos"])

# Converts an instance of DictItem back into a dictionary
def item_to_dict(item):
    return {
        "topic": item.topic,
        "word": item.word,
        "meaning": item.meaning,
        "pos": item.pos,
    }

class Database:
    def __init__(self, filename):
        self._filename = filename
        self._data = {}
        self._load()

# Opens and reads the database file, loading JSON data into _data
    def _load(self):
        try:
            with open(self._filename) as file:
                self._data = json.loads(file.read())
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            print(f"Error: failed to load data file {self._filename}: {exc}")

    #Converts _data to a JSON string and writes it to the file
    def _save(self):
        data = json.dumps(self._data, indent=2)
        with open(self._filename, "w") as file:
            file.write(data)

    # Retrieves the data by a username
    def get_user(self, username):
        return self._data.setdefault(username, {
            "settings": {
                "goal": 0
            },
            "dictionary": {}
        })

    # Retrieves the settings for a given username
    def get_settings(self, username):
        return self.get_user(username).get("settings")

    # Updates the settings for a given username, saves the updated data to the file
    def update_settings(self, username, settings):
        self.get_user(username)["settings"] = settings
        self._save()

    # Gets dictionary of specific user
    def get_dictionary(self, username):
        return self.get_user(username).setdefault("dictionary", {})

    #
    def get_topic_names(self, username):
        return self.get_dictionary(username).keys()

    def get_topic(self, username, topic):
        return self.get_dictionary(username).setdefault(topic, [])

    # Retrieves all words as DictItem instances under a specific topic for a given username
    def get_words(self, username, topic):
        result = []
        for word in self.get_topic(username, topic):
            result.append(item_from_dict(word))
        return result

    # Adds a new unique word to a topic in a user's dictionary
    def add_new_word(self, username, item):
        topic = self.get_topic(username, item.topic)
        for word in topic:
            if word["word"] == item.word:
                raise RuntimeError(f'Word "{item.word}" already exists')
        topic.append(item_to_dict(item))
        self._save()

