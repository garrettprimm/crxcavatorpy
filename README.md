# Crxcavatorpy

A python package for working with the CRXCavator api as an imported package or as a command line utility

# Installation

```
pip install crxcavatorpy
```

# CLI Usage

## Get a single report
```
# Generic Use
python3 -m crxcavator report <extension_id> <extension_version>

# Example Use
python3 -m crxcavator report aapbdbdomjkkjkaonfhkkikfgjllcleb 2.0.13

```
# Example Output for a single extension report
[report-output.json](docs/report-output.json)


## Get all reports for an extension
```
# Generic Use
python3 -m crxcavator reports <extension_id>

# Example Use
python3 -m crxcavator reports aapbdbdomjkkjkaonfhkkikfgjllcleb

```
### Example Output for all reports for a single extension
[all-reports-output.json](docs/all-reports-output.json)
## Submit an extension to be scanned
```
# Generic Use
python3 -m crxcavator submit <extension_id>

# Example Use
python3 -m crxcavator submit aapbdbdomjkkjkaonfhkkikfgjllcleb

```
### Example Output for extension scan submission
```json
{
  "code": 801,
  "extensionID": "aapbdbdomjkkjkaonfhkkikfgjllcleb",
  "message": "Extension successfully submitted",
  "platform": "Chrome",
  "version": "2.0.13"
}
```