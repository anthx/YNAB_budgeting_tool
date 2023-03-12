from __future__ import annotations
from dataclasses import dataclass
from textwrap import indent
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
    budgeted: float

    def __repr__(self) -> str:
        out = f"Master:{self.isMaster} \n Name: {self.name} \n Amount: ${self.amount} Budget: ${self.budgeted}\n"
        out += "    " f"{self.categories}"
        return out

    def Get_Child_Category(self, name: str) -> Category:
        for each in self.categories:
            if each.name == name:
                return each

budget = Category(name="budget", categories=[], isMaster=False, amount=None, budgeted=None)
for m in ynab.master_categories:
    if m.name != "Hidden Categories":
        this_master = Category(m.name, [], True, 0, 0)
        budget.categories.append(this_master)
        for c in m.categories:
                this_category = Category(c.name, [], False, 0, c.cached_balance)
                this_master.categories.append(this_category)
                this_master.budgeted += c.cached_balance


for a in ynab.accounts:
    for tran in a.transactions.since(datetime.date.today().replace(day=1).isoformat()):
        if tran.category:
            tran_cat = budget.Get_Child_Category(tran.category.master_category.name)
            tran_cat.amount += tran.amount
            tran_cat.budgeted += abs(tran.amount)

            tran_master_cat = budget.Get_Child_Category(tran.category.master_category.name).Get_Child_Category(tran.category.name)
            tran_master_cat.amount += tran.amount
            tran_master_cat.budgeted += abs(tran.amount)

print(budget)