from requests import get
import click
import json
import sys
from typing import List, Dict


@click.command()
@click.argument('user')
def fetch_github_user(user):
    url = f'https://api.github.com/users/{user}/events'
    headers = {
        "User-Agent" : "python requests"
    }

    hasil = get(url, headers=headers)
    try:
        # ok
        if hasil.status_code == 200:
            data = hasil.json()
            if not data:
                print("data kosong")
                sys.exit(1)

            display(data)
        # 404
        elif hasil.status_code == 404:
            print(f"user ini {user} ga ditemukan")
            sys.exit(1)
        else:
            print(f"error fetching : {hasil.status_code}")
            sys.exit(1)
    except Exception as e :
        print(f"error : {e}")
        sys.exit(1)

# autocomplete
def display(events: List[Dict]):

    if not events:
        print("no activity found")
        return

    # loop data starred
    for event in events:

        # type
        event_type = event.get('type')
        # gunakan data ini jika kosong
        repo_name = event.get('repo',{}).get('name','unknown repo')
        payload = event.get('payload',{})

        # cek event type
        match event_type:

            # case on type

            case "PushEvent":
                # default kosong
                commit_count = len(payload.get('commits',[]))
                print(f"🫸 Pushed : {commit_count} commit(s) to {repo_name}")
            case "WatchEvent":
                print(f"⭐ starred : {repo_name}")
            case "ForkEvent":
                print(f"🍴 Forked : {repo_name}")
            case "CreateEvent":
                ref_type = payload.get("ref_type","something")
                print(f"🛠️ created {ref_type} in {repo_name}")
            case _:
                print(f"👁️‍🗨️ {event_type} in {repo_name}")




if __name__ == '__main__':
    event = fetch_github_user()