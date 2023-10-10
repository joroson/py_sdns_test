## Requirements

This script is dependent on the `dnspython` package. This can be pip installed with the following command

`pip install -r requirements.txt`

## Running

The variables for the test are passed when the script is invoked. The arguments that must be provied are:

**--dns_server**:The SDNS server that the test should use

**--fqdn**:The fully qualified domain name for the test.

**--num_requests**:The number of requests to be sent to the SDNS server

**--concurrency**:The number of threads for the process

Example:

`python dnstest.py --dns_server 172.16.1.254 --fqdn gslb.blinky.light --num_requests 50000 --concurrency 50
`

## Results

This will generate a json file that contains all the test results, it will be located in the same place that the test
was run from. The filename also contains some information about the test run.

`4743-rps_10-art_50000-rqusts_50-thrds_gslb.blinky.light_joe-mbp.local.json`