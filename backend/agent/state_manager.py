class ConversationState:

    def __init__(self):
        self.intent = None
        self.pending_confirmation = False


state_store = {}