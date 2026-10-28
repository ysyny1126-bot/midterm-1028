# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # bool은 int의 하위 클래스라 따로 제외 (#5)
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


class LibraryLoan:
    def __init__(self):
        self._loans = {}      # book_id -> (name, 빌린 날, 반납 기한)
        self._bans = {}       # name -> [(정지 시작일, 정지 끝일(포함))]

    def borrow(self, book_id, name, day):
        if not isinstance(book_id, str) or book_id not in BOOKS:     # 실패 1
            return False
        if not _valid_day(day):                                       # 실패 2
            return False
        if book_id in self._loans:                                    # 실패 3
            return False
        mine = [due for (who, _, due) in self._loans.values() if who == name]
        if len(mine) >= MAX_LOANS:                                    # 실패 4
            return False
        if any(day > due for due in mine):                            # 실패 5
            return False
        for start, end in self._bans.get(name, []):                   # 실패 6
            if start <= day <= end:
                return False
        self._loans[book_id] = (name, day, day + LOAN_DAYS)
        return True

    def return_book(self, book_id, name, day):
        if not isinstance(book_id, str) or book_id not in self._loans:
            return -1
        who, borrowed, due = self._loans[book_id]
        if who != name:
            return -1
        if not _valid_day(day):
            return -1
        if day < borrowed:
            return -1
        overdue = max(0, day - due)
        del self._loans[book_id]
        if overdue > 0:
            # 반납한 날부터 연체 일수만큼 정지. 겹치면 구간의 합집합 = 더 늦게 끝나는 쪽
            self._bans.setdefault(name, []).append((day, day + overdue - 1))
        return overdue

    def get_loans(self, name):
        result = [(b, due) for b, (who, _, due) in self._loans.items() if who == name]
        result.sort(key=lambda t: (t[1], t[0]))
        return result
