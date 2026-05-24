import time


def main() -> None:
    iteration = 0
    while True:
        print(f"Iteration: {iteration}")
        time.sleep(10)
        iteration += 1


if __name__ == "__main__":
    main()
