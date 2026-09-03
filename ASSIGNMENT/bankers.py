"""
UniCore - Banker's Algorithm Simulator
CO2 - Deadlock Avoidance
Resources: R1=DB-Lock, R2=File-Lock(Exam records), R3=Print/Report, R4=Network-IO channel
Processes: P1 OnlineExam, P2 DigitalClassroom, P3 LibraryService, P4 ResearchJob, P5 BackupService
"""

processes = ["P1_OnlineExam", "P2_DigitalClassroom", "P3_LibraryService", "P4_ResearchJob", "P5_BackupService"]
resources = ["R1_DBLock", "R2_FileLock", "R3_Print", "R4_NetIO"]

Allocation = [
    [0, 1, 0, 1],   # P1_OnlineExam
    [2, 0, 0, 1],   # P2_DigitalClassroom
    [3, 0, 2, 1],   # P3_LibraryService
    [2, 1, 1, 1],   # P4_ResearchJob
    [0, 0, 2, 1],   # P5_BackupService
]

Maximum = [
    [7, 5, 3, 2],   # P1_OnlineExam
    [3, 2, 2, 2],   # P2_DigitalClassroom
    [9, 0, 2, 2],   # P3_LibraryService
    [2, 2, 2, 2],   # P4_ResearchJob
    [4, 3, 3, 2],   # P5_BackupService
]

Total_Resources = [10, 5, 7, 6]


def compute_available(alloc, total):
    allocated_sum = [sum(p[j] for p in alloc) for j in range(len(total))]
    return [total[j] - allocated_sum[j] for j in range(len(total))]


def compute_need(alloc, maxm):
    return [[maxm[i][j] - alloc[i][j] for j in range(len(alloc[0]))] for i in range(len(alloc))]


def print_matrix(title, matrix, header, labels):
    print(f"\n{title}")
    print(f"{'Process':<22}" + "".join(f"{h:>10}" for h in header))
    for lbl, row in zip(labels, matrix):
        print(f"{lbl:<22}" + "".join(f"{v:>10}" for v in row))


def safety_algorithm(alloc, need, available, labels, verbose=True):
    n = len(alloc)
    m = len(available)
    work = available.copy()
    finish = [False] * n
    safe_sequence = []
    step = 1

    if verbose:
        print("\nSafety Algorithm Trace")
        print(f"Initial Work = {work}")

    progressed = True
    while progressed:
        progressed = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                work = [work[j] + alloc[i][j] for j in range(m)]
                finish[i] = True
                safe_sequence.append(labels[i])
                if verbose:
                    print(f"Step {step}: {labels[i]} runs "
                          f"(Need {need[i]} <= Work). New Work = {work}")
                step += 1
                progressed = True

    is_safe = all(finish)
    return is_safe, safe_sequence, work


if __name__ == "__main__":
    print("=" * 70)
    print("UNICORE BANKER'S ALGORITHM - DEADLOCK AVOIDANCE SIMULATOR")
    print("=" * 70)
    print(f"\nTotal Resources {resources}: {Total_Resources}")

    Available = compute_available(Allocation, Total_Resources)
    Need = compute_need(Allocation, Maximum)

    print_matrix("Allocation Matrix", Allocation, resources, processes)
    print_matrix("Maximum Matrix", Maximum, resources, processes)
    print_matrix("Need Matrix (Max - Allocation)", Need, resources, processes)
    print(f"\nAvailable Vector = {dict(zip(resources, Available))}")

    safe, seq, final_work = safety_algorithm(Allocation, Need, Available, processes)

    print("\n" + "-" * 70)
    if safe:
        print(f"RESULT: System is in a SAFE STATE")
        print(f"Safe Sequence: {' -> '.join(seq)}")
    else:
        print("RESULT: System is in an UNSAFE STATE / DEADLOCK POSSIBLE")

    # ---- Additional resource request that makes system unsafe ----
    print("\n" + "=" * 70)
    print("REQUEST TEST: P5_BackupService requests (R1=0, R2=3, R3=0, R4=0)")
    print("=" * 70)
    request = [0, 3, 0, 0]
    p_idx = processes.index("P5_BackupService")

    ok = True
    for j in range(len(resources)):
        if request[j] > Need[p_idx][j]:
            print(f"ERROR: Request exceeds declared maximum need for {resources[j]}")
            ok = False
        if request[j] > Available[j]:
            print(f"Request[{resources[j]}]={request[j]} > Available[{resources[j]}]={Available[j]}")
            ok = False

    if ok:
        trial_alloc = [row.copy() for row in Allocation]
        trial_avail = Available.copy()
        trial_need = [row.copy() for row in Need]
        for j in range(len(resources)):
            trial_alloc[p_idx][j] += request[j]
            trial_avail[j] -= request[j]
            trial_need[p_idx][j] -= request[j]

        print(f"Tentative Available after grant = {trial_avail}")
        safe2, seq2, _ = safety_algorithm(trial_alloc, trial_need, trial_avail, processes, verbose=True)
        print("-" * 70)
        if safe2:
            print(f"Request CAN be granted safely. New safe sequence: {' -> '.join(seq2)}")
        else:
            print("Request CANNOT be granted -> system would enter an UNSAFE state.")
            print("Decision: Request is DENIED / P5_BackupService is made to WAIT.")
    else:
        print("Decision: Request is immediately DENIED (fails basic Banker's checks).")
