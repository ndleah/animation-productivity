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

## Folder Structure

```bash
./AL-data-pipeline
├── .github/
│   └── pull_request_template.md
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
│
├── archieve/
│   ├── AL-data-pipeline.Rproj
│   ├── EDA.ipynb
│   ├── Overheads.R
│   ├── combine_data_leah.R
│   ├── eda_leah.R
│   └── snowflake code - upload.txt
│
├── img/
│   ├── Animal_Logic_logo.png
│   └── framework.png
│
├── utils/
│   ├── chart.py
│   └── db.py
│
├── .gitignore
├── Dockerfile
├── README.md
├── home.py
└── requirements.txt
```

## Application Framework

![framework](img/framework.png)

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


## 📝 Metrics Description
### 🚀 Productivity:
* **Total Review Value:** The weighted value of reviews from submitted work. A Director review has a value of 1, internal review has a value of 0.75, and automated reviews have a vlue of 0.05.
* **File Size Change:** The change in the file size from the last recorded entry. This approximates the magnitude of the work completed.
* **Total File Size:** The total size of the file submitted. This approximates the work completed and the complexity of its context.
* **Normalised Productivity:** This take the *File Size Chnage* and normalises by the peak productivity over the project ( % peak peak productivity). This should only be used after completion of the project.

### 👤 Overheads:
* **Overhead Hours:** Hours submitted with tasks: `td`,`meeting`,`prod`,``training`, or `supervision`. These indicate human hours with no direct value added to this project.
* **Productive Hours:** Hours submitted that are not *Overhead Hours*
* **Overheads per Productive Hour:** The number of *Overhead ours per Productive Hour*. This may identify inefficiencies where Overheads are high when not justified in business context.

