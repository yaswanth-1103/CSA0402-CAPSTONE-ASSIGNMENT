"""
UniCore - CPU Scheduling Simulator
CO2 - Compare FCFS and Round Robin (quantum=4) for interactive exam/classroom
processes vs background research/backup jobs.
"""

processes = [
    # name,             arrival, burst, type
    ("P1_OnlineExam",     0,  5, "interactive"),
    ("P2_DigitalClassroom", 1, 3, "interactive"),
    ("P3_LibraryQuery",   2,  8, "interactive"),
    ("P4_ExamGrading",    3,  6, "interactive"),
    ("P5_ResearchJob",    4, 20, "background"),
    ("P6_BackupService",  5, 15, "background"),
    ("P7_IoTLogger",      6,  4, "background"),
    ("P8_ExamRecordSync", 6,  7, "interactive"),
]


def fcfs(procs):
    procs = sorted(procs, key=lambda p: p[1])
    t = 0
    rows = []
    for name, arrival, burst, kind in procs:
        start = max(t, arrival)
        completion = start + burst
        waiting = start - arrival
        turnaround = completion - arrival
        response = waiting
        rows.append((name, kind, arrival, burst, start, completion, waiting, turnaround, response))
        t = completion
    return rows


def round_robin(procs, quantum=4):
    from collections import deque
    procs_sorted = sorted(procs, key=lambda p: p[1])
    n = len(procs_sorted)
    remaining = {p[0]: p[2] for p in procs_sorted}
    arrival = {p[0]: p[1] for p in procs_sorted}
    kind = {p[0]: p[3] for p in procs_sorted}
    first_response = {}
    completion = {}
    t = 0
    q = deque()
    added = set()
    gantt = []

    idx = 0
    # add processes that arrive at time 0
    while idx < n and procs_sorted[idx][1] <= t:
        q.append(procs_sorted[idx][0]); added.add(procs_sorted[idx][0]); idx += 1

    while q:
        pname = q.popleft()
        if pname not in first_response:
            first_response[pname] = t
        run = min(quantum, remaining[pname])
        gantt.append((pname, t, t + run))
        t += run
        remaining[pname] -= run

        # enqueue any new arrivals during this slice
        while idx < n and procs_sorted[idx][1] <= t:
            q.append(procs_sorted[idx][0]); added.add(procs_sorted[idx][0]); idx += 1

        if remaining[pname] > 0:
            q.append(pname)
        else:
            completion[pname] = t

        if not q and idx < n:
            t = max(t, procs_sorted[idx][1])
            while idx < n and procs_sorted[idx][1] <= t:
                q.append(procs_sorted[idx][0]); added.add(procs_sorted[idx][0]); idx += 1

    rows = []
    for name, arr, burst, k in procs_sorted:
        wait = completion[name] - arr - burst
        turnaround = completion[name] - arr
        response = first_response[name] - arr
        rows.append((name, k, arr, burst, None, completion[name], wait, turnaround, response))
    return rows, gantt


def summarize(rows, title):
    print(f"\n{title}")
    header = f"{'Process':<20}{'Type':<12}{'Arr':>5}{'Burst':>6}{'Compl':>7}{'Wait':>6}{'TAT':>6}{'Resp':>6}"
    print(header)
    total_wait = {"interactive": [], "background": []}
    total_tat = {"interactive": [], "background": []}
    for (name, kind, arrival, burst, start, completion, waiting, turnaround, response) in rows:
        print(f"{name:<20}{kind:<12}{arrival:>5}{burst:>6}{completion:>7}{waiting:>6}{turnaround:>6}{response:>6}")
        total_wait[kind].append(waiting)
        total_tat[kind].append(turnaround)
    for kind in ("interactive", "background"):
        avg_w = sum(total_wait[kind]) / len(total_wait[kind])
        avg_t = sum(total_tat[kind]) / len(total_tat[kind])
        print(f"  -> Avg waiting time ({kind}) = {avg_w:.2f}, Avg turnaround = {avg_t:.2f}")
    all_wait = [w for k in total_wait for w in total_wait[k]]
    print(f"  -> Overall Avg Waiting Time = {sum(all_wait)/len(all_wait):.2f}")


if __name__ == "__main__":
    print("=" * 78)
    print("UNICORE CPU SCHEDULING COMPARISON: FCFS vs ROUND ROBIN (q=4)")
    print("=" * 78)

    fcfs_rows = fcfs(processes)
    summarize(fcfs_rows, "FCFS Scheduling Result")

    rr_rows, gantt = round_robin(processes, quantum=4)
    summarize(rr_rows, "Round Robin (Quantum = 4) Scheduling Result")

    print("\nRound Robin Gantt Chart (process:start-end):")
    print(" | ".join(f"{p}:{s}-{e}" for p, s, e in gantt))
