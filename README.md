nessusScanUploader
==================

---

nessusScanUploader is a python module to pull new scan results from a Nessus 
Manager instance and send them to an Azure storage instance (blob or file),
or an AWS api-gateway.

## Installation

Recommended to be installed as an unprivileged user on your Nessus Manager host
or another host that has access to its API.

```bash
python3 -m pip install --user nessusScanUpload-0.0.1-py3-none-any.whl
```

## Configuration

Configuration file defaults to ~/nessusScanUpload.conf
and will also look for these files on Linux:
- /etc/nessusScanUpload.conf
- ~/.nessusScanUpload

or Windows:
- nessusScanUpload.ini
- %APPDATA%/nessusScanUpload.ini

**An example configuration file:**
```
[nessus]
# Access key for an account that can read scan results
accessKey = wnimhx040msap14c5sk0ick5drtct5f2jdwpf90dkqguvqdzhhsvxku51zgwecxh
secretKey = zxx19f0126ta40c64t3qw4tr990uq67fv8gdcbi7s2hwtlfrnitfhb5oqugy1sjo
# host can be ip or name
host = nessushostname.org
port = 8834
ssl_verify = False
scheme = https

[azure]
connection_string =
# Can be a blob container or a file share folder, not both.
container =
folder = foldername

[aws]
url = 
api_key = <as advised>
repo = <as advised>
ssl_verify = False

[savefile]
path=~/nessusScanUpload.save
```

## Usage

python3 -m nessusScanUpload

## Logging

Logging is to syslog/NTEventLog depending on system platform used.
