prison   :- punished.
innocent :- not punished.

punished :- tax_deadline_passed, not paid_taxes.

tax_deadline_passed.
{paid_taxes}.

{immunity}.
:- punished, immunity.

