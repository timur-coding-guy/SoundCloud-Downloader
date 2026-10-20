import logging
from bot.handlers import SoundcloudBot

logging.disable(logging.CRITICAL)


def main():
    bot = SoundcloudBot()
    bot.run()


if __name__ == "__main__":
    main()
