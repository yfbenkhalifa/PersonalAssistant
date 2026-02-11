import unittest
from agents import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent()

    def test_agent_initialization(self):
        self.assertIsNotNone(self.agent)

    def test_agent_has_required_methods(self):
        self.assertTrue(hasattr(self.agent, 'run'))
        self.assertTrue(callable(getattr(self.agent, 'run')))

    def tearDown(self):
        self.agent = None


if __name__ == '__main__':
    unittest.main()