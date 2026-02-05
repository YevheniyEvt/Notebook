import bleach

# Const for  sanitizing the HTML with bleach
ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + ['p', 'pre', 'code', 'span', 'div', 'br', 'hr']
ALLOWED_ATTRS = {'span': ['class'], 'code': ['class']}