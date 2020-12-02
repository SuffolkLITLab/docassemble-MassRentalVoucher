from docassemble.base.core import DAObject, DAList, DADict, DAOrderedDict
from docassemble.base.util import Value, PeriodicValue, FinancialList, PeriodicFinancialList
from decimal import Decimal
import datetime
import docassemble.base.functions
from collections import OrderedDict
import json

def cash_type_list() :
    """Returns a list of assset types for a multiple choice dropdown"""
    cash_list = DAOrderedDict()
    cash_list.auto_gather = False
    cash_list.gathered = True
    cash_list.elements.update([
        ('Salary, wages, including overtime and tips', 'Salary & wages, including overtime & tips'),
        ('Income from Business or Profession', 'Net income from Business or Profession'),
        ('Unemployment or Disability Compensation', 'Unemployment or Disability Compensation'),
        ('TAFDC  or Public Assistance', 'TAFDC or Public Assistance'),
        ('Social Secuirty Benefits and SSI (Supplemental Secuirty Income), including SSP (State Supplement Program)', 'Social Secuirty Benefits and SSI, including SSP (State Supplement Program)'),
        ('VA Disability Income', 'VA Disability Income'),
        ('Pensions, Annuities, Dividends, and Interests', 'Pensions, Annuities, Dividends, and Interests'),
        ('Other', 'Other Income:')
    ])
    return cash_list

class IncomeList(DAList):
    """Represents a filterable DAList of income items, each of which has an associated period or hourly wages."""
    
    def init(self, *pargs, **kwargs):
        self.elements = list()
        if not hasattr(self, 'object_type'):
            self.object_type = Income
        return super(IncomeList, self).init(*pargs, **kwargs)        
    def types(self):
        """Returns a set of the unique types of values stored in the list."""
        types = set()
        for item in self.elements:
            if hasattr(item,'type'):
                types.add(item.type)
        return types

    def owners(self, type=None):
        """Returns a set of the unique owners for the specified type of value stored in the list. If type is None, returns all 
        unique owners in the IncomeList"""
        owners=set()
        if type is None:
            for item in self.elements:
                if hasattr(item, 'owner'):
                    owners.add(item.owner)
        elif isinstance(type, list):
            for item in self.elements:
                if hasattr(item,'owner') and hasattr(item,'type') and item.type in type:
                    owners.add(item.owner)
        else:
            for item in self.elements:
                if hasattr(item,'owner') and item.type == type:
                    owners.add(item.owner)
        return owners

    def matches(self, type):
        """Returns an IncomeList consisting only of elements matching the specified Income type, assisting in filling PDFs with predefined spaces. Type may be a list"""
        if isinstance(type, list):
            return IncomeList(elements = [item for item in self.elements if item.type in type])
        else:
            return IncomeList(elements = [item for item in self.elements if item.type == type])

    def total(self, period_to_use=1, type=None,owner=None):
        """Returns the total periodic value in the list, gathering the list items if necessary.
        You can specify type, which may be a list, to coalesce multiple entries of the same type.
        Similarly, you can specify owner."""
        self._trigger_gather()
        result = 0
        if period_to_use == 0:
            return(result)
        if type is None:
            for item in self.elements:
                #if self.elements[item].exists:
                result += Decimal(item.gross(period_to_use=period_to_use))
        elif isinstance(type, list):
            for item in self.elements:
                if item.type in type:
                    if owner is None:
                        result += Decimal(item.gross(period_to_use=period_to_use))
                    else:
                        if item.owner == owner:
                            result += Decimal(item.gross(period_to_use=period_to_use))
        else:
            for item in self.elements:
                if item.type == type:
                    if owner is None:
                        result += Decimal(item.gross(period_to_use=period_to_use))
                    else:
                        if item.owner == owner:
                            result += Decimal(item.gross(period_to_use=period_to_use))
        return result





