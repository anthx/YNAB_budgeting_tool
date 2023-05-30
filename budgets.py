from __future__ import annotations
from dataclasses import dataclass
from textwrap import indent
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append('../')
from pynab.ynab import YNAB
import datetime
from typing import List
ynab = YNAB('YNAB', 'TestBudget')

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
# print(ynab.monthly_budgets[-1::][0])
categories = ynab.master_categories
a_category = categories[2]
print(categories)
print('33:',a_category)
a_budgeted_amount = a_category.categories.monthly_sub_category_budgets[0]
print(a_budgeted_amount)
print(a_budgeted_amount[0].budgeted)
# print(ynab.monthly_budgets[-1::][0].monthly_sub_category_budgets['Food'].category)
exit()
budget = Category(name="budget", categories=[], isMaster=False, amount=None, budgeted=None)
for m in ynab.master_categories:
    if m.name != "Hidden Categories":
        this_master = Category(m.name, [], True, 0, ynab.monthly_budgets[-1::][0].monthly_sub_category_budgets[-1::])
        budget.categories.append(this_master)
        for c in m.categories:
                this_category = Category(c.name, [], False, 0, c.monthly_sub_category_budgets[0].budgeted)
                this_master.categories.append(this_category)
                # this_master.budgeted += sum(this_category.monthly_sub_category_budgets.budgeted)


for a in ynab.accounts:
    for tran in a.transactions.since(datetime.date.today().replace(day=1).isoformat()):
        if tran.category:
            tran_cat = budget.Get_Child_Category(tran.category.master_category.name)
            tran_cat.amount += tran.amount
            # tran_cat.budgeted += abs(tran.amount)

            tran_master_cat = budget.Get_Child_Category(tran.category.master_category.name).Get_Child_Category(tran.category.name)
            tran_master_cat.amount += tran.amount
            tran_master_cat.budgeted += abs(tran.amount)
# print(ynab.monthly_budgets[-1::][0].monthly_sub_category_budgets[-1::][0])
# print(budget)