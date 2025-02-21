# 📝 Relatos Consumidores

## 📖 About the Project

This repository contains the source code for the final graduation project, **"Modelagem e Construção de uma Base Pública de Relatos de Consumidores"**, which can be accessed here:  
🔗 [Project Link](https://linktr.ee/biamsarmento)

### Project Overview

This work focuses on developing a **public structured database** from consumer reports extracted from the **Consumidor.gov.br** website. The main motivation is to provide **easy and automated access to public data**, which is often available in an unstructured and hard-to-manage format, limiting its usability for researchers and professionals.

To address these challenges, the project employs a **web scraping approach**, combined with:
- **Database modeling methodologies**  
- **ETL processes (Extraction, Transformation, and Loading)**  
- **Data analysis with machine learning techniques**  

## 📂 Project Structure

The code is organized as follows:

- **`web_scraping.py`** → Main script where the desired extraction dates are set.  
- **`functions.py`** → Contains functions for web scraping using **BeautifulSoup**.  
- **`database.py`** → Saves extracted data into a **MySQL database** (which must be preconfigured).  
- **`randomForest.py`** → Processes the structured data (saved in JSON format) and provides basic statistics.  
  - It attempts to **predict the rating (1 to 5)** that a user will give based on the **status and content of the report**, using the **Random Forest algorithm**.  

## 🎯 Objective

The goal of this project is to **facilitate public data extraction and structuring** to make consumer reports easily accessible and useful for researchers, analysts, and professionals. 

## 🚀 Outcome

This project enables **automated and structured extraction of consumer complaints**, making public data more accessible for analysis and research.

## 🛠️ Technologies and Tools Used

- **Python**
  - BeautifulSoup (**Web Scraping**)
  - Pandas (**Data Processing**)
  - Scikit-Learn (**Machine Learning - Random Forest**)
- **MySQL** (**Database Storage**)
- **JSON** (**Data Formatting**)

## 📚 What I Learned

Through this project, I gained valuable experience in:
- **Web Scraping techniques** with BeautifulSoup  
- **ETL (Extract, Transform, Load) processes** for structuring public data  
- **Database modeling and interaction** with MySQL  
- **Machine Learning for data analysis and prediction**  

## 🔧 How to Run the Project

### 📦 Cloning the Repository
```bash
git clone https://github.com/biamsarmento/relatos-consumidores.git
cd relatos-consumidores
