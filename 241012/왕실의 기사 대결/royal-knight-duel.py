from collections import deque

# 체스판의 크기, 기사의 수, 명령의 수
N, M, Q = map(int, input().split())

arr = [[2]*(N+2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(N)] + [[2]*(N+2)]
units = {}  # 1번 기사부터 N번 기사까지 순서대로 정보 저장
# v = [[0]*(N+2) for _ in range(N+2)]
init_k = [0]*(M+1)  # 초기 체력

for m in range(1, M+1):  # 초기 세팅
    si, sj, h, w, k = map(int, input().split())
    units[m] = [si, sj, h, w, k]
    init_k[m] = k

    # for i in range(si, si+h):
    #     v[i][sj:sj+w] = [m]*w

def push_unit(start, dr):
    di = [-1, 0, 1, 0]
    dj = [0, 1, 0, -1]
    q = deque()
    q.append(start)
    pset = set()    # 밀어낼 후보들
    damage = [0]*(M+1)
    pset.add(start)

    while q:
        cur = q.popleft()
        ci, cj, h, w, k = units[cur]

        ni, nj = ci + di[dr], cj + dj[dr]   # 기사가 이동하면
        for i in range(ni, ni+h):
            for j in range(nj, nj+w):
                if arr[i][j] == 2:
                    return
                if arr[i][j] == 1:     # 함정이면
                    damage[cur] += 1    # 데미지 누적

        for idx in units:
            if idx in pset: # 움직일 대상이면 넘어가기
                continue

            ti, tj, th, tw, tk = units[idx]

            if ni<=ti+th-1 and nj<=tj+tw-1 and ni+h-1>=ti and tj<=nj+w-1:   # 겹치면
                q.append(idx)
                pset.add(idx)

    damage[start] = 0

    # 데미지 처리
    for idx in pset:
        si, sj, h, w, k = units[idx]

        if k <= damage[idx]:
            units.pop(idx)
        else:
            ni, nj = si+di[dr], sj+dj[dr]
            units[idx] = [ni, nj, h, w, k-damage[idx]]


for _ in range(Q):
    idx, dr = map(int, input().split())
    if idx in units:
        push_unit(idx, dr)

ans = 0
for idx in units:
    ans += init_k[idx] - units[idx][4]
print(ans)