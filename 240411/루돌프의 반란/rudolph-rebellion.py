import sys
input = sys.stdin.readline
N, M, P, C, D = map(int, input().split())
Rx, Ry = map(int, input().split())
santa = []
board = [[0]*(N+2) for _ in range(N+2)]

board[Rx][Ry] = 2
temp = [list(map(int, input().split())) for _ in range(P)]
temp.sort(key=lambda x:x[0])
for p in range(P):
    n, x, y = temp[p]

    santa.append([x, y, 0, 2])  # x, y, score, live(0:dead, 1:기절, 2:live)
    board[x][y] = 1

dx, dy = [-1, -1, 0, 1, 1, 1, 0, -1], [0, 1, 1, 1, 0, -1, -1, -1]

# 기절
down = [0] * P

# 충돌
def crush(turn, Rx, Ry, Sx, Sy, d):    # 누구차례(1:산타, 2:루돌프), 루돌프 x, y, 산타 x, y, 이동한 방향
    if turn == 2:   # 루돌프 차례
        for idx, val in enumerate(santa):
            x, y, score, live = val[0], val[1], val[2], val[3]
            if (Sx, Sy) == (x, y):
                santa[idx][2] += C
                nx, ny = Rx + C*dx[d], Ry + C*dy[d]                 # 루돌프 방향으로 밀림
                if nx <= 0 or nx > N or ny <= 0 or ny > N:
                    santa[idx][3] = 0
                    return

                elif board[nx][ny] == 1:
                    push(nx, ny, d)
                    santa[idx][0], santa[idx][1] = nx, ny
                else:   # 밀린 위치가 빈 칸일 때
                    santa[idx][0], santa[idx][1] = nx, ny
                    board[nx][ny] = 1
                santa[idx][3] = 1
                down[idx] = 2
                return
    elif turn == 1: # 산타 차례
        for idx, val in enumerate(santa):
            x, y, score, live = val[0], val[1], val[2], val[3]
            if (Sx, Sy) == (x, y):
                santa[idx][2] += D
                d = (d+4)%8
                nx, ny = Rx + D*dx[d], Ry + D*dy[d]     # 루돌프로부터 반대 방향으로 밀림

                if nx <= 0 or nx > N or ny <= 0 or ny > N:
                    santa[idx][3] = 0
                    return
                elif board[nx][ny] == 1:
                    push(nx, ny, d)
                    santa[idx][0], santa[idx][1] = nx, ny
                else:   # 밀린 위치가 빈 칸일 때
                    santa[idx][0], santa[idx][1] = nx, ny
                    board[nx][ny] = 1
                santa[idx][3] = 1
                down[idx] = 2
                return
    # return board, santa
    pass

# 상호작용 : 산타가 산타에게 밀림
def push(Sx, Sy, d):
    for idx, val in enumerate(santa):
        x, y, score, live = val[0], val[1], val[2], val[3]
        if (Sx, Sy) == (x, y):
            nx, ny = x + dx[d], y + dy[d]   # 1칸 밀림
            if nx <= 0 or nx > N or ny <= 0 or ny > N:  # 칸 밖
                santa[idx][3] = 0
                return
            elif board[nx][ny] == 1:    # 연쇄 충돌
                push(nx, ny)
                santa[idx][0], santa[idx][1] = nx, ny
            else:                       # 빈 칸
                board[nx][ny] = 1
                santa[idx][0], santa[idx][1] = nx, ny
            return



for k in range(M):
    cnt = 0
    for i in range(len(santa)):
        if santa[i][3] == 0:
            cnt += 1
    if cnt == len(santa):
        break


    # [1] 루돌프 이동
    distance = []   # 번호, 거리, r, c
    board[Rx][Ry] = 0

    for i in range(len(santa)):
        if santa[i][3] == 1 and down[i] != 0:   # 기절했을 때 다음 턴으로
            down[i] -= 1
        if santa[i][3] == 1 and down[i] == 0:
            santa[i][3] = 2

    # 가장 가까운 산타 계산
    for idx, val in enumerate(santa):
        if val[3] != 0:
            distance.append((idx, (Rx - val[0])**2 + (Ry - val[1])**2, val[0], val[1]))

    distance.sort(key=lambda x: (x[1], -x[2], -x[3]))
    go_sx, go_sy = distance[0][2], distance[0][3]

    # 가까운 산타에게 가까워지는 방향으로 1칸
    go_distance = []    # 거리, r, c, d
    for i in range(8):
        nx, ny = Rx + dx[i], Ry + dy[i]
        if 0 < nx <= N and 0 < ny <= N:
            go_distance.append(((go_sx - nx)**2 + (go_sy - ny)**2, nx, ny, i))

    go_distance.sort(key=lambda x : x[0])
    go_finish = go_distance[0]


    d, Rx, Ry = go_finish[3], go_finish[1], go_finish[2]    # 방향, 루돌프가 도착한 x, y
    if board[Rx][Ry] == 1:  # 산타가 있으면 산타가 밀림
        # board, santa = crush(2, Rx, Ry, board, santa, d)
        crush(2, Rx, Ry, Rx, Ry, d)
    board[Rx][Ry] = 2




    # [2] 산타 이동
    for idx, val in enumerate(santa):
        x, y, score, live = val[0], val[1], val[2], val[3]
        distance = []   # 거리, nx, ny, 방향
        if live == 2:
            board[x][y] = 0
            # 루돌프로 전진
            for i in (0, 2, 4, 6):
                nx, ny = x + dx[i], y + dy[i]
                if nx <= 0 or nx > N or ny <= 0 or ny > N or board[nx][ny] == 1:    # 격자 밖, 다른 산타 있음
                    continue
                elif board[nx][ny] == 2:    # 루돌프 충돌
                    crush(1, Rx, Ry, x, y, i)
                elif ((nx - Rx)**2 + (ny - Ry)**2) < ((x - Rx)**2 + (y - Ry)**2):  # 이동했을 때 거리가 적으면
                    distance.append((((nx - Rx)**2 + (ny - Ry)**2), nx, ny, i))
                
            if distance:
                distance.sort(key=lambda x: (x[0], x[3]))
                go_distance = distance[0]
                d, x, y = go_distance[3], go_distance[1], go_distance[2]

                board[x][y] = 1
                santa[idx][0] = x
                santa[idx][1] = y
            if (santa[idx][0], santa[idx][1]) == (x, y):
                board[x][y] = 1

    for idx, val in enumerate(santa):
        if santa[idx][3] != 0:
            santa[idx][2] += 1

for i in range(len(santa)):
    print(santa[i][2], end=' ')