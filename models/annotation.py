class Annotation:
    class Area:
        def __init__(self, start, end) -> None:
            self.start = start
            self.end = end

        def __str__(self) -> str:
            return f"[{self.start}: {self.end}]"

    def __init__(self, start: int, end: int, score: int, area: Area) -> None:
        self.start = start
        self.end = end
        self.score = score
        self.area = area

    def __str__(self) -> str:
        return f"[{self.start}: {self.end}] - {self.score} | {self.area}"
