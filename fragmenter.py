import unicodedata
import re

def get_number_in_base(n,base):
   convertString = "0123456789ABCDEF"
   if n < base:
      return convertString[n]
   else:
      return get_number_in_base(n//base,base) + convertString[n%base]

def generate_string_fragments(src_str, transform_functions=[lambda s: s.lower(), lambda s: s.title()]):
    tokens = src_str.strip().split(' ')
    transformed_tokens = []
    for transform in transform_functions:
        transformed_tokens.append([transform(s) for s in tokens])
    fragments = []
    base = (len(transformed_tokens)+1)
    digit_bases = [get_number_in_base(digit_value, base) for digit_value in range(1, base)]
    for permutation in range(0, base**(len(tokens))):
        assignment = get_number_in_base(permutation, base).zfill(len(tokens))
        fragment = []
        for digit_idx, digit in enumerate(assignment):
            for digit_value_idx, digit_value in enumerate(digit_bases):
                if digit == digit_value:
                    fragment.append(transformed_tokens[digit_value_idx][digit_idx])
        if len(fragment) != 0:
            fragments.append(' '.join(fragment))
    return fragments

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = str(unicodedata.normalize('NFKD', value).encode('ascii', 'ignore'))
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '-', value))

    return value
