from collections import deque

R, C, K = map(int, input().split())
unit = [list(map(int, input().split())) for _ in range(K)]
arr = [[1]+[0]*C+[1] for _ in range(R+3)] + [[1]*(C+2)]
exit_set = set()

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def bfs(si, sj):
    q = deque()
    q.append((si, sj))
    visited = [[0]*(C+2) for _ in range(R+4)] # 환경은 동일하게 세팅
    visited[si][sj] = 1
    mx_i = 0    # -2해서 리턴하기, 최대 행

    while q:
        ci, cj = q.popleft()
        mx_i = max(mx_i, ci)

        for i in range(4):
            ni, nj = ci+di[i], cj+dj[i]
            # print('?:', ni, nj)
            if 0 <= ni < R+4 and 0 <= nj < C+2 and not visited[ni][nj] and (arr[ci][cj]==arr[ni][nj] or ((ci, cj) in exit_set and arr[ni][nj] > 1)):
                q.append((ni, nj))
                visited[ni][nj] = 1

    return mx_i-2


ans = 0
num = 2 # 골렘 숫자

for cj, dr in unit:
    ci = 1
    # [1] 남쪽으로 최대한 이동(남 -> 서 -> 동)
    while True:
        if arr[ci+1][cj-1]+arr[ci+2][cj]+arr[ci+1][cj+1] == 0:  # 남쪽
            ci += 1
        elif (arr[ci-1][cj-1]+arr[ci][cj-2]+arr[ci+1][cj-1]+ arr[ci+1][cj-2]+arr[ci+2][cj-1]) == 0:    # 서쪽 이동 + 회전
            ci += 1
            cj -= 1 # 이동
            dr = (dr-1)%4   # 회전
        elif (arr[ci-1][cj+1]+arr[ci][cj+2]+arr[ci+1][cj+1]+arr[ci+1][cj+2]+arr[ci+2][cj+1]) == 0:  # 동쪽 이동 + 회전
            ci += 1
            cj += 1
            dr=(dr+1)%4
        else:
            break   # 이동 끝

    if ci < 4:  # 몸이 범위밖(골렘들 초기화)
        arr = [[1]+[0]*C+[1] for _ in range(R+3)] + [[1]*(C+2)]
        exit_set = set()
        num = 2 # 골렘도 다 초기화
    else:
        # [2] 골렘 표시 + 비상구위치 추가
        arr[ci+1][cj] = arr[ci-1][cj] = num
        arr[ci][cj-1:cj+2] = [num] * 3
        num += 1    # 다음 골렘

        exit_set.add((ci+di[dr], cj+dj[dr]))
        ans += bfs(ci, cj)  # 골렘이 떨어져서 요정이 이동한 최종 위치 더하기

print(ans)