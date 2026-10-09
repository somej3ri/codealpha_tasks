def get_response(message):
    """Return a predefined reply based on the user's message."""
    if message in ("hello", "hi", "hey"):
        return "Hi!"
    elif message == "how are you":
        return "I'm fine, thanks!"
    elif message in ("bye", "goodbye", "exit", "quit"):
        return "Goodbye!"
    else:
        return "Sorry, I don't understand that."


def chat():
    print("Chatbot: Hi! Type 'bye' to end the chat.")
    while True:
        user_input = input("You: ").strip().lower()   # normalise input
        reply = get_response(user_input)              # decide the reply
        print("Chatbot:", reply)
        if user_input in ("bye", "goodbye", "exit", "quit"):
            break                                     # leave the loop


if __name__ == "__main__":
    chat()