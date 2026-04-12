# AWS EMR + S3 Setup Guide (Project)

> ⚠️ First-time: complete the PEM setup section before trying to connect.

---

# Overview

This project uses:

- **AWS EMR** for distributed PySpark computation
- **Amazon S3** for shared data storage
- **JupyterHub on EMR** for notebooks

For deployment on EMR, our dataset is stored in:

```text
s3://msbx5420-2026/teams/team_15/
```

This guide walks through:

1. Setting up your `.pem` key
2. Connecting to the EMR cluster
3. Creating your team workspace
4. Uploading files from your machine
5. Copying data to S3
6. Opening JupyterHub
7. Reading data from S3 in PySpark

---

## Why move or copy the `.pem` file?

In Lab 7, `MSBX5420.pem` was kept inside the lab folder.

That works, but it is inconvenient because it makes it seem like you must always `cd` into that folder before using `ssh` or `scp`.

You do **not** need to keep:

- the `.pem` file
- your dataset
- your project folder

all in the same place.

A cleaner setup is:

- keep the key in one permanent location
- keep your repo wherever you want
- keep your dataset wherever you want
- use paths explicitly in your commands

---

# PART 0 — PEM FILE SETUP

## Mac Setup

### Step 1 — Create a keys folder

```bash
mkdir -p ~/keys
```

---

### Step 2 — Copy the `.pem` from Lab 7

Your `.pem` file already exists from Lab 7.

Example path (adjust if needed):

```bash
cp "/Users/your-username/lab7/MSBX5420.pem" ~/keys/
```

---

### Step 3 — Set permissions

```bash
chmod 600 ~/keys/MSBX5420.pem
```

---

### Step 4 — Verify

```bash
ls ~/keys
```

You should see:

```bash
MSBX5420.pem
```

---

## Windows Setup (PowerShell / Command Prompt)

### Step 1 — Create a keys folder

Open PowerShell:

```powershell
mkdir C:\keys
```

---

### Step 2 — Copy the `.pem` from Lab 7

Locate your Lab 7 folder (where your `.pem` already exists).

Example path (adjust if needed):

```powershell
copy "C:\Users\your-username\lab7\MSBX5420.pem" C:\keys\
```

You can also drag and drop the file into:

```text
C:\keys\
```

---

### Step 3 — Verify

```powershell
dir C:\keys
```

You should see:

```text
MSBX5420.pem
```

---

## Important Notes

- Windows does NOT require `chmod`
- You do NOT need to `cd` into the key folder before using it
- The key can live in a completely different location than your dataset or project

---

# PART 1 — CONNECT TO THE EMR CLUSTER

## Cluster addresses

### Cluster 1

```text
ec2-54-202-219-129.us-west-2.compute.amazonaws.com
```

### Cluster 2

```text
ec2-35-91-212-82.us-west-2.compute.amazonaws.com
```

---

## Mac Connection

```bash
ssh -i ~/keys/MSBX5420.pem hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com
```

---

## Windows Connection

```powershell
ssh -i C:\keys\MSBX5420.pem hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com
```

---

## First-time connection

Type:

```bash
yes
```

You should see:

```bash
[hadoop@ip-... ~]$
```

---

# PART 2 — CHECK OR CREATE YOUR TEAM DIRECTORY (ON CLUSTER)

```bash
cd /mnt1/msbx5420_teams
ls
```

Look for:

```bash
team_15
```

If it exists:

```bash
cd /mnt1/msbx5420_teams/team_15
```

If not:

```bash
mkdir /mnt1/msbx5420_teams/team_15
cd /mnt1/msbx5420_teams/team_15
```

---

# PART 3 — UPLOADING FILES (KEY AND DATA DO NOT NEED TO MATCH LOCATIONS)

## IMPORTANT — Run this from your local machine

All upload commands in this section must be run from your **local machine**, NOT from inside the cluster.

If you are still connected to the cluster, exit first:

```bash
exit
```

### Quick Check

Before running `scp`, check your terminal prompt:

