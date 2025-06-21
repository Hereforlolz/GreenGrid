🌿 GreenGrid AI

AI-powered neighborhood energy orchestration for equitable, sustainable power in Missouri

📌 Problem Statement

Missouri’s suburban and urban communities face high energy costs, aging grid infrastructure, and lack of user-friendly tools to optimize household usage- especially in linguistically diverse and low-income neighborhoods.

➡️ In St. Louis City alone, ~20,000 households spend 6%-30% of income on utilities.
➡️ Grid reliability struggles with peak loads and limited coordination.

GreenGrid AI tackles this by forecasting household energy demand, balancing loads, and providing personalized, multilingual sustainability tips.

💡 Solution Overview

✅ IoT Edge: Simulated smart meters (AWS IoT Greengrass)
✅ Cloud ML: Amazon SageMaker predicts next-day usage
✅ Generative AI: Amazon Bedrock creates personalized, multilingual tips
✅ Frontend App: AWS Amplify shows live usage, forecast, and actions

⚙️ Technical Architecture

  ![architecture.png](attachment:be508e55-6017-4a29-bf6b-7d5a075b9e4f:architecture.png)

🎥 Demo Video
👉 Watch on YouTube: https://www.youtube.com/watch?v=DHTxfkB2HR8&feature=youtu.be
📃 Read on Notion: https://www.notion.so/GeenGrid-212b2f6a587d8061a859ed697f4ab5d6?source=copy_link

📂 Repository Structure

Root/
│
├── .vscode/             # VSCode configs
├── amplify/             # Amplify deployment configs
│   ├── .config/
│   ├── backend/
│   │   ├── auth/greengrid73fa1012
│   │   ├── function/greengridforecastfunction
│   │   ├── types/
│   │   ├── backend-config.json
│   │   ├── tags.json
│   ├── hooks/
│   ├── cli.json
│   ├── team-provider-info.json
│
├── docs/                # Diagrams, slides
│   ├── architecture.mmd
│
├── greengrid-frontend/  # Your React frontend
│   ├── amplify/
│   ├── .config/
│   ├── hooks/
│   ├── public/
│   ├── src/ (App.js etc.)
│   ├── .amplifyignore
│   ├── .gitignore
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│
├── notebooks/           # Jupyter notebooks for SageMaker
│   ├── greengrid_energy_insights.ipynb
│
├── scripts/             # Python helper scripts
│
├── src/                 # Backend Python scripts
│   ├── __init__.py
│   ├── check_aws.py
│   ├── dynamo_utils.py
│   ├── lambda_function.py
│   ├── main_pipeline.py
│   ├── simulate_neighborhood.py
│   ├── test_lambda.py
│   ├── requirements.txt
│
├── tests/               # Unit tests
├── .gitignore
├── README.md            # Root README (the one you want to polish)
├── requirements.txt     # Python deps
├── package.json / lock  # Node deps (if needed)


🚀 How to Run Locally

Clone this repo

  git clone https://github.com/Hereforlolz/GreenGrid.git
  cd GreenGrid

Install dependencies

  pip install -r requirements.txt

Run local test scripts (for simulation)

  # Example: test the forecast notebook
  jupyter notebook sagemaker/forecast_notebook.ipynb

Deploy frontend (optional)

  cd greengrid-frontend
  npm install
  npm start

📈 Future Work

  🔄 Connect live data to frontend and polish the UX
  🔄 Live data API, smart plug integration, pilot with real households

🙌 Author
👤 SreeNidhi (Solo Builder)

🏆 License
MIT — open for learning and impact.
