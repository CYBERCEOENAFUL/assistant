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
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
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

        # মেসেজ না থাকলে বা টেক্সট না থাকলে স্কিপ করবে
        if not message_object.text:
            return

        user_msg = str(message_object.text).lower()
        admin_id = admin_config.get("admin_id", "100001890117053")
        dev_tag = "\n\n(developer by ENAFUL)"

        # ১. অ্যাডমিন যদি মেসেজ দেয়
        if str(author_id) == str(admin_id):
            reply = admin_config.get("admin_greeting", "আসসালামু আলাইকুম বস!")
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)
            return

        # ২. পরিচয় জানতে চাইলে
        if any(word in user_msg for word in ["কে", "identity", "who are you"]):
            reply = random.choice(identity_data['replies']) if identity_data else "আমি একজন এআই বট।"
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৩. কাজের বিষয়ে বা প্রজেক্ট নিয়ে
        elif any(word in user_msg for word in ["কাজ", "work", "project"]):
            reply = random.choice(work_data['replies']) if work_data else "কাজ চলছে..."
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৪. ফানি বা মজার কিছু চাইলে
        elif any(word in user_msg for word in ["মজা", "funny"]):
            reply = random.choice(funny_data['replies']) if funny_data else "হাহাহা!"
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৫. হট বা বোল্ড কিছু চাইলে
        elif any(word in user_msg for word in ["hot", "আগুন"]):
            reply = random.choice(hot_data['replies']) if hot_data else "🔥"
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

        # ৬. ডিফল্ট হিসেবে ফ্লার্টিং বক্স থেকে রিপ্লাই
        else:
            reply = random.choice(flirt_data['replies']) if flirt_data else "হাই!"
            self.send(Message(text=reply + dev_tag), thread_id=thread_id, thread_type=thread_type)

# ফেসবুক কুকি দিয়ে লগইন করা
try:
    with open('fb_session.json', 'r') as f:
        cookies = json.load(f)
    
    # কুকি ফরম্যাট ঠিক করা
    session_cookies = {c['key']: c['value'] for c in cookies}
    
    # আপনার রিকোয়েস্ট অনুযায়ী ইউজার এজেন্ট অ্যাডজাস্ট করা হলো
    ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    client = EnafulBot(' ', ' ', session_cookies=session_cookies, user_agent=ua)
    print("ENAFUL Bot is running successfully...")
    client.listen()
except Exception as e:
    print(f"Login failed: {e}")
