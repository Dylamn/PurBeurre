import requests

API_BASE = "http://127.0.0.1:5000/"

OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"


def test_post_category_validation_error():
    test_status = "Test {status}.  Expected: 400 | Got: {got}"

    print(WARNING + "Starting [POST] category validation test..." + ENDC)

    # This request must receive an HTTP 400 response.
    response = requests.post(API_BASE + 'categories', {
        "id": "en:none",
        # "name": "none"
    })

    status = response.status_code

    if status == 400:
        print(
            OKGREEN + test_status.format(status="Succeeded", got=status) + ENDC,
            sep='\n'
        )
    else:
        print(
            FAIL + test_status.format(status="Failure", got=status) + ENDC,
            sep='\n'
        )

    print(
        f'status : {status}', f'payload : {response.json()}',
        sep='\n'
    )


test_post_category_validation_error()
