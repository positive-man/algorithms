from __future__ import annotations

WALL = '#'
HOLE = 'O'
RED_BALL = 'R'
BLUE_BALL = 'B'
BALLS = [RED_BALL, BLUE_BALL]
EMPTY = '.'

ALL_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

ATTEMPT_LIMIT = 10


def __combine(paths):
    """
    입력된 경로에 다음 이동시킬 위치를 조합하여 반환한다.
    """
    result = []
    for path in paths:
        latest = path[-1]
        if latest[0]:
            # 직전 시도에서 x-축으로 기울임. 다음번 시도는 y-축으로 기울임
            for d in [d for d in ALL_DIRECTIONS if d[0] == 0]:
                result.append(path + [d])
        else:
            # 직전 시도에서 y-축으로 기울임. 다음번 시도는 x-축으로 기울임
            for d in [d for d in ALL_DIRECTIONS if d[0] != 0]:
                result.append(path + [d])

    return result


# 경로 생성
PATHS = [[direction] for direction in ALL_DIRECTIONS]
for i in range(ATTEMPT_LIMIT - 1):
    PATHS = __combine(PATHS)


class Location:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_x = self.x
        self.prev_y = self.y

    def equals(self, x, y):
        """
        주어진 위치와 동일한지 비교하고, 동일하면 True, 그렇지 않으면 False 를 반환한다.
        """
        return x == self.x and y == self.y


class Ball(Location):
    def __init__(self, x, y, game: Game):
        super().__init__(x, y)
        self.__start_x = x
        self.__start_y = y
        self.game = game

    def roll(self, dir_x, dir_y):
        """
        주어진 방향으로 공을 굴린다.
        """
        while True:
            self.__move(dir_x, dir_y)

            if self.game.get(self) == HOLE:
                # 구멍을 만나면, 멈춘다
                break
            elif self.game.red_ball.equals(self.game.blu_ball.x, self.game.blu_ball.y):
                # 다른 공을 만나면, 멈춘다
                self.__undo()
                break
            elif self.game.get(self) == EMPTY:
                # 빈 공간이면, 계속 굴러간다
                continue
            elif self.game.get(self) == WALL:
                # 벽을 만나면, 멈춘다
                self.__undo()
                break
            else:
                raise RuntimeError('Not supported character: ' + self.game.get(self))

    def reset(self):
        """
        시작 위치로 되돌린다.
        """
        self.x = self.__start_x
        self.y = self.__start_y

    def __move(self, x, y):
        """
        주어진 값만큼 위치를 이동시킨다.
        """

        # 직전 위치 기억
        self.prev_x = self.x
        self.prev_y = self.y

        # 위치 갱신
        self.x += x
        self.y += y

    def __undo(self):
        """
        움직이기 이전 위치로 돌아간다.
        """
        self.x = self.prev_x
        self.y = self.prev_y


class Game:

    def __init__(self, map_str: str):
        rows = map_str.split('\n')
        self.map = [[_ for _ in row] for row in rows[1:]]

        loc_red_ball = self.__find(RED_BALL)
        loc_blu_ball = self.__find(BLUE_BALL)

        self.red_ball = Ball(loc_red_ball.x, loc_red_ball.y, self)
        self.blu_ball = Ball(loc_blu_ball.x, loc_blu_ball.y, self)

        # 맵에서 공을 지운다
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                loc = Location(x, y)
                if self.get(loc) in BALLS:
                    self.__set(loc, EMPTY)

    def run(self) -> int:
        """
        게임을 실행한다.
        :return: 빨간공을 구멍에 넣을 수 있는 최소 횟 수, 10회 이내에 성공할 수 없는 경우에는 -1
        """

        # 성공한 경로 중 최소 시도 횟수
        success_min_count = None
        for path in PATHS:
            self.__reset()
            count = 0

            for direction in path:
                # 시도 횟수를 증가시킨다
                count += 1

                if success_min_count and count >= success_min_count:
                    # 성공한 적이 있고, 현재 시도 횟수가 최소 성공 횟수 보다 크거나 같으면, 더 이상 진행하지 않음
                    break

                # 기울이기 전 공들의 위치를 기억해두자
                mem = self.red_ball.x, self.red_ball.y, self.blu_ball.x, self.blu_ball.y

                # 기울인다
                self.__tilt(*direction)

                if mem == (self.red_ball.x, self.red_ball.y, self.blu_ball.x, self.blu_ball.y):
                    # 기울이기 전/후 공들의 위치가 동일하다면, 더이상 진행하지 않는다
                    break

                if self._is_hole(self.red_ball):
                    # 빨간공이 구멍에 들어갔다면,
                    if self._is_hole(self.blu_ball):
                        # 파란공도 구멍에 들어갔다면, 더 이상 진행하지 않는다
                        break
                    else:
                        # 파란공이 구멍에 들어가지 않았다면,
                        success_min_count = count

        return success_min_count if success_min_count else -1

    def get(self, loc: Location) -> str:
        """
        해당 로케이션에 무엇이 있는지 반환한다.
        """
        return self.map[loc.y][loc.x]

    def __print_map(self):
        """
        맵을 출력한다
        """
        print()
        for y in range(len(self.map)):
            row = []
            for x in range(len(self.map[y])):
                if self.red_ball.equals(x, y):
                    row.append(RED_BALL + HOLE if self._is_hole(Location(x, y)) else RED_BALL)
                elif self.blu_ball.equals(x, y):
                    row.append(BLUE_BALL + HOLE if self._is_hole(Location(x, y)) else BLUE_BALL)
                else:
                    row.append(self.map[y][x])
            print(row)

    def __set(self, loc: Location, c):
        """
        위치에 문자 설정한다
        """
        self.map[loc.y][loc.x] = c

    def __find(self, target) -> Location:
        """
        해당 문자를 찾는다.
        """
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if target == self.map[y][x]:
                    return Location(x, y)

        raise RuntimeError('Can not find the target: ' + target)

    # noinspection PyAttributeOutsideInit
    def __reset(self):
        """
        공들을 최초 위치에 놓는다.
        """
        self.red_ball.reset()
        self.blu_ball.reset()

    def __tilt(self, dir_x, dir_y):
        """
        보드를 기울인다.
        """
        balls = [self.red_ball, self.blu_ball]
        if dir_x:
            balls.sort(key=lambda b: b.x, reverse=dir_x > 0)
        if dir_y:
            balls.sort(key=lambda b: b.y, reverse=dir_y < 0)

        for ball in balls:
            ball.roll(dir_x, dir_y)

    def __is_wall(self, loc: Location) -> bool:
        """
        해당 위치가 벽인지 확인한다.
        """
        return self.get(loc) == WALL

    def _is_hole(self, loc) -> bool:
        """
        해당 위치가 구멍인지 확인한다.
        """
        return self.get(loc) == HOLE


def run(map_str: str) -> int:
    """
    게임을 실행한다.
    :param map_str: 보드(지도) 정보
    :return: 빨간공을 구멍에 넣을 수 있는 최소 횟 수, 10회 이내에 성공할 수 없는 경우에는 -1
    """
    return Game(map_str).run()
