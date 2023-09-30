# system and file:
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np     
import pandas as pd

#cli tool
import click
from prettytable import PrettyTable

# plots
import matplotlib.pyplot as plt   

@click.group()
def stats():
    """Manage score view functions"""

@stats.command()
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
    t.field_names = ['nr', 
                     'habit name', 
                     'start','curr. streak (days)',
                     'longest streak', 
                     'completed', 
                     'last updated']
    t.add_rows([[i+1, 
                 h.habit_name, 
                 h.habit_start_time.date(),
                 h.streak, 
                 h.max_streak, 
                 h.completed, 
                 h.habit_last_update.date()] 
                    for i, h in enumerate(habit_list)])       
    click.echo(t) 

@stats.command()
@click.pass_context
@click.option( '-s', '--single', is_flag=True, help='show streak chart for a single habit')
@click.option( '-d', 'frequency', flag_value='1d', default=True, help='daily habits presented by default')
@click.option( '-w', 'frequency', flag_value='1w',  help='choose watching weekly habits')

def score_charts(ctx, single, frequency):
    """shows performance chart for habits - default: daily"""
    fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8))
    habits = ctx.obj.user_habit_list
    if frequency == '1d':
        headline = 'daily'
    else:
        headline = 'weekly'
    x2 = []
    y2_ticks = []
    for h in habits:
        
        if h.habit_frequency == frequency:
            x1 = list(range(1, len(h.info.log) + 1))
            y1 = [streak for streak in h.info.log]
            ax1.plot(x1, y1, label=h.habit_name)
            
            success_rate = h.info.success_period / h.info.total_period * 100
            x2.append(int(success_rate))
            y2_ticks.append(h.habit_name)
            
    ax1.set(xlabel='number of streaks')
    ax1.set(ylabel='streak length')
    ax1.legend()
    
    y2 = list(range(1, len(x2) + 1))
    ax2.barh(y2, x2, align='center')
    ax2.set_yticks(y2, labels= y2_ticks)
    ax2.set_xlabel('Performance (%)')
    plt.suptitle(f'your {headline} habit results')
    plt.show()
        
    # chose a single habit for which to show data:    
    if single:
        ctx.invoke(get_habits)
        i = int(click.prompt('choose a habit number to watch'))
        h = ctx.obj.user_habit_list[i - 1]
        click.echo(h.info.log)
        bar_titles = [f'streak {i}' for i in range(1, len(h.info.log) + 1)]
        fig = plt.figure(figsize=(10, 4))
        plt.bar(bar_titles, h.info.log, color= 'maroon')
        plt.xlabel('streaks')
        plt.ylabel('streaks length')
        plt.title(f'habit {h.habit_name} streaks')
        plt.show()    

@stats.command()
@click.pass_context
def monthly_scores(ctx):
    """check last month performance: x- success"""
    today = datetime.today().date()
    last_month = today - relativedelta(months=+1)
    month_days = np.arange(today, last_month, relativedelta(days=-1)).tolist()
    month_days = list(map(lambda x: x.date(), month_days))
    df = pd.DataFrame({'date': month_days})

    for i, h in enumerate(ctx.obj.user_habit_list):
        
        last_updated = h.habit_last_update.date()
        
        if h.completed:
            print('marked as completed')
            if h.info.days_from_completion < len(month_days) or h.info.days_from_completion is None:
                h.info.days_from_completion = today - h.complete_date.date()
                last_updated = h.info.days_from_completion

        try:
            print('last update', last_updated)
            start_index = df.index[df['date'] == last_updated].tolist()[0]
        except IndexError:
            print('index error excepted')
            continue
        
        # collecting streaks and counting them sorted backwards: 
        streaks = h.info.log + [h.streak]
        # convert weekly streaks to days 
        if h.habit_frequency == '1w':
            weekly_daily = []
            for s in streaks:
                if s == 0:
                    weekly_daily.extend([0] * 7)
                else:
                    weekly_daily.append(s * 7)
            streaks = weekly_daily
            
        streaks.reverse()
        
        # converting results to user-friendly view
        scores_list = []
        scores_list += start_index * ['--']
        
        for s in streaks:
            if s == 0:
                scores_list += ['_']
                    
            # limiting the list to length of one month:
            else:
                remaining_size = df.shape[0] - len(scores_list)
                if remaining_size > s:
                    scores_list += s * ['x']
                else:
                    scores_list += remaining_size * ['x']
                
            if len(scores_list) >= df.shape[0]:
                break

        if len(scores_list) < df.shape[0]:
            remaining_size = df.shape[0] - len(scores_list)
            scores_list += remaining_size * ["--"]
        
        df[h.habit_name] = scores_list
    
    click.echo(df) 
    
    
