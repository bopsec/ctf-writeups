import requests
import base64
import json

def send_file_to_api(file_path, api_url):
    # Read the binary file
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Base64 encode the file content
    encoded_content = base64.b64encode(file_content).decode('utf-8')

    payload = json.dumps({"input": encoded_content})

    # Set headers for JSON content type
    headers = {'Content-Type': 'application/json'}
    cookie = {'access_token': 'ACCESS TOKEN HER'}
    # Send the POST request
    response = requests.post(api_url, data=payload, headers=headers, cookies=cookie)

    return response

# File path of the modified binary file
file_path = 'modified_access16_update.bin'  # Update this path with the actual file path

# API URL
api_url = "https://mov16.cybertalent.no/app/7c77afd9-3cf9-4ba6-8596-4caf56382f81/aksess"
# Send the file
response = send_file_to_api(file_path, api_url)

# Print the response from the server
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("Response JSON:")
    print(response.json())
else:
    print("Response content:")
    print(response.content)
