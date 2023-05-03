import requests
import openpyxl
import pandas as pd
import sys
import os.path
import numpy as np
import json

filename = sys.argv[1]

RISK_SCORE_CACHE = "riskScoreCache.xlsx"
URL = "https://api.crxcavator.io/v1"
total_new_entries = 0

OUTPUT_JSON = []


def crxcavatorApi(extension_info, api_call):
    global total_new_entries, OUTPUT_JSON
    match api_call:
        case 0:
            # case 0 gets all reports and gets the latest report from all reports api
            try:
                fullUrl = f"{URL}/report/{extension_info[0]}"
                r = requests.get(url=fullUrl).json()
                if r == None:
                    # TODO: if none submit an extension to be analyzed
                    pass
                return r[-1]["data"]["risk"]["total"]
            except:
                return "FAIL"
        case 1:  # case 1 gets the exact report for the version of a extension
            try:
                fullUrl = f"{URL}/report/{extension_info[0]}/{extension_info[1]}"
                r = requests.get(url=fullUrl).json()
                OUTPUT_JSON.append(r)
                print(
                    f"\rExtension Lookup #{extension_info.name+1}/{total_new_entries}",
                    end="",
                )

                return r["data"]["risk"]["total"]
            except:
                return "FAIL"
        case 2:
            try:

                fullUrl = f"{URL}/submit/"
                data = {
                    "extension_id": extension_info[0],
                    "version": extension_info[1],
                }
                r = requests.post(url=fullUrl, data=data).json()
                print(r)
                OUTPUT_JSON.append(r)
                print(
                    f"\rSubmitting Unknown Extensions for Review",
                    end="",
                )

                return r
            except:
                return "FAIL"


def validateDataSchema(input_schema):
    """Read CSV with expected table schema:
    "extension_uuid",
    "extension_name",
    "extension_version",
    """

    expected_schema = set(
        [
            "extension_uuid",
            "extension_name",
            "extension_version",
        ]
    )

    input_schema = set(input_schema)

    validated_schema = expected_schema.difference(input_schema)

    if validated_schema:
        print(f"ERROR Invalid Schema: Missing Columns {validated_schema}")
        return 1
    else:
        return 0


def getExtensionId(extension_path):
    # Parse the extension_path column and return the extension_id
    try:
        extension_id = extension_path.split("\\")[-2]
        return extension_id
    except:
        return "FAIL"


def riskCacheCheck():
    # Returns true or false if the extensions cache exists
    print(f"Checking for risk score cache")
    if os.path.exists(RISK_SCORE_CACHE):
        return pd.read_excel(RISK_SCORE_CACHE)

    print(f"Creating risk score cache")
    pd.DataFrame(
        columns=["extension_uuid", "extension_version", "risk_score"]
    ).to_excel(RISK_SCORE_CACHE, index=False)
    return pd.read_excel(RISK_SCORE_CACHE)


def riskCacheCompare(dedup_df, risk_cache_df):
    # this function performs a comparison on the cache to see determine new extensions for the cache
    updated_cache_extensions_df = pd.concat(
        [
            risk_cache_df,  # data to keep
            dedup_df[  # data to add
                ~dedup_df["extension_uuid"].isin(risk_cache_df["extension_uuid"])
                & ~dedup_df["extension_version"].isin(
                    risk_cache_df["extension_version"]
                )
            ],
        ],
        ignore_index=True,
    )

    return updated_cache_extensions_df


def main(filename):
    global total_new_entries, OUTPUT_JSON
    df = pd.read_csv(filename)

    # Validate Schema
    if validateDataSchema(df.columns.array) == 1:
        return 1

    # List of deduped extensions by extension_id and extension_version
    # This list is to be used to diff the new extension+version combinations against the existing risk cache
    dedup_df = (
        df[["extension_uuid", "extension_version"]]
        .drop_duplicates(subset=["extension_uuid", "extension_version"], keep="last")
        .reset_index(drop=True)
    )

    # Load the risk cache into memory
    risk_cache_df = riskCacheCheck()

    diff_df = dedup_df[
        ~dedup_df["extension_uuid"].isin(risk_cache_df["extension_uuid"])
        & ~dedup_df["extension_version"].isin(risk_cache_df["extension_version"])
    ]

    print("deduped")

    diff_df["risk_score"] = diff_df.apply(crxcavatorApi, api_call=1, axis=1)

    risk_cache_df = risk_cache_df.merge(
        diff_df,
        on=["extension_uuid", "extension_version", "risk_score"],
        how="outer",
        suffixes=(False, False),
    )

    # Write riskcache updates to excel
    risk_cache_df.to_excel(RISK_SCORE_CACHE, index=False)

    failed_extensions_df = risk_cache_df.loc[
        risk_cache_df["risk_score"] == "FAIL"
    ].copy()
    # Submit FAIL for additional lookup
    # TODO: Fix this
    # failed_extensions_df.apply(crxcavatorApi, api_call=2, axis=1)

    # Attempt secondary check on failed lookups
    """failed_extensions_df["risk_score"] = failed_extensions_df.apply(
        crxcavatorApi, api_call=1, axis=1
    )"""

    # print(failed_extensions_df)
    # Write the actual results out to a spreadsheet
    df = df.merge(risk_cache_df, on=["extension_uuid", "extension_version"], how="left")
    df.to_csv("chromeextensions.csv", index=False)

    OUTPUT_JSON = json.dumps(OUTPUT_JSON, indent=4)
    with open("extension_data.json", "w") as outfile:
        outfile.write(OUTPUT_JSON)


exit(main(filename))
