from collections import deque

K, M = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(5)]
lst = list(map(int, input().split()))
ans = []

def bfs(arr, visited, si, sj, clr):
    q = deque()
    q.append((si, sj))
    visited[si][sj] = 1
    sset = set()
    sset.add((si, sj))
    cnt = 0
    cnt += 1

    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]

    while q:
        ci, cj = q.popleft()
        for i in range(4):
            ni, nj = ci + dx[i], cj + dy[i]
            if 0 <= ni < 5 and 0 <= nj < 5 and not visited[ni][nj] and arr[ci][cj] == arr[ni][nj]:
                q.append((ni, nj))
                visited[ni][nj] = 1
                cnt += 1
                sset.add((ni, nj))

    if cnt >= 3: # 유물이 3개 이상이면
        if clr == 1:     # 지워야 하면
            for i, j in sset:
                arr[i][j] = 0

        return cnt
    else:
        return 0




def count_clear(arr, clr):
    visited = [[0]*5 for _ in range(5)]
    cnt = 0
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                t = bfs(arr, visited, i, j, clr)
                cnt += t
    return cnt


def rotate(arr, si, sj):
    narr = [x[:] for x in arr]
    for i in range(3):
        for j in range(3):
            narr[si+i][sj+j] = arr[si+3-j-1][sj+i]
    return narr

for _ in range(K):
    # [1] 탐사 진행
    mx_cnt = 0
    for rot in range(1, 4): # 회전수 -> 열 -> 행
        for sj in range(3):
            for si in range(3):
                narr = [x[:] for x in arr]
                for _ in range(rot):    # 90도씩 회전
                    narr = rotate(narr, si, sj)
                t = count_clear(narr, 0)    # 유물 획득
                if mx_cnt < t:  # 유물 가치 최대화
                    mx_cnt = t
                    marr = narr

    if mx_cnt == 0: # 유물 없으면 종료
        break

    # [2] 유물 연쇄획득
    cnt = 0
    arr = marr
    while True:
        t = count_clear(arr, 1) # 획득해서 그 부분 없애기
        if t == 0:  # 연쇄 획득 종료
            break
        cnt += t

        for j in range(5):
            for i in range(4, -1, -1):
                if arr[i][j] == 0:
                    arr[i][j] = lst.pop(0)  # 빠진 부분 집어넣기

    ans.append(cnt)
print(*ans)