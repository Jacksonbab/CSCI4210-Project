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


def next_exp(ceiling):
    while 1:
        #  -log(r) / lambda
        random_num = (-math.log(uniform_generator.drand())) / lbd


        # if math.floor(random_num) <= upper_bound:
        #     return random_num

        
        if ceiling and math.ceil(random_num) <= upper_bound:
            return random_num
        elif (not ceiling) and random_num <= upper_bound:
            return random_num


def generate_inter_arrival_times(cpu_bound, num_cpu_bursts):
    cpu_bursts = {num: [] for num in range(num_cpu_bursts)}
    for j in range(num_cpu_bursts - 1):
        if not cpu_bound:
            cpu_burst_time = math.ceil(next_exp(True))
            io_burst_time = 10 * math.ceil(next_exp(True))
            cpu_bursts[j] = [cpu_burst_time, io_burst_time]
        else:
            cpu_burst_time = math.ceil(next_exp(True)) * 4
            io_burst_time = (10 * math.ceil( next_exp(True))) // 4
            cpu_bursts[j] = [cpu_burst_time, io_burst_time]
        print("--> CPU burst {}ms --> I/O burst {}ms".format(cpu_burst_time, io_burst_time))
    if not cpu_bound:
        cpu_burst_time = math.ceil(next_exp(True))
    else:
        cpu_burst_time = math.ceil(next_exp(True))* 4
    print("--> CPU burst {}ms".format(cpu_burst_time))
    cpu_bursts[num_cpu_bursts - 1] = [cpu_burst_time]  # No I/O burst time for last CPU burst
    return cpu_bursts


# Reference: https://stackoverflow.com/questions/5574702/how-do-i-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    exit(1)


n = len(sys.argv)
if n != 6:
    eprint("ERROR: Wrong number of command-line arguments")

if not sys.argv[1].isdigit():
    eprint("ERROR: argv[1] should be a digit")
num_process = int(sys.argv[1])  # the number of processes to simulate
if not (1 <= num_process <= 26):
    eprint("ERROR: Illegal number of process, should be [1,26]")

if not sys.argv[2].isdigit():
    eprint("ERROR: argv[2] should be a digit")
num_CPU_bound = int(sys.argv[2])  # number of processes that are CPU bounded
if not (0 <= num_CPU_bound <= num_process): 
    eprint("ERROR: Illegal number of CPU bound processes")

if not sys.argv[3].isdigit():
    eprint("ERROR: argv[3] should be a digit")
random_seed = int(sys.argv[3])  # the seed for the pseudo-random number sequence

if random_seed < 0: 
    eprint("ERROR: argv[3] should be positive integer")

try:
    lbd = float(sys.argv[4])  # 1/lbd will be the average random value generated
except ValueError:
    eprint("ERROR: argv[4] should be a float")
    
if (lbd <= 0):
    eprint("ERROR: lambda cannot be less than or equal to 0")

try:
    upper_bound = float(sys.argv[5])  # the upper bound for valid pseudo-random numbers
except ValueError:
    eprint("ERROR: argv[5] should be a float")

if not (0 < upper_bound):
    eprint("ERROR: Illegal upper bound")

num_IO_bound = num_process - num_CPU_bound
if num_CPU_bound == 1:
    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound process >>>".format(num_process, num_CPU_bound))
else:
    print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound processes >>>".format(num_process, num_CPU_bound))

uniform_generator = Rand48()
uniform_generator.srand(random_seed)

process_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in range(num_process):
    init_arr_time = math.floor(next_exp(False))
    num_CPU_bursts = math.ceil(100 * uniform_generator.drand())  # num_CPU_bursts \in [1, 100]
    if i < num_IO_bound:
        print("I/O-bound process {}: arrival time {}ms;".format(process_string[i],
                                                                               init_arr_time
                                                                               ),end=" ")
        if num_CPU_bursts == 1:
            print("{} CPU burst:".format(num_CPU_bursts))
        else:
            print("{} CPU bursts:".format(num_CPU_bursts))
        generate_inter_arrival_times(False, num_CPU_bursts)
    else:
        print("CPU-bound process {}: arrival time {}ms;".format(process_string[i],
                                                                                init_arr_time), end=" ")
        if num_CPU_bursts == 1:
            print("{} CPU burst:".format(num_CPU_bursts))
        else:
            print("{} CPU bursts:".format(num_CPU_bursts))
        generate_inter_arrival_times(True, num_CPU_bursts)
