import logging

import azure.functions as func
import openai
import os
context = """
use below data 
Rental Agreement:
This agreement made between John Doe and Jane Smith for the rental of a 1-bedroom apartment located at 123 Main Street, starting on January 1st, 2023 and ending on December 31st, 2023. Rent is $1,200 per month, due on the 1st of each month. No subleasing allowed.

Lease Contract:
This contract made between Mark Brown and Sarah Johnson for the lease of a 2-bedroom house located at 456 Park Avenue, starting on February 1st, 2023 and ending on January 31st, 2024. Rent is $2,000 per month, due on the 5th of each month. No smoking allowed on the premises.

Rental Agreement:
This agreement made between David Wilson and Emily Davis for the rental of a studio apartment located at 789 Ocean Drive, starting on March 1st, 2023 and ending on February 28th, 2024. Rent is $800 per month, due on the 10th of each month. Tenant must pay for utilities.

Lease Contract:
This contract made between Michael Green and Rachel Lee for the lease of a 3-bedroom townhouse located at 101 Mountain View, starting on April 1st, 2023 and ending on March 31st, 2024. Rent is $1,500 per month, due on the 15th of each month. No pets allowed.

Rental Agreement:
This agreement made between Matthew Clark and Jessica Smith for the rental of a 1-bedroom condo located at 202 River Road, starting on May 1st, 2023 and ending on April 30th, 2024. Rent is $1,000 per month, due on the 20th of each month. Tenant must provide proof of renters insurance.

Lease Contract:
This contract made between James Wilson and Lauren Johnson for the lease of a 2-bedroom apartment located at 303 City Center, starting on June 1st, 2023 and ending on May 31st, 2024. Rent is $1,200 per month, due on the 25th of each month. No loud music allowed after 10 PM.

Rental Agreement:
This agreement made between Richard Brown and Olivia Davis for the rental of a studio loft located at 404 Art District, starting on July 1st, 2023 and ending on June 30th, 2024. Rent is $900 per month, due on the 1st of each month. Tenant must clean common areas.

Lease Contract:
This contract made between Thomas Green and Samantha Lee for the lease of a 3-bedroom duplex located at 505 Sunset Boulevard, starting on August 1st, 2023 and ending on July 31st, 2024. Rent is $1,800 per month, due on the 5th of each month. No illegal activities allowed.

Rental Agreement:
This agreement made between Henry Clark and Elizabeth Smith for the rental of a 1-bedroom house located at 606 Forest Drive, starting on September 1st, 2023 and ending on August 31st, 2024. Rent is $1,100 per month, due on the 10th of each month. Tenant must maintain the yard.

Lease Contract:
This contract made between Jacob Wilson and Caroline Johnson for the lease of a 2-bedroom cottage located at 707 Beach Road, starting on October 1st, 2023 and ending on September 30th, 2024. Rent is $1,400 per month, due on the 15th of each month. No smoking allowed inside the house.

"""
GPT_ENGINE = "text-davinci-003"
def recognize_entities(prompt, engine=GPT_ENGINE):
    """Recognize entities in text using OpenAI's text classification API."""
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=1,
        max_tokens=2048,
    )
    return response.choices[0].text


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    openai.api_type = "azure"
    openai.api_key = os.getenv("OPENAI_API_KEY")  # SET YOUR OWN API KEY HERE
    openai.api_base = os.getenv("OPENAI_RESOURCE_ENDPOINT")  # SET YOUR RESOURCE ENDPOINT
    openai.api_version = "2022-06-01-preview"

    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            prompt = req_body.get('prompt')

    if prompt:
        prompt = prompt + context


        result = recognize_entities(prompt, engine=GPT_ENGINE)

        return func.HttpResponse(result)

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a prompt in the query string or in the request body for a personalized response.",
             status_code=200
        )
