import os
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor

from django.db import close_old_connections
from .models import Student


def run_query():
    return Student.objects.count()


def task():
    close_old_connections()
    try:
        return run_query()
    finally:
        close_old_connections()



def run_parallel(num_threads: int, num_queries: int = 150):
    start = perf_counter()

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(executor.map(lambda _: task(), range(num_queries)))

    return perf_counter() - start


def benchmark():
    THREADS = [1, 2, 4, 8, 16]
    REQUESTS = 150

    results = []

    for t in THREADS:
        time_sec = run_parallel(t, REQUESTS)
        results.append({
            "threads": t,
            "requests": REQUESTS,
            "time_sec": round(time_sec, 4)
        })

    return results
