workspace {

    model {
        user = person "User"
        cloudier = softwareSystem "Cloudier" {
            validationQueue = container "Validation Queue" "" "SQS" "Amazon Web Services - Simple Queue Service	"
            invalidShipmentNotification = container "InvalidShipmentNotification" "" "SNS" "Amazon Web Services - Simple Notification Service Topic"
            validShipmentNotification = container "ValidShipmentNotification" "" "SNS" "Amazon Web Services - Simple Notification Service Topic"
            validShipmentsQueue = container "ValidShipmentsQueue" "" "SQS" "Amazon Web Services - Simple Queue Service"

            gateway = container "Gateway" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                -> user "Send shipment data"
                -> validationQueue "Queue shipment for further operations"
            }

            validator = container "Validator" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                lambdaHandler = component "Lambda handler" "" "" ""
                validatorComponent = component "Validator" "" "Python" "Python"
                dhlValidatorComponent = component "Validate DHL shipment" "" "" ""

                lambdaHandler -> validatorComponent "Validate shipment"
                lambdaHandler -> validationQueue "Get shipment data from queue"
                lambdaHandler -> invalidShipmentNotification "Notify about invalid shipment"
                lambdaHandler -> validShipmentNotification "Notify about valid shipment"
                validatorComponent -> dhlValidatorComponent "Validate shipment using DHL specification"
            }
        }

        user -> cloudier "Order shipment"
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

        component validator "Validator" {
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
