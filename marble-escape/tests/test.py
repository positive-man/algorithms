import main
import unittest
import os

testcases = {
    """5 5
#####
#..B#
#.#.#
#RO.#
#####""": 1,

    """7 7
#######
#...RB#
#.#####
#.....#
#####.#
#O....#
#######""": 5,

    """7 7
#######
#..R#B#
#.#####
#.....#
#####.#
#O....#
#######""": 5,

    """10 10
##########
#R#...##B#
#...#.##.#
#####.##.#
#......#.#
#.######.#
#.#....#.#
#.#.#.#..#
#...#.O#.#
##########""": -1,

    """3 7
#######
#R.O.B#
#######""": 1,

    """10 10
##########
#R#...##B#
#...#.##.#
#####.##.#
#......#.#
#.######.#
#.#....#.#
#.#.##...#
#O..#....#
##########""": 7,

    """3 10
##########
#.O....RB#
##########""": -1
}


class Tests(unittest.TestCase):
    def test(self):
        number = 1
        for tc in testcases.keys():
            expected_result = testcases.get(tc)
            actual_result = main.run(tc)

            assert expected_result == actual_result, \
                os.linesep.join([
                    'The actual result is not equals with the expected result.',
                    f'Expected: {str(expected_result)}',
                    f'Actual: {str(actual_result)}'
                ])

            print(f'{str(number)}. PASSED: {str(actual_result)}')
