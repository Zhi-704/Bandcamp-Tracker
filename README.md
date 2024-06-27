# 🎸 Bandcamp Data Pipeline



## 🔎 Overview

### 📝 Description
> Welcome to Team Apollo's project revolving around the creation of a data pipeline via the use of Bandcamp's API and webscraping. The data is then used to create a dashboard which will provide various information on artists and genres regarding their sales and popularity both recently and over time.

### 👩‍💼 Stakeholder Requirements
- Obtain latest sales data from Bandcamp on artists/genre
- Automatically alert, notify, and/or send PDFs to subscribers regarding this data.

### 🎯 Deliverables
- A full data pipeline, hosted in the cloud.
- A long-term storage solution for the data extracted from Bandcamp.
- Some form of visualisation of the data.


## ✏️ Design

### 📏 Entity-Relationship Diagram
![ERD Diagram](https://github.com/Zhi-704/c11-apollo-bandcamp-tracker/blob/main/diagrams/ERD.png)
### 📐 Architecture Diagram
![Architecture Diagram](https://github.com/Zhi-704/c11-apollo-bandcamp-tracker/blob/main/diagrams/Architecture_Diagram.png)

## ✅ Getting Started

### 💿 Installations
The following languages/softwares are required for this project. Things assigned as optional are only required if you desire to host this system on the cloud.
- Python
- Bash
- Docker (Optional)

### ❗️ Dependencies
There are various folders for each part of the project. In order to run the scripts in each folder, you will need to install the required libraries. This can be done using the code provided below:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 🏃‍♂️‍➡️ Running the scripts
All the scripts only require basic commands to be executed. Different commands are used depending on the software. Ensure that you are in the directory of the file you want to run before using these commands.
```
# Python
python3 "script.py"

# Bash
bash "script.sh"

# Docker
docker build -t "image"
docker run --env-file .env -t "image: tag"
```
#### **IMPORTANT**
 One thing to note is that the majority of scripts use environment variables. Make sure to create your own .env and fill out all the variables required to run the code successfully. Smaller READMEs will be found in each folder going into more depth on how to use that specific part of the repository.


## 🚀 Running the Repository

### 🗂️ Repository Structure
WIP

### ☁️ Cloud Resources
For this project, we have designed it with the intention of hosting everything on the cloud in order to automate it. The python scripts can still be ran locally but the terraform scripts have been included within the repository if you desire to host this system on the cloud as well. The cloud service that has been used is **AWS**.


## 🚨 Help
Common issues which people face are:

- Temp problem 1

- Temp problem 2

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

