from __future__ import annotations
from dataclasses import dataclass
from ynab import YNAB
import datetime
from typing import List
ynab = YNAB('~/Dropbox/YNAB', 'My Budget from 2015 (2)')

@dataclass
class Category(object):
    name: str
    categories: List
    isMaster: bool
    amount: float

    def __repr__(self) -> str:
        out = f"Master:{self.isMaster} \n Name: {self.name} \n Amount: ${self.amount} \n"
        out += "    " f"{self.categories}"
        return out

    def Get_Child_Category(self, name: str) -> Category:
        for each in self.categories:
            if each.name == name:
                return each

budget = Category(name="budget", categories=[], isMaster=False, amount=None)
for m in ynab.master_categories:
    this_master = Category(m.name, [], True, 0)
    budget.categories.append(this_master)
    for c in m.categories:
        if c.name != "Hidden Categories":
            this_category = Category(c.name, [], False, 0)
            this_master.categories.append(this_category)


for a in ynab.accounts:
    for tran in a.transactions.since(datetime.date.today().replace(day=1).isoformat()):
        if tran.category:
            budget.Get_Child_Category(tran.category.master_category.name).amount += tran.amount
            budget.Get_Child_Category(tran.category.master_category.name).Get_Child_Category(tran.category.name).amount += tran.amount

print(budget)