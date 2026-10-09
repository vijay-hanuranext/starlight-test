# Running the Starlight Tests in GitHub Actions

Written for: the live demo. Screenshot spots are marked **[SCREENSHOT]**.

## The Problem

Right now the tests only run when one of us remembers to run them, on our own laptop.
Somebody merges a change on Friday evening and nobody runs the suite. On Monday the login is broken and nobody knows which change did it.

I want the tests to run by themselves every time code lands on a release branch, on a clean machine, so the answer is waiting for us when we look.

That is what CI does. Here I use GitHub Actions because the code is already on GitHub, so there is nothing extra to sign up for.

## What We Built

One file does it all: `.github/workflows/tests.yml`. GitHub reads every file in that folder.

**[SCREENSHOT 1]** The file open in the repo on GitHub, on the `release/day-5-demo` branch.

## How To Create a New Workflow

A workflow is just a text file in `.github/workflows/`. There is nothing to install. You can make it two ways.

**In the browser.** On the repo, open the **Actions** tab and click **New workflow**, then **set up a workflow yourself**. GitHub opens an editor with a blank file. When you commit it, make sure you pick the `release/day-5-demo` branch in the commit box, not `main`.

**On your laptop.** Create the folder and the file yourself, commit, and push.

**[SCREENSHOT 0]** The Actions tab, New workflow, and the blank editor.

I always start with a tiny file that only proves GitHub is running something.

```yaml
name: Hello CI
on: workflow_dispatch
jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Hello from GitHub"
```

Commit it, click **Run workflow**, and watch it go green. Now we know the machinery works, and we add one piece at a time:

1. Change `on:` so it starts on a push to `release/**`.
2. Add `actions/checkout@v4` as the first step, so the machine has our code.
3. Add `actions/setup-python@v5` and `pip install -r requirements.txt`.
4. Add `playwright install --with-deps chromium`.
5. Add the secrets and the two URLs under `env:`.
6. Add `pytest --html=report.html --self-contained-html`.
7. Add `actions/upload-artifact@v4` with `if: always()` so we keep the report.

Run it after each piece. If one breaks, you know exactly which line did it. The next steps explain each piece in turn.

## Step 1: Decide When It Runs

```yaml
on:
  push:
    branches: ["release/**"]
  pull_request:
    branches: ["release/**"]
  workflow_dispatch:
```

I only want it on release branches. A merge into a branch counts as a push to that branch, so merging the feature branch into `release/day-5-demo` starts the run. `workflow_dispatch` adds a Run workflow button for when I want to start it by hand.

## Step 2: Give It the Login (Secrets)

The tests log in to the CRM. I don't want that password sitting in the code, and my `.env` file is not in git, so the clean machine won't have it.

In the repo: Settings, Secrets and variables, Actions. I added two secrets, `CRM_USERNAME` and `CRM_PASSWORD`. GitHub hides the values after you save them.

**[SCREENSHOT 2]** The Secrets page showing both names (the values are hidden).

The workflow hands them to the tests as environment variables, the same names the `.env` file uses. `BASE_URL` and `API_URL` are not secret, so they sit right in the file.

## Step 3: The Steps the Machine Follows

The machine starts completely empty, so we tell it everything, in order.

| Step | What it does |
|---|---|
| `actions/checkout` | Downloads our code |
| `actions/setup-python` | Installs Python 3.12 |
| `pip install -r requirements.txt` | Installs Playwright, pytest and the rest |
| `playwright install --with-deps chromium` | Installs the browser the tests drive |
| Wake the API | The API is on a free plan and goes to sleep. This knocks on the door first |
| `pytest --html=report.html` | Runs the tests and writes a report |
| `actions/upload-artifact` | Keeps the report so we can download it, even when tests fail |

I run the tests one at a time on purpose. The CRM numbers new employees by counting them, so two tests creating and deleting at once can collide.

## Step 4: Start a Run

I created `release/day-5-demo` from `main`, merged `feature/day-5-content` into it, and pushed. That push started the run.

```bash
git switch -c release/day-5-demo main
git merge --no-ff feature/day-5-content
git push -u origin release/day-5-demo
```

**[SCREENSHOT 3]** The Actions tab with the run just started (yellow dot).

## Step 5: Read the Result

Click the run, then the job called `test`. Each step has a green tick as it finishes. Open the pytest step to see the tests scroll by.

**[SCREENSHOT 4]** The job with all steps green and the pytest step expanded.

My run: **43 passed** in about 2 minutes.

Every test passed, so the run is green. If even one had failed, the whole run would turn red.

## Step 6: Download the Report

At the bottom of the run page, under Artifacts, there is `test-report`. Download it and open `report.html` for the full list of tests.

**[SCREENSHOT 5]** The Artifacts section, and the opened report.

## Step 7: Show It Catching Something

To prove it isn't just always green, push a small change to the release branch and watch a second run start by itself. If you want to show a red run, break an assertion on purpose, push, and show the red cross and the failing test in the log. Then revert it.

## If Something Goes Wrong

- **Login fails on the first test.** The secrets are missing or misspelled. They must be named exactly `CRM_USERNAME` and `CRM_PASSWORD`.
- **Import errors.** The runner only sees what is pushed. Check the file is committed.
- **The first test times out.** The API was asleep. Re-run the job.
- **Nothing starts.** The branch name must begin with `release/`.

## Next

The same four ideas (get the code, install, run, keep the report) are what Jenkins and Azure DevOps do too. Only the file format changes.
