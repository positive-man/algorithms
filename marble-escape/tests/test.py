import os
import time
import unittest

import main

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
            # 예상결과
            expected_result = testcases.get(tc)

            # 시작 시간 기록
            start_time = time.time()

            # 실행
            actual_result = main.run(tc)

            # 2초 이내에 완료되었는지 확인
            assert time.time() - start_time < 2, r'The algorithm should be done in 2 seconds.'

            # 예상 결과 및 실제 결과 비교
            assert expected_result == actual_result, \
                os.linesep.join([
                    'The actual result is not equals with the expected result.',
                    f'Expected: {str(expected_result)}',
                    f'Actual: {str(actual_result)}'
                ])

            # 잘 동작했군 !!!
            print(f'{str(number)}. PASSED: {str(actual_result)}')
            number += 1
