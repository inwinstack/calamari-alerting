import exceptions


BYTE_UNITS = {
    'b': 1,
    'k': 1024,
    'm': 1024 * 1024,
    'g': 1024 * 1024 * 1024
}


def parse_bytes(s):
    if len(s) == 0:
        s = 0
    else:
        if s[-2:-1].isalpha() and s[-1].isalpha():
            if s[-1] == "b" or s[-1] == "B":
                s = s[:-1]
        units = BYTE_UNITS
        suffix = s[-1].lower()

        # Check if the variable is a string representation of an int
        # without a units part. Assuming that the units are bytes.
        if suffix.isdigit():
            digits_part = s
            suffix = 'b'
        else:
            digits_part = s[:-1]

        if suffix in units.keys() or suffix.isdigit():
            try:
                digits = int(digits_part)
            except ValueError:
                message = ('Failed converting the string value for'
                           'memory ({0}) to a number.')
                formatted_message = message.format(digits_part)
                raise exceptions.FormatException(formatted_message)

            s = digits * units[suffix]
        else:
            message = ('The specified value for memory'
                       ' ({0}) should specify the units. The postfix'
                       ' should be one of the `b` `k` `m` `g`'
                       ' characters')
            raise exceptions.FormatException(message.format(s))

    return s