# AWS EMR + S3 Setup Guide (Project)

> ⚠️ FIRST TIME MAC/LINUX USERS: Complete the PEM setup section before attempting to connect to the cluster.

---

# 🧠 Overview

This project uses AWS EMR for distributed computing and S3 for shared data storage.

All team data must be stored in:

**s3://msbx5420-2026/teams/team_15**

This guide walks through:

1. Setting up your `.pem` key  
2. Connecting to the EMR cluster  
3. Creating your team workspace  
4. Uploading project files  
5. Uploading data to S3  
6. Running notebooks  

---

## 🔑 PART 0 — PEM FILE SETUP

### 🧠 What is `~`?

On Mac/Linux:

```
~
```

means your home directory:

```
/Users/your-username
```

Example:

```
~/keys/MSBX5420.pem
```

is:

```
/Users/your-username/keys/MSBX5420.pem
```

---

## 🔁 If you already have the `.pem` file from Lab 7

In Lab 7, the `.pem` file was placed inside your `lab7` folder.

We will **copy it** into a standard location so it can be reused across projects.

### Step 1 — Create keys folder

```
mkdir -p ~/keys
```

### Step 2 — Copy the `.pem` file

If your `lab7` folder is in your home directory:

```
cp ~/lab7/MSBX5420.pem ~/keys/
```

If your `lab7` folder is elsewhere, adjust the path accordingly.

### 🔍 Not sure where your `.pem` file is?

Run:

```
find ~ -name "MSBX5420.pem" 2>/dev/null
```

Then copy from the location shown.

### Step 3 — Set permissions

```
chmod 600 ~/keys/MSBX5420.pem
```

### Step 4 — Verify

```
ls ~/keys
```

You should see:

```
MSBX5420.pem
```

### 💡 Why we COPY instead of MOVE

- Keeps Lab 7 folder intact  
- Avoids breaking previous work  
- Ensures a consistent key location  

---

## 🆕 If you downloaded the `.pem` file separately

### Step 1 — Create keys folder

```
mkdir -p ~/keys
```

### Step 2 — Move file from Downloads

```
mv ~/Downloads/MSBX5420.pem ~/keys/
```

### Step 3 — Set permissions

```
chmod 600 ~/keys/MSBX5420.pem
```

### Step 4 — Verify

```
ls ~/keys
```

You should see:

```
MSBX5420.pem
```

---

## 🪟 Windows Setup (PowerShell)

### Step 1 — Create folder

```
mkdir C:\keys
```

### Step 2 — Move file

Move `MSBX5420.pem` into:

```
C:\keys\
```

### Step 3 — Use this path later

```
C:\keys\MSBX5420.pem
```

---

## ⚠️ Important Rules

- Do NOT store `.pem` in this repository  
- Do NOT upload `.pem` to GitHub  
- The `.pem` file is your authentication key  
- The `.pem` file is **provided**, not created  

# 🖥️ PART 1 — CONNECT TO CLUSTER

## 🍎 Mac

```
ssh -i ~/keys/MSBX5420.pem hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
```

---

## 🪟 Windows

```
ssh -i C:\keys\MSBX5420.pem hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
```

---

## ✅ First-time connection

- Type **yes** when prompted  
- You should see:

```
hadoop@ip-xxx-xxx-xxx
```

---

# 📁 PART 2 — CHECK / CREATE TEAM DIRECTORY

```
cd /mnt1/msbx5420_teams
ls
```

---

## 🔍 Check for your team folder

Look for:

```
team_15
```

---

## 🆕 FIRST TIME SETUP

```
mkdir team_15
cd team_15
```

---

## 🔁 RE-ENTRY

```
cd team_15
ls
```

---

# 📤 PART 3 — UPLOAD PROJECT FROM LOCAL MACHINE

Exit cluster:

```
exit
```

---

## Upload project folder

```
scp -i ~/keys/MSBX5420.pem -r ./MSBX_Final_Project_Spark \
hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com:/mnt1/msbx5420_teams/team_15
```

---

## Reconnect and verify

```
ssh -i ~/keys/MSBX5420.pem hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
cd /mnt1/msbx5420_teams/team_15
ls
```

---

# ☁️ PART 4 — UPLOAD TO S3

Navigate to project folder:

```
cd /mnt1/msbx5420_teams/team_15/MSBX_Final_Project_Spark
```

---

## Upload dataset

```
aws s3 cp data/raw/credit_card_transactions.csv \
s3://msbx5420-2026/teams/team_15/data/raw/
```

---

## Upload entire data folder

```
aws s3 cp data/ \
s3://msbx5420-2026/teams/team_15/data/ \
--recursive
```

---

## Verify upload

```
aws s3 ls s3://msbx5420-2026/teams/team_15/
```

---

# 📊 PART 5 — USING S3 IN PYSPARK

Always use S3 paths:

```
df = spark.read.csv(
    "s3://msbx5420-2026/teams/team_15/data/raw/credit_card_transactions.csv",
    header=True,
    schema=TRANSACTION_SCHEMA
)
```

---

# 📓 PART 6 — JUPYTERHUB (OPTIONAL)

## FIRST TIME ONLY

```
sudo docker exec jupyterhub useradd -m -s /bin/bash -N {username}
sudo docker exec jupyterhub bash -c "echo {username}:{password} | chpasswd"
```

---

## EVERY TIME

```
ssh -i ~/keys/MSBX5420.pem -N -L localhost:8080:localhost:9443 \
hadoop@ec2-52-32-236-168.us-west-2.compute.amazonaws.com
```

---

## Open browser

https://localhost:8080

If blocked:
- click Advanced  
- OR type: thisisunsafe  

---

# ⚠️ IMPORTANT RULES

- Do NOT upload large files to JupyterHub  
- Always use S3 for data  
- Clean up cluster files after upload  
- Only use `/mnt1/msbx5420_teams/team_15`  

---

# 🚀 RECOMMENDED WORKFLOW

1. Develop locally (Docker)  
2. Test locally  
3. Upload to S3  
4. Run on EMR  
5. Iterate  

---

# ✅ SUMMARY

| Component | Purpose |
|----------|--------|
| `.pem` | authentication |
| EMR | compute |
| S3 | storage |
| Jupyter | interface |

---

# 💬 FINAL NOTES

- Replace `{username}` and `{password}` if using Jupyter  