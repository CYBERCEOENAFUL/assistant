import json
import random
import os
from fbchat import Client
from fbchat.models import Message, ThreadType

# ... (আগের load_json ফাংশনগুলো একই থাকবে)

class EnafulBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # এনক্রিপশন চেক
        if kwargs.get('is_encrypted'):
            print(f"Encrypted message received from {author_id}")
        
        if author_id == self.uid:
            return

        # মেসেজ টেক্সট না থাকলে স্কিপ
        msg_text = message_object.text
        if not msg_text:
            return

        user_msg = str(msg_text).lower()
        dev_tag = "\n\n(developer by ENAFUL)"

        # আপনার কি-ওয়ার্ড লজিক এখানে থাকবে...
        if "hi" in user_msg or "hello" in user_msg:
            self.send(Message(text="হ্যালো! আমি বস্ এনাফুলের রোবট সহকারী।" + dev_tag), thread_id=thread_id, thread_type=thread_type)
