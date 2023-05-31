import argparse

from crxcavator import api


def main():
    main_parser = argparse.ArgumentParser(
        prog="crxcavator",
        description="""
                        CLI utility for doing lookups against the crxcavator
                        api
                        https://crxcavator.io/apidocs
                        """,
        add_help=False,
    )

    main_parser.add_argument(
        "action",
        choices=["report", "reports", "submit"],
        help="Select one of the available actions",
    )

    main_args, _ = main_parser.parse_known_args()

    parser = argparse.ArgumentParser(parents=[main_parser])

    if main_args.action in ["reports", "submit"]:
        parser.add_argument(
            "extension_id", help="The extension id of the extension", type=str
        )
        args = parser.parse_args()

        if main_args.action == "reports":
            report = api.get_all_reports(args.extension_id)
            print(report)

        if main_args.action == "submit":
            submission_status = api.submit_extension(args.extension_id)
            print(submission_status)

    elif main_args.action == "report":
        parser.add_argument(
            "extension_id",
            help="The extension id of the extension",
            type=str
        )
        parser.add_argument(
            "extension_version",
            help="The extension version of the extension",
            type=str
        )
        args = parser.parse_args()
        reports = api.get_report(
            args.extension_id, args.extension_version)
        print(reports)


if __name__ == "__main__":
    main()
