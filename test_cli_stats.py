import unittest
from click.testing import CliRunner
import os
import sys
import utils

#append app folder to package:
sys.path.append('..')
from cli import cli

class StatsHabitTest(unittest.TestCase):
    
    def test_get_habits(self):
        """tests getting weekly habit list for existing user"""
        runner = CliRunner()
        result = runner.invoke(cli, ['tim', 'get-habits'])
        self.assertIn('sports 4 times a week', result.output)
        self.assertEqual(result.exit_code, 0)
    
    def test_get_weekly_habits(self):
        """tests getting weekly habit list for existing user"""
        runner = CliRunner()
        result = runner.invoke(cli, ['tim', 'get-habits', '-w'])
        self.assertIn('do charity', result.output)
        self.assertEqual(result.exit_code, 0)
    
    def test_score_charts(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['tim', 'score-charts'])
        self.assertEqual(result.exit_code, 0)
        
    def test_habit_score_charts_single(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['tim', 'habit-score-charts', '--single'], input='4')
        self.assertEqual(result.exit_code, 0)

        
    def test_monthly_scores(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['tim', 'monthly-scores'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('x', result.output)
        
   
    # def test_add_habit_new_user(self):
    #     """tests for case of correct new user"""
    #     runner = CliRunner()
    #     result = runner.invoke(cli, ['-n','inbal', 'add-habit'],  input='6')
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertIn('new user: inbal', result.output)
        
    #     os.remove('./data/inbal.json')

    
    # def test_add_habit_out_of_range(self):
    #     """tests adding habit to existing user for an unexisting habit option"""
    #     runner = CliRunner()
    #     input = 'new habit'
    #     result = runner.invoke(cli, ['tim', 'add-habit'],  input=input)
    #     self.assertNotEqual(result.exit_code, 0)
        
    # def test_track_habit(self):
    #     # this test works only for known len of updatable habits
    #     """test habit tracking for existing user"""
    #     runner = CliRunner()
    #     input = '\n'.join(['y', 'y', 'y', 'y', 'y', 'y'])
    #     result = runner.invoke(cli, ['tim', 'track-habit'], input=input)
    #     self.assertEqual(result.exit_code, 0)
        
        
if __name__ == '__main__':
    
    unittest.main()
    
