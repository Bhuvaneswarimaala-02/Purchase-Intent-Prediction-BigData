# 🛒 Purchase Intent Prediction (Big Data Project)

This project aims to predict whether an online shopper will make a purchase or not based on their interaction data collected from an e-commerce website. Built using **Apache Spark**, the model leverages big data capabilities for large-scale processing and achieves a strong **90% accuracy** using the **Random Forest** classification algorithm.

---

## 🧠 Problem Statement

- Help e-commerce business owners gain **analytical insights** from user session data.
- Identify user behaviors that **lead to revenue** generation.
- Use the model to **target high-potential users** through personalization and business strategies.

---

## 📊 Data Overview

- **Source:** [UCI Online Shoppers Purchasing Intention Dataset](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset)
- **Format:** CSV
- **Total Rows:** 12,330  
  - ✅ 1,908 positive samples (purchase made)  
  - ❌ 10,422 negative samples (no purchase)
- **Total Columns:** 17
- **Time Frame:** Data collected over a **1-year period** (to remove holiday/event bias)

---

## 🧾 Features

### 🧩 Page Interaction Types
| Category       | Description |
|----------------|-------------|
| Administrative | Self-service pages like "My Account", "Order History", etc. |
| Informational  | About, Contact, FAQs |
| Product Related| Product listing, search, best-sellers |

- **Duration Fields**: Time spent on each of the above page types

### 📈 Google Analytics Metrics
- **Bounce Rate**: User left without any action  
- **Exit Rate**: Last page before leaving  
- **Page Value**: Average monetary value of a page

### 🌍 Other Features
- Special Day, Month, Operating System, Browser, Region, Traffic Type, Visitor Type, Weekend

### 🎯 Label
- `Revenue` (Boolean): Whether the session resulted in a purchase or not

---

## 🛠 Tools Used

- **Apache Spark** for distributed data processing
- **MLlib** for machine learning model training (Random Forest)
- **Python** for scripting
- **Google Colab** for exploratory analysis and visualization
- **Fast API** for endpoint

---

## 🔄 Data Preprocessing

- Handling missing values
- Encoding categorical features
- Feature transformation:
  - **Total Duration** = `Administrative_Duration` + `Informational_Duration` + `ProductRelated_Duration`
  - **Session Type**: Categorized as Low / Moderate / High based on total duration

---

## 📈 Visualization

Various visualizations were generated during EDA to understand:

- Revenue distribution across months
- Session types vs revenue
- Product page duration impact on purchase intent
- ![image](https://github.com/user-attachments/assets/92ca6b27-7a74-4d9f-959e-420668a8412f)


---

## 🧪 Model Training

- Algorithm: **Random Forest Classifier (Spark MLlib)**
- Achieved **90% Accuracy**
- Evaluation: Accuracy, Precision, Recall, F1-score

---

## Backend Endpoint (using FastAPI)

![image](https://github.com/user-attachments/assets/7651159b-a8e4-4563-8d7d-fda852db8170)

---

## 🚀 Deployment (Work In Progress)

The model will soon be integrated into a web app for interactive user prediction.  

---
