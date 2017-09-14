import Jusibe
import dotenv

dotenv.load()

public_key = dotenv.get('JUSIBE_PUBLIC_KEY')
access_token = dotenv.get('JUSIBE_ACCESS_TOKEN')
jusibe = Jusibe(public_key, access_token)

def send_sms(phone_number, message):
	response = jusibe.send_message(phone_number 'TEST APPLICATION', message)
