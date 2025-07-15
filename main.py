from chatbot import WeatherChatbot

def main():
    bot = WeatherChatbot()
    print("🌦️  Weather Chatbot — how can I help you today?.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Bot: Goodbye!")
            break
        response = bot.handle_input(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()
