def clear_previous_logs() -> None:
    with open("../expected_results.txt", "w"):
        pass


def collect_log(log: str) -> None:
    print(log)
    with open("../expected_results.txt", "a") as f:
        f.write(f"{log}\n")
