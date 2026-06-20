def build_puzzle(partial: str) -> str:
    remaining = 81 - len(partial)
    return partial + "." * remaining


def solved_puzzle() -> str:
    return "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
