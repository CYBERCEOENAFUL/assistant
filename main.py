import json
import random
import os
from fbchat import Client
from fbchat.models import Message

# আপনার জেসন ফাইলগুলো লোড করার ফাংশন
def load_json(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# ফাইলগুলো লোড করা হচ্ছে
hot_data = load_json('hot_captions.json')
funny_data = load_json('funny_replies.json')
work_data = load_json('work_examples.json')
flirt_data = load_json('flirting_box.json')
admin_config = load_json('admin_config.json')
identity_data = load_json('identity.json')

class EnafulBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # নিজের মেসেজে রিপ্লাই দেওয়া বন্ধ রাখা
        if author_id == self.uid:
            return

        user_msg = str(message_object.text).lower()
        admin_id = admin_config.get("admin_id", "100001890117053")
        dev_tag = "\n\n(developer by ENAFUL)"

        # ১. অ্যাডমিন যদি মেসেজ দেয়
        if author_id == admin_id:
            reply = admin_config.get("admin_greeting", "আসসালামু আলাইকুম বস!")
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)
            return

        # ২. পরিচয় জানতে চাইলে
        if "কে" in user_msg or "identity" in user_msg or "who are you" in user_msg:
            reply = random.choice(identity_data['replies'])
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৩. কাজের বিষয়ে বা প্রজেক্ট নিয়ে
        elif "কাজ" in user_msg or "work" in user_msg or "project" in user_msg:
            reply = random.choice(work_data['replies'])
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৪. ফানি বা মজার কিছু চাইলে
        elif "মজা" in user_msg or "funny" in user_msg:
            reply = random.choice(funny_data['replies'])
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৫. হট বা বোল্ড কিছু চাইলে
        elif "hot" in user_msg or "আগুন" in user_msg:
            reply = random.choice(hot_data['replies'])
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৬. নরমাল হাই/হ্যালো বা অন্যান্য ক্ষেত্রে ফ্লার্টিং/জেনারেল রিপ্লাই
        else:
            # ডিফল্ট হিসেবে ফ্লার্টিং বক্স থেকে রিপ্লাই দিবে
            reply = random.choice(flirt_data['replies'])
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

# ফেসবুক কুকি দিয়ে লগইন করা
try:
    with open('fb_session.json', 'r') as f:
        cookies = json.load(f)
    
    # কুকি ফরম্যাট ঠিক করা
    session_cookies = {c['key']: c['value'] for c in cookies}
    
    client = EnafulBot(' ', ' ', session_cookies=session_cookies)
    print("ENAFUL Bot is running...")
    client.listen()
except Exception as e:
    print(f"Error: {e}")
