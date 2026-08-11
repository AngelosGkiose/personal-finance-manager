def add_expense(db,expense):
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense