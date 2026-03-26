from telegram import Bot

async def get_user_id(bot_token, username_or_id):
    """Username या ID से User ID ढूंढने वाला फंक्शन"""

    # अगर आपने सीधे नंबर (ID) डाला है, तो उसे सीधे इस्तेमाल करो
    if str(username_or_id).replace('-', '').isdigit():
        return int(username_or_id)

    # अगर यूजरनेम है (@ के साथ या बिना @ के)
    username = str(username_or_id).replace('@', '').strip()
    bot = Bot(token=bot_token)

    try:
        # यह केवल तभी काम करेगा अगर बोट और यूजर एक ही ग्रुप में हों
        # और बोट वहां एडमिन हो।
        chat = await bot.get_chat(f"@{username}")
        return chat.id
    except Exception as e:
        print(f"Lookup failed for {username}: {e}")
        return None