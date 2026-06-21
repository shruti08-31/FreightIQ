import pdfplumber
import pandas as pd
import re

MECH_PDF = "MECHANICAL_TRUCKS.pdf"
HYD_PDF = "HYDRAULIC_CATEGORIES.pdf"

# =====================================================
# HELPERS
# =====================================================

def normalize_name(name):
    name = name.lower()

    replacements = [
        ("m/s", ""),
        ("pvt. ltd.", ""),
        ("pvt ltd", ""),
        ("limited", ""),
        ("ltd.", ""),
        ("ltd", ""),
        ("corporation", ""),
        ("(p)", ""),
        (",", "")
    ]

    for old, new in replacements:
        name = name.replace(old, new)

    return " ".join(name.split())


def update_if_present(record, field, value):
    if value and str(value).strip():
        if not record.get(field):
            record[field] = value


# =====================================================
# MASTER DICTIONARY
# =====================================================

transporters = {}

# =====================================================
# MECHANICAL TRANSPORTERS
# =====================================================

mechanical_transporters = [
    "Associated Road Carriers Ltd.",
    "Awagaman Road Carriers Limited",
    "Bharatiya Roadlines Pvt. Ltd.",
    "CJ Darcl Logistics Ltd.",
    "Saket Road Carriers Pvt. Ltd.",
    "South Assam Roadways Ltd.",
    "OM Sai Logistics",
    "ESSEL Transport Pvt. Ltd.",
    "New Kumar Transport Corporation",
    "Shailsuta Logistics Pvt. Ltd."
]

# =====================================================
# READ MECHANICAL PDF
# =====================================================

with pdfplumber.open(MECH_PDF) as pdf:

    iba_text = pdf.pages[1].extract_text() or ""

    contact_text = ""

    for page in pdf.pages[2:]:
        txt = page.extract_text() or ""
        contact_text += "\n" + txt

# =====================================================
# INITIAL RECORDS
# =====================================================

for name in mechanical_transporters:

    transporters[normalize_name(name)] = {
        "Category": "Mechanical",
        "Transporter": name,
        "Address": "",
        "Phone": "",
        "Email": "",
        "MSME Status": "",
        "IBA Code": "",
        "IBA Validity": ""
    }

# =====================================================
# CONTACT BLOCKS
# =====================================================

positions = []

for name in mechanical_transporters:

    aliases = [
        name,
        name.replace(" Pvt. Ltd.", ""),
        name.replace(" Limited", ""),
        name.replace(" Ltd.", "")
    ]

    found = False

    for alias in aliases:

        m = re.search(
            re.escape(alias),
            contact_text,
            flags=re.I
        )

        if m:
            positions.append((m.start(), name))
            found = True
            break

positions.sort()

phone_pattern = (
    r'(?:\+91[- ]?)?[6-9]\d{9}'
    r'|'
    r'\d{3,5}[- ]?\d{5,8}'
)

for i, (start_pos, name) in enumerate(positions):

    end_pos = (
        positions[i + 1][0]
        if i < len(positions) - 1
        else len(contact_text)
    )

    block = contact_text[start_pos:end_pos]

    phones = sorted(set(
        re.findall(phone_pattern, block)
    ))

    emails = sorted(set(
        re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            block
        )
    ))

    lines = [
        x.strip()
        for x in block.split("\n")
        if x.strip()
    ]

    address_lines = []

    for line in lines[1:]:

        if "@" in line:
            break

        if re.search(phone_pattern, line):
            continue

        address_lines.append(line)

    address = " ".join(address_lines)

    key = normalize_name(name)

    update_if_present(
        transporters[key],
        "Address",
        address
    )

    update_if_present(
        transporters[key],
        "Phone",
        ", ".join(phones)
    )

    update_if_present(
        transporters[key],
        "Email",
        ", ".join(emails)
    )

# =====================================================
# MECHANICAL IBA TABLE
# =====================================================

for line in iba_text.split("\n"):

    m = re.search(
        r'^\d+\.\s+(.*?)\s+'
        r'(NON-MSE|MSE \(Small\)|MSE \(Medium\))\s+'
        r'([A-Z]{3}-\d+)\s+'
        r'([\d/-]+)',
        line
    )

    if not m:
        continue

    name = m.group(1).strip()

    msme = m.group(2)
    iba = m.group(3)
    validity = m.group(4)

    target = normalize_name(name)

    for key in transporters:

        if target in key or key in target:

            update_if_present(
                transporters[key],
                "MSME Status",
                msme
            )

            update_if_present(
                transporters[key],
                "IBA Code",
                iba
            )

            update_if_present(
                transporters[key],
                "IBA Validity",
                validity
            )

# =====================================================
# HYDRAULIC PDF
# =====================================================

hyd_text = ""

with pdfplumber.open(HYD_PDF) as pdf:

    for page in pdf.pages:
        hyd_text += "\n" + (page.extract_text() or "")

pattern = re.compile(
    r'(\d+)\s+(.*?)\s+'
    r'(Small|Medium|NON-MSE)\s+'
    r'([A-Z]{3}-\d+)\s+'
    r'(\d{2}\.\d{2}\.\d{4})'
)

for m in pattern.finditer(hyd_text):

    name = m.group(2).strip()

    transporters[normalize_name(name)] = {
        "Category": "Hydraulic",
        "Transporter": name,
        "Address": "",
        "Phone": "",
        "Email": "",
        "MSME Status": m.group(3),
        "IBA Code": m.group(4),
        "IBA Validity": m.group(5)
    }

# =====================================================
# EXPORT CSV
# =====================================================

df = pd.DataFrame(
    transporters.values()
)

df = df.sort_values(
    ["Category", "Transporter"]
)

df.to_csv(
    "Transporter_Details.csv",
    index=False,
    encoding="utf-8-sig"
)

print("=" * 80)
print("CSV GENERATED")
print("=" * 80)

for _, row in df.iterrows():
    print(
        row["Transporter"],
        "| Phones:",
        row["Phone"]
    )

print("\nTotal Transporters:", len(df))
print("Output: Transporter_Details.csv")