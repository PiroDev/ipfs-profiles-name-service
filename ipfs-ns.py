# Parse command-line args
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--request-type",
    type=str,
    choices=["name-record-set", "name-record-get"],
    required=True,
)
parser.add_argument("--uid", type=str, required=True, help="<username>:<pubkey>")
parser.add_argument("--ipfs-link", type=str)
parser.add_argument("--sig", type=str)
parser.add_argument("--encoding", type=str, choices=["b64", "hex"], default="hex")

args = parser.parse_args()

print()


from status_codes import StatusCode

status_code = StatusCode.OK

from base64 import b64encode


def wrap_b64(data, encoding):
    # Base64 encoding for provided hex data
    if encoding == "hex":
        if data.startswith("0x") or data.startswith("0X"):
            data = data[2:]
        try:
            data = b64encode(bytearray.fromhex(data)).decode()
        except:
            return None, StatusCode.ERROR_WRONG_ENCODING
    return data, StatusCode.OK


def wrap_pubkey(key, encoding):
    key, status_code = wrap_b64(key, encoding)

    if status_code == StatusCode.OK and not key.startswith("-"):
        key = "-----BEGIN PUBLIC KEY-----\n" + key + "\n-----END PUBLIC KEY-----"

    return key, status_code


def parse_uid(uid):
    # Get username and public key from provided uid
    credentials = None
    status_code = StatusCode.OK
    sep_pos = uid.find(":")
    if sep_pos != -1:
        username = uid[:sep_pos]
        pubkey, status_code = wrap_pubkey(uid[sep_pos + 1 :], args.encoding)

        if status_code == StatusCode.OK:
            credentials = {
                "username": username,
                "pubkey": pubkey
            }
            args.uid = (
                credentials["username"]
                + ":"
                + wrap_b64(uid[sep_pos + 1 :], args.encoding)[0]
            )
        else:
            print("Wrong pubkey or signature encoding!")
    return credentials, status_code


if status_code == StatusCode.OK:
    credentials, status_code = parse_uid(args.uid)
    if credentials is None and status_code == StatusCode.OK:
        print("Wrong uid format!")
        status_code = StatusCode.ERROR_WRONG_UID_FORMAT

from crypto.rsa import verify_sign
from ipfs.ipfs_client import (
    get_ipfs_link_by_uid,
    get_data_by_ipfs_link,
    set_user_ipfs_link,
)

if status_code == StatusCode.OK:
    if args.request_type == "name-record-set":
        if args.ipfs_link is None:
            print("Link required!")
            status_code = StatusCode.ERROR_LINK_REQUIRED
        elif args.sig is None:
            print("Signature required!")
            status_code = StatusCode.ERROR_SIGNATURE_REQUIRED
        else:
            # Signature verification
            if verify_sign(
                args.ipfs_link, credentials["pubkey"], wrap_b64(args.sig, args.encoding)[0]
            ):
                print("result: ok (signature correct)")
                # Set ipfs link for current user
                set_user_ipfs_link(args.uid, args.ipfs_link)
            else:
                print("Signature verification failed!")
                status_code = StatusCode.ERROR_SIGNATURE_VERIFICATION_FAILED

    elif args.request_type == "name-record-get":
        # Get ipfs link from table by user id
        ipfs_link, status_code = get_ipfs_link_by_uid(args.uid)
        if status_code == status_code.OK:
            print("link:", ipfs_link)
            # Get data from IPFS by link
            data, status_code = get_data_by_ipfs_link(ipfs_link)
            if status_code == status_code.OK:
                print("data from IPFS:")
                print(data)
        else:
            print("No such user in table!")

exit(status_code)
