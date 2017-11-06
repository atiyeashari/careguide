#finds overlapping intervals
def overlap(times, interval):
    overlapped = []
    for i, time in enumerate(times):
        if interval[0] >= time[0] and interval[0] <= time[1]:
            overlapped.append(i)
            continue
        if interval[1] >= time[0] and interval[1] <= time[1]:
            overlapped.append(i)
    return overlapped


def merge_interval(times, interval):
    overlapped_intervals = overlap(times, interval)
    print(overlapped_intervals)
    merged_interval = interval
    for i in overlapped_intervals:
        merged_interval[0] = min(times[i][0], merged_interval[0])
        merged_interval[1] = max(times[i][1], merged_interval[1])
    return merged_interval


def included(times, interval):
    for i, time in enumerate(times):
        time[0] <= interval[0] and time[1] >= interval[1]
        return i
    return -1

times = [[1, 5], [6, 7], [15, 30]]
print(merge_interval(times, [2, 6]))
print(times)
