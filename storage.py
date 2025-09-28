import json
import os
from typing import List, Dict, Optional

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "posts.json")

#load the json as f (read only)
def load_post() -> List[Dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

#safes the entire list of posts (write the post into the json file f
def save_posts(posts: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, encoding="utf-8")

# using the id to find a post
#trying to set the ID as a primary key into the sql database
def get_post_by_id(post_id: int) -> Optional[Dict]:
    for p in load_post():                                                          #where is load_post
        if p.get("id") == post_id:
            return p
    return None

#creating the next, highest id
def next_id(posts: List[Dict]) -> int:
    max_id = 0
    for p in load_post():
        if p.get("id") == max_id:
            if p.get("date") > max_id:
                max_id = p.get("id")
    return max_id +1


