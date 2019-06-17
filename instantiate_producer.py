from TwitterUser import TwitterUser

tu = TwitterUser('Tommaso', 'Scarlatti')
# TODO: devo checkare che ci sia una consumer instance prima di inviare il messaggio
while True:
    message_text = input("What's happening? \t")
    tu.produce('middleware', message_text)
