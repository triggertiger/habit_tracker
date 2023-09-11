import datetime
import time
import json
import os
import jsonpickle as jp
import matplotlib as mpl
import matplotlib.pyplot as plt
from tabulate import tabulate
import schedule


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
    
    #setting a closed list of habit examples: 
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
    
    def create_habit(self):
        """
        creates new habit.
        if habit is chosen from the list, attributes are preset. 
        for other habits name and frequency are defined.
        saves the habit in the current username's list
        """
        habit_chosen = self.get_input_new_habit()
        start_time = datetime.datetime.now().isoformat()
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
            if int(habit_chosen) == 2: 
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

        
class Habit():
    """
    sets and manages updates of habit objects
    """
    def __init__(self, habit_name, habit_frequency, start_time):
        self.habit_name = habit_name
        self.habit_frequency = habit_frequency
        self.habit_start_time = start_time
        self.habit_last_update = start_time
        self.streak = 0
        self.streaks_list = []
        self.max_streak = 0
        self.completed = False
    
    def __str__(self):
        return "Habit: name: ({})".format(self.habit_name)
   
    def track_progress(self):
        while self.completed == False:
            if self.habit_frequency == '1d':
                schedule.every(15).seconds.do(self.reminder_input_allocator)
                
            if self.habit_frequency == '1w':
                schedule.every(25).seconds.do(self.reminder_input_allocator)  
        
        
    # create a method to track the habits by user input: 
    def reminder_input_allocator(self):
        """
        prompts the user for update on the habit status and updates the attributes self.streak and streaks_list. 
        The function 
        """
           
        # message to be printed    
        reminder_msg = f'did you make it to your goal of {self.habit_name} (Y/N)?'
        
        # activation: input and update to streak/ streak list according to answer
        while True:
            answer = input(reminder_msg).lower()
                        
            # if answer yes, the streak continues
            if answer == 'y':
                self.streak += 1
                if self.streak > self.max_streak:
                    self.max_streak = self.streak
                    print(f' Great!! your longest streak so far! keep it up!\n***reminding every 15 seconds for demonstration')
                else:
                    print(f'Yey you made it again!! keep up the good work!!\n***reminding every 15 seconds for demonstration')
                break
            
            # if answer no, the streak goes to streak list and count is re-initialized            
            elif answer == 'n':
                self.streaks_list.append(self.streak)
                print(f'Great! You made a streak of {self.streak} !!\n***reminding every 15 seconds for demonstration')
                self.streak = 0
                print('streak initialized', self.streak)
                break
            else:
                print('answer y/n')
        return self 

    def complete_habit(self):
        """sets habit status to completed"""
        self.completed = True
        self.habit_last_update = datetime.datetime.now().isoformat()
        self.streak_list.append(self.streak)
        
    def analyze(self):
        """visualise habit performance"""
        fig  = plt.figure(figsize= (5, 5))
        nr_of_streaks = list(range(1,len(self.streaks_list)))
        plt.bar(nr_of_streaks, self.streaks_list, width= 0.4, color= 'maroon')
        
        plt.xlabel(self.habit_name)
        plt.ylabel('streaks duration')
        plt.title(f'habit {self.habit_name} statistics')
        plt.show()
        

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

