## About

I built a full stack MVP for a client that allows landlords to take out loans and use their future property rent as collateral.

### Key features

- User authentication to allow registration, log in and password reset over email
- Stateful authentication with token authentication
- Ability to create an advance (loan) and submit supporting documents
- Schedule of payments and their statuses are generated once the state of each loan changes
- Custom admin panel that allows administrators to change loan and payment details, plus 2FA for admin users
- Third party API integration with Persona for KYC (Know Your Customer) checks and Sendgrid (for emails)

### Tech used

- Languages: Python, JavaScript, CSS
- Frameworks and Libraries: React, Django, Django REST Framework
- Deployment: AWS Amplify, Elastic Beanstalk, Load Balancers, S3

### Planning

After a few lengthy discussions with the client, I codified the spec for this MVP into a doc (high level points can be found at the bottom of this readme) so that there would be no misunderstanding and a clear record of business logic.

It was decided to develop the frontend first with the use of local storage and demo data. This is so that the client would be able to show off the MVP to potential investors while the backend is being built out.

Later, as the backend was being built out, I started connecting the frontend to the REST API to enable end to end functionality and move away from storing app data in local storage.

### Frontend

React – I used React for the frontend functionality and axios library for interacting with the backend. When a user logs in, an auth token is saved to local storage and is used with each request to the backend to authenticate it. I also used react router dom to fetch the URL details to identify each advance (loan).

CSS3 - I decided to use vanilla CSS for this MVP because I wanted to revise some of the styling and positioning skills that I learned in 2022. This also gave me the perfect opportunity to practise more advanced layout features like flexbox and grid. The client specified that mobile friendly frontend was not a priority for this MVP, however I still tried my best to design pages that would look good on all screen sizes.

### Backend

Django REST Framework (DRF) – the backend is based on Django and DRF, and for the database, I used PostgreSQL. I configured 2 third party APIs into the backend – Sendgrid to send emails to existing users that would like to reset their passwords, and created a webhook for Persona (along with IP whitelisting) that would accept a POST request whenever a user would successfully verify their identity on the frontend, which in turn would change the `is_verified` flag in the backend.

I also utilised UUID and short UUID for identifying users and loans, as that is more secure than using sequential IDs that are default in Django.

To create superuser admin accounts, I would `ssh` into the EC2 instance and use the CLI to configure the administrator commands.

### Deployment

The frontend app is deployed on AWS Amplify that syncs with a GitHub repo and adds environment variables. I added a YAML file in the root directory that would `cd` into the client folder as I initially thought both the backend and the frontend would be in the same repo (which is one of the reasons why there are multiple branches in the frontend repo).

The backend app and database are set up with AWS Elastic Beanstalk (EB), along with S3 for file storage. The EB environment has a load balancer with a couple of listeners that handle HTTP and HTTPS requests (the HTTPS listener was configured to use SSL certificates held by the main domain of the project).

### Challenges & Solutions

### Frontend

Challenge - at the beginning, I used `useContext` hook and create a global context that could share data across any pages or components. However, I came across cases where there would be a race condition between the functions executing inside the global context and the async functions in the page/component, which lead to some unnecessary re-renders and API calls.

Solution - I moved away from using global context and added similar code to each page/component to ensure no race conditions would be present. This is not the most elegant solution and in the future, I plan to refactor the code, and perhaps use React Router Dom or Redux to reduce the amount of states and functions.

### Backend

Challenge - for Persona webhook, I had to implement IP whitelisting to allow requests only from Persona’s range of IP addresses, otherwise the user would be able to change their own KYC status by sending the request directly to the backend. The problem is that each client request is handled by a load balancer and thus, Django sees the IP address of the load balancer, and not the IP address of the client.

Solution - I utilised `HTTP_X_FORWARDED_FOR` of the request to fetch the origination IP address of the client and check if that address belongs to a list of whitelisted IP addresses. This way only authorised requests would be successfully processed by the backend.

---

### OLD README - Ignore

### MVP for Factored

#### Overview

Create a full stack app that uses React for the frontend and Django REST API for the backend. This app would allow users to create an account, log in, pass certain checks and create an advance (loan).

#### Frontend spec

- Users need to have the ability to create an account using email and password
- Users need to have the ability to reset their password using the online form
- Register and login pages are public, all other pages require authentication
- Users need to accept Ts&Cs and Privacy Policy before creating an account
- When logged in,the user has to complete these steps before they can create their advance
  - Complete Persona's KYC flow
  - Complete Persona's current address verification flow
  - Update their mobile number
  - Go through address history for the last 3 years
- Integrate with Persona's API for KYC
- Once they passed these checks, they can create their advance - the flow will include 4 screens:
  - Description, reason for advance, property address and monthly rent details
  - Document upload for lease agreement (required), tenant vetting and rent protection (latter two are optional)
  - Advance finance details - amount of £ required, term and display calculations
  - Bank account details - name, sort code and account number
- Logged in dashboard needs to display a table with user's advances
- User should be able to view their profile e.g. name, email, current address address

#### Backend spec

- Use Django admin panel for user and advance management
  - Each user needs to have a comment box
  - Each advance needs to show the uploaded documents (pull from S3)
  - Each advance needs to have a comment box
  - Admin can change the status of each advance
- Use DRF for the REST API
- Use Postgres for the DB
- Advance will have 5 statuses:
  - Incomplete
  - Pending approval
  - Active
  - In arrears
  - Repaid
- User's KYC status has to be updated based on their Persona flow outcome
- Email notification
  - Send the user an email when they sign up
  - Send the user an email when they request to reset password
  - Send the user an email when their advance has been created
  - Send the user an email when the status of their advance changes
  - Send admin an email when an advance is created
- Controls
  - Cannot make authenticated API requests to view other users
  - Cannot make authenticated API requests to view other advances
  - Cannot change the user ID or advance ID

#### Nice-to-haves

- Mobile support
- Integrate soft credit checks (third party API) into the verification flow
- Two-factor authentication for the user

#### DevOps

- Host the app on AWS
- Configure the DNS so that the app is hosted on "app.example.com"
- Use Docker (?)
