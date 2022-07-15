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

### Variables

This project uses `python-dotenv` library. This expects a file called `.env` which contains the environment variables. An example `.env` has been included in `.env.example`.

| Variable     | Type   | Description                                | Example                  |
| :----------- | :----- | :----------------------------------------- | :----------------------- |
| TFCB_URL     | string | Protocol and domain for API calls          | https://app.terraform.io |
| TFCB_ORG     | string | Name of the TFCB Organization              | example_org              |
| TFCB_API_KEY | string | API key created in TFCB                    | a1b2c3d4                 |
| OUTPUT_DIR   | string | name of directory to write the output file | output                   |


### Local Execution

Virtual environments are highly recommended for local execution. A Pipfile is included if you are using (pipenv)[https://pipenv.pypa.io/en/latest/]. If you are not using pipenv you can create a virtual environment using the default (venv)[https://docs.python.org/3/library/venv.html].

If you are creating a virtual environment using venv you will need to install the dependancies: `pip install -r requirements.txt`

After creating the `.env` file and virtual environment you can run the script by typing in `python main.py`.

### Docker Execution

A Docker file is included to simplify Python and its dependencies.

To build the image: `docker build -t drift_container .`

To run the image: `docker run -v $(pwd):/home/devuser -ti drift_container`

The -v will mount the local directory to the /home/devuser directory. This will allow the container to read and write from the local directory where the script resides.

After launching the docker container type in `python main.py` to run the script.
