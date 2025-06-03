
class NotifierContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def notify(self, subject, message, recipient):
        self.strategy.send(subject, message, recipient)
