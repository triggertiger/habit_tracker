from prettytable import PrettyTable

def habit_options():
    habit_options = [{'name': 'do charity', 'frequency': '1w'}, 
                            {'name': 'sports 4 times a week', 'frequency': '1w', 'completed': False}, 
                            {'name': 'read a book', 'frequency': '1w', 'completed': False}, 
                            {'name': 'sleep early', 'frequency': '1d', 'completed': False},
                            {'name': 'vegan day', 'frequency': '1d', 'completed': False},
                            {'name': 'not smoke', 'frequency': '1d', 'completed': False},
                            {'name': 'other', 'frequency': '1d', 'completed': False}]

    return habit_options


def option_table(habit_options):
    """creates a preset list of habits for inspiration"""    

    # print in table version
    option_table = PrettyTable()
    option_table.field_names = ['option nr', 'name of habit']
    option_table.add_rows([[i+1, x['name']] for i,x in enumerate(habit_options)])
    return option_table

if __name__ == '__main__':
    
    x = habit_options()
    h = option_table(x)
    print(h)