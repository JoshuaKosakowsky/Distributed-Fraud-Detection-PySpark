# AWS EMR — Running Code & Jupyter Workflow

---

# 🧠 Overview

This guide explains how to:

- Connect to the EMR cluster  
- Set up JupyterHub  
- Run notebooks  
- Use S3 data in PySpark  

---

# 🖥️ PART 1 — CONNECT TO CLUSTER

## 🍎 Mac

'''
ssh -i ~/keys/MSBX5420.pem hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
'''

---

## 🪟 Windows

'''
ssh -i C:\keys\MSBX5420.pem hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
'''

---

# 📁 PART 2 — NAVIGATE TO TEAM DIRECTORY

'''
cd /mnt1/msbx5420_teams/team_15
ls
'''

---

# ☁️ PART 3 — VERIFY S3 ACCESS

'''
aws s3 ls s3://msbx5420-2026
aws s3 ls s3://msbx5420-2026/teams/team_15/
'''

---

# 📓 PART 4 — CREATE JUPYTER USER (FIRST TIME ONLY)

'''
sudo docker exec jupyterhub useradd -m -s /bin/bash -N {username}
sudo docker exec jupyterhub bash -c "echo {username}:{password} | chpasswd"
'''

Then exit cluster:

'''
exit
'''

---

# 🔌 PART 5 — CONNECT TO JUPYTER (PORT FORWARDING)

## Cluster 1

'''
ssh -i ~/keys/MSBX5420.pem -N -L localhost:8080:localhost:9443 \
hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
'''

---

## Cluster 2

'''
ssh -i ~/keys/MSBX5420.pem -N -L localhost:8081:localhost:9443 \
hadoop@ec2-34-221-98-70.us-west-2.compute.amazonaws.com
'''

---

# 🌐 PART 6 — OPEN JUPYTER

Go to:

- https://localhost:8080 (cluster 1)  
- https://localhost:8081 (cluster 2)  

If blocked:

- click “Advanced”  
- OR type: thisisunsafe  

Login with your username/password.

---

# 📊 PART 7 — RUN PYSPARK NOTEBOOK

## ⚠️ IMPORTANT

- Do NOT upload datasets into JupyterHub  
- Always read from S3  

---

## Example: Read data from S3

'''
df = spark.read.csv(
    "s3://msbx5420-2026/teams/team_15/data/raw/credit_card_transactions.csv",
    header=True,
    schema=TRANSACTION_SCHEMA
)
'''

---

## Select PySpark Kernel

- Choose **PySpark kernel**
- NOT Python 3

---

# 📦 Installing packages (if needed)

'''
sc.install_pypi_package("package_name")
'''

---

# 🛑 PART 8 — STOP NOTEBOOK

In Jupyter:

- File → Close and Halt  

---

# 🔌 PART 9 — DISCONNECT

In terminal:

'''
CTRL + C   (or CMD + C)
'''

---

# ⚠️ IMPORTANT RULES

- Do NOT upload full repo to S3  
- Only upload data  
- Do NOT upload data to JupyterHub  
- Always use S3 paths  
- Keep same username across clusters  

---

# 🚀 WORKFLOW SUMMARY

1. Upload data → S3  
2. Connect → EMR  
3. Start → JupyterHub  
4. Run → PySpark notebooks  
5. Read/write → S3  

---

# 💬 FINAL NOTES

- Replace `team_15` with your team name  
- Replace `{username}` and `{password}`  
- This workflow separates compute and storage correctly  