import sys
import math


# Reference: https://stackoverflow.com/questions/7287014/is-there-any-drand48-equivalent-in-python-or-a-wrapper-to-it
class Rand48(object):
    def __init__(self, seed=0):
        self.n = seed

    def seed(self, seed):
        self.n = seed

    def srand(self, seed):
        self.n = (seed << 16) + 0x330e

    def next(self):
        self.n = (25214903917 * self.n + 11) & (2 ** 48 - 1)
        return self.n

    def drand(self):
        return self.next() / 2 ** 48

    # def lrand(self):
    #     return self.next() >> 17
    #
    # def mrand(self):
    #     n = self.next() >> 16
    #     if n & (1 << 31):
    #         n -= 1 << 32
    #     return n


def next_exp():
    while 1:
        #  -log(r) / lambda
        random_num = (-math.log(uniform_generator.drand())) / lbd
        if math.floor(random_num) <= upper_bound:
            return random_num


def generate_inter_arrival_times(cpu_bound, num_cpu_bursts):
    cpu_bursts = {num: [] for num in range(num_cpu_bursts)}
    for j in range(num_cpu_bursts - 1):
        if not cpu_bound:
            cpu_burst_time = math.ceil(next_exp())
            io_burst_time = 10 * math.ceil(next_exp())
            cpu_bursts[j] = [cpu_burst_time, io_burst_time]
        else:
            cpu_burst_time = math.ceil(next_exp()) * 4
            io_burst_time = math.floor(10 * math.ceil( next_exp()) / 4)
            cpu_bursts[j] = [cpu_burst_time, io_burst_time]
        print("--> CPU burst {}ms --> I/O burst {}ms".format(cpu_burst_time, io_burst_time))
    if not cpu_bound:
        cpu_burst_time = math.ceil(next_exp())
    else:
        cpu_burst_time = math.ceil(next_exp())* 4
    print("--> CPU burst {}ms".format(cpu_burst_time))
    cpu_bursts[num_cpu_bursts - 1] = [cpu_burst_time]  # No I/O burst time for last CPU burst
    return cpu_bursts


n = len(sys.argv)
if n != 6:
    sys.exit("ERROR: Wrong number of command-line arguments")

if not sys.argv[1].isdigit(): sys.exit("ERROR: argv[1] should be a digit")
num_process = int(sys.argv[1])  # the number of processes to simulate
if not (0 <= num_process <= 26): sys.exit("ERROR: Illegal number of process, should be [0,26]")

if not sys.argv[2].isdigit(): sys.exit("ERROR: argv[2] should be a digit")
num_CPU_bound = int(sys.argv[2])  # number of processes that are CPU bounded
if not (0 <= num_CPU_bound <= num_process): sys.exit("ERROR: Illegal number of CPU bound processes")

if not sys.argv[3].isdigit(): sys.exit("ERROR: argv[3] should be a digit")
random_seed = int(sys.argv[3])  # the seed for the pseudo-random number sequence

try:
    float(sys.argv[4])
except ValueError:
    sys.exit("ERROR: argv[4] should be a float")
lbd = float(sys.argv[4])  # 1/lbd will be the average random value generated

try:
    float(sys.argv[5])
except ValueError:
    sys.exit("ERROR: argv[5] should be a float")
upper_bound = float(sys.argv[5])  # the upper bound for valid pseudo-random numbers
if not (0 < upper_bound): sys.exit("ERROR: Illegal upper bound")

num_IO_bound = num_process - num_CPU_bound
if num_CPU_bound == 1 or num_CPU_bound == 0:
    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound process >>>".format(num_process, num_CPU_bound))
else:
    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound processes >>>".format(num_process, num_CPU_bound))

uniform_generator = Rand48()
uniform_generator.srand(random_seed)

process_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in range(num_process):
    init_arr_time = math.floor(next_exp())
    num_CPU_bursts = math.ceil(100 * uniform_generator.drand())  # num_CPU_bursts \in [1, 100]
    if i < num_IO_bound:
        print("I/O-bound process {}: arrival time {}ms; {} CPU bursts:".format(process_string[i],
                                                                               init_arr_time,
                                                                               num_CPU_bursts))
        generate_inter_arrival_times(False, num_CPU_bursts)
    else:
        print("CPU-bound process {}: arrival time {}ms; {} CPU bursts:".format(process_string[i],
                                                                                init_arr_time,
                                                                                num_CPU_bursts))
        generate_inter_arrival_times(True, num_CPU_bursts)
