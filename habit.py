from datetime import datetime, timedelta
import json
import os
#import jsonpickle as jp
import matplotlib.pyplot as plt
import schedule
from streak import Streak

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
        self.max_streak = 0
        self.info = Streak()
        self.completed = False
        self.complete_date = None
    
    def __str__(self):
        return "Habit: name: ({})".format(self.habit_name)
   
    def track_progress(self):
        while self.completed == False:
            if self.habit_frequency == '1d':
                schedule.every(15).seconds.do(self.reminder_input_allocator)
                               
            else:
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
            self.stats.total_period += 1
            answer = input(reminder_msg).lower()
                        
            # if answer yes, the streak continues
            if answer == 'y':
                self.streak += 1
                self.stats.success_period += 1
                if self.streak > self.max_streak:
                    self.max_streak = self.streak
                    print(f' Great!! your longest streak so far! keep it up!\n***reminding every 15 seconds for demonstration')
                else:
                    print(f'Yey you made it again!! keep up the good work!!\n***reminding every 15 seconds for demonstration')
                break
            
            # if answer no, the streak goes to streak list and count is re-initialized            
            elif answer == 'n':
                self.stats.log.append(self.streak)
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
        self.habit_last_update = datetime.now().isoformat()
        self.stats.log.append(self.streak)
        
    def analyze(self):
        """visualise habit performance"""
        fig  = plt.figure(figsize= (5, 5))
        nr_of_streaks = list(range(1,len(self.stats.log)))
        plt.bar(nr_of_streaks, self.stats.log, width= 0.4, color= 'maroon')
        
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


