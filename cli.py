# system and file:
import os
import json
import jsonpickle as jp
from datetime import datetime, timedelta

#cli tool
import click
import utils
from prettytable import PrettyTable

# habit and user class:
import habit

# plots
import matplotlib.pyplot as plt   

# setting a similarly defined class for the User and Habit classes for structure availability:
class User:
    """ manages user data in a json string file"""
    def __init__(self, username):
        self.username = username
        self.user_habit_list = []
        self.filepath = f'./data/{self.username}.json'
        
        
class Habit():
    def __init__(self, habit_name, habit_frequency, start_time):
        """ class Habit creates and manages the habit objects. """
        self.habit_name = habit_name
        self.habit_frequency = habit_frequency
        self.habit_start_time = start_time
        self.habit_last_update = start_time
        self.streak = 0
        self.streaks_log = []
        self.max_streak = 0
        self.completed = False
        self.complete_date = None


# cli tool group commands
@click.group()

# create first data structure
@click.argument('username')
@click.option('-n', is_flag=True, help='create new user')
@click.pass_context
def cli(ctx, n, username):
    """Welcome to your Habit tracker!
    load data for existing users, or create new user for tracking your habits with the option -n.
    for new users: data saved only after adding first habit. Good Luck!!
    """
    # creating a new user instance 
    if n:
        path = f'./data/{username}.json'
        if os.path.exists(path):
            click.echo('user exists. Did you mean loading data without -n?')
            exit()
        else:    
            ctx.obj = habit.User(username)
            click.echo(f'new user: {ctx.obj.username}')
    
    # opening user object from file: 
    else: 
        ctx.obj = habit.set_user(username)
        click.echo(f'loading data for {ctx.obj.username}')

@cli.command()
@click.pass_context
def save_user(ctx):
    """ saves user data to a json string in a file in 'data' folder. """
    
    # create a json string encoded object: 
    json_string = jp.encode(ctx.obj)
    
    # save to file
    with click.open_file(ctx.obj.filepath, 'w') as f:
        json.dump(json_string, f, indent=4)


@cli.command()
@click.pass_context
@click.option( '-d', is_flag=True, help='see only daily habits')
@click.option( '-w', is_flag=True, help='see only weekly habits')
def get_habits(ctx, d, w):
    """ get a status for each of your habits"""
    
    habit_list = ctx.obj.user_habit_list
    if d:
        habit_list = [habit for habit in habit_list if habit.habit_frequency == '1d']
    
    if w:
        habit_list = [habit for habit in habit_list if habit.habit_frequency == '1w']
    
    # create a table version of the main kpi's for each habit
    t = PrettyTable()
    t.field_names = ['nr', 'habit name', 'start','curr. streak (days)', 'longest streak', 'completed', 'last updated']
    t.add_rows([[i+1, h.habit_name, h.habit_start_time.date(), h.streak, h.max_streak, h.completed, h.habit_last_update.date()] for i, h in enumerate(habit_list)])       
    click.echo(t)        

@cli.command()
@click.pass_context
def delete_habit(ctx):
    """delete a habit from the list"""
    ctx.invoke(get_habits)
    click.echo('choose a habit number to delete')

    # get input
    h = int(click.getchar())
    i = h - 1
    
    if click.confirm('Do you want to delete?', abort= True):
        ctx.obj.user_habit_list.pop(i)
  
    ctx.forward(get_habits)

    ctx.forward(save_user)

# add new habit to a user's list:
@cli.command()
@click.pass_context   
def add_habit(ctx):
    """
    add a habit with a daily or weekly frequency. 
    Habit is tracked automatically
    """
    # instruct user:     
    click.echo('choose an item from the list') 
    habit_options = utils.habit_options()
    option_table = utils.option_table(habit_options)
    click.echo(option_table)
    
    # get input of choice
    h = int(click.getchar())
    
    # record start time for the habit
    start_time = datetime.now()#.isoformat()
    
    # handle different choices - starting with 'other':
    if h==7:
        # get custom name
        habit_chosen = click.prompt('enter new habit name:', type=str)
        
        # get frequency (daily/weekly)    
        while True:
            answer = click.prompt(f'how often do you want to track {habit_chosen}? (D/W)', type=str).upper()
            if answer == 'D':
                freq = '1d'
                break
            elif answer == 'W':
                freq = '1w'
                break
            
            # exit if invalid
            else:
                exit()
        
        # set new habit
        new_habit = Habit(habit_chosen, freq, start_time)
    
    # set name for each of the options:
    else:
        habit_options = utils.habit_options()
        if h in range(1,7,1):
            habit_chosen = habit_options[h - 1]['name']
        # exit if invalid
        else:
            habit_chosen = 'not picked'
            exit()
        
        # create habit with the relevant attributes:
        habit_chosen = next((habit for habit in habit_options if habit['name'] == habit_chosen), None)
        new_habit = Habit(habit_chosen['name'], habit_chosen['frequency'], start_time)
    
    # add to users habits list:
    ctx.obj.user_habit_list.append(new_habit)
    
    # notification to user:
    l = len(ctx.obj.user_habit_list) - 1
    click.echo(f'habit added: {ctx.obj.user_habit_list[l].habit_name}')
    
    # display new list of habits:
    ctx.forward(get_habits)

    # save before exit: 
    ctx.forward(save_user)
      
    
