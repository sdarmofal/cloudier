# Cloudier

This repository contains an example AWS API Gateway application.

## Business case

The application can be used in company that sends many shipments. It allows a user to put a shipment
(by its size definition) and then automatic system will find a carrier that can deliver the shipment.

If the operation finish successfully, the shipment will be stored in the database along with the
carrier and pricing information. The user can monitor the total price for specified time interval.

If the operation fails, then system will send an email notification to the user.

## Used ASW services

- Lambda
- Simple Notification Service (SNS)
- Simple Queue Service (SQS)
- Identity and Access Management (IAM)
- Relational Database Service (RDS)
- Secrets Manager
- CloudWatch
- API Gateway
- CloudFormation
- Serverless Application Model (SAM)

## Running

### Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality
for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that
matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM
  CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application
to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region,
  and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual
  review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for
  the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required
  permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value
  for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must
  explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the
  project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your
  application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
cloudier$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it
in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input
that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
cloudier$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
cloudier$ sam local start-api
cloudier$ curl http://localhost:3000/
```

### Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack
name, you can run the following:

```bash
sam delete --stack-name cloudier
```

## Occurred problems and solutions

### Connect from local machine to RDS instance 

1. Open RDS panel in AWS console
2. In Connectivity & security tab, click on the VPC security groups
3. Click on the security group that is assigned to the RDS instance
4. In the Inbound rules tab, click Edit inbound rules
5. Click Add rule
6. Select PostgreSQL in the Type dropdown
7. Select Custom in the Source dropdown
8. Enter your IP address followed by /32 in the Source field
9. Click Save rules
10. Click Apply immediately

### Retry to process queue message

In the `template.yaml` file, the `RetryAttempts` property is set to 0. This means that the message will be processed only
once. If the message processing fails, then it will be moved to the Dead Letter Queue (DLQ).

The solution is to define the Dead Letter Queue and link it with the main queue.

### Access to the RDS instance from Lambda function

The Lambda function is not able to access the RDS instance. The solution is to add the Lambda function to the VPC.

1. Open Lambda panel in AWS console
2. Click on the function name
3. In the Configuration tab, click on the Edit button in the VPC section
4. Set the VPC and Subnets that are used by the RDS instance
5. Click Save

### Write and read to SNS / SQS

The Lambda function is not able to write to SNS and SQS. The solution is to add the Lambda function to the IAM policy
that is assigned to the SNS and SQS.

You can achieve it through the SAM template. In the `template.yaml` file, add the following lines to the `Policies`
property of the Lambda function:

```yaml
- SNSPublishMessagePolicy:
    TopicName: !Ref TopicName
- SQSSendMessagePolicy:
    QueueName: !Ref QueueName
```

### Disabling API Gateway

<<<<<<< HEAD
The API Gateway is not able to be disabled. Because of it, it can be accessible by others and may generate cost.
The solution is to open tha API Gateway in the AWS console and delete it.
=======
The API Gateway is not able to be disabled. The solution is to open tha API Gateway in the AWS console and delete it.
>>>>>>> origin/main

### Input data validation

The input data can be validated in two ways:

1. In the Lambda function - the god way to deal with business validation
2. In the API Gateway (Models) - the good way to deal with schema validation 

