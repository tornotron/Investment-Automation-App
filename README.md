<div align="center">
<img alt="GitHub contributors" src="https://img.shields.io/github/contributors/tornotron/Investment-Automation-App?style=for-the-badge">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/tornotron/Investment-Automation-App?style=for-the-badge">
<img alt="GitHub repo stars" src="https://img.shields.io/github/stars/tornotron/Investment-Automation-App?style=for-the-badge">
<img alt="GitHub issues" src="https://img.shields.io/github/issues-raw/tornotron/Investment-Automation-App?style=for-the-badge">
<img alt="GitHub license" src="https://img.shields.io/github/license/tornotron/Investment-Automation-App?style=for-the-badge">
</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tornotron">
    <img src="assets/img/favicon.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Investment Automation App</h3>
  <div align="center">
    Attendance Management App  
    <br />
    <a href="https://github.com/tornotron/Investment-Automation-App/docs/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/tornotron/Investment-Automation-App/demo/README.md">View Demo</a>
    ·
    <a href="https://github.com/tornotron/Investment-Automation-App/issues">Report Bug</a>
    ·
    <a href="https://github.com/tornotron/Investment-Automation-App/issues">Request Feature</a>
  </div>
</div>

<!-- TABLE OF CONTENTS -->
<details open>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

<div align="center">
  <!-- Product snapshots should be added here later.... -->
  <!-- <img alt="Product Image 1" width="30%" height="30%" src="Investment-Automation-App-Dashboard-1.png">
  <img alt="Product Image 1" width="30%" height="30%" src="Investment-Automation-App-Dashboard-2.png">
  <img alt="Product Image 1" width="30%" height="30%" src="Investment-Automation-App-Dashboard-3.png"> -->
  <!-- Add vertical space -->
  <br>  
  <br>  
  <br>

</div>

- This is a Flutter application for automating investment with stock broker APIs.
- It is designed to be user-friendly and customizable according to specific requirements.

## Major Features Include:

- **User Authentication**: The app supports user authentication to ensure secure access to data.
- **Portfolio Management**: The app can maintain a portfolio on behalf of the user by interfacing with different stock brokers
- **Automated Optimization**: Automated optimization of portfolio for better returns
- **Multiple Algorithms**: Implementation of multiple trading algorithms for the user to select from

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<!-- Using Devicon font -->
<!-- <img height="50px" width="50px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg" /> -->
<!-- * [![Flutter][Flutter-Icon]][https://flutter.dev] -->

<!-- Using skill-icons -->
<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,fastapi,sqlite,vscode,neovim,docker,kubernetes,dynamodb,githubactions" />
  </a>
</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Using Shields.io and Simple Icons -->
<!-- <img src="https://img.shields.io/badge/Flutter-20232A?style=for-the-badge&logo=flutter&logoColor=61DAFB" />   -->

<!-- GETTING STARTED -->

## Getting Started

The App can be deployed with Python production environment.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

- Setup local dev environment with necessary libraries
- Setup either `anaconda` or `python virtual env`

### Installation

1. Install fastapi and uvicorn before running the project

```bash
  pip install fastapi
  pip install uvicorn
```

2. To start the server run the command below , it will run at endpoint http://localhost:8000/

```bash
uvicorn main:app --reload
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

3. To setup database for local development run:

```bash
postgres -U postgres -f sql/table.sql
```

Note: The directory is not checked into version control, request the developers for getting the file.

## Usage

- The docker files for production will be made available soon

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the GNU License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Proposed folder structure of the project

```
investment_automation_app/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── portfolio.py
│   │   │   │   ├── trade.py
│   │   │   │   └── ...
│   │   │   ├── __init__.py
│   │   │   └── dependencies.py
│   │   ├── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── base.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   ├── trade.py
│   │   │   └── ...
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   ├── trade.py
│   │   │   └── ...
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── portfolio.py
│   │   │   ├── trade.py
│   │   │   └── ...
│   │   ├── __init__.py
│   ├── services/
│   │   ├── data_processing.py
│   │   ├── trading.py
│   │   └── ...
│   ├── main.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_user.py
│   ├── test_portfolio.py
│   └── ...
├── scripts/
│   ├── data_fetch.py
│   ├── data_analysis.py
│   └── ...
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

<!-- CONTACT -->

## Contact

Tornotron - [@tornotron](https://twitter.com/tornotron) - info@tornotron.com

Project Link: [https://github.com/tornotron/Investment-Automation-App](https://github.com/tornotron/Investment-Automation-App)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Branch Ownership

| Status | Branch         | Owner                                                 |
| ------ | -------------- | ----------------------------------------------------- |
|        | `development`  | [Abhijith Anandakrishnan](abhijithananthan@gmail.com) |
|        | `stock-branch` | [Hrishikesh Ajith](hrishikeshajith0@gmail.com)        |

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- Tornotron E Commerce Private Ltd. - [https://tornotron.com](https://tornotron.com)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
