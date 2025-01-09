import requests, jwt

#email = 'tim@plymouth.ac.uk'
#pwd = 'COMP2001!'


def auth(cred):
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

    # cred ={
    #     'email' : email,
    #     'password' : pwd
    # }

    response = requests.post(auth_url, json=cred)


    if response.status_code == 200:
        try:
            json_response = response.json()
            print("Authenticated successfully:", json_response)
            return json_response

        except requests.JSONDecodeError:
            print("Response is not valid JSON. Raw response content:")
            print(response.text)

    else:
        print(f"Authentication failed with status code {response.status_code}")
        return 0
    print("Response content:", response.text)
