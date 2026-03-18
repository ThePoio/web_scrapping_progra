import random

def get_random_user_agent(filepath='user-agents.txt'):
    with open(filepath, 'r', encoding='utf-8') as f:
        user_agent=[line.strip() for line in f if line.strip()]
    return random.choice(user_agent) if user_agent else None
