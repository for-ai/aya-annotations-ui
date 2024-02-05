# Team Scripts

## `add_dataset.py`

This script allows users to add a dataset to the `dataset` table along with randomly sampled prompt-completion pairs to the `task` table.


To run the script you must have:

1. An env file. Create a file called `.env.team-instruct-multilingual-app.prod` in this directory.

2. The production database URI and Discord webhook URL. You can retrieve them from GCP and going to `Secrets Manager`, clicking on `TEAM_INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD` / `DISCORD_ALERTS_WEBHOOK_URL`, then clicking the `Actions` button and `View Secret Value`. Copy the value to your `.env` file:
```python
TEAM_INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD=<secret>
DISCORD_ALERTS_WEBHOOK_URL=<secret>
```

3. A working Python environment with >= Python 3.10. Run `pip install -r requirements.txt` using the requirements file in this directory.

4. The dataset files on-disk. 

- If using your local machine and the dataset is relatively small (< 10GB) you must ensure that:
  - you [install gcloud CLI](https://cloud.google.com/sdk/docs/install#deb)
  - the IP address of the URI in your `.env` file is the **public** IP address of our database (check Cloud SQL to confirm or DM the UI team)
- If using a GCP VM (see `#gcp-cloud-users` in Discord for setup), you must ensure that:
  - the VM is in `us-east1` where our Cloud SQL instance is hosted
  - the IP address of the URI in your `.env` file is the **private** IP address of our database (check Cloud SQL or DM the UI team)

5. If using your local machine, then you need the ability to connect to Cloud SQL
  - Download and set up Cloud SQL Auth Proxy: https://cloud.google.com/sql/docs/postgres/connect-auth-proxy#tcp-sockets
  - Swap the public IP address of the `TEAM_INSTRUCT_MULTILINGUAL_APP_DB_URI_PROD` value with `127.0.0.1`

You can then run:

```console
gsutil -m cp gs://BUCKET_NAME/OBJECT_NAME LOCAL_DIR
```

replacing `BUCKET_NAME`, `OBJECT_NAME`, and `LOCAL_DIR` with the names you're using.

**ASSUMPTIONS:** 
- The data is assumed to be (read: must be) in the following format within the directories: `<original-dataset-name>/<fromlanguage>_<charset>_to_<tolanguage>_<charset>/<model-name>/<template-name>/<date>/<split>.<jsonl_or_csv>`
  - `fromlanguage` and `tolanguage` can be the same if the model isn't translated
  - `template-name` can be a reasonable name like `no-template` if it doesn't use a template
  - `model-name` can be a name like `no-model` is no model was used

If you need to see an example, plese view the `team3` datasets buckets in Cloud Storage.


**Run the script**: If you made it this far you should be able to run the script. Try:

```console
python -m add_dataset
```

And you should see the following output:

```console
Usage: python -m add_dataset.py [OPTIONS]

Options:
  --dataset-dir TEXT              The directory containing the datasets
                                  [required]
  --sample-size INTEGER           The number of lines to sample from each
                                  dataset file  [default: 1000]
  --add-full-dataset              Whether or not to add an entire dataset to
                                  the database
  --task-type [audit_translation|audit_xp3|audit_crowdsourced_data]
                                  The type of task to create  [required]
  --splits [train|validation|test|all]
                                  The splits to load into the database. Can
                                  specify more than one.Use "all" to load all
                                  splits.  [required]
  --file-type [jsonl|csv]         The type of file to load  [required]
  --translated                    Whether the dataset was translated by C4AI
  --templated                     Whether the dataset was generated using a
                                  template
  --prompt-key TEXT               Key to read in .jsonl files that maps to the
                                  prompt value. "e.g.
                                  {"meaning_representation": <prompt>}
                                  [default: inputs]
  --completion-key TEXT           Key to read in .jsonl files that maps to the
                                  completion value. "e.g. {"human_reference":
                                  <completion>}  [default: targets]
  --dry-run                       Whether to perform a dry run (i.e. do not
                                  insert into the database)
  --help                          Show this message and exit.
```

**NOTEs:** 
- `--templated` and `--translated` should be here only if the dataset was templated and/or translated by our teams
- `--prompt-key` and `--completion-key` should be used if the dataset has different names for prompts and completions, other than `inputs` and `targets`
- `--task-type` should be `audit_translation` if the prompt-completion pairs were translated (team 3), `audit_xp3` if the data comes from xP3 directly (team 2), or `audit_crowdsourced_data` if the data comes from the Aya Discord server
- If you're running the script from your personal machine:
  - You should have a stable internet connection (ethernet is best)
  - You should expect the script to take ~30 minutes or less for datasets of size 5GB or less

You can run the script with the following options to do a dry run (no inserts):

```console
python -m add_dataset \
--dataset-dir sampledata/ \
--sample-size 100 \
--task-type audit_translation \
--splits all \
--file-type jsonl \
--templated \
--translated \
--dry-run
```

If you see a lot of errors, you can run:

```console
python -m add_dataset \
--dataset-dir sampledata/ \
--sample-size 100 \
--task-type audit_translation \
--splits all \
--file-type jsonl \
--templated \
--translated \
--dry-run \
>> out.log 2>&1
```

to get the output in a log file. Please send this log file along with any questions to Team 1.

Otherwise, look at the summary report and if it looks good then remove the `--dry-run` flag and run it again.
