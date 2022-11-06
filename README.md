
# JIRAlice [![Build Status](https://travis-ci.org/sbraverman/jiralice.svg)](https://travis-ci.org/sbraverman/jiralice)
Generate JIRA tickets from Pager Duty webhooks via [Chalice](https://github.com/awslabs/chalice)!

# What is JIRAlice?
JIRAlice is a mashup of JIRA and Chalice.
Open source project that creates JIRA tickets from Pager Duty webhooks using serverless technologies: AWS Lambda and AWS API Gateway (deployed/managed via Chalice).

This is a new option for making JIRA tickets from Pager Duty alerts.
No need to host the code on your personal server (unless you want to).
Customizable to fit your requirements.
Easy to setup.

JIRAlice uses the following technologies:
* Python2.7
* AWS Lambda
* AWS API Gateway
* CloudWatch (Lambda Logs)
* PagerDuty Webhooks

This project enhances previous project: [pd2jira_python](https://github.com/sbraverman/pd2jira_python)

# Let's get started!
JIRAlice will be up and running within minutes. Just follow this guide!

1. Fork this project into your account and clone into local directory

  ```
  git clone git@github.com:<your_github_handle>/JIRAlice.git
  ```
_note: replace <your_github_handle> with your Github handle_

2. Replace the example data in the environment_variables key inside:
_jiralice/.chalice/configs.json
Explanations:
  * JIRA_URL -- the site which your JIRA application is hosted from
  * JIRA_USERNAME -- Username for service user account for which the JIRA tickets will be "created by." User must be registered with your JIRA account and have permissions to create tickets in the project specified below.
  * JIRA_PASSWORD -- Password for the above user.
  * JIRA_PROJECT -- the project for which the ticket will be generated for (Project is usually capital... just saying).
  * LABELS -- any labels (comma delimited) you would like to create the ticket with. 'PagerDuty' is selected as default. Leave this as an empty string if you do not want a label for your newly created ticket. Example of multiple labels: 'PagerDuty,PD,extra-label'
  * CUSTOM_FIELDS -- Any fields your project deems as necessary that are not of the default values from above. These must be comma delimited key:value pairs. Example: 'customfield_10021:value,customfield_10022:another value'

_If your project requires many customfields to generate a ticket, this will make the setup longer_

  ```
  "environment_variables": {
    "JIRA_URL": "https://my-jira.jira.com",
    "JIRA_USERNAME": "service-account",
    "JIRA_PASSWORD": "topsecretpassword",
    "JIRA_PROJECT": "DEVOPS",
    "LABELS": "PagerDuty,PD,automated-ticket",
    "CUSTOM_FIELDS": ""
  },
  ```
3. Upload to AWS
  * Follow directions to ensure your [~/.aws/credentials](http://boto3.readthedocs.io/en/latest/guide/configuration.html) file is set up
  * Run the following command from jiralice/jiralice directory (ls should show app.py) ```chalice deploy```
  * Output should reveal the API Gateway endpoint. Copy this for the next step. (You will need to add 'create-ticket' to the end)!

4. Set up Pager Duty webhook.
  * Navigate to your Pager Duty account
  * Select a service you would like to create JIRA tickets from or create a new service
  * Click on "Integrations" tab and and Extension "Generic Webhook"
  * Give your webhook a name and paste the URL from the previous step. After the last forward-slash, add the following: "create-ticket"
  * full example of url is something like: "https://5x9iwjzqw3.execute-api.us-west-1.amazonaws.com/dev/create-ticket" (Notice I added create-ticket to the end. You need to do this!)
  * You are done! Let's test it out

# Test your Lambda function
1. In Pager Duty, navigate to the service you added the webhook to.
2. Trigger an alert. NOTE: Make sure the person you are about to alert is aware that you are testing. You may want to create a new service or temporarily set yourself up as the on-call scheduled person.
4. Go to JIRA and ensure your ticket was generated correctly. If you see your ticket, SUCCESS! If your new ticket was not created within 5 seconds, continue to the next step.
3. Log in to AWS. Navigate to your Lambda function. Click on "Monitoring." Click on "View Logs in CloudWatch"
4. View the log stream that was generated. This will give you some ideas as to why your ticket failed to be generated. Most likely, there are some custom fields you need to set to create tickets or your Configs were not properly configured. When you update the code, you will have to run the `chalice deploy` to upload your new package.


# Running tests
1. To run the unit tests you must be in the project root directory and have nose installed

  ```
  nosetests
  ```
_Tests are currently limited. Want to add more?_

# Contributing
1. Fork the repository.
2. Make your changes.
3. Add unit tests.
4. Ensure unit tests pass.
5. Submit pull-request. Please make sure your commit message contains a helpful comment. Please ensure you add a comment alongside your pull-request showing proof that your code works.

# Current Shortcomings
1. If your JIRA application is private to the world, you will need to generate a VPC, internet gateway, nat gateway, routes, subnet associations, elastic IP, and whitelist the IP
2. Does not create a CloudFormation template for managing AWS resources. Chalice currently can create packages and create a CloudFormation template for you based off SAM, but this has bot yet been investigated by myself.
3. Does not report back to PagerDuty if you resolve this ticket.
4. Does not create a link to this ticket from Pager Duty alert.
