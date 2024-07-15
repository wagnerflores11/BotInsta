from instabot import Bot
import random
import time
import os

followers_file = 'followers.txt'
following_file = 'following.txt'
output_file = 'not_following_back.txt'

username = 'username'  # Insira seu usuário do Instagram aqui
password = 'password'  # Insira sua senha do Instagram aqui

bot = Bot()

def login_with_retry():
    if not bot.api.is_logged_in:
        try:
            bot.login(username=username, password=password)
        except Exception as e:
            print(f"Error during login: {e}")
            print("Retrying login in 5 minutes...")
            time.sleep(300)  # Espera 5 minutos antes de tentar novamente
            login_with_retry()

login_with_retry()

def get_followers(profile):
    try:
        followers = bot.get_user_followers(profile)
        with open(followers_file, 'w', encoding='utf-8') as file:
            for follower in followers:
                file.write(follower + '\n')
        print(f'Data written successfully to file: {followers_file}')
    except Exception as e:
        print(f"Error fetching followers: {e}")

def get_following(profile):
    try:
        following = bot.get_user_following(profile)
        with open(following_file, 'w', encoding='utf-8') as file:
            for followed in following:
                file.write(followed + '\n')
        print(f'Data written successfully to file: {following_file}')
    except Exception as e:
        print(f"Error fetching following: {e}")

def compare_followers_and_following(followers_file, following_file):
    try:
        with open(followers_file, 'r', encoding='utf-8') as file1, open(following_file, 'r', encoding='utf-8') as file2:
            followers = set(file1.read().splitlines())
            following = set(file2.read().splitlines())

        print(f'Comparing Following with Followers...')
        differences = following.difference(followers)

        with open(output_file, 'w', encoding='utf-8') as file3:
            for line in differences:
                file3.write(line + '\n')
    except Exception as e:
        print(f"Error comparing followers and following: {e}")

def unfollow_users():
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            users = file.read().splitlines()
            for user in users[:198]:
                try:
                    bot.unfollow(user)
                    print(f'Unfollowed {user}')
                    time.sleep(random.randint(2, 5)) #tempo entre unfollow e outro
                except Exception as e:
                    print(f"Error unfollowing {user}: {e}")
                    if "429" in str(e):
                        print("Too many requests. Retrying in 10 minutes...")
                        time.sleep(600)  # Espera 10 minutos antes de tentar novamente
                    else:
                        print("Retrying in 5 minutes...")
                        time.sleep(300)  # Espera 5 minutos antes de tentar novamente
                    bot.unfollow(user)
    except FileNotFoundError:
        print(f'File {output_file} not found. Run option 3 to generate this file.')
    except Exception as e:
        print(f"Error reading {output_file}: {e}")

if __name__ == "__main__":
    while True:
        option = int(input('''
        PLEASE CHOOSE AN OPTION:

        1) --- LIST FOLLOWERS
        2) --- LIST FOLLOWING
        3) --- CHECK USERS NOT FOLLOWING BACK
        4) --- UNFOLLOW USERS
        0) --- Exit script
        '''))
        if option not in [1, 2, 3, 4, 0]:
            print('Invalid option. Please try again.')
            continue
        elif option == 0:
            break
        elif option == 1:
            get_followers(username)
        elif option == 2:
            get_following(username)
        elif option == 3:
            compare_followers_and_following(followers_file, following_file)
        elif option == 4:
            unfollow_users()
