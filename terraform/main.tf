## Initial Setup

provider "aws" {
    access_key = var.ACCESS_KEY
    secret_key = var.SECRET_ACCESS_KEY
    region = var.REGION
}

data "aws_vpc" "c11-VPC" {
    id = var.VPC
}

data "aws_iam_role" "ecs_task_execution_role" {
  name = var.ECS_IAM_ROLE
}


## RDS - This works to construct a database. However, we didn't want to reset the database
## in order to preserve the data we have already scraped from the band camp API. Currently, 
## use this as the code to refer to the existing database whenever you need to:
## {
##     "name": "DB_ENDPOINT",
##     "value": var.DB_ENDPOINT
## },
## If you wish to change the script so that you construct the rds too, you need to uncomment
## the code below and replace the variable mentioned above with the variable mentioned below.
## {
##    "name": "DB_HOST",
##    "value": "${aws_db_instance.apollo_test_db.endpoint}"
## },

# resource "aws_security_group" "apollo_test_db_sg" {
#     name = var.SG_DB_NAME
#     description = "Security group that allows inputting data into the rds"
#     vpc_id = data.aws_vpc.c11-VPC.id

#     tags = {
#         Name = var.SG_DB_IDENTIFIER
#     }

#     ingress {
#         from_port = 5432
#         to_port = 5432
#         protocol = "tcp"
#         cidr_blocks = ["0.0.0.0/0"]
#     }

#     egress {
#         from_port = 0
#         to_port = 0
#         protocol = "-1"
#         cidr_blocks = ["0.0.0.0/0"]
#     }
# }

# resource "aws_db_instance" "apollo_test_db" {
#     identifier = var.DB_IDENTIFIER
#     allocated_storage = 20
#     engine = "postgres"
#     engine_version = "16.3"
#     instance_class = "db.t3.micro"
#     db_name = var.DB_NAME
#     username = var.DB_USERNAME
#     password = var.DB_PASSWORD
#     db_subnet_group_name = var.DB_SUBNET_GROUP
#     vpc_security_group_ids = [aws_security_group.apollo_test_db_sg.id]
#     publicly_accessible = true
#     performance_insights_enabled = false
#     skip_final_snapshot = true
# }


## Pipeline

resource "aws_ecr_repository" "apollo_test_ecr_pipeline" {
    name = var.ECR_PIPELINE
    image_tag_mutability = "MUTABLE" 
}

resource "null_resource" "dockerise_pipeline" {
  depends_on = [aws_ecr_repository.apollo_test_ecr_pipeline]

  provisioner "local-exec" {
    command = <<EOT
      aws ecr get-login-password --region ${var.REGION} | docker login --username AWS --password-stdin ${aws_ecr_repository.apollo_test_ecr_pipeline.repository_url};
      cd ../pipeline && docker build --platform ${var.DOCKER_PLATFORM} -t ${aws_ecr_repository.apollo_test_ecr_pipeline.repository_url}:latest .;
      cd ../pipeline && docker tag apollo_test_ecr_pipeline:latest ${aws_ecr_repository.apollo_test_ecr_pipeline.repository_url}:latest;
      cd ../pipeline && docker push ${aws_ecr_repository.apollo_test_ecr_pipeline.repository_url}:latest;
    EOT
  }
}


## Dashboard

resource "aws_ecr_repository" "apollo_test_ecr_dashboard" {
    name = var.ECR_DASHBOARD
    image_tag_mutability = "MUTABLE" 
}

resource "null_resource" "dockerise_dashboard" {
  depends_on = [aws_ecr_repository.apollo_test_ecr_dashboard]

  provisioner "local-exec" {
    command = <<EOT
      aws ecr get-login-password --region ${var.REGION} | docker login --username AWS --password-stdin ${aws_ecr_repository.apollo_test_ecr_dashboard.repository_url};
      cd ../dashboard && docker build --platform ${var.DOCKER_PLATFORM} -t ${aws_ecr_repository.apollo_test_ecr_dashboard.repository_url}:latest .;
      cd ../dashboard && docker tag apollo_test_ecr_dashboard:latest ${aws_ecr_repository.apollo_test_ecr_dashboard.repository_url}:latest;
      cd ../dashboard && docker push ${aws_ecr_repository.apollo_test_ecr_dashboard.repository_url}:latest;
    EOT
  }
}

resource "aws_ecs_task_definition" "apollo_test_dashboard_task_def" {
    family = "apollo-test-dashboard-task-definition"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = 1024
    memory = 3072
    execution_role_arn = data.aws_iam_role.ecs_task_execution_role.arn
    container_definitions = jsonencode(([
        {
            name = "apollo-test-dashboard-ecr"
            image = "${aws_ecr_repository.apollo_test_ecr_dashboard.repository_url}:latest"
            cpu = 1024
            memory = 3072
            essential = true
            portMappings = [
                {
                    hostPort = 80
                    containerPort = 80
                },
                {
                    hostPort = 8501
                    containerPort = 8501
                }
            ]
            environment = [
                {
                    "name": "DB_ENDPOINT",
                    "value": var.DB_ENDPOINT
                },
                {
                    "name": "DB_NAME",
                    "value": var.DB_NAME
                },
                {
                    "name": "DB_PASSWORD",
                    "value": var.DB_PASSWORD
                },
                {
                    "name": "DB_PORT",
                    "value": var.DB_PORT
                },
                {
                    "name": "DB_SCHEMA",
                    "value": var.DB_SCHEMA
                },
                {
                    "name": "DB_USER",
                    "value": var.DB_USERNAME
                },
                {
                    "name": "ACCESS_KEY",
                    "value": var.ACCESS_KEY
                },
                {
                    "name": "SECRET_ACCESS_KEY",
                    "value": var.SECRET_ACCESS_KEY
                }
            ]
        }
    ]))
    runtime_platform {
      operating_system_family = "LINUX"
      cpu_architecture = "X86_64"
    }

}


resource "aws_security_group" "apollo_test_dashboard_sg" {
    name = var.SG_DASHBOARD_NAME
    description="Security group that allows connecting to the dashboard"
    vpc_id = data.aws_vpc.c11-VPC.id

    tags = {
        Name = var.SG_DASHBOARD_IDENTIFIER
    }

    ingress {
        from_port   = 8501
        to_port     = 8501
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 8501
        to_port     = 8501
        protocol    = "tcp"
        ipv6_cidr_blocks = ["::/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_ecs_cluster" "apollo_test_dashboard_cluster" {
  name = "apollo_test_dashboard_cluster"
}

resource "aws_ecs_service" "dashboard_service" {
    name = "apollo-test-dashboard-service"
    cluster = aws_ecs_cluster.apollo_test_dashboard_cluster.arn
    task_definition = aws_ecs_task_definition.apollo_test_dashboard_task_def.arn
    desired_count = 1
    launch_type = "FARGATE"
    network_configuration {
      subnets = [var.C11_PUBLIC_SUBNET_1, var.C11_PUBLIC_SUBNET_2, var.C11_PUBLIC_SUBNET_3]
      security_groups = [aws_security_group.apollo_test_dashboard_sg.id]
      assign_public_ip = true
    }
}

## PDF

resource "aws_ecr_repository" "apollo_test_ecr_pdf" {
    name = var.ECR_PDF
    image_tag_mutability = "MUTABLE" 
}

resource "null_resource" "dockerise_pdf" {
  depends_on = [aws_ecr_repository.apollo_test_ecr_pdf]

  provisioner "local-exec" {
    command = <<EOT
      aws ecr get-login-password --region ${var.REGION} | docker login --username AWS --password-stdin ${aws_ecr_repository.apollo_test_ecr_pdf.repository_url};
      cd ../pdf_report && docker build --platform ${var.DOCKER_PLATFORM} -t ${aws_ecr_repository.apollo_test_ecr_pdf.repository_url}:latest .;
      cd ../pdf_report && docker tag apollo_test_ecr_pdf:latest ${aws_ecr_repository.apollo_test_ecr_pdf.repository_url}:latest;
      cd ../pdf_report && docker push ${aws_ecr_repository.apollo_test_ecr_pdf.repository_url}:latest;
    EOT
  }
}

## Notifications

resource "aws_ecr_repository" "apollo_test_ecr_notifications" {
    name = var.ECR_NOTIFICATIONS
    image_tag_mutability = "MUTABLE" 
}

resource "null_resource" "dockerise_notifications" {
  depends_on = [aws_ecr_repository.apollo_test_ecr_notifications]

  provisioner "local-exec" {
    command = <<EOT
      aws ecr get-login-password --region ${var.REGION} | docker login --username AWS --password-stdin ${aws_ecr_repository.apollo_test_ecr_notifications.repository_url};
      cd ../notifications && docker build --platform ${var.DOCKER_PLATFORM} -t ${aws_ecr_repository.apollo_test_ecr_notifications.repository_url}:latest .;
      cd ../notifications && docker tag apollo_test_ecr_notifications:latest ${aws_ecr_repository.apollo_test_ecr_notifications.repository_url}:latest;
      cd ../notifications && docker push ${aws_ecr_repository.apollo_test_ecr_notifications.repository_url}:latest;
    EOT
  }
}