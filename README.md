# IPFS profiles name-service

The program implements name-service for creating user profiles in IPFS. This is a service where "name" is a combination of "user_name + user_public_key (from RSA key pair)" and the response to provided name is an IPFS link to the user data. A user holding a secret key from his RSA pair can update the IPFS link to his profile by sending an update request to the service by signing the new link with his secret key. 

## Installation
>Program requires python3

### Install IPFS client:
>Program supports go-ipfs client up to 0.7.0 version

On Ubuntu:
```
$ sudo apt-get update
$ sudo apt-get install golang-go -y
$ wget https://dist.ipfs.io/go-ipfs/v0.7.0/go-ipfs_v0.7.0_linux-386.tar.gz
$ tar xvfz go-ipfs_v0.7.0_linux-386.tar.gz
$ sudo mv go-ipfs/ipfs /usr/local/bin/ipfs
```

On Arch:
```
$ sudo pacman -S go-ipfs
```

### Add your file to IPFS

Init and run ipfs daemon:

```
$ ipfs init
$ ipfs daemon
```

Add your file to ipfs (for examlple profile.txt):
```
$ ipfs add profile.txt
```

Copy recieved link.

### Install python dependencies

`$ pip3 install -r requirements.txt`

## Usage

>Program supports **hex** and **base64** encoding for public RSA key and signature (hex is default)

### Update or set profile link:

```
$ python3 ipfs-ns.py --request-type=name-record-set --uid=<name>:<pubkey> --ipfs-link=<ipfs_link> --sig=<signed_link> [--encoding=b64]
```

Example input:
```
$ python3 ipfs-ns.py --request-type=name-record-set --uid=pirodev:MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsKcek7fguXqyHNWzK3ekwN9nC9ziMvhTqtFMAjm0qCcVScCXbOireD5KqfmgFkd3TQmziKVL5GjWWTZwEZUasyjmYiNsprY3gXX6gNOLKH1LOh3u+0XPfY+ZFS+7th2vu42oCkqQ4Jvugi9+cpH2EVZQZW+GUakPEneZoaLrpMQIDAQAB --ipfs-link=QmXR5eHHSuy43fahbyaFiiVBZKMgr9pSiVC8GmLf6zJHBw --sig=Vvty7LQMJtPvRLLBGnVPkzTn2VkHDxF7BjnpCj3Y9PV3UeC5oBiXVp3FuNDUIuhkd83yLrNev8Ma0pZ7I4ljQP+fSgk7Ul/pNpL+tKhBdgNCV8cnkvwPO0st8R0Vrp4BpeUT8VlAvlREZz0lCY3VGBqBMTeoFnAsV+pTw72SAMg= --encoding=b64
```

Example output:
```
result: ok (signature correct)
```

### Get profile data from IPFS

```
$ python3 ipfs-ns.py --request-type=name-record-get --uid=<name>:<pubkey> [--encoding=b64]
```

Example input:
```
$ python3 ipfs-ns.py --request-type=name-record-get --uid=pirodev:0x30819f300d06092a864886f70d010101050003818d0030818902818100ac29c7a4edf82e5eac87356ccadde93037d9c2f7388cbe14eab453008e6d2a09c5527025db3a2ade0f92aa7e680591ddd3426ce22952f91a35964d9c046546acca399888db29ad8de05d7ea034e2ca1f52ce877bbed173df63e6454beeed876beee36a0292a43826fba08bdf9ca47d845594195be1946a43c49de66868bae9310203010001 --encoding=hex
```

Example output:
```
link: QmXR5eHHSuy43fahbyaFiiVBZKMgr9pSiVC8GmLf6zJHBw
data from IPFS:
Name: PiroDev
Birthdate: ???
```