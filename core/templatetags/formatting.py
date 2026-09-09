from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from django import template

register = template.Library()


def _to_decimal(value):
    if value is None or value == '':
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


@register.filter

def angka_id(value):
    """Format angka dengan pemisah ribuan gaya Indonesia: 42500 -> 42.500."""
    number = _to_decimal(value)
    if number is None:
        return '—'
    number = number.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return f'{number:,.0f}'.replace(',', '.')


@register.filter

def rupiah(value):
    """Format nominal Rupiah tanpa desimal: 176000000 -> Rp 176.000.000."""
    number = _to_decimal(value)
    if number is None:
        return 'Rp —'
    number = number.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return f'Rp {number:,.0f}'.replace(',', '.')


@register.filter

def desimal_id(value, digits=2):
    """Format angka desimal gaya Indonesia, mis. 12.50 -> 12,50."""
    number = _to_decimal(value)
    if number is None:
        return '—'
    digits = int(digits)
    quant = Decimal('1.' + ('0' * digits))
    number = number.quantize(quant, rounding=ROUND_HALF_UP)
    formatted = f'{number:,.{digits}f}'
    return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
