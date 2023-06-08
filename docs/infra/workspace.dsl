workspace {

    model {
        user = person "User"
        cloudier = softwareSystem "Cloudier" {
            deadLetterQueue =  container "DeadLetterQueue" "" "SQS" "Amazon Web Services - Simple Queue Service"
            validationQueue = container "Validation Queue" "" "SQS" "Amazon Web Services - Simple Queue Service	" {
                -> deadLetterQueue "Queue invalid event"
            }
            invalidShipmentNotification = container "InvalidShipmentNotification" "" "SNS" "Amazon Web Services - Simple Notification Service Topic"
            validShipmentNotification = container "ValidShipmentNotification" "" "SNS" "Amazon Web Services - Simple Notification Service Topic"
            validShipmentsQueue = container "ValidShipmentsQueue" "" "SQS" "Amazon Web Services - Simple Queue Service" {
                -> deadLetterQueue "Queue invalid event"
            }
            estimatedShipmentsQueue = container "EstimatedShipmentsQueue" "" "SQS" "Amazon Web Services - Simple Queue Service" {
                -> deadLetterQueue "Queue invalid event"
            }
            estimatedShipmentNotification = container "EstimatedShipmentNotification" "" "SNS" "Amazon Web Services - Simple Notification Service Topic"
            rds = container "RDS" "" "RDS" "Amazon Web Services - Aurora PostgreSQL Instance"


            gateway = container "Gateway" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                -> user "Send shipment data"
                -> validationQueue "Queue shipment for further operations"
            }

            validator = container "Validator" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                validatorLambdaHandler = component "Lambda handler" "" "" ""
                validatorComponent = component "Validator" "" "Python" "Python"
                dhlValidatorComponent = component "Validate DHL shipment" "" "" ""

                validatorLambdaHandler -> validatorComponent "Validate shipment"
                validatorLambdaHandler -> validationQueue "Get shipment data from queue"
                validatorLambdaHandler -> invalidShipmentNotification "Notify about invalid shipment"
                validatorLambdaHandler -> validShipmentNotification "Notify about valid shipment"
                validatorComponent -> dhlValidatorComponent "Validate shipment using DHL specification"
            }

            estimator = container "Estimator" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                estimatorLambdaHandler = component "Lambda handler" "" "Python" ""
                estimatorComponent = component "Estimator" "" "Python" ""
                dhlEstimatorComponent = component "Estimate DHL shipment" "" "Python" ""

                estimatorLambdaHandler -> validShipmentsQueue "Get shipment data from queue"
                estimatorLambdaHandler -> estimatorComponent "Estimate shipment"
                estimatorLambdaHandler -> estimatedShipmentNotification "Notify about estimated shipment"
                estimatorLambdaHandler -> invalidShipmentNotification "Notify about invalid shipment"
                estimatorComponent -> dhlEstimatorComponent "Estimate shipment using DHL specification"
            }

            deadLetterProcessor = container "Dead letter processor "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                -> deadLetterQueue "Get not processable events"
                -> invalidShipmentNotification "Notify about not processable shipment"
            }

            order = container "Order" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                -> estimatedShipmentsQueue "Get estimated shipment data from queue"
                -> rds "Persist ordered shipment"
            }

            reports =  container "Reports" "" "Lambda" "Amazon Web Services - AWS Lambda Lambda Function" {
                -> user "Get price report"
                -> rds "Get data for the report"
            }
        }

        user -> cloudier "Order shipment"
        validShipmentNotification -> validShipmentsQueue "Queue valid shipment"
        estimatedShipmentNotification -> estimatedShipmentsQueue "Queue estimated shipment"
    }

    views {
        systemContext cloudier "SystemContext" {
            include *
            autoLayout
        }

        container cloudier "Cloudier" {
            include *
            autoLayout lr
        }

        component validator "Validator" {
            include *
            autoLayout
        }

        component estimator "Estimator" {
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
