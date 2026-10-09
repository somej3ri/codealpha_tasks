import random

WORDS = ["python", "guitar", "planet", "rocket", "puzzle"]
MAX_WRONG = 6

HANGMAN_PICS = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """
]


def show_state(word, guessed, wrong):
    """Print the gallows, the masked word, and the letters guessed so far."""
    print(HANGMAN_PICS[wrong])

    display = " ".join(letter if letter in guessed else "_" for letter in word)
    print(f"Word:  {display}")
    print(f"Lives: {MAX_WRONG - wrong} left")

    missed = sorted(l for l in guessed if l not in word)
    if missed:
        print("Missed letters: " + ", ".join(missed))
    print()


def is_solved(word, guessed):
    return all(letter in guessed for letter in word)


def play():
    word = random.choice(WORDS)
    guessed = set()
    wrong = 0

    print("\n=== HANGMAN ===")

    while True:
        show_state(word, guessed, wrong)

        if is_solved(word, guessed):
            print(f"You win! The word was '{word}'. 🎉")
            break
        if wrong >= MAX_WRONG:
            print(f"Out of guesses! The word was '{word}'.")
            break

        guess = input("Guess a letter: ").lower().strip()

        # validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (a-z).\n")
            continue
        if guess in guessed:
            print(f"You already guessed '{guess}'. Try a different letter.\n")
            continue

        # process the guess
        guessed.add(guess)
        if guess in word:
            print(f"Good! '{guess}' is in the word.\n")
        else:
            wrong += 1
            print(f"Sorry, '{guess}' is not in the word.\n")


def main():
    while True:
        play()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()