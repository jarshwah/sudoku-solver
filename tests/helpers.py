def build_puzzle(partial: str) -> str:
    remaining = 81 - len(partial)
    return partial + "." * remaining
