import pandas as pd
import os, sys
import warnings

HERE = os.path.dirname(os.path.realpath(__file__))

BASE_WHD_PATH = os.path.join(HERE, "../data/whd-enforcement-database/")

data_dict = pd.read_excel(BASE_WHD_PATH + "Standard_WH_Dictionary for FOIA 773130.xls")

warnings.simplefilter(action="ignore", category=pd.io.common.DtypeWarning)
warnings.simplefilter(action="ignore", category=UserWarning)

def date_to_fy(date):
    if date.month < 10: return date.year
    else: return date.year + 1

def normalize_string(x):
    return (x or "").upper().strip()

def load_table(path, tbname, **kwargs):
    """
    Given a table's path and name, load that table from the WHD database.
    """
    whd_table_cols = data_dict.groupby("TBNAME")["DATAELEMENT"].apply(list)
    translated = pd.read_csv(path, sep="|", header=None,
        names=whd_table_cols.ix[tbname], encoding="cp1252",
        **kwargs)
    return translated

def load_employers():
    """
    Load employer info, and standardize employer ID
    """
    employers = load_table(BASE_WHD_PATH + "case_employer.txt", "CASE_EMPLOYER")

    # If EIN not supplied, use "Legal Name" or "Trade Name"
    eins_to_replace = [
        "EIN Missing",
        "Owner SSN",
        "ER Refused",
        "Conciliated",
        "Dropped",
        "99-9999999",
        "11-1111111",
        "00-0000000",
        "WHMIS Unk"
    ]

    employers["employer_id"] = employers["ER_EIN"]\
        .apply(lambda x: None if x in eins_to_replace else x)\
        .fillna(employers["ER_LEGAL_NAME"])\
        .fillna(employers["ER_TRADE_NAME"])\
        .fillna("")\
        .apply(lambda x: x.strip())

    return employers

def date_parser(x):
    return pd.to_datetime(x, format="%Y%m%d", errors="coerce")

def load_cases():
    """
    Load top-level data on each case.
    """
    date_cols = [
        "DATE_BEG_INV_PER",
        "DATE_END_INV_PER",
        "DATE_REGISTERED",
        "DATE_CONCLUDED"
    ]

    # Parse table
    _cases = load_table(BASE_WHD_PATH + "kase.txt", "KASE",
        parse_dates=date_cols,
        date_parser=date_parser)

    # Get years
    for col in date_cols:
        _cases[col + "_YEAR"] = _cases[col].apply(lambda x: x.year)
        _cases[col + "_FY"] = _cases[col].apply(date_to_fy)

    invest_tools = load_table(BASE_WHD_PATH + "v_invest_tools.txt", "V_INVEST_TOOLS")

    cases = _cases.set_index("INVEST_TOOL_ID")\
        .join(invest_tools.set_index("INVEST_TOOL_ID")[["INVEST_TOOL_DESC"]])\
        .reset_index()

    return cases

def load_act_summaries():
    act_summaries = load_table(BASE_WHD_PATH + "case_act_summary.txt", "CASE_ACT_SUMMARY")
    act_summaries["ACT_ID"] = act_summaries["ACT_ID"].apply(normalize_string)
    return act_summaries

