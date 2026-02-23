#!/usr/bin/env python3
"""
fix_json_quotes.py -- Auto-fix unescaped double quotes inside JSON string values.

Problem: The Write tool converts Chinese typographic quotes "..." (U+201C/U+201D)
to ASCII double quotes ", breaking JSON validity when those quotes appear inside
string values.

Solution: A state-machine parser that identifies whether each " is a structural
JSON delimiter or an inner content quote, and escapes the latter.

Usage:
    python3 fix_json_quotes.py <input.json>               # fix in-place
    python3 fix_json_quotes.py <input.json> <output.json> # write to separate file
"""

import sys
import json


def fix_json_quotes(text):
    """Fix unescaped double quotes inside JSON string values.

    Uses a character-by-character state machine.  Within a string, a " is
    treated as the *end* of the string only when the next non-whitespace
    character is one of the valid JSON post-string tokens: , } ] : newline.
    Otherwise the " is treated as inner content and escaped with backslash.
    """
    result = []
    i = 0
    in_string = False
    escape_next = False

    while i < len(text):
        c = text[i]

        # If the previous character was a backslash, pass this char through
        # regardless (it is already escaped).
        if escape_next:
            result.append(c)
            escape_next = False
            i += 1
            continue

        # Backslash: toggle escape flag and pass through.
        if c == '\\':
            result.append(c)
            escape_next = True
            i += 1
            continue

        if not in_string:
            # Outside a string: only " can open one.
            if c == '"':
                in_string = True
            result.append(c)
        else:
            # Inside a string: check whether this " closes it or is inner content.
            if c == '"':
                # Peek at next non-whitespace character.
                j = i + 1
                while j < len(text) and text[j] in ' \t':
                    j += 1
                next_char = text[j] if j < len(text) else ''

                # Valid JSON post-string tokens (ASCII only):
                # ,  next element in object/array
                # }  end of object
                # ]  end of array
                # :  key-value separator (after a key string)
                # \n \r  end of line (common in pretty-printed JSON)
                if next_char in ',}]:\n\r':
                    in_string = False
                    result.append(c)
                else:
                    # Inner content quote -- escape it.
                    result.append('\\')
                    result.append(c)
            else:
                result.append(c)

        i += 1

    return ''.join(result)


def main():
    if len(sys.argv) < 2:
        print("Usage: fix_json_quotes.py <input.json> [output.json]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file

    with open(input_file, 'r', encoding='utf-8') as f:
        original = f.read()

    fixed = fix_json_quotes(original)

    # Validate the result.
    try:
        data = json.loads(fixed)
        chapters = data.get('chapters', data.get('citations', []))
        print("OK  JSON valid after fix (%d top-level items)" % len(chapters))
    except json.JSONDecodeError as e:
        print("ERR Still invalid after fix: %s" % e, file=sys.stderr)
        # Print context around the error for debugging.
        lines = fixed.split('\n')
        err_line = e.lineno - 1
        for idx in range(max(0, err_line - 1), min(len(lines), err_line + 2)):
            print("  L%d: %s" % (idx + 1, lines[idx][:120]), file=sys.stderr)
        sys.exit(1)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed)

    if output_file == input_file:
        print("    Fixed in-place: %s" % output_file)
    else:
        print("    Written to: %s" % output_file)


if __name__ == '__main__':
    main()
