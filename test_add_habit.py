import unittest
from click.testing import CliRunner
import os
import sys
sys.path.append('..')
from app.cli import cli
from app.cli import stats
class ManageHabitTest(unittest.TestCase):
    
    def test_add_habit(self):
        """tests adding habit to existing user"""
        runner = CliRunner()
        result = runner.invoke(cli, ['tim', 'add-habit'],  input='6')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('not smoke', result.output)
    
    def test_delete_habit(self):
        runner = CliRunner()
        input = '\n'.join(['10', 'y'])
        result = runner.invoke(cli, ['tim', 'delete-habit'], input=input)
        #print(result.return_value)
        self.assertEqual(result.exit_code, 0)

        
    def test_add_habit_unknown_user(self):
        """test for unexisting file name"""
        runner = CliRunner()
        result = runner.invoke(cli, ['inbal', 'add-habit'],  input='6')
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn('user not found. try creating a new user', result.output)
        
   
    def test_add_habit_new_user(self):
        """tests for case of correct new user"""
        runner = CliRunner()
        result = runner.invoke(cli, ['-n','inbal', 'add-habit'],  input='6')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('new user: inbal', result.output)
        
        os.remove('./data/inbal.json')

    
    def test_add_habit_out_of_range(self):
        """tests adding habit to existing user for an unexisting habit option"""
        runner = CliRunner()
        input = 'new habit'
        result = runner.invoke(cli, ['tim', 'add-habit'],  input=input)
        self.assertNotEqual(result.exit_code, 0)
        
    def test_track_habit(self):
        # this test works only for known len of updatable habits
        """test habit tracking for existing user"""
        runner = CliRunner()
        input = '\n'.join(['y', 'y', 'y', 'y', 'y', 'y'])
        result = runner.invoke(cli, ['tim', 'track-habit'], input=input)
        print(result)
        self.assertEqual(result.exit_code, 0)
    
    def test_get_habits(self):
        """tests getting weekly habit list for existing user"""
        runner = CliRunner()
        result = runner.invoke(cli, ['-w', 'tim', 'get-habits'])
        self.assertIn('sports 4 times a week', result.output)
        self.assertEqual(result.exit_code, 0)
        
if __name__ == '__main__':
    
    unittest.main()
    
