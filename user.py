from datetime import datetime, timedelta
import json
import os
#import jsonpickle as jp
import matplotlib.pyplot as plt
from habit import Habit


class User:
    """ 
    describes the user by name and list of habits,
    and handles recording a file with the user data.
    """
    def __init__(self, username):
        self.username = username
        self.user_habit_list = []
        self.filepath = f'./data/{self.username}.json'
        
    def user_json_encode(self):
        ''' encodes the user data into json format and saves to file'''
        encoded = jp.encode(self,keys= True)
        with open(self.filepath, 'w') as f:
            json.dump(encoded, f, indent= 4)
    
    def user_json_decode(self)->json:
        """
        decodes user data from json. in case user data needs to be uploaded
        """
        with open(self.filepath, 'r') as f:
            revived_user = json.load(f, object_hook= jp.decode)
        return revived_user
    
    # setting a closed list of habit examples: 
    habit_options = [{'name': 'do charity', 'frequency': '1w'}, 
                        {'name': 'sports 4 times a week', 'frequency': '1w', 'completed': False}, 
                        {'name': 'read a book', 'frequency': '1w', 'completed': False}, 
                        {'name': 'sleep early', 'frequency': '1d', 'completed': False},
                        {'name': 'vegan day', 'frequency': '1d', 'completed': False},
                        {'name': 'not smoke', 'frequency': '1d', 'completed': False},
                        {'name': 'other', 'frequency': '1d', 'completed': False}]
    
    def get_input_new_habit(self)->dict:
        """
        prints the habits from the preset list with serialized number and prompts the user for input of choice.
        does not process the input into Habit objects. 
        """
        
        print('chose a habit from the list: \n')
        [print('(', i + 1, ') ', item['name']) for i, item in enumerate(self.habit_options)]
        habit_chosen = input()
        
        return habit_chosen
    
    def create_habit(self, start_time=None):
        """
        creates new habit.
        if habit is chosen from the list, attributes are preset. 
        for other habits name and frequency are defined.
        saves the habit in the current username's list
        """
        habit_chosen = self.get_input_new_habit()
        if start_time == None:
            start_time = datetime.now().isoformat()
        
        # get the correct frequency for the new habit: 
        if int(habit_chosen) == 7:
            habit_chosen = input('what is the habit name?' ) 
            
            while True:
                habit_freq = input('how often would you like to track (D/W)?' ) .upper()
            
                if habit_freq == 'D':
                    habit_freq = '1d'
                    break
                elif habit_freq == 'W':
                    habit_freq = '1w'
                    break
                else:
                    habit_freq = input('invalid frequency. how often would you like to track (D/W)? ')
            new_habit = Habit(habit_chosen, habit_freq, start_time)   

        else: 
            # if the habit is chosen from the list, get the full properties of the item by the habit-name: 
            if int(habit_chosen) == 1: 
                habit_chosen = 'do charity'
            elif int(habit_chosen) == 2: 
                habit_chosen = 'sports 4 times a week'
            elif int(habit_chosen) == 3: 
                habit_chosen = 'read a book'
            elif int(habit_chosen) == 4: 
                habit_chosen = 'sleep early'
            elif int(habit_chosen) == 5: 
                habit_chosen = 'vegan day'
            elif int(habit_chosen) == 6: 
                habit_chosen = 'not smoke'
            
            habit_chosen = next((habit for habit in self.habit_options if habit['name'] == habit_chosen), None)
            new_habit = Habit(habit_chosen['name'], habit_chosen['frequency'], start_time)
        self.user_habit_list.append(new_habit)    
        return new_habit

    def get_habit_status(self):
        """prints a table with summarized data of all habits"""
        data = [[h.habit_name, h.streak, h.max_streak, h.completed] for h in self.user_habit_list]
        headers = ['habit name', 'current streak', 'longest streak', 'completed']
        print(tabulate(data, headers= headers, tablefmt= 'orgtbl'))
        return data, headers

if __name__ == '__main__':
    
    def create_new_user():
        # get new name input
        username = input('enter username: ')
        new_user = User(username)
        # create a file for the new user
        try:
            data = open(new_user.filepath, 'x')
            data.close()
        # if file exist return message 
        except FileExistsError:
            print('username exists. try set_user() to load existing user')
            return  
        return new_user
    

    def set_user(username):
        """loads user data by username for existing  users"""
        path = f'./data/{username}.json'    
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                current_user = jp.loads(json.load(f))
            return current_user
        else:
            print('user not found. try creating a new user')
            return
    
    bla = create_new_user()
    starting_times = [45, 40, 35, 30, 25, 20, 12, 7, 1]
    counter = 0
    for i in starting_times:
        
        start_time = (datetime.now() - timedelta(days=i))
        bla.create_habit(start_time=start_time)
        
        print('saved data',bla.user_habit_list[counter].habit_name)
        counter += 1
    bla.user_json_encode()        
    bla_uploaded = set_user('tim')
    print(type(bla_uploaded))        
    print('uploaded data: ', bla_uploaded.user_habit_list[0].habit_name)
