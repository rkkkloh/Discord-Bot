from random import choice, randint

def get_response(user_input: str) -> str: 
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'how are you' in lowered:
        return 'Good, thanks!'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll' in lowered:
        return f'You rolled {str(randint(1,6))}'
    elif 'help' in lowered:
        return "`This is a help message that you can modify.`"
    else:
        return choice(['I don\'t understand...',
                       'What are you talking about?',
                       'Do you mind rephrasing that?',
                       '我不太明白你的意思👀'])