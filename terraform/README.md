# Terraform



## 🔎 Overview

### 📝 Description
> This directory focuses on **terraforming** all the AWS cloud services that are used throughout the tracker.

## 💻 Scripts

### 🪐 Terraform
- `main.tf` - This script contains all the code required to successfully **terraform** the tracker.

#### **IMPORTANT**
 >Refer back to the [**root README**](../README.md) if you need a reminder on how to run the main.tf script. 


## ❗️ Dependencies

### 🧪 Environment Variables
One thing to note is that all these scripts run using **environment variables** so you will need to create your own .env file and include them. Below is a list of all the environment variables:

- `ACCESS_KEY`
- `SECRET_ACCESS_KEY`
- `REGION`
- `VPC`
- `ECS_IAM_ROLE`
- `SG_DB_NAME`
- `SG_DB_IDENTIFIER`
- `DB_IDENTIFIER`
- `DB_NAME`
- `DB_USERNAME`
- `DB_PASSWORD`
- `DB_SUBNET_GROUP`
- `DB_PORT`
- `DB_SCHEMA`
- `DB_ENDPOINT`
- `DB_USER`
- `DOCKER_PLATFORM`
- `ECR_PIPELINE`
- `ECR_DASHBOARD`
- `SG_DASHBOARD_IDENTIFIER`
- `SG_DASHBOARD_NAME`
- `C11_PUBLIC_SUBNET_1`
- `C11_PUBLIC_SUBNET_2`
- `C11_PUBLIC_SUBNET_3`
- `ECR_PDF`
- `ECR_NOTIFICATIONS`
- `CSS_PATH`
- `FILENAME`
- `SES_SENDER`

#### **IMPORTANT**
 >Refer back to the [**root README**](../README.md) and go to the help section if you need a reminder on how to setup environment variables.