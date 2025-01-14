import requests
import json

# Load the configuration from the external file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract the API key and URL from the config
api_key = config['api_key']
url = config['url']

# Update headers with the authorization token
headers = config['headers']
headers['Authorization'] = f"Bearer {api_key}"

# Extract the desired filename from the config
filename = config['filename']

# Extract the payload from the config
payload = config['payload']

# Send a POST request to the OpenAI API
response = requests.post(url, headers=headers, 
 data=json.dumps(payload))

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()

    # Iterate over the generated images and save them
    for i, image_info in enumerate(data['data']):
        image_url = image_info['url']
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            # Save the image with the desired filename and index
            image_filename = f"{filename}{i + 1}.png"
            with open(image_filename, 'wb') as img_file:
                img_file.write(image_response.content)
            print(f"Image saved as {image_filename}")
        else:
            print(f"Failed to download image {i + 1}: {image_response.status_code} {image_response.content}")
else:
    print(f"Failed to generate image: {response.status_code}")
    print(response.text)

