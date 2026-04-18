from string import punctuation


def get_words(s):
    for p in punctuation:
        s = s.replace(p, " ")
    return sorted(word.upper() for word in s.split())


if __name__ == "__main__":
    tests = [
        ("Hello, world! Hello Python.", ["HELLO", "HELLO", "PYTHON", "WORLD"]),
        ("", []),
        ("   ", []),
        ("!!!,,,...", []),
        ("One", ["ONE"]),
        ("b a c", ["A", "B", "C"]),
        ("Hi-there, you!", ["HI", "THERE", "YOU"]),
        ("  multiple   spaces\tand\nnewlines  ",
         ["AND", "MULTIPLE", "NEWLINES", "SPACES"]),
        ("Don't stop-me now!", ["DON", "ME", "NOW", "STOP", "T"]),
        ("a!b@c#d", ["A", "B", "C", "D"]),
    ]

    all_ok = True
    for src, expected in tests:
        got = get_words(src)
        status = "OK" if got == expected else "FAIL"
        if status == "FAIL":
            all_ok = False
        print(f"{status}: get_words({src!r}) -> {got} (expected {expected})")

    print("\nALL TESTS PASSED" if all_ok else "\nSOME TESTS FAILED")
