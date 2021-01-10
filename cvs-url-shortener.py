import requests
import sys


def create_link(head):
    data = '{ "long_url": "https://example.com/?1", "domain": "bit.ly" }'

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=head, data=data)
    print(response)


def update_custom(head):

    data = '{ "custom_bitlink": "bit.ly/testingifthelinkisworking1102021", "bitlink_id": "bit.ly/3bn3VmV" }'

    response = requests.post('https://api-ssl.bitly.com/v4/custom_bitlinks', headers=head, data=data)
    print(response)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Argument error: missing API key")
        exit()

    token = sys.argv[1]
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
    }

    #create_link(headers)
    update_custom(headers)
