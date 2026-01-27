from fastapi import Query


def page_number(page: int = Query(1, ge=1)) -> int:
    return page
