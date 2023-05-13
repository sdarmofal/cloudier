workspace {

    model {
        user = person "User"
        cloudier = softwareSystem "Cloudier" {
            sqs = container "SQS" "" "" "Amazon Web Services - Simple Queue Service	"
            sns = container "SNS" "" "" "Amazon Web Services - Simple Notification Service"

            gateway = container "Gateway" "" "" "Amazon Web Services - AWS Lambda Lambda Function" {
                -> user "Send shipment data"
                -> sqs "Queue shipment for further operations"
            }
        }

        user -> cloudier "Uses"
    }

    views {
        systemContext cloudier "SystemContext" {
            include *
            autoLayout
        }

        container cloudier "Cloudier" {
            include *
            autoLayout
        }

        theme https://static.structurizr.com/themes/amazon-web-services-2023.01.31/theme.json
        styles {
            element "Person" {
                shape Person
            }
        }
    }



}
