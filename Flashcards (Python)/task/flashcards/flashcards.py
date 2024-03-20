import io
import random
import sys

class Flashcards:
    def __init__(self):
        self.cards = {}
        self.log = io.StringIO()
        self.export_file = None
        self.import_file = None

        # Parsing command-line arguments for --import_from and --export_to options
        for arg in sys.argv[1:]:  # Skip the first argument, which is the program name itself
            if arg.startswith("--export_to="):
                self.export_file = arg.split("=")[1]
            elif arg.startswith("--import_from="):
                self.import_file = arg.split("=")[1]

        # Automatically import cards if --import_from was specified
        if self.import_file:
            self.import_cards(self.import_file)

    def log_message(self, message):
        print(message)
        self.log.write(message + '\n')

    def input_message(self, message):
        self.log_message(message)
        user_input = input()
        self.log.write(user_input + '\n')
        return user_input

    def add_card(self):
        term = self.input_message("The card:")
        while term in self.cards:
            term = self.input_message(f'The term "{term}" already exists. Try again:')
        definition = self.input_message("The definition of the card:")
        while any(definition == d['definition'] for d in self.cards.values()):
            definition = self.input_message(f'The definition "{definition}" already exists. Try again:')
        self.cards[term] = {'definition': definition, 'mistake_count': 0}
        self.log_message(f'The pair ("{term}":"{definition}") has been added.')

    def remove_card(self):
        term = self.input_message("Which card?")
        if term in self.cards:
            del self.cards[term]
            self.log_message("The card has been removed.")
        else:
            self.log_message(f'Can\'t remove "{term}": there is no such card.')

    def import_cards(self, filename=None):
        if filename is None:
            filename = self.input_message("File name:")
        try:
            with open(filename, 'r') as file:
                imported_count = 0
                for line in file:
                    term, definition, mistake_count = line.strip().split('\t')
                    self.cards[term] = {'definition': definition, 'mistake_count': int(mistake_count)}
                    imported_count += 1
                self.log_message(f"{imported_count} cards have been loaded.")
        except FileNotFoundError:
            self.log_message("File not found.")

    def export_cards(self, filename=None):
        if filename is None:
            filename = self.input_message("File name:")
        card_count = 0
        with open(filename, 'w') as file:
            for term, data in self.cards.items():
                file.write(f'{term}\t{data["definition"]}\t{data["mistake_count"]}\n')
                card_count += 1
        print(f"{card_count} cards have been saved.")

    def ask(self):
        if not self.cards:  # Check if the cards dictionary is empty
            self.log_message("No cards to ask.")
            return  # Exit the method early if there are no cards

        n = int(self.input_message("How many times to ask?"))
        for _ in range(n):
            term, data = random.choice(list(self.cards.items()))
            user_answer = self.input_message(f'Print the definition of "{term}":')
            if user_answer == data['definition']:
                self.log_message("Correct!")
            else:
                data['mistake_count'] += 1
                correct_term = [t for t, d in self.cards.items() if d['definition'] == user_answer]
                additional_info = f", but your definition is correct for \"{correct_term[0]}\" card." \
                    if correct_term else "."
                self.log_message(f'Wrong. The right answer is "{data["definition"]}"{additional_info}')

    def hardest_card(self):
        if not self.cards or all(data['mistake_count'] == 0 for data in self.cards.values()):
            self.log_message("There are no cards with errors.")
        else:
            max_mistakes = max(self.cards.values(), key=lambda x: x['mistake_count'])['mistake_count']
            hardest_cards = [term for term, data in self.cards.items() if data['mistake_count'] == max_mistakes]
            if len(hardest_cards) == 1:
                self.log_message(f'The hardest card is "{hardest_cards[0]}". '
                                 f'You have {max_mistakes} errors answering it.')
            else:
                hardest_cards_str = '", "'.join(hardest_cards)
                self.log_message(f'The hardest cards are "{hardest_cards_str}". '
                                 f'You have {max_mistakes} errors answering them.')

    def reset_stats(self):
        for data in self.cards.values():
            data['mistake_count'] = 0
        self.log_message("Card statistics have been reset.")

    def save_log(self):
        file_name = self.input_message("File name:")
        with open(file_name, 'w') as file:
            self.log.seek(0)
            file.write(self.log.read())
        self.log_message("The log has been saved.")

    def run(self):
        while True:
            action = self.input_message(
                "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
            if action == "exit":
                if self.export_file:
                    self.export_cards(self.export_file)
                self.log_message("Bye bye!")
                break
            elif action == "add":
                self.add_card()
            elif action == "remove":
                self.remove_card()
            elif action == "import":
                self.import_cards()
            elif action == "export":
                self.export_cards()
            elif action == "ask":
                self.ask()
            elif action == "log":
                self.save_log()
            elif action == "hardest card":
                self.hardest_card()
            elif action == "reset stats":
                self.reset_stats()


if __name__ == "__main__":
    app = Flashcards()
    app.run()
