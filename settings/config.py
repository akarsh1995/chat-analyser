class IMConfig:
    HOOKS = {
        'WhatsApp': [r'^(?=\d?\d/\d\d/\d\d)'],
        'Telegram': [r"{\n \"about\": \"Here is the data you requested."]
    }
    date_strptime_fmt = '%d/%m/%y, %I:%M %p'
    date_strftime_fmt = "%A, %B %e, %Y"
    time_strftime_fmt = "%l:%M %p"
    word_regex = r'([a-zA-Z]+)'
    char_regex = r'[^\s]'


class TelegramConfig(IMConfig):
    pass