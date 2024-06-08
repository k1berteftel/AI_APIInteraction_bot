from yoomoney import Authorize

client_id = ''
client_secret = ''
token = '4100118670194784.3BED92B83D591D395C33BD9CFFAD8EA70AC3100E3B4A58D800D65A7B2DB0716ECD1762C5A17672414E06A1' #token invalid



def test_token():
    from yoomoney import Client
    client = Client(token)
    user = client.account_info()
    print("Account number:", user.account)
    print("Account balance:", user.balance)
    print("Account currency code in ISO 4217 format:", user.currency)
    print("Account status:", user.account_status)
    print("Account type:", user.account_type)
    print("Extended balance information:")
    for pair in vars(user.balance_details):
        print("\t-->", pair, ":", vars(user.balance_details).get(pair))
    print("Information about linked bank cards:")
    cards = user.cards_linked
    if len(cards) != 0:
        for card in cards:
            print(card.pan_fragment, " - ", card.type)
    else:
        print("No card is linked to the account")

test_token()
