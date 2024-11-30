import re

def extract_dates(text):
    date_patterns = [
        # dd-mm-yyyy, dd.mm.yyyy, dd/mm/yyyy
        r'\b(?P<day1>0?[1-9]|[12][0-9]|3[01])[-./](?P<month1>0?[1-9]|1[0-2])[-./](?P<year1>(19|20)?\d{2})\b',
        # Month dd yyyy
        r'\b(?P<month2>[A-Za-z]+)\s+(?P<day2>0?[1-9]|[12][0-9]|3[01])\s+(?P<year2>(19|20)?\d{2})\b',
        # ddth Month yyyy
        r'\b(?P<day3>0?[1-9]|[12][0-9]|3[01])(st|nd|rd|th)?\s+(?P<month3>[A-Za-z]+)\s+(?P<year3>(19|20)?\d{2})\b',
        # yyyy-mm-dd
        r'\b(?P<year4>(19|20)?\d{2})[-./](?P<month4>0?[1-9]|1[0-2])[-./](?P<day4>0?[1-9]|[12][0-9]|3[01])\b'
    ]

    # combining all the patterns
    combined_pattern = '|'.join(date_patterns)
    matches = re.finditer(combined_pattern, text)


    valid_dates = []
    for match in matches:
        day = match.group('day1') or match.group('day2') or match.group('day3') or match.group('day4')
        month = match.group('month1') or match.group('month2') or match.group('month3') or match.group('month4')
        year = match.group('year1') or match.group('year2') or match.group('year3') or match.group('year4')

        if validate_date(day, month, year):
            valid_dates.append(f"{day}-{month}-{year}")
    return valid_dates


def validate_date(day, month, year):
    """
    validates the extracted date components for logical correctness.
    """
    if not day or not month or not year:
        return False

    # Convert to integers where applicable
    day = int(day) if day.isdigit() else None
    year = int(year)

    # Handle two-digit years by assuming 1900-2099 range
    if year < 100:
        year += 1900 if year > 22 else 2000

    # Convert month name to number if necessary
    if not month.isdigit():
        month = convert_month_to_number(month)
    else:
        month = int(month)

    # Validate ranges
    if not (1 <= month <= 12):
        return False

    # Days in months (February has 29 days in leap years)
    days_in_month = [31, 29 if is_leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= day <= days_in_month[month - 1]


def convert_month_to_number(month_name):
    """
    Converts a month name (e.g., 'January') or abbreviation (e.g., 'Jan') to its corresponding number (1-12).
    """
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12,
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    return months.get(month_name.lower())


def is_leap_year(year):
    """
    Determines whether a given year is a leap year.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# Example text with various date formats
text = """
Mr. XYZ was admitted in the critical care unit on Apr 17 2023 and diagnosed with liver cirrhosis,
but referred to the Gastroenterology department on 19th April 2023. Later he was diagnosed
with low haemoglobin on 9/01/2024.

mr. XYZ was admitted in the critical care unit on March 17 23 and diagnosed with liver cirrhosis,
but referred to the Gastroenterology department on 19th june 2023. Later he was diagnosed
with low haemoglobin on 9/01/2024. and 4th december 2025 he came back for another test

Mr. XYZ was admitted in the critical care unit on 2023 March 12th and diagnosed with liver cirrhosis,
but referred to the Gastroenterology department on 34/9/23. Later he was diagnosed
with low haemoglobin on 9/01/2024.


"""

# Extract and print valid dates
extracted_dates = extract_dates(text)
print("Extracted Dates:")
for date in extracted_dates:
    print(date)

"""
output Extracted Dates:
17-Apr-2023
19-April-2023
9-01-2024
17-March-23
19-june-2023
9-01-2024
4-december-2025
23-9-34
9-01-2024


##it did not extracted 34/9/23
"""