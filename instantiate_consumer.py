from TwitterUser import TwitterUser
import requests
import json
from colorama import Fore, Back, Style
import keyboard

LOGIN_STRING = """
 #                                                    #    #                             #######
 #        ####   ####     # #    #    #####  ####     #   #    ##   ###### #    #   ##      #    #    # # ##### ##### ###### #####
 #       #    # #    #    # ##   #      #   #    #    #  #    #  #  #      #   #   #  #     #    #    # #   #     #   #      #    #
 #       #    # #         # # #  #      #   #    #    ###    #    # #####  ####   #    #    #    #    # #   #     #   #####  #    #
 #       #    # #  ###    # #  # #      #   #    #    #  #   ###### #      #  #   ######    #    # ## # #   #     #   #      #####
 #       #    # #    #    # #   ##      #   #    #    #   #  #    # #      #   #  #    #    #    ##  ## #   #     #   #      #   #
 #######  ####   ####     # #    #      #    ####     #    # #    # #      #    # #    #    #    #    # #   #     #   ###### #    #
"""

def login(name, surname):
    url=f"http://localhost:8082/consumers/{surname}"

    headers = {
    "Content-Type" : "application/vnd.kafka.json.v2+json"
    }

    payload = {
      "name": f"{name}",
      "format": "binary",
      "auto.offset.reset": "earliest",
      "auto.commit.enable": "true" # se metto a 'true' cancella i messaggi: va messo per il singolo consumer
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    json_data = json.loads(r.text)
    if 'error_code' in json_data:
        if json_data['error_code'] == 40902:
            print(f'Welcome back, {name}!')
    else:
        print(f"We're creating your KafkaTwitter account, {name}!")
    return TwitterUser(name, surname)

if __name__ == '__main__':
    print(f'{Fore.BLUE}{LOGIN_STRING}{Style.RESET_ALL}')
    name = input('Enter Name: ')
    surname = input('Enter Surname: ')
    tu = login(name, surname)
    tu.subscribe_to_topic('middleware')
    mode_chosen = False
    while True:
        while not mode_chosen:
            mode = input('What do you want to do? (Read | Write)  ')
            if mode not in ['Read','Write']:
                print('The only possible choices are: Read or Write.')
            else:
                mode_chosen = True

        if mode == 'Read':
            try:
                tu.get_message_streaming()
            except KeyboardInterrupt:
                print('Bye!')
                tu.delete_consumer_instance()
        elif mode == 'Write':
            try:
                tu.produce('middleware')
            except KeyboardInterrupt:
                print('Bye!')
                tu.delete_consumer_instance()
