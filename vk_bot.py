import logging
import random
from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import detect_intent_texts

logger = logging.getLogger(__name__)


def send_message(user_id, text, vk_api):
    try:
        vk_api.messages.send(
            user_id=user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )
    except Exception as e:
        logger.error(e)


def main():
    env = Env()
    env.read_env()
    vk_token = env('VK_TOKEN')
    project_id = env('PROJECT_ID')
    try:
        vk_session = vk.VkApi(token=vk_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                session_id = f'vk-{event.user_id}'
                text = detect_intent_texts(session_id, event.text, project_id)
                if not text:
                    logger.info('Unclear question')
                else:
                    send_message(event.user_id, text, vk_api)

    except Exception as e:
        logger.error(e, exc_info=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    main()
