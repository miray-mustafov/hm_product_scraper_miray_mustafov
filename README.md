<p align="left"><img src="media/project_logo.png" alt="project_logo" width="400"></p>

## Table of contents

* [Task Description](#task-description)
* [Project Overview](#project-overview)
* [Folder Structure](#folder-structure)
* [Setup](#setup)
* [Useful Stuff](#useful-stuff)

---

## Task Description

> 🤖 You can use AI tools, but we will ask questions around scrapy and the problems you faced during the process

#### 1. Introduction

- As part of the team, you'll be responsible for keeping millions of products up to date.
  Using the python Scrapy framework, go to https://www2.hm.com/bg_bg/productpage.1274171042.html
  and retrieve **single** product information about its:
    - name
    - selected color
    - available colors
    - price
    - reviews data

<br>

#### 2. The solution should include:

- the navigation to the product page
- extraction of the data
- Output of the parsed data needs to be in a JSON file.

<br>

#### 3. The following steps need to be implemented:

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

<br>

#### 4. Send solution

- Provide the solution as a link to GitHub/GitLab repository to  
  `anton.popov@edited.com` and `stanislav.milchev@edited.com`

[↑ Back to Top](#table-of-contents)

---

## Project Overview

#### Summary:

- Web scraper for extracting products data from H&M's website

#### Tech:

- <img src="media/scrapy_icon.svg" width="26" height="26" valign="middle">Scrapy,
  <img src="media/postgresql_icon.svg" width="18" height="18" valign="middle"> PostgreSQL,
  <img src="media/docker_icon.svg" width="18" height="18" valign="middle"> Docker,

#### Key Technical Implementations:

- **User-Agent Rotation:** Integrated [RandomUserAgentMiddleware](hm_scraper/hm_scraper/settings.py) that rotates
  between 2,000+ browser identifiers, preventing
  fingerprinting.  
  <br>
- **Proxy IP Rotation:** Integrated proxy rotation to avoid IP-based blocks.
    - *Note:* Despite testing 3 providers, H&M's protection currently holds the line.
    - *Status:* Ongoing development is tracked in
      the [feat/proxy](https://github.com/miray-mustafov/hm_product_scraper_miray_mustafov/tree/feat/proxy) branch.  
      <br>
- **PyCharm Debugger Configuration:** Configured [hm_scraper_debug](.run/hm_scraper_debug.run.xml)
  for direct Scrapy execution and breakpoints within the IDE.  
  <br>
- **Database**: Implemented a [SaveToRDBMSPipeline](hm_scraper/hm_scraper/pipelines.py) that loads
  the item data in a `PostgreSQL` database running on a `Docker` container  
  <br>
- **Error handling & Logging**: added in [SaveToRDBMSPipeline](hm_scraper/hm_scraper/pipelines.py)

#### Upcoming Features:

- Ruff code formatting, Testing, CI/CD, Deployment

[↑ Back to Top](#table-of-contents)

---

## Folder Structure

```shell
hm_product_scraper_miray_mustafov/
├── hm_scraper/                     # project source root directory (contains scrapy.cfg)
│   ├── hm_scraper/                 # project's python module (actual app code)
│   │   ├── database.py             # [Load] db access layer
│   │   ├── items.py                # templates for how our items/products should look
│   │   ├── middlewares.py          # hooks for modifying requests/responses
│   │   ├── pipelines.py            # [Transform] logic for processing scraped items
│   │   ├── settings.py             # global configurations for the app
│   │   └── spiders/                # [Extract] data
│   │       ├── product_spider.py   # main spider to crawl and parse H&M products
│   ├── results/                    # place for the export results (JSON, CSV, etc.)
│   └── scrapy.cfg                  
```

Helper terminal command for generating the tree:

```
uv run python -m directory_tree -I temporary .venv media __pycache__ __init__.py
```

[↑ Back to Top](#table-of-contents)

---

## Setup

<span style="color: #888; font-size: 12px;">Local setup for Windows OS</span>

#### Open the terminal, navigate to a desired folder, and pull the project:

```shell
git clone git@github.com:miray-mustafov/hm_product_scraper_miray_mustafov.git
```

<br>

#### Navigate to the root level of the project:

```shell
cd hm_product_scraper_miray_mustafov
```

<br>

#### Configure and activate python virtual environment

- If uv not installed:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- Then:

```shell
uv venv --python 3.13
.venv\Scripts\activate
```

<br>

#### Install dependencies:

```shell
uv sync
```

<br>

#### Create a copy of `.env.example` file and name it `.env`:

<br>

#### 🚀 Run the app from `hm_product_scraper_miray_mustafov/hm_scraper`:

```shell
uv run scrapy crawl product_spider -O results/product_data_result.json
```
> Results will be saved here: 📂 [results](hm_scraper/results)

<br>

#### If you want to set up also the PostgreSQL database with Docker

1. Make sure Docker Desktop is installed and running.
2. Create a `.env` file in the project root by copying `.env.example`.
3. [Optional] Update the database values in `.env`.
4. Create the PostgreSQL container using the command from [.env.example](.env.example).


[↑ Back to Top](#table-of-contents)

---

## Useful Stuff

- How to initialize a scrapy project:  
  ```scrapy startproject <project_name>```


- How to initialize a scrapy spider:  
  ```scrapy genspider <spider_name> <your.website.com>```  
  ```scrapy genspider product_spider hm.com```


- How to start scrapy shell:  
  ```scrapy shell```


- How to request a URL in Scrapy shell and select elements:  
  ```fetch('<your_url>')``` creates response object  
  ```products = response.css('product-item')```

[↑ Back to Top](#table-of-contents)

---
