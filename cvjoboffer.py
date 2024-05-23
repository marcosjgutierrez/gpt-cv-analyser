#!/usr/bin/env python3
import os
import sys
import argparse
import openai
import re

# Definition of Contants values.
GPT_MODEL= "gpt-3.5-turbo"

# Get the OpenAI API key
openai_api_key = os.environ.get('OPENAI_API_KEY')

# Check if the API key is found
if openai_api_key is None:
    sys.exit("API key not found")
else:
    print("API key found")
    print("Using GPT model:", GPT_MODEL)


def preprocess_text(text):
    # Remove special characters
    text = re.sub(r'\W', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Convert text to lowercase
    text = text.lower()
    
    return text






# Function to validate the CV and job offer files
def validate_files(cv_file, job_offer_file):
    # Open and preprocess CV file
    try:
        with open(cv_file, 'r') as cv:
            cv_contents = cv.read()
            cv_contents = preprocess_text(cv_contents)
    except FileNotFoundError:
        print(f"Error: {cv_file} does not exist.")
        return False
    
    # Open and preprocess job offer file
    try:
        with open(job_offer_file, 'r') as job_offer:
            job_offer_contents = job_offer.read()
            job_offer_contents = preprocess_text(job_offer_contents)
    except FileNotFoundError:
        print(f"Error: {job_offer_file} does not exist.")
        return False
    
    return cv_contents, job_offer_contents


job_prompt = """You are an AI assistant tasked with comparing a CV against a job offer. Your goal is to identify matches and gaps between the job requirements and the candidate's qualifications. 
Additionally, you will provide a final score indicating the overall match percentage.\n\n

Input Format\n
The job offer and CV should be provided in plain text between the specified delimiters:\n\n

Job Offer: <JOB_OFFER> and </JOB_OFFER>\n
CV: <CV> and </CV>\n
Matching Criteria\n
Skills: Compare the skills listed in the job offer with those in the CV.\n
Experience: Compare the years and types of experience required with those listed in the CV.\n
Education: Compare the educational qualifications required with those listed in the CV.\n
Scoring Methodology\nMatches: Each match between the job offer and the CV will contribute positively to the final score.\n
Gaps: Each gap will reduce the final score.\n
Final Match Score: The percentage of match between the job offer and the CV will be calculated based on the number of matches and gaps.\n
Output Format\n
The output must list the following:\n\n

Matches\n
[List of matches between the job offer and the CV]\n\n

Gaps\n
[List of gaps between the job offer and the CV]\n\n

Final Match Score\n
[Percentage of match between the job offer and the CV]"""

# Function to process the content of a file using chatgpt, the response is an object
def process_file_gpt(Job_offer, CV):
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": f"{job_prompt}"},
                {"role": "user", "content": f"\n\n<JOB_OFFER>\n{Job_offer}\n</JOB_OFFER>\n<CV>\n{CV}\n</CV>\n\n```n\n```"}
            ],
            max_tokens=1000,
            temperature=0.0
        )
    except Exception as e:
        print("Error processing the data")
        print(e)
        response = None     
    return response


# Main function
def main():
    parser = argparse.ArgumentParser(description='Validate CV and job offer files.')
    parser.add_argument('--CV', required=True, help='Path to the CV file')
    parser.add_argument('--JO', required=True, help='Path to the job offer file')
    args = parser.parse_args()

    cv_file = args.CV
    job_offer_file = args.JO

    if not os.path.exists(cv_file):
        print(f"Error: {cv_file} does not exist.")
        return
    if not os.path.exists(job_offer_file):
        print(f"Error: {job_offer_file} does not exist.")
        return

    if validate_files(cv_file, job_offer_file):
        # Perform further processing on the files
        print("Both files are valid. Processing...")
        cv_contents, job_offer_contents = validate_files(cv_file, job_offer_file)
        response = process_file_gpt(job_offer_contents, cv_contents)
        print(response.choices[0].message['content'])

if __name__ == "__main__":
    main()



