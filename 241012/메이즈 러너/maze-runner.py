N, M, K = map(int, input().split()) # 미로 크기, 참가자 수, 게임 시간
arr = [list(map(int, input().split())) for _ in range(N)]

for _ in range(M):
    i, j = map(lambda x : int(x)-1, input().split())    # 참가자 좌표
    arr[i][j] -= 1  # 참가자 수만큼 뺌

ei, ej = map(lambda x:int(x)-1, input().split())    # 비상구 좌표
arr[ei][ej] = -11

def find_square(arr):
    mn = N
    # [1] 작은 정사각형 길이 구하기
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0: # 사람이면
                mn = min(mn, max(abs(ei-i), abs(ej-j))) # 비상구와 사람 간의 거리 구하기

    # [2]
    for si in range(mn+1):
        for sj in range(mn+1):
            if si <= ei <= si+mn and sj <= ej <= sj + mn:   # 비상구 있으면
                for i in range(si, si+mn+1):
                    for j in range(sj, sj+mn+1):
                        if -11 < arr[i][j] < 0: # 사람 있으면
                            return si, sj, mn+1 # 사람 간의 거리 + 1 = 정사각형 길이

def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -11:
                return i, j

ans = 0
cnt = M  # 참가자 수
for _ in range(K):
    # [1] 모든 참가자를 동시에 한 칸 이동 -> 최단거리 -> 상 -> 하
    narr = [x[:] for x in arr]
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0:
                dist = abs(ei-i)+abs(ej-j)
                # 네 방향 (상하우선), 범위내, 벽 아니고 <=0, 거리가 dist보다 작으면
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] <= 0 and dist > (abs(ei-ni) + abs(ej-nj)):
                        ans += arr[i][j]    # (참가자가 이동한 거리만큼 누적)
                        narr[i][j] -= arr[i][j] # 참가자 이동
                        if arr[ni][nj] == -11:
                            cnt += arr[i][j]    # 탈출
                        else:
                            narr[ni][nj] += arr[i][j]   # 비상구가 아니면 들어온 인원 추가
                        break

    arr = narr
    if cnt == 0:    # 다 탈출하면
        break

    # [2] 미로회전
    # 시계방향 90도 회전 : 같은 크기 > 좌상단행열, 내구도 -1
    si, sj, L = find_square(arr)    # 출구와 한 명 이상 참가자를 포함하는 가장 작은 정사각형

    narr = [x[:] for x in arr]
    for i in range(L):
        for j in range(L):
            narr[si+i][sj+j] = arr[si+L-1-j][sj+i]
            if narr[si+i][sj+j] > 0:
                narr[si+i][sj+j] -= 1

    arr = narr
    # 회전 후, 비상구 위치 저장
    ei, ej = find_exit(arr)


print(-ans)
print(ei+1, ej+1)