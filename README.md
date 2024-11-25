## ServiceNow: Accelerator Recommendation Engine (sn_sys_are)

1. https://github.com/dev-philip/Accelerator-Recommendation-Engine
2. https://github.com/dev-philip/Recommendation-Engine-Frontend

Your mission is to develop an innovative and robust recommendation engine designed to enhance our Technical Accelerators program. At any given time, our team is developing 8-10 new Accelerators while actively delivering up to 600 ongoing projects. The challenge is to develop a way to match customers to the Accelerators they would benefit from the most.

The core objective is to build a recommendation engine that excels in two key areas:

1. Recommending New Accelerators to Existing Customers
2. Recommending New Accelerators to New Customers

Your submissions will be evaluated on the following criteria:

1. Accuracy and Relevance: How well the recommendation engine can match accelerators to the needs of existing customers
2. Predictive Capability: The engine’s ability to efficiently recommend accelerators to new customers with minimal historical data.

## Data Set: They Provided 4 Excel file

1. accelerators.xlsx => This file contains the accelerators we want to recommend to both New Customers and Existing Customers
2. Products.xlsx => This contains the products and categories the accelerators fall under
3. Entitlements.xlsx => This file contains the accelerators the company already purchased there is a column called “implements” which is a boolean value that means if the company has already implemented the accelerators or not. For example “true” means the company has already implemented the accelerators and has started using them, and “False” means the company has not implemented them yet
4. Companies.xlsx - This file contains the existing customers (companies) that are already using some accelerators and may or may have not implemented them. So the recommendation system will recommend more accelerators to them that will help them achieve their goal or task or build their productivity or similar to something they are doing

## Here’s the list of Python libraries I am using:

1. pandas (for data manipulation)
2. scikit-learn (for machine learning algorithms and similarity metrics)
3. Surprise (for collaborative filtering models)
4. numpy (for numerical computations)
5. jupyterlab (for running notebooks)
6. matplotlib (for visualizations)
7. Flask (For APi's)

## To install these libraries, run:

`pip install -r requirements.txt`

## Activate Virtual Environment using Conda

1. Create a New Conda Environment
   `conda create --name sn_sys_are python=3.11`

2. Activate the Conda Environment
   `conda activate sn_sys_are`

3. Create a requirements.txt File

4. Install Packages Using requirements.txt
   `pip install -r requirements.txt`

5. Verify Installed Packages
   `pip list`

## GIT

…or create a new repository on the command line
echo "# Accelerator-Recommendation-Engine" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/dev-philip/Accelerator-Recommendation-Engine.git
git push -u origin main

## Execution

1. python src/collaborative_filtering.py
2. python src/collaborative_filtering_all.py
3. python src/content_based_filtering.py
4. python src/hybrid_recommendation.py
5. python src/hybrid_recommend_langchain.py

## Run the Flask Server

1. Navigate to the directory where your app.py file is located
2. Activate the Conda Environment
   `conda activate sn_sys_are`
3. run the following command: `python app.py`

## Deployment (Optional)

If you want to deploy your Flask app for production, consider using a WSGI server like Gunicorn:

`sudo apt-get update -y`
`sudo apt install python3-pip -y`
`sudo apt install python3-virtualenv -y`
`virtualenv venv`
`source venv/bin/activate`

`pip install -r requirements.txt`
`pip install gunicorn`

`pip install gunicorn`
`gunicorn -w 5 -b 0.0.0.0:5000 app:app`

## Certbot is used to obtain the SSL certificate. Install it on your EC2 instance.

1. Install Certbot
   `sudo apt update -y`
   `sudo apt install certbot -y`
   `sudo apt install python3-certbot-nginx`

2. Install Web Server
   `sudo apt install nginx -y`

3. Start and enable Nginx:
   `sudo systemctl start nginx`
   `sudo systemctl enable nginx`

4. Nginx Configuration: Create a new Nginx configuration file for your Flask app:

`sudo nano /etc/nginx/sites-available/flask_app`

5. Add the following content:

`server {
listen 80;
server_name courseeventapp.online;

    location / {
        proxy_pass http://54.196.142.248:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}`

6. Enable the configuration:

`sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/`
`sudo nginx -t` # Test the configuration
`sudo systemctl reload nginx` # Reload Nginx

7. Obtain the SSL Certificate: Run the Certbot command to obtain an SSL certificate.

- `sudo certbot --nginx -d your-domain.com -d www.your-domain.com`
- `sudo certbot --nginx -d courseeventapp.online -d www.courseeventapp.online`

8. Automate Certificate Renewal
1. Open the crontab:
   `sudo crontab -e`
1. Add the following line to renew certificates daily. This runs the renewal process every day at 3:00 AM and reloads Nginx if a certificate is renewed:
   `0 3 * * * certbot renew --quiet && systemctl reload nginx`