- If you see something like:
  ```bash
  user@local-machine ~ %
  ```
  for Mac

  *or*

  ```powershell
  "C:\Users\your-username\
  ```
  for PC

  you are on your local machine (correct)

- If you see something like:
  ```bash
  [hadoop@ip-... ~]$
  ```
  you are on the cluster (incorrect for `scp`)

---

You do NOT need to place your dataset in the same folder as your `.pem`.

`scp` allows you to:

- specify the key location
- specify the file location
- specify the destination independently

---

# PART 4 — UPLOAD A SINGLE FILE (From Local)

If your file or folder path contains spaces, wrap the local path in quotes:

```bash
scp -i ~/keys/MSBX5420.pem -r \
"/path/with spaces/folder" \
hadoop@host:/mnt1/msbx5420_teams/team_15/
```

## Mac

```bash
scp -i ~/keys/MSBX5420.pem \
~/Downloads/credit_card_transactions.csv \
hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com:/mnt1/msbx5420_teams/team_15/
```

---

## Windows

```powershell
scp -i C:\keys\MSBX5420.pem ^
C:\Users\your-username\Downloads\credit_card_transactions.csv ^
hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com:/mnt1/msbx5420_teams/team_15/
```

---

# PART 5 — UPLOAD AN ENTIRE FOLDER (From Local)

## Mac

```bash
scp -i ~/keys/MSBX5420.pem -r \
~/Documents/MSBX_Final_Project_Spark \
hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com:/mnt1/msbx5420_teams/team_15/
```

---

## Windows

```powershell
scp -i C:\keys\MSBX5420.pem -r ^
C:\Users\your-username\Documents\MSBX_Final_Project_Spark ^
hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com:/mnt1/msbx5420_teams/team_15/
```

---

# PART 6 — COPY DATA TO S3 (On Cluster)

## IMPORTANT — Reconnect to the Cluster

This step must be run on the EMR cluster.

If you are not currently connected, reconnect now:

```bash
ssh -i <path-to-key> hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com
```

```bash
cd /mnt1/msbx5420_teams/team_15
```

Then run the following to upload a single file.

```bash
aws s3 cp credit_card_transactions.csv s3://msbx5420-2026/teams/team_15/
```

Run the following to upload a complete folder.

```bash
aws s3 cp emr s3://msbx5420-2026/teams/team_15/emr --recursive
```

---

Verify:

```bash
aws s3 ls s3://msbx5420-2026/teams/team_15/
```

---

# PART 7 — JUPYTERHUB (RUNNING YOUR PROJECT ON EMR)

We use JupyterHub on the EMR cluster to:

- Run PySpark notebooks on the cluster
- Execute your project code in a distributed environment
- Work with data stored in S3

---

## Step 1 — Create JupyterHub user (FIRST TIME ONLY)

After connecting to the cluster via SSH, run:

```bash
sudo docker exec jupyterhub useradd -m -s /bin/bash -N {username}
sudo docker exec jupyterhub bash -c "echo {username}:{password} | chpasswd"
```

Replace `{username}` and `{password}` with your credentials.

This only needs to be done once per user.

---

## Step 2 — Start SSH tunnel (from your machine)

### Mac

```bash
ssh -i ~/keys/MSBX5420.pem -N -L localhost:8080:localhost:9443 hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com
```

---

### Windows

```powershell
ssh -i C:\keys\MSBX5420.pem -N -L localhost:8080:localhost:9443 hadoop@ec2-54-202-219-129.us-west-2.compute.amazonaws.com
```

---

## Step 3 — Open JupyterHub in browser

Go to:

```text
https://localhost:8080
```

If you see a security warning:

- click **Advanced** or **Details**
- continue to the site  
- OR type: `thisisunsafe`

---

## Step 4 — Log in

Use the username and password you created in Step 1.

---

## Step 5 — Run your project

Inside JupyterHub:

- Open or upload your project notebook
- Use the **PySpark kernel**
- Run your existing pipeline and model code
- Ensure your data paths point to S3

---

## Important Notes

- Do NOT upload large datasets into JupyterHub workspace  
- Always use S3 paths for data  
- JupyterHub is only for running code — not for storing data  