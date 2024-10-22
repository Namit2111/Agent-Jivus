# import requests

# # Your HubSpot Private App Access Token
# access_token = 

# # API endpoint for creating a contact
# url = 'https://api.hubapi.com/crm/v3/objects/contacts'

# # Headers including the Authorization token
# headers = {
#     'Authorization': f'Bearer {access_token}',
#     'Content-Type': 'application/json'
# }

# # List of contacts to be created
# contacts = [
#     {
#         "name": "Namit Jain",
#         "phone": "+18147079186",
#         "linkedin_url": "https://www.linkedin.com/in/namit2111"
#     }
# ]

# # Function to create a contact
# def create_contact(contact):
#     data = {
#         "properties": {
#             "firstname": contact["name"],
#             "phone": contact["phone"],
#             "linkedinbio": contact["linkedin_url"]  # Using 'linkedinbio' for LinkedIn URL
#         }
#     }

#     # Make the POST request to create a contact
#     response = requests.post(url, headers=headers, json=data)

#     # Check if the request was successful
#     if response.status_code == 201:
#         print(f"Contact {contact['name']} created successfully!")
#         print("Response:", response.json())
#     else:
#         print(f"Failed to create contact {contact['name']}. Status code:", response.status_code)
#         print("Response:", response.json())

# # Loop through each contact and create them in HubSpot
# for contact in contacts:
#     create_contact(contact)


import requests

# Your HubSpot Private App Access Token
access_token =

# API endpoint for retrieving contacts
url = 'https://api.hubapi.com/crm/v3/objects/contacts'

# Headers including the Authorization token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Parameters to specify the properties to retrieve
params = {
    'properties': 'firstname,lastname,phone,linkedinbio'
}

def delete_contact(contact_id):
    durl = "https://api.hubapi.com/contacts/v1/contact/vid/{}".format(contact_id)
    r = requests.delete(url=durl, headers=headers, params=params)

    if r.status_code == 204:
        print(f"Contact {contact_id} deleted successfully!")
    else:
        print(f"Failed to delete contact {contact_id}. Status code:", r.text)
# Function to get and print contact details
def get_contacts():
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        contacts = response.json().get('results', [])

        for contact in contacts:
            print(contact)
            id = contact.get('id')

            properties = contact.get('properties', {})
            firstname = properties.get('firstname', 'N/A')
            lastname = properties.get('lastname', 'N/A')
            phone = properties.get('phone', 'N/A')
            linkedinbio = properties.get('linkedinbio', 'N/A')
            name = f"{firstname} {lastname}"

            # print(f"Name: {name}")
            # print(f"Phone: {phone}")
            # print(f"LinkedIn URL: {linkedinbio}")
            # print("-" * 40)
    else:
        print("Failed to retrieve contacts. Status code:", response.status_code)
        print("Response:", response.json())

# Retrieve and print the contact details
get_contacts()







# =------------------------------------------------------------------------------------------------------


# does not work with private apps 

# import requests

# # Your HubSpot Private App Access Token
# access_token = 

# # API endpoint for getting the current user
# url = 'https://api.hubapi.com/oauth/v1/access-tokens/

# # Headers including the Authorization token
# headers = {
#     # 'Authorization': f'Bearer {access_token}',
#     'Content-Type': 'application/json'
# }

# # Make the GET request to retrieve the logged-in user's information
# response = requests.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     user_data = response.json()
#     print(user_data)
#     # user_name = user_data.get('user', {}).get('fullName', 'N/A')
#     # print(f"Logged-in User's Email: {user_name}")
# else:
#     print("Failed to retrieve user information. Status code:", response.status_code)
#     print("Response:", response.json())
