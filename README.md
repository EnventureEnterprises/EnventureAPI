#enventure-api


http://en.wikipedia.org/wiki/Debits_and_credits

In Double Entry Accounting there are 5 account types: Asset, Liability, Income, Expense and Equity defined as follows:

Asset is a resource controlled by the entity as a result of past events and from which future economic benefits are expected to flow to the entity

Liability is defined as an obligation of an entity arising from past entries or events, the settlement of which may result in the transfer or use of assets, provision of services or other yielding of economic benefits in the future.

Income is increases in economic benefits during the accounting period in the form of inflows or enhancements of assets or decreases of liabilities that result in increases in equity, other than those relating to contributions from equity participants.

Expense is a decrease in economic benefits during the accounting period in the form of outflows or depletions of assets or incurrences of liabilities that result in decreases in equity, other than those relating to distributions to equity participants.

Equity consists of the net assets of an entity. Net assets is the difference between the total assets of the entity and all its liabilities.

In each entry, sources are credited and destinations are debited.

I repeat: credit is the source and debit is the destination.

debit and credit affect balance of an account differently depending on the account type.

For Asset and Expense accounts, Debit increases the balance, and credit decreases it. For the rest of the accounts it is the opposite. i.e. debit decreases and credit increases the balance.

Accounting Equation

At any given point accounts should satisfy the following equation:

Assets + Expenses = Liabilities + Equity + Income
You can verify it with Account.balanced?.

Debitcredit takes care to keep the system balanced at all times, if you get an unbalanced state, its a bug, please report immediately!
