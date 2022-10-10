![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

# Data Pipeline for Productivity <img src="http://pixelartmaker-data-78746291193.nyc3.digitaloceanspaces.com/image/96a034beedb086d.png" align="right" width="150" />

> Group project assignment for the iLab2 subject - Spring 2022

## 👤 Authors

* [Leah Nguyen](https://github.com/)
* [Michelle Xiong](https://github.com/)
* [William Mcdermott](https://github.com/)
* [Mingpeng Wang](https://github.com/)


## :octocat: GitHub Branch Structure

```
.main/               <- Main branch
│
├── will/            <- Will's branch
│
├── leah/            <- Leah's branch
│
├── michelle/        <- Michelle's branch
│
├── mingpeng/        <- Mingpeng's branch
```

## Framework
![framework](framework.png)

## ⚙️ Setup Instruction

<details>
<summary>
Step 1: Clone the repository. 
</summary>

Open git bash and type:

```bash
git clone https://github.com/ndleah/credit-card.git
```

> This makes a local copy of the repository in your machine.

</details> 

---

<details>
<summary>
Step 2: Switch to your branch
</summary>

```bash
git checkout branch_name    <--- Switching the branch
```

For example

```bash
git checkout akshaya        <--- Switching the branch
```

</details> 

---

<details>
<summary>
Step 3: Ready, Set, Go...
</summary>

**Commit your changes locally**

```bash
git commit -m "description of your commit".
```

**Upload the changes (including your new branch) to GitHub**

```bash
git push origin MyNewBranch
```

For example

```bash
git push origin akshaya
```
</details> 

---

<details>
<summary>
Step 4: Pull Requests
</summary>

Once you have completed these steps, you are ready to start contributing to the project and creating **pull requests**.

Steps need to take:

> 1. Go to the main repo on GitHub where you should now see your new branch
> 2. Click on your branch name
> 3. click on “Pull Request” button (URC)
> 4. Click on “Send Pull Request”

</details> 

## ⚙️ Instructions

Clone the repository

```bash
git clone https://github.com/ndleah/AL-data-pipeline.git
cd AL-data-pipeline
```

Run the Docker container with docker compose

```bash
docker-compose up -d --build
```

The container will start in detached mode and can now be accessed via [http://localhost:8501](http://localhost:8501). 

Whenever you change the app/streamlit_app.py the steamlit application will update too. If you want to build upon that example, just add your dependencies to the Dockerfile and rebuild the image using docker-compose.

After you are done, and you want to tear down the application, either

```bash
docker-compose stop
```

to stop the application, or use 

```bash
docker-compose down --rmi all
```

to stop the application, remove the stopped containers and optionally `--rmi all` / remove all images associated in the docker-compose.yml file.