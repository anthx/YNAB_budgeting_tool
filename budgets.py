from ynab import YNAB
ynab = YNAB('~/Dropbox/YNAB', 'My Budget from 2015 (2)')

print(ynab.categories['Food'])