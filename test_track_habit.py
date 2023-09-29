import unittest
from click.testing import CliRunner
import os
import sys
sys.path.append('..')
from app.cli import cli
        
def test_track_habit():
    # this test works only for known len of updatable habits
    """test habit tracking for existing user"""
    runner = CliRunner()
    input = '\n'.join(['y', 'y', 'y', 'y', 'y', 'y'])
    result = runner.invoke(cli, ['tim', 'track-habit'], input=input)
    print(result)
    assert(result.exit_code==0)
        
if __name__ == '__main__':
    
    test_track_habit()
    
