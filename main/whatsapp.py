from twilio.rest import Client


def send_whatsapp(to_number, message):
    client = Client()
    from_whatsapp_number = 'whatsapp:+919873966484'
    to_whatsapp_number='whatsapp:+91'+str(to_number)
    try:
        client.messages.create(body='Ahoy, world!',
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)
        return True
    except:
        return False