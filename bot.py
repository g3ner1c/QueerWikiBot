import os
import re

import fandom
import praw
from dotenv import load_dotenv

r = praw.Reddit(client_id=os.getenv('client_id'), client_secret=os.getenv('client_secret'),
                     password=os.getenv('password'), user_agent="reddit:QueerWikiBot:v0.1.0 (by u/awesomeplaya211)",
                     username="QueerWikiBot")
r.validate_on_submit = True

fandom.set_wiki('LGBTA')

# comments = r.subreddit("test").stream.comments(skip_existing = True)
comments = r.subreddit("all").stream.comments(skip_existing = True)


regex = r"https:\/\/lgbta\.fandom\.com\/wiki\/(.+?)(?:[^a-zA-Z0-9]|$)"
# finds article names on lgbta.fandom.com

for comment in comments:

    text = comment.body


    if comment.author.name != "QueerWikiBot":

        matches = re.finditer(regex, text, re.MULTILINE | re.UNICODE)
        matches_list = []

        for match in matches: # matched urls

            # print(match)
            
            for group in match.groups(): # article names

                print(group)
                matches_list.append(group)

        if bool(matches_list): # comment has article link

            print(f"{comment.author}\n{text}\n")

            matches_list = list(dict.fromkeys(matches_list)) # removes duplicates

            reply = ""

            for page_title in matches_list: # for every article linked
                
                try:

                    page = fandom.page(title=page_title).content['content']
                    summary = (f"[**{page_title}**](https://lgbta.fandom.com/wiki/{page_title})" +
                        "\n" + ">" + page.content['content'].strip().split('\n')[0] +
                        "\n\n") # summary of article
                    
                    reply += summary
                
                except fandom.error.PageError:

                    pass

            reply += "*I'm a bot still in development! Contact my* [*creator*](https://www.reddit.com/user/awesomeplaya211) *if you have feedback!*"
            comment.reply(reply)


        if 'u/QueerWikiBot' in text:
            print(f"{comment.author}\n{text}\n")
            # comment.reply('hi!')
