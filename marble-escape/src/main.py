from __future__ import annotations

WALL = '#'
HOLE = 'O'
RED_BALL = 'R'
BLUE_BALL = 'B'
BALLS = [RED_BALL, BLUE_BALL]
EMPTY = '.'

ALL_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Location:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_x = self.x
        self.prev_y = self.y

    def equals(self, x, y):
        return x == self.x and y == self.y


class Ball(Location):
    def __init__(self, x, y, game: Game):
        super().__init__(x, y)
        self.__start_x = x
        self.__start_y = y
        self.game = game

    def roll(self, dir_x, dir_y):
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
        self.x = self.__start_x
        self.y = self.__start_y

    def __move(self, x, y):
        # 직전 위치 기억
        self.prev_x = self.x
        self.prev_y = self.y

        # 위치 갱신
        self.x += x
        self.y += y

    def __undo(self):
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

    def run(self):
        # 경로를 생성합니다
        paths = None
        for i in range(9):
            paths = self.__combine([[direction] for direction in ALL_DIRECTIONS])

        # 성공한 경로 중 최소 시도 횟수
        success_min_count = None
        for path in paths:
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

    def get(self, loc: Location):
        return self.map[loc.y][loc.x]

    def __print_map(self):
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
        self.map[loc.y][loc.x] = c

    def __find(self, target):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if target == self.map[y][x]:
                    return Location(x, y)

        raise RuntimeError('Can not find the target: ' + target)

    # noinspection PyAttributeOutsideInit
    def __reset(self):
        self.red_ball.reset()
        self.blu_ball.reset()

    def __tilt(self, dir_x, dir_y):
        balls = [self.red_ball, self.blu_ball]
        if dir_x:
            balls.sort(key=lambda b: b.x, reverse=dir_x > 0)
        if dir_y:
            balls.sort(key=lambda b: b.y, reverse=dir_y < 0)

        for ball in balls:
            ball.roll(dir_x, dir_y)

    @classmethod
    def __combine(cls, paths):
        result = []
        for path in paths:
            latest = path[-1]
            if latest[0]:
                for d in [d for d in ALL_DIRECTIONS if d[0] == 0]:
                    result.append(path + [d])
            else:
                for d in [d for d in ALL_DIRECTIONS if d[0] != 0]:
                    result.append(path + [d])

        return result

    def __is_wall(self, loc: Location):
        return self.get(loc) == WALL

    def _is_hole(self, loc):
        return self.get(loc) == HOLE


def run(map_str: str):
    return Game(map_str).run()
