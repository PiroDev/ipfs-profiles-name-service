import ipfshttpclient
import pickle

from status_codes import StatusCode

# Path to db file (binary dict with <username>:<pubkey> key-value pairs)
db_path = "db.data"


def set_user_ipfs_link(user, link):
    db_dict = {}
    # Read dict from file
    try:
        with open(db_path, "rb") as db:
            db_dict = pickle.load(db)
    except:
        # Nothing has been saved so far
        pass
    # Update dict
    db_dict[user] = link
    with open(db_path, "wb") as db:
        pickle.dump(db_dict, db)


def get_ipfs_link_by_uid(user):
    db_dict = {}
    # Read dict from file
    try:
        with open(db_path, "rb") as db:
            db_dict = pickle.load(db)
    except:
        return None, StatusCode.ERROR_TABLE_NOT_EXISTS
    link = db_dict.get(user)
    return link, StatusCode.ERROR_NO_SUCH_USER_IN_TABLE if link is None else StatusCode.OK


def get_data_by_ipfs_link(link):
    try:
        client = ipfshttpclient.connect()
    except:
        print("Error while getting data: ipfs daemon is not running!")
        return None, StatusCode.ERROR_DAEMON_IS_NOT_RUNNING
    try:
        data = client.cat(link).decode()
    except:
        print("Error while getting data: wrong link!")
        return None, StatusCode.ERROR_WRONG_LINK
    return data, StatusCode.OK
