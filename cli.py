# system and file:
import os
import json
import jsonpickle as jp
from datetime import datetime, timedelta

#cli tool
import click
import utils
import stats

# habit and user class:
from user import User 
from habit import Habit
from streak import Streak

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
    # new user instance 
    if n:
        path = f'./data/{username}.json'
        if os.path.exists(path):
            click.echo('user exists. Did you mean loading data without -n?')
            exit()
        else:    
            ctx.obj = User(username)
            click.echo(f'new user: {ctx.obj.username}')
            
    # opening user object from file: 
    else: 
        path = f'./data/{username}.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                current_user = jp.loads(json.load(f))
            ctx.obj = current_user
            click.echo(f'loading data for {ctx.obj.username}')
        else:
            click.echo('user not found. try creating a new user')

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
def add_habit(ctx):
    """
    add a habit with a daily or weekly frequency. 
    """
    # instruct user:     
    click.echo('choose an item from the list') 
    habit_options = utils.habit_options()
    option_table = utils.option_table(habit_options)
    click.echo(option_table)
    
    # get input of choice
    h = int(click.getchar())
    
    # record start time for the habit
    start_time = datetime.now()
    
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
    ctx.forward(stats.get_habits)
    ctx.forward(save_user)
    
@cli.command()
@click.pass_context
def delete_habit(ctx):
    """delete a habit from the list"""
    ctx.invoke(stats.get_habits)

    # get input
    h = click.prompt('choose a habit number to delete', type= int)
    i = h - 1
    
    # safety question before deleting:
    if click.confirm('Do you want to delete?', abort= True):
        ctx.obj.user_habit_list.pop(i)
    
    # display habit list after change and save to file: 
    ctx.forward(stats.get_habits)
    ctx.forward(save_user)

@cli.command()
@click.option('-f', is_flag=True, default=False, help='change frequency 1d/1w')
@click.option('-s', is_flag=True, default=False, help='change status to completed')
@click.pass_context
def change_habit_settings(ctx, f, s):
    """mark habits as completed or change frequency"""
    
    # current habit list:
    ctx.invoke(stats.get_habits)
    click.echo('choose a habit number to update')

    # get input
    habit_list = ctx.obj.user_habit_list
    h = click.echo('choose a habit number to update', type=int)
    i = h - 1
    
    # handle status change to completed (and back)
    if s:
        status = ctx.obj.user_habit_list[i].completed
        
        # when completed, reverse to uncompleted:
        if status:
            click.echo('habit already marked as completed. Start a new habit instead')
            
        # if not completed, mark as completed    
        else:     
            click.echo('Choose the number of habit you want to mark as completed:') 
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
    ctx.invoke(save_user)

@cli.command()
@click.pass_context
def track_habit(ctx):
    """ update your periodical progress for each habit"""
    
    # check for each habit the last update (by frequency), and asks for the next update. 
    for h in ctx.obj.user_habit_list: 
        if not h.completed:
            if h.habit_frequency == '1d':
                interval = timedelta(days=1)
                #update_interval = timedelta(seconds=24)
                question_phrase = 'today'
            else:
                interval = timedelta(weeks=1)
                #update_interval = timedelta(seconds=24)
                question_phrase = 'this week'
            
            try:
                time_from_last_update = datetime.now() - datetime.fromisoformat(h.habit_last_update)    
            except TypeError:
                time_from_last_update = datetime.now() - h.habit_last_update
            
            if time_from_last_update >= interval:
                answer = click.prompt(f'did you meet the goal of {h.habit_name} {question_phrase} [y/n]?').lower()
                h.info.total_period += 1
                # update current streak and check for maximal length
                if answer == 'y':
                    h.streak += 1
                    h.info.success_period += 1
                    h.habit_last_update = h.habit_last_update + interval
                    click.echo(f'current streak: {h.streak}')
                    if h.streak > h.max_streak:
                        h.max_streak = h.streak
                        
                # terminate streak, send to streak log and restart current count:
                elif answer == 'n':
                    click.echo(f'you managed a streak of: {h.streak}!')
                    h.info.log.append(h.streak)
                    h.streak = 0
                    h.habit_last_update = h.habit_last_update + interval
                    
                else:
                    click.echo('Invalid input - aborting without change')
            else:
                click.echo(f'habit {h.habit_name} is up to date')
    ctx.invoke(save_user)
         
cli.add_command(stats.get_habits)
cli.add_command(stats.score_charts)
cli.add_command(stats.monthly_scores)


if __name__ == '__main__':
   cli()
