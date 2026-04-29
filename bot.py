import requests

def get_weather(city):
    return f"Погода в {city}: +20°C, ясно"

def handle_message(text):
    text = text.lower()

    if "погода" in text:
        return get_weather("Москва")
    elif "привет" in text:
        return "Привет! Я простой Telegram-бот."
    else:
        return "Не понял команду"

if __name__ == "__main__":
    while True:
        user_input = input("Вы: ")
        print("Бот:", handle_message(user_input))
