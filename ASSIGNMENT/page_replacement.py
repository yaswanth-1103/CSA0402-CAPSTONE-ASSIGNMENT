"""
UniCore - Page Replacement Simulator
CO3 - FIFO / LRU / Optimal comparison for a 15-reference string,
using 3 frames and 4 frames.
"""

reference_string = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]


def fifo(refs, frames):
    memory = []
    queue = []
    faults = 0
    trace = []
    for r in refs:
        if r in memory:
            trace.append((r, list(memory), False))
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(r)
            queue.append(r)
        else:
            victim = queue.pop(0)
            memory[memory.index(victim)] = r
            queue.append(r)
        trace.append((r, list(memory), True))
    return faults, trace


def lru(refs, frames):
    memory = []
    last_used = {}
    faults = 0
    trace = []
    for i, r in enumerate(refs):
        if r in memory:
            last_used[r] = i
            trace.append((r, list(memory), False))
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(r)
        else:
            lru_page = min(memory, key=lambda p: last_used[p])
            memory[memory.index(lru_page)] = r
        last_used[r] = i
        trace.append((r, list(memory), True))
    return faults, trace


def optimal(refs, frames):
    memory = []
    faults = 0
    trace = []
    for i, r in enumerate(refs):
        if r in memory:
            trace.append((r, list(memory), False))
            continue
        faults += 1
        if len(memory) < frames:
            memory.append(r)
        else:
            future = refs[i + 1:]
            farthest = -1
            victim = None
            for p in memory:
                if p not in future:
                    victim = p
                    break
                else:
                    idx = future.index(p)
                    if idx > farthest:
                        farthest = idx
                        victim = p
            memory[memory.index(victim)] = r
        trace.append((r, list(memory), True))
    return faults, trace


def print_trace(name, refs, frames, faults, trace):
    print(f"\n{name} — {frames} Frames -> Total Page Faults = {faults}")
    line1 = "Ref  : " + "  ".join(f"{r:>2}" for r in refs)
    line2 = "Fault: " + "  ".join(f"{'F' if hit else '.':>2}" for (_, _, hit) in trace)
    print(line1)
    print(line2)


if __name__ == "__main__":
    print("=" * 78)
    print("UNICORE PAGE REPLACEMENT SIMULATOR (Reference string length = "
          f"{len(reference_string)})")
    print("Reference String:", reference_string)
    print("=" * 78)

    results = {}
    for frames in (3, 4):
        print(f"\n{'#'*78}\nFRAME COUNT = {frames}\n{'#'*78}")
        for algo_name, algo in (("FIFO", fifo), ("LRU", lru), ("Optimal", optimal)):
            faults, trace = algo(reference_string, frames)
            print_trace(algo_name, reference_string, frames, faults, trace)
            results[(algo_name, frames)] = faults

    print("\n" + "=" * 78)
    print("SUMMARY TABLE — Total Page Faults")
    print("=" * 78)
    print(f"{'Algorithm':<12}{'3 Frames':>12}{'4 Frames':>12}")
    for algo_name in ("FIFO", "LRU", "Optimal"):
        f3 = results[(algo_name, 3)]
        f4 = results[(algo_name, 4)]
        print(f"{algo_name:<12}{f3:>12}{f4:>12}")

    print("\nBelady's Anomaly check (FIFO): "
          f"{results[('FIFO',3)]} (3 frames) vs {results[('FIFO',4)]} (4 frames)")
    if results[('FIFO', 3)] < results[('FIFO', 4)]:
        print("-> Belady's anomaly OBSERVED for FIFO (faults increased with more frames).")
    else:
        print("-> No Belady's anomaly observed for FIFO on this reference string "
              "(faults did not increase with more frames).")
