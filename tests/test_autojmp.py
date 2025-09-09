import unittest
from autojmp import to_vec, corr
import math

class TestAutoJMP(unittest.TestCase):
    def test_basic_functionality(self):
        # Test the provided example
        v1 = to_vec('/Users/thaut/HomeGit/homey/process-compose')
        v2 = to_vec('/Users/thaut/.docker/cli-plugins')
        query = to_vec('compose')

        result1 = corr(v1, query)
        result2 = corr(v2, query)

        # The path with 'compose' in its name should have higher correlation
        self.assertGreater(result1, result2)

    def test_edge_cases(self):
        # Test with empty strings
        empty_vec = to_vec('')
        query_vec = to_vec('test')
        self.assertEqual(corr(empty_vec, query_vec), 0.0)

        # Test with identical strings (account for floating point precision)
        identical_vec = to_vec('test/path')
        self.assertAlmostEqual(corr(identical_vec, identical_vec), 1.0, places=10)

    def test_similarity_ranking(self):
        # Test ranking of similar paths
        path1 = to_vec('/home/user/project-compose')
        path2 = to_vec('/home/user/compose-tool')
        path3 = to_vec('/home/user/other-project')
        query = to_vec('compose')

        corr1 = corr(path1, query)
        corr2 = corr(path2, query)
        corr3 = corr(path3, query)

        # Both paths with 'compose' should have higher correlation than path without
        self.assertGreater(corr1, corr3)
        self.assertGreater(corr2, corr3)

if __name__ == '__main__':
    unittest.main()