def load_violations():
    """
    Load all the violations, add details from other tables,
    and identify non-violation rows.
    """
    viol_path = BASE_WHD_PATH + "case_act_eer_viol.txt"
    viol_detail_path = BASE_WHD_PATH + "v_act_violations.txt"
    comply_path = BASE_WHD_PATH + "v_comply_status.txt"

    date_cols = [
        "DATE_BEG_VIOL",
        "DATE_END_VIOL",
    ]

    _violations = load_table(viol_path, "CASE_ACT_EER_VIOL",
        parse_dates=date_cols,
        date_parser=date_parser)

    # Get years
    for col in date_cols:
        _violations[col + "_YEAR"] = _violations[col].apply(lambda x: x.year)
        _violations[col + "_FY"] = _violations[col].apply(date_to_fy)

    _violations["ACT_ID"] == _violations["ACT_ID"].apply(normalize_string)

    viol_details = load_table(viol_detail_path, "V_ACT_VIOLATIONS")\
        .set_index("VIOLATION_ID")[[ "VIOLATION_NO", "VIOLATION_DESC" ]]

    violations = _violations\
        .set_index("VIOLATION_ID").join(viol_details)\
        .reset_index()

    violations["whd_ee_violation_found"] = (
        ~violations["VIOLATION_NO"].isin([ "00", "00 F", "NC" ]) &
        ~violations["VIOLATION_TYPE"].isin([ "NR" ]) &
        (violations["ER_EE_VIOL"] == "E")
    )

    violations["violation_found"] = (
        ~violations["VIOLATION_NO"].isin([ "00", "00 F", "NC" ]) &
        ~violations["VIOLATION_TYPE"].isin([ "NR" ]) &
        ~(violations["COMPLIANCE_STATUS"].isin([ 1, 4 ]))
        # 1: "Compliance (no violations found)"
        # 4: "Not Applicable"
    )

    # Make sure that we haven't introduced extra rows
    assert(len(violations) == len(_violations))

    return violations

if __name__ == "__main__":
    """
    Make sure that we're counting violations the same as WHD does.
    """
    sys.stderr.write("Loading cases...\n")

    cases = load_cases().set_index("CASE_ID")

    sys.stderr.write("Loading summaries...\n")

    act_summaries = load_act_summaries().set_index("CASE_ID")

    sys.stderr.write("Loading violations...\n")

    violations = load_violations().set_index("CASE_ID")\
        .join(cases[[ "DATE_REGISTERED_FY" ]])\
        .reset_index()

    sys.stderr.write("Running tests...\n")

    ee_comparison = pd.DataFrame({
        "from_violations": violations[
            violations["whd_ee_violation_found"] == True
        ].groupby("CASE_ID")["CASE_EER_ID"].nunique(),
        "from_cases":  cases["UNDUP_EES_VIOLATED"],
        "DATE_REGISTERED_FY": cases["DATE_REGISTERED_FY"]
    }).fillna(0)

    ee_mismatches = ee_comparison[
        (ee_comparison["from_violations"] != ee_comparison["from_cases"]) &
        (ee_comparison["DATE_REGISTERED_FY"] > 2003)
    ]

    assert(len(ee_comparison) > 0)
    assert(len(ee_comparison) == len(cases))
    assert(len(ee_mismatches) == 10)

    ee_mismatch_summaries = act_summaries.ix[ee_mismatches.index]
    ee_mismatch_acts = ee_mismatch_summaries["ACT_ID"].value_counts()
    assert(("FLSA" in ee_mismatch_acts.index) and (ee_mismatch_acts["FLSA"] > 0))
    assert("H2A" not in ee_mismatch_acts.index)
    assert("H2B" not in ee_mismatch_acts.index)

    ttl_comparison = pd.DataFrame({
        "from_violations": violations[
            violations["violation_found"] == True
        ].groupby("CASE_ID")["NUM_EES_REPRESENTD"].sum(),
        "from_cases": cases["TTL_CASE_VIOLATION"],
        "DATE_REGISTERED_FY": cases["DATE_REGISTERED_FY"]
    }).fillna(0)

    ttl_mismatches = ttl_comparison[
        (ttl_comparison["from_violations"] != ttl_comparison["from_cases"]) &
        (ttl_comparison["DATE_REGISTERED_FY"] > 2003)
    ]

    assert(len(ttl_comparison) > 0)
    assert(len(ttl_comparison) == len(cases))
    assert(len(ttl_mismatches) == 163)
    ttl_diff = (ttl_mismatches["from_cases"] - ttl_mismatches["from_violations"]).abs().sum()
    assert(ttl_diff == 255)
