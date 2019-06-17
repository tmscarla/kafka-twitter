from TwitterUser import TwitterUser
import requests
import json
from colorama import Fore, Back, Style
from KafkaTwitter import KafkaTwitter

if __name__ == '__main__':
    app = KafkaTwitter()
    app.mainloop()
