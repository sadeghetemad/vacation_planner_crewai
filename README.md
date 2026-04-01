# 🌍 Vacation Planner Crew AI

An AI-powered vacation planning system built with CrewAI and AWS
Bedrock.\
This project uses multiple AI agents to collaboratively research
destinations and generate structured travel itineraries.

------------------------------------------------------------------------

## ✨ Features

-   🤖 Multi-agent system (Researcher + Planner)
-   🌐 Intelligent destination research
-   🗺️ Detailed itinerary generation
-   🍝 Local food recommendations
-   🧠 Powered by AWS Bedrock LLMs
-   🎨 Streamlit UI for interaction
-   🔐 Environment-based configuration with `.env`

------------------------------------------------------------------------

## 🧠 Agents

### 1. Vacation Researcher

-   Role: Senior Vacation Researcher\
-   Goal: Find the best destinations related to the user's topic\
-   Specialty: Hidden gems, unique experiences

### 2. Itinerary Planner

-   Role: Itinerary Planner\
-   Goal: Create a structured travel plan\
-   Includes:
    -   City overview & history\
    -   Tourist attractions\
    -   Local food recommendations

------------------------------------------------------------------------

## 🏗️ Project Structure

    vacation_planner/
    ├── .venv/
    ├── knowledge/
    ├── src/vacation_planner/
    │   ├── config/
    │   ├── tools/
    │   ├── crew.py
    │   ├── main.py
    │   └── __init__.py
    ├── tests/
    ├── .env
    ├── streamlit_ui.py
    ├── AGENTS.md
    ├── pyproject.toml
    ├── uv.lock
    └── README.md

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone the repository

``` bash
git clone https://github.com/sadeghetemad/vacation-planner.git
cd vacation-planner
```

### 2. Create virtual environment

``` bash
uv venv
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

``` bash
uv pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 Environment Variables

Create a `.env` file:

    AWS_ACCESS_KEY_ID=your_key
    AWS_SECRET_ACCESS_KEY=your_secret
    AWS_DEFAULT_REGION=us-west-2
    MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

------------------------------------------------------------------------

## 🚀 Running the Project

### ▶ Run CrewAI pipeline

``` bash
crewai run
```

### 🎨 Run Streamlit UI

``` bash
streamlit run streamlit_ui.py
```

------------------------------------------------------------------------

## 🧪 Example Input

    Plan a 5-day vacation in Italy focused on culture and food

------------------------------------------------------------------------

## 🧰 Tech Stack

-   Python
-   CrewAI
-   AWS Bedrock
-   Streamlit
-   python-dotenv

------------------------------------------------------------------------

## ⚠️ Notes

-   Do NOT commit your `.env`
-   Use correct Bedrock model IDs
-   Ensure AWS region matches model availability

------------------------------------------------------------------------

## 📄 License

MIT License
