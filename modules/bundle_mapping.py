"""OFFER_COLUMNS = {

    # DATA
    "1GB @1K": "E",
    "300MB @1K": "F",
    "165MB @1K": "G",
    "400MB @1K": "H",

    # VOICE
    "80Min @1,000": "J",
    "70Min+5SMS+5MB @1,000": "K",
    "40Min @1,000 (All Networks)": "L",
    "25Min @1,000 (All Networks)": "M",
    "40Min @1,000": "N",

}"""

# Website bundle name -> Excel bundle name
OFFER_MAPPING = {

    # ================= DATA =================
    "1GB @1K": "1 GB 1K",
    "300MB @1K": "300MB 1K",
    "165MB @1K": "165MB 1K",
    "400MB @1K": "400MB 1K",
    "5GB @1k"  : "5GB 1K",


    # ================= VOICE =================
    "80Min @1,000": "80@1000",
    "70Min+5SMS+5MB @1,000": "70@1000",
    "40Min @1,000 (All Networks)": "40Allnet@1000",
    "25Min @1,000 (All Networks)": "25allnet@1000",
    "40Min @1,000": "40mins@1000",
}

EXCEL_COLUMNS = {
    "1 GB 1K": "D",
    "300MB 1K": "E",
    "165MB 1K": "F",
    "400MB 1K": "G",
    "5GB 1K"  :  "H",

    "80@1000": "J",
    "70@1000": "K",
    "40Allnet@1000": "L",
    "25allnet@1000": "M",
    "40mins@1000": "N",
}