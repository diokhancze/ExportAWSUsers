# ExportAWSUsers
Python tool to export AWS IAM Users on the account. It will also get creation dates, last login dates, and any API keys associated with the account.

## Requirements ##
Requires Python3 and the Boto3 libraries.

## Running the Script ##
- make sure you use dedicated API key with built-in IAM Read Only role
- modify the script to add your AWS API key and Secret key
- run the script with following command:
*./exportawsusers.py*
- once the script is run, it will output file called “iam_user_accounts.txt” containing the requested information
