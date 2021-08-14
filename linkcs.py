"""Fetch data from LinkCS."""

from requests import get, post

from config import client_id, client_secret, scope, username, password, auth_url, linkcs_api_url


def fetch_linkcs_user(login: str):
    """Fetch LinkCS data for user with login.

    Args:
        login (str): Login of the user.

    Returns:
        json: The fetched data.

    """
    # Fetching auth token
    request = post(auth_url, headers={
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

    url = linkcs_api_url
    headers = {'Authorization': "Bearer {}".format(token)}

    # GraphQL request
    query = """user(login: "{}") {{
        firstName
        lastName
        login
        birthDate
    }}""".format(login)

    request = get("{url}?query={{{query}}}".format(url=url, query=query), headers=headers)
    data = request.json()

    return data


if __name__ == '__main__':

    login = "your_id"

    data = fetch_linkcs_user(login)

    print(data)
