## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Live Deployment](#live-deployment)
- [Quickstart](#quickstart)
  - [Requirements](#requirements)
  - [Development Workflow](#development-workflow)
    - [Clone the repository](#clone-the-repository)
    - [Build and launch all containers](#build-and-launch-all-containers)
    - [(Optional) Reset dev environment](#optional-reset-dev-environment)
- [Development Guide](#development-guide)
  - [Backend Django](#backend-aspnet-core)
    - [Configuration](#configuration)
    - [Dependencies](#dependencies)
    - [Entity Framework Migrations](#entity-framework-migrations)
    - [Admin User Setup](#admin-user-setup)
    - [Run tests](#run-tests)
    - [Database Schema](#database-schema)
  - [Frontend (HTML, CSS, Javascript)](#frontend-angular--angular-material)
    - [Dependencies](#dependencies-1)
    - [Run tests](#run-tests-1)
---

## Tech Stack

| Layer         | Technology            |
|---------------|-----------------------|
| Frontend      | HTML, CSS, Javascript |
| Backend       | Django                |
| Database      | PostgreSQL            |

---

## Architecture Overview

### Requirements

### Development Workflow

#### Clone the repository
```bash
git clone https://github.com/yourusername/Horizon_Analytics
cd Horizon_Analytics
```
#### Build and start the containers
```bash
docker-compose up --build
```

#### Stop the containers
```bash
docker-compose down
```