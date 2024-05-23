# gpt-cv-analyser

A simple CV analyser written in Python that uses OpenAI's GPT-3 model to match a CV to a job offer.

## Installation

Before running the script, you need to install the required Python packages. You can do this by running the following command in your terminal:

```sh
pip install -r requirements.txt
```
## Usage
To run the script, you need to set your OpenAI API key as an environment variable. You can do this by running the following command in your terminal:

```sh
export OPENAI_API_KEY=value-of-apy-key
```

Then, you can run the script with the following command:
```sh
cvjoboffer.py --CV cv.txt --JO joboffer.txt
```
Replace your_api_key with your actual OpenAI API key, and cv.txt and joboffer.txt with the paths to your CV and job offer files, respectively.

## License
This project is licensed under the terms of the LICENSE file.

