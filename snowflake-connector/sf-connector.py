from snowflake import connector

def sf_conn(account_url, username=None, password=None):
    try:
        if username and password:
            conn = connector.connect(
                user = username,
                password = password,
                account_url = account_url
            )
        else:
            oauth_token = 'My Oauth Token'
            conn = connector.connect(
                user = username,
                authentication = 'oauth',
                token = oauth_token,
                account_url = account_url
            )
    except Exception as err:
        print("Connection errored out with: ", err)