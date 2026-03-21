<p align="left"><img src="media/project_logo.png" alt="project_logo" width="300"></p>

## Table of contents

* [Task Description](#task-description)
* [Project Overview](#project-overview)
* [Folder Structure](#folder-structure)
* [Setup](#setup)
* [Useful Stuff](#useful-stuff)

---

## Task Description

### 1. Introduction

- As part of the team, you'll be responsible for keeping millions of products up to date.
  Using the python Scrapy framework, go to https://www2.hm.com/bg_bg/productpage.1274171042.html
  and retrieve **single** product information about its:
    - name
    - selected color
    - available colors
    - price
    - reviews data

### 2. The solution should include:

- the navigation to the product page
- extraction of the data
- Output of the parsed data needs to be in a JSON file.

### 3. The following steps need to be implemented:

- request to load the page located at https://www2.hm.com/bg_bg/productpage.1274171042.html
- parse of the HTML
- collect the data:
    - name
    - price
    - selected default color
    - available colors
    - review count + review score
    - output the data as a JSON file, for example:
        ```json
        {
          "name": "String",
          "price": "Decimal",
          "current_color": "String",
          "available_colors": "Array",
          "reviews_count": "Integer",
          "reviews_score": "Double"
        }
        ```

### 4. Send solution

- Provide the solution as a link to GitHub/GitLab repository to  
  `anton.popov@edited.com` and `stanislav.milchev@edited.com`

### *NOTE

You can use AI tools, but we will ask questions around **scrapy** and the **problems you faced during the process**

[↑ Back to Top](#table-of-contents)

---

## Project Overview

* **Summary**: Web scraper for extracting products data from H&M's website
* **Tech**: Scrapy, `todo`

### Key Technical Implementations:

`todo`

### Upcoming Features & Scale-Up Plan:

`todo`

[↑ Back to Top](#table-of-contents)

---

## Folder Structure

```shell
root_folder/
└── src/
    └── hm_scraper/
        ├── spiders/            # Extract/Scrape data
        │   └── hm_products.py
        ├── __init__.py
        ├── items.py            # define templates, how our product would look
        ├── pipelines.py        # Transform/Load data
        └── settings.py
```

helper terminal command for generating the tree:

```shell
uv run python -m directory_tree -I temporary media __init__.py __pycache__ *.*
```

[↑ Back to Top](#table-of-contents)

---

## Setup

Local setup for Windows OS

### Open the terminal, navigate to a desired folder, and pull the project:

```shell
git clone git@github.com:miray-mustafov/hm_product_scraper_miray_mustafov.git
```

### Navigate to the root level of the project:

```shell
cd hm_product_scraper_miray_mustafov
```

### Configure and activate python virtual environment

If uv not installed:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then:

```shell
uv venv --python 3.13
.venv\Scripts\activate
```

### Install dependencies:

```shell
uv sync
```

### Create a copy of `.env.example` file and name it `.env`:

### Run the app:

```shell
todo
```

[↑ Back to Top](#table-of-contents)

---

## Useful Stuff

How to initialize a scrapy project:  
```scrapy startproject <project_name>```

[↑ Back to Top](#table-of-contents)

---
