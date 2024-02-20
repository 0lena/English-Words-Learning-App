from storage import *

class Service:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def add_new_word(self, topic, word, meaning, pos):
        new_item = DictItem(topic=topic, word=word, meaning=meaning, pos=pos)
        new_item.validate_input()

        # Storage instance to write this new word to the file
        items = self.dictionary.read()
        for item in items:
            if item.word == new_item.word:
                raise RuntimeError(f"Word {item.word} already exists")
        items.append(new_item)
        self.dictionary.write(items)


    def get_sorted_topics(self):
        topics = set()
        for word in self.dictionary.read():
            topics.add(word.topic)
        return list(sorted(topics))

    # Filter words by specific topic
    def get_words_by_topic(self, topic):
        items = self.dictionary.read()
        words_by_topic = [] # DictItem objects sorted by chosen topic
        for item in items:
            if item.topic == topic:
                words_by_topic.append(item)
        return words_by_topic

