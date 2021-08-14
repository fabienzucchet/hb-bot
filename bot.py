"""Main bot function : answers messages from the users."""

from requests import get, post

from config import client_id, client_secret, scope, username, password

# Récupération du token d'authentification
request = post('https://auth.viarezo.fr/oauth/token', headers={
    'Content-type': 'application/x-www-form-urlencoded'
}, data={
    'grant_type': 'password',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope,
    'username': username,
    'password': password,
})

token = request.json()['access_token']

url = 'https://api.linkcs.fr/v1/graphql/'
headers = {'Authorization': "Bearer {}".format(token)}

# La requête GraphQL
query = """users(limit:60) {
    firstName
    lastName
    ctiPhotoURI
    login
}"""

request = get("{url}?query={{{query}}}".format(url=url, query=query), headers=headers)
data = request.json()

print(data)
