# TFCB Drift Detection Report

This project will search a TFCB organization and report on workspaces where drift is enabled or disabled. If the workspace is configured for drift it will report if drift has been detected and when the last run occured.

It will output a csv report with the workspace name, if drift is configured on the workspace, has drift been detected, and the last time drift was checked.

An example of the output:
```csv
workspace_name,drift_configured,drift_detected,drift_last_checked
azure_basic_synk_infracost,True,False,
test,False,,
api-test,False,,
azure_basic_bridgecrew,False,,
cli_workflow,False,,
github_action_demo,False,,
tf_packer_demo,False,,
hashicat-azure,False,,
terraform_esxi,False,,
tf_module_test,False,,
generate_aws_creds,False,,
```

### Requirements

Developed on `python==3.10.4`

Python dependancies documented in `requirements.txt`

### Execution

This project uses `python-dotenv` library. This expects a file called `.env` which contains the environment variables. An example `.env` has been included in `.env.example`.

| Variable     | Type   | Description                                | Example                  |
| :----------- | :----- | :----------------------------------------- | :----------------------- |
| TFCB_URL     | string | Protocol and domain for API calls          | https://app.terraform.io |
| TFCB_ORG     | string | Name of the TFCB Organization              | example_org              |
| TFCB_API_KEY | string | API key created in TFCB                    | a1b2c3d4                 |
| OUTPUT_DIR   | string | name of directory to write the output file | output                   |

After creating the `.env` file you can run the script by typing in `python main.py`.
