import subprocess
from subprocess import TimeoutExpired
from tqdm import tqdm
import time

# Definim path pentru fisiere .onnx și .vnnlib
onnx_files = [
    "vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_{}_{}_batch_2000.onnx".format(i, j)
    for i in range(1, 6)
    for j in range(1, 10)
]

vnnlib_files = [
    "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_{}.vnnlib".format(k)
    for k in range(1, 11)
]

# Combinatiile pentru primele 4 fisiere vnnlib cu toate cele 45 de fisiere onnx
combinations = []

for vnnlib_file in vnnlib_files[:4]:
    combinations.extend([(onnx_file, vnnlib_file) for onnx_file in onnx_files])

# Combinatiile pentru cele 6 perechi extra
extra_combinations = [
    ("vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_1_1_batch_2000.onnx", "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_5.vnnlib"),
    ("vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_1_1_batch_2000.onnx", "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_6.vnnlib"),
    ("vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_1_9_batch_2000.onnx", "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_7.vnnlib"),
    ("vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_2_9_batch_2000.onnx", "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_8.vnnlib"),
    ("vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_3_3_batch_2000.onnx", "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_9.vnnlib"),
    ("vnncomp2023_benchmarks/benchmarks/acasxu/onnx/ACASXU_run2a_4_5_batch_2000.onnx", "vnncomp2023_benchmarks/benchmarks/acasxu/vnnlib/prop_10.vnnlib")
]

# Adaugarea combinatiilor extra
combinations.extend(extra_combinations)

# Lista pentru a stoca rezultatele
results = []

# Executia comenzilor pentru fiecare combinatie si afisarea rezultatelor in terminal + scrierea lor într-un fisier
with open("rezultate.txt", "w") as result_file, tqdm(total=len(combinations)) as pbar:
    for onnx_file, vnnlib_file in combinations:
        command = [
            "python3",
            "main.py",
            "--net",
            onnx_file,
            "--spec",
            vnnlib_file,
            "--disable_restart"
        ]

        # Start timer
        start_time = time.time()

        try:
            # Execute the command with a timeout of 120 seconds
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate(timeout=120)

            # Check if the process terminated successfully
            if process.returncode == 0:
                result = (command, output.decode(), error.decode())
            else:
                result = (command, f"Process returned non-zero exit code: {process.returncode}", error.decode())
        except TimeoutExpired:
            # Handle timeout
            result = (command, "Timeout: Command exceeded 120 seconds", "")

        results.append(result)

        # Afiseaza rezultatul in terminal
        print("\n".join(result[0]))  # Afișează comanda
        print(result[1])  # Afișează rezultatul

        # Scrie rezultatul în fisier
        result_file.write(" ".join(result[0]) + "\n")
        result_file.write(result[1] + result[2] + "\n")

        pbar.update(1)
