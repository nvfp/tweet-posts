import os
import requests


def post_mastodon(text, image):
    print('INFO: Sending to Mastodon.')
    access_token = os.environ['MASTODON_ACCESS_TOKEN']

    ## Image
    with open(image, 'rb') as file:
        response = requests.post(
            'https://mastodon.social/api/v2/media',
            headers={'Authorization': f'Bearer {access_token}'},
            files={'file': file}
        )
        if response.status_code != 200:
            print(f'WARNING: image response: {response}')
            return
    media_id = response.json()['id']

    ## Text
    payload = {'status': text, 'media_ids[]': media_id}
    response = requests.post(
        'https://mastodon.social/api/v1/statuses',
        headers={'Authorization': f'Bearer {access_token}'},
        data=payload
    )
    if response.status_code != 200:
        print(f'WARNING: text response: {response}')
        return
    print('INFO: Sent.')
    # print(json.dumps(response.json(), indent=4))