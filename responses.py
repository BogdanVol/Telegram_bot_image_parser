from datetime import datetime


def sample_responses(input_text):
    user_massage = str(input_text).lower()

    if user_massage in ('hello', 'hi'):
        return "hello"

    if user_massage in "time":
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M:%S")

        return str(date_time)

    return "I don`t understand you. Give me your photo"
