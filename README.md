# Amplitude Project

The Amplitude Project is using Amplitude's Export API (https://amplitude.com/docs/apis/analytics/export) to bring back data of the TIL website interactions.

This data includes PII, such as IP addresses, geographical data, to user ids and therefore have not been committed to the repo.

This particular script brings back the website traffic data from the previous day, where this data can then be used to understand how visitors use our website.

This can then be investigated to understand behaviours and identify potential pain points and hotspots to configure our website further.

# Table of Contents
### 1. [Extract](#getting-started)
### 2. [Load](#example2)
### 3. [Transform](#third-example)

<a id="getting-started"></a>

# Extract
This stage of the project was used to consolidate understanding of Python, combining separate elements from various Python projects we had done over the few days to call the API and to save that data locally.

## Getting Started

First, all documentation should be read: https://amplitude.com/docs/apis/analytics/export

This provides a better understanding of the API and how it works, and this then helps with planning and accommodating.

### Setting up the project

First we need to create a new branch:

```
git switch -c extract-branch
```

Then create the virtual environment and activate it:

```
python -m venv .venv

.venv/Scripts/activate
```

Then all required packages can be installed, we will need requests (to call the API) and the dotenv package (to call the .env file):

```
pip install requests

pip install python-dotenv
```

Next up is to create the .env file and putting the AMP API and AMP key in there.