@cli.command()
@click.option('-f', is_flag=True, default=False, help='change frequency 1d/1w')
@click.option('-s', is_flag=True, default=False, help='change status to completed')
@click.pass_context
def change_habit_settings(ctx, f, s):
    """
    mark habits as completed or change frequency"""
    
    # current habit list:
    ctx.invoke(get_habits)
    click.echo('choose a habit number to update')

    # get input
    habit_list = ctx.obj.user_habit_list
    h = int(click.getchar())
    i = h - 1
    
    # handle status change to completed (and back)
    if s:
        status = ctx.obj.user_habit_list[i].completed
        
        # when completed, reverse to uncompleted:
        if status:
            if click.confirm('habit marked as completed. Resume?'):
                ctx.obj.user_habit_list[i].completed = False
                ctx.obj.user_habit_list[i].complete_date = None
                click.echo('habit resumed')
            else:
                click.echo('habit completed, no update done')
        
        # if not completed, mark as completed    
        else:     
            click.echo('choose the number of habit you want to mark as completed:') 
            ctx.obj.user_habit_list[i].completed = True
            ctx.obj.user_habit_list[i].complete_date = datetime.now()
            click.echo(f'{habit_list[i].habit_name} completed!')
    
    # handle change of frequency    
    if f: 
        if click.confirm(f'{habit_list[i].habit_name} frequency is {habit_list[i].habit_frequency}. change?'):

            if habit_list[i].habit_frequency == '1d':
                ctx.obj.user_habit_list[i].habit_frequency = '1w'
            else: 
                ctx.obj.user_habit_list[i].habit_frequency = '1d'
            
            click.echo('frequency changed')
        else:
            click.echo('Invalid input - aborting without change')
    
    # save before exit
    ctx.invoke(save_user)

@cli.command()
@click.pass_context
def track_habit(ctx):
    """ update your periodical progress for each habit"""
    
    # check for each habit the las update (by frequency), and asks for the next update. 
    # #this way no tracking periods are forgotten, also if the user forgot. 
    for h in ctx.obj.user_habit_list: 
        if not h.completed:
            if h.habit_frequency == '1d':
                interval = timedelta(seconds=24)
                question_phrase = 'today'
            else:
                interval = timedelta(minutes=1)
                question_phrase = 'this week'
            
            try:
                time_from_last_update = datetime.now() - datetime.fromisoformat(h.habit_last_update)    
            except TypeError:
                time_from_last_update = datetime.now() - h.habit_last_update
            
            if time_from_last_update >= interval:
                
                answer = click.prompt(f'did you meet the goal of {h.habit_name} {question_phrase} [y/n]?').lower()
                # update current streak and check for maximal length
                if answer == 'y':
                    h.streak +=1
                    h.habit_last_update = h.habit_last_update + interval
                    click.echo(f'current streak{h.streak}')
                    if h.streak > h.max_streak:
                        h.max_streak = h.streak
                        
                # terminate streak, send to streak log and restart current count:
                elif answer == 'n':
                    click.echo(f'current streak{h.streak}')
                    streak_for_log = h.streak
                    click.echo(streak_for_log)
                    h.streaks_log.append(streak_for_log)

                    h.habit_last_update = h.habit_last_update + interval
                    click.echo(h.streaks_log)
                else:
                    click.echo('Invalid input - aborting without change')
            else:
                click.echo(f'habit {h.habit_name} is up to date')
    # save before exit
    ctx.invoke(save_user)

         
@cli.command()
@click.pass_context
@click.option( '-s', '--single', is_flag=True, help='show streak chart for a single habit')
@click.option( '--1d', 'frequency', flag_value='1d', default=True, help='daily habits presented by default')
@click.option( '--1w', 'frequency', flag_value='1w',  help='choose watching weekly habits')

def habit_score_charts(ctx, single, frequency):
    """shows performance chart for habits - default: daily"""
    #fig, (ax1, ax2) = plt.subplots(2)
    #ax1 = plt.plot()
    habits = ctx.obj.user_habit_list
    for h in habits:
        if h.habit_frequency == frequency:
            x = list(range(1, len(h.streaks_log) + 1))
            y = [streak for streak in h.streaks_log]

            click.echo(h.habit_name)
            click.echo(h.streaks_log)
            click.echo(x)
            click.echo(y)
            plt.plot(x, y, label=h.habit_name)
    plt.xlabel='number of streaks'
    plt.ylabel='streak length'
    plt.legend()
    plt.show()
        
    # chose a single habit for which to show data:    
    if single:
        ctx.invoke(get_habits)
        i = int(click.prompt('choose a habit number to watch'))
        h = ctx.obj.user_habit_list[i - 1]
        click.echo(h.streaks_log)
        bar_titles = [f'streak {i}' for i in range(1, len(h.streaks_log) + 1)]
        streak_size = [s['length'] for s in h.streaks_log]
        plt.bar(bar_titles, h.streaks_log, color= 'maroon')
        plt.xlabel('streaks')
        plt.ylabel('streaks length')
        plt.title(f'habit {h.habit_name} statistics')
        plt.show()    

if __name__ == '__main__':
   cli()