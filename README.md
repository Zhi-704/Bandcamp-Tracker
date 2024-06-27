# 🎼 Apollo



## 🔎 Overview

### 📝 Description
> Welcome to Team Apollo's sales tracker revolving around the creation of an ETL pipeline via the use of Bandcamp's API and webscraping. The data is then used to create three different outputs which will provide various information on artists and genres regarding their sales and popularity both recently and over time. These are: **dashboard**, **email notifications**, and **PDFs**. This results in our **tracker** which is provided to consumers as a service.

### 👩‍💼 Stakeholder Requirements
- Obtain **latest** sales data from Bandcamp on artists/genre
- Automatically **alert**, **notify**, and/or **send** PDFs to subscribers regarding this data.

### 🎯 Deliverables
- A **full data pipeline**, hosted in the cloud.
- A **long-term storage solution** for the data extracted from Bandcamp.
- **Visualisation** of the sales data.


## ✏️ Design

### 📏 Entity-Relationship Diagram
![ERD Diagram](https://github.com/Zhi-704/c11-apollo-bandcamp-tracker/blob/main/diagrams/ERD.png)

This diagram explicitly shows how the data extracted from the API is stored in the database. We have decided to use a **3NF RD** for our database due to the requirements of the tracker. As we care about various sources of data such as countries, tags, and artists, other types of schema such as STAR Schema would not be suitable for our aims as we need to query multiple tables. 

### 📐 Architecture Diagram
![Architecture Diagram](https://github.com/Zhi-704/c11-apollo-bandcamp-tracker/blob/main/diagrams/Architecture_Diagram.png)

This is a diagram that shows how every different AWS services work and interact with each other in order to complete the requirements of the tracker.

#### **IMPORTANT**
 >Information regarding each section of the AD will not be found here. Instead, **clicking on** the bullet points below will send you to the relative **README** located in the **directories** of the section that you would like to look at. There you can find out all the information that you need.


- [**ETL Pipeline**](./pipeline/README.md)

- [**RDS**](./schema/README.md)

- [**PDF Report**](./pdf_report/README.md)

- [**Notifications**](./notifications/README.md)

- [**Dashboard**](./dashboard/README.md)




## ✅ Getting Started

### 💿 Installations
The following languages/softwares are **required** for this project. Things assigned as **optional** are only required if you desire to host this tracker on the cloud.
- Python
- Bash
- Docker (Optional)

### ❗️ Dependencies
There are various **directories** for each part of the project. In order to run the scripts in each folder, you will need to install the **required libraries**. This can be done using the code provided below:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 🏃‍♂️‍➡️ Running the scripts
All the scripts only require **basic** commands to be executed. Different commands are used **depending on the software**. Ensure that you are in the directory of the file you want to run before using these commands.
```
# Python
python3 "script.py"

# Bash
bash "script.sh"

# Terraform
terraform init
terraform apply
yes

# Docker
docker build -t "image"
docker run --env-file .env -t "image: tag"
```
#### **IMPORTANT**
>One thing to note is that the majority of scripts use environment variables. Make sure to create your own .env and fill out all the variables required to run the code successfully. Smaller READMEs will be found in each folder going into more depth on how to use that specific part of the repository.


## 🚀 Running the Repository

### 🗂️ Repository Structure
There are several directories within the repository to maintain an organised project. Each directory will be labelled below with a brief sentence explaining what they do. 

#### **IMPORTANT**
>Clicking on the link provided will redirect you to the README in that directory which provides more information

- `dashboard` - Contains all the scripts involved in creating and hosting the dashboard. [**Click here**](./dashboard/README.md).
- `diagrams` - Only contains the .png files of the diagrams used in this README. No need to go here.
- `notifications` - Contains all the scripts required in order to send emails to subscribers to notify them when a tag that they're interested in is trending. [**Click here**](./notifications/README.md).
- `pdf_report` - Contains all the scripts required to send a daily email to registered subscribers which contains the PDF on the data from yesterday. [**Click here**](./pdf_report/README.md)
- `pipeline` - Contains all the scripts involved in creating the ETL pipeline for the sales tracker. The data is then used to support all the other outputs. [**Click here**](./pipeline/README.md).
- `schema` - Contains the schema used to create the RDS hosted on AWS. [**Click here**](./schema/README.md).
- `terraform` - Contains the main terraform script used to host the tracker on the cloud. [**Click here**](./terraform/README.md).


### ☁️ Cloud Resources
For this tracker, we have designed it with the intention of hosting everything on the cloud in order to automate it. The python scripts can still be ran locally but the terraform scripts have been included within the repository if you desire to host this service on the cloud as well. The cloud service that has been used is **AWS**.


## 🚨 Help
Common issues which people face are:

- Not setting up environment variables correctly - you need to ensure that you have done the following: 
  1. **Create** .env file for python scripts or a terraform.tfvars for terraform scripts
  2. Create the file in the **same directory as the file** you want to run
  3. Make sure the variable names in your **file are the same as the ones used in the script** that you would like to run.

- Not downloading the required libraries before running the script.
  1. **Go to the directory** of the script that you want to run.
  2. **Create** a .venv and activate it.
  3. **Install** the requirements onto your .venv.

- For any other problems, make sure to reach out and contact us so we can support you further.


## 📖 Authors
- https://github.com/alina-101
- https://github.com/e-lemma
- https://github.com/Lasped13
- https://github.com/Zhi-704


## 📚 Version History
- 1.0
  - Initial release


## © License
This project is licensed under alina101, e-lemma, Lasped13, and Zhi-704 - see the LICENSE.md file for details.

## ❤️ Acknowledgements
- 🎹 **Band Camp** for providing us with data.
- 🧡 **Sigma Labs** for giving us this project.
- 🎼 **Team Apollo** for creating this tracker via the use of:
  1. *Ten percent luck*
  2. *Twenty percent skill*
  3. *Fifteen percent concentrated power of will*
  4. *Five percent pleasure*
  5. *Fifty percent pain*