import time


class PerformanceProfiler:

    def __init__(self):
        self.data = {}

    def start(self, name):
        self.data[name] = time.perf_counter()

    def stop(self, name):
        elapsed = time.perf_counter() - self.data[name]
        self.data[name] = elapsed
        return elapsed

    def summary(self):

        total = sum(self.data.values())

        print("\n----------- Performance -----------")

        for name, value in self.data.items():
            print(f"{name:<20} {value:.3f} sec")

        print("-----------------------------------")
        print(f"{'TOTAL':<20} {total:.3f} sec")
        print("-----------------------------------")

        return total