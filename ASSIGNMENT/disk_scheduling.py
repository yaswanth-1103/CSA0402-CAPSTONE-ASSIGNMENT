"""
UniCore - Disk Scheduling Simulator
CO4 - FCFS / SSTF / SCAN / C-SCAN comparison
Disk: 200 cylinders (0-199). Head starts at 90.
"""

MAX_CYL = 199
requests = [55, 182, 45, 108, 130, 12, 170, 90, 25, 160, 195]
head_start = 90


def fcfs(reqs, start):
    seq = [start] + reqs
    total = sum(abs(seq[i + 1] - seq[i]) for i in range(len(seq) - 1))
    return reqs, total


def sstf(reqs, start):
    remaining = reqs.copy()
    seq = []
    current = start
    total = 0
    while remaining:
        nxt = min(remaining, key=lambda c: abs(c - current))
        total += abs(nxt - current)
        current = nxt
        seq.append(nxt)
        remaining.remove(nxt)
    return seq, total


def scan(reqs, start, max_cyl, direction="up"):
    # Elevator algorithm; assumes head goes to the end of the disk on its way.
    seq = []
    total = 0
    current = start
    up = sorted([r for r in reqs if r >= start])
    down = sorted([r for r in reqs if r < start], reverse=True)

    if direction == "up":
        path = up + [max_cyl] + down
    else:
        path = down + [0] + up

    for c in path:
        total += abs(c - current)
        current = c
        seq.append(c)
    # Remove the boundary cylinder from the printed service sequence if it
    # wasn't an actual pending request
    seq_display = [c for c in seq if c in reqs]
    return seq_display, total, seq


def c_scan(reqs, start, max_cyl, direction="up"):
    seq = []
    total = 0
    current = start
    up = sorted([r for r in reqs if r >= start])
    down = sorted([r for r in reqs if r < start])

    if direction == "up":
        # go up to max, jump to 0, continue up through remaining (down list)
        path = up + [max_cyl, 0] + down
    else:
        down_desc = sorted([r for r in reqs if r < start], reverse=True)
        up_desc = sorted([r for r in reqs if r >= start], reverse=True)
        path = down_desc + [0, max_cyl] + up_desc

    for c in path:
        total += abs(c - current)
        current = c
        seq.append(c)
    seq_display = [c for c in seq if c in reqs]
    return seq_display, total, seq


if __name__ == "__main__":
    print("=" * 78)
    print(f"UNICORE DISK SCHEDULING SIMULATOR  (0-{MAX_CYL} cylinders, head start = {head_start})")
    print(f"Pending Requests ({len(requests)}): {requests}")
    print("=" * 78)

    f_seq, f_total = fcfs(requests, head_start)
    print(f"\nFCFS   Service Order: {head_start} -> " + " -> ".join(map(str, f_seq)))
    print(f"FCFS   Total Head Movement = {f_total} cylinders")

    s_seq, s_total = sstf(requests, head_start)
    print(f"\nSSTF   Service Order: {head_start} -> " + " -> ".join(map(str, s_seq)))
    print(f"SSTF   Total Head Movement = {s_total} cylinders")

    sc_disp, sc_total, sc_full = scan(requests, head_start, MAX_CYL, "up")
    print(f"\nSCAN   Full Path (incl. disk end): {head_start} -> " + " -> ".join(map(str, sc_full)))
    print(f"SCAN   Total Head Movement = {sc_total} cylinders")

    cs_disp, cs_total, cs_full = c_scan(requests, head_start, MAX_CYL, "up")
    print(f"\nC-SCAN Full Path (incl. wrap to 0): {head_start} -> " + " -> ".join(map(str, cs_full)))
    print(f"C-SCAN Total Head Movement = {cs_total} cylinders")

    print("\n" + "=" * 78)
    print("SUMMARY TABLE")
    print("=" * 78)
    print(f"{'Algorithm':<10}{'Total Head Movement':>22}{'Avg Seek/Request':>20}")
    n = len(requests)
    for name, total in (("FCFS", f_total), ("SSTF", s_total), ("SCAN", sc_total), ("C-SCAN", cs_total)):
        print(f"{name:<10}{total:>22}{total / n:>20.2f}")
