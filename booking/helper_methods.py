from booking.models import *
import pytz
utc=pytz.UTC


# Finds overlapping intervals
def overlap(times, interval):
    overlapped = []
    for i, time in enumerate(times):
        if interval.start_time >= time.start_time and interval.start_time <= time.end_time:
            overlapped.append(i)
            continue
        if interval.end_time >= time.start_time and interval.end_time <= time.end_time:
            overlapped.append(i)
    return overlapped


# Merges intervals and returns the merged interval
def merge_interval(times, interval):
    overlapped_intervals = overlap(times, interval)
    merged_interval = interval
    for i in overlapped_intervals:
        merged_interval.start_time = min(times[i].start_time, merged_interval.start_time)
        merged_interval.end_time = max(times[i].end_time, merged_interval.end_time)
    return merged_interval


def included(times, interval):
    for i, time in enumerate(times):
        time.start_time <= interval.start_time and time.end_time >= interval.end_time
        return i
    return -1


# Input is an availability object
# It finds all the overlapping availabilities and deletes them and adds the new availability to database
def add_availability(availability):
    availability.start_time = utc.localize(availability.start_time)
    availability.end_time = utc.localize(availability.end_time)
    booked_times = BookedTime.objects.filter(baby_sitter=availability.baby_sitter)
    if len(overlap(booked_times, availability)) > 0:
        print("This time cannot be available because it's booked.")
        return "This time cannot be available because it's booked."
    if availability.start_time >= availability.end_time:
        print("Start time must be sooner than end time")
        return "Start time must be sooner than end time"
    print(availability.baby_sitter)
    availabilities = Availability.objects.filter(baby_sitter=availability.baby_sitter)
    overlapped_availabilities = overlap(availabilities, availability)
    new_availability = merge_interval(availabilities, availability)
    print(new_availability.start_time)
    print(new_availability.end_time)
    for i in overlapped_availabilities:
        availabilities[i].delete()
    new_availability.save()
    return "availability successfully added."
