import subprocess
import concurrent.futures
import signal
import sys

def check_output(start_letter):
    try:
        result = subprocess.run(["2_2_2.exe", start_letter], capture_output=True, text=True)
        output = result.stdout
    except subprocess.TimeoutExpired:
        print(f"Subprocess timed out for starting letter {start_letter}")
    except Exception as e:
        print(f"Error running subprocess for starting letter {start_letter}: {e}")

def worker_thread(start_letter):
    print(f"Thread started for starting letters: {start_letter}")
    start_letter = [*start_letter]
    check_output(start_letter[0])
    check_output(start_letter[1])

def main():
    total_threads = 13
    alphabet_pairs = ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV", "WX", "YZ"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=total_threads) as executor:
        for letters in alphabet_pairs:
            executor.submit(worker_thread, letters)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
