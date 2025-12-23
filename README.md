# Sample OAuth App (FastAPI + React)

This project demonstrates a simple implementation of Google OAuth 2.0 authentication using a **FastAPI** backend and a **React (Vite)** frontend.

## Project Structure

- **`backend/`**: A Python FastAPI application that handles OAuth flow, session management, and API routes.
- **`frontend/`**: A React application built with Vite that provides the user interface for login, logout, and profile display.

## Prerequisites

- **Python** (v3.12+ recommended)
- **Node.js** (v18+ recommended)
- **Google Cloud Platform Account** (for OAuth credentials)

## Setup Instructions

### 1. Google Cloud Configuration

Before running the app, you need to set up a project in the Google Cloud Console.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project or select an existing one.
3.  **OAuth Consent Screen**:
    - Navigate to "APIs & Services" > "OAuth consent screen".
    - Select **External** (unless you are a G-Suite user testing internally).
    - Fill in the required app information.
    - **Important**: Add your email address to the **Test users** list if the app status is "Testing".
4.  **Credentials**:
    - Navigate to "APIs & Services" > "Credentials".
    - Click "Create Credentials" > "OAuth client ID".
    - Application type: **Web application**.
    - **Authorized JavaScript origins**: `http://localhost:3001`
    - **Authorized redirect URIs**: `http://localhost:8000/auth`
    - Copy the **Client ID** and **Client Secret**.

### 2. Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  Install dependencies:
    ```bash
    pip install fastapi uvicorn authlib httpx python-dotenv itsdangerous
    # OR using uv
    uv pip install fastapi uvicorn authlib httpx python-dotenv itsdangerous
    ```
4.  Configure Environment Variables:
    - Create a `.env` file in the `backend/` directory.
    - Add the following content, replacing the placeholders with your Google credentials:
      ```env
      GOOGLE_CLIENT_ID=your-google-client-id
      GOOGLE_CLIENT_SECRET=your-google-client-secret
      SECRET_KEY=your-random-secret-key
      FRONTEND_URL=http://localhost:5173
      ```

### 3. Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```

## Running the Application

1.  **Start the Backend Server**:
    In the `backend` directory (with virtual environment activated):
    ```bash
    python main.py
    ```
    The backend will run at `http://localhost:8000`.

2.  **Start the Frontend Development Server**:
    In the `frontend` directory:
    ```bash
    npm run dev
    ```
    The frontend will run at `http://localhost:3001`.

## Usage

1.  Open your browser and navigate to `http://localhost:3001`.
2.  Click the **"Sign in with Google"** button.
3.  You will be redirected to Google to sign in.
4.  Upon success, you will be redirected back to the app, and your profile name, email, and picture will be displayed.

## Troubleshooting

- **Access Blocked (org_internal)**: Ensure your OAuth Consent Screen is set to **External** and you have added your email to the **Test users** list.
- **Connection Timeout**: The backend is configured with a 30s timeout for Google connections to handle slow network responses.
- **CORS Errors**: Ensure `FRONTEND_URL` in `backend/.env` matches your frontend URL exactly.


The SECRET_KEY is a cryptographic key used to ensure the integrity and security of user sessions.

  Here is the breakdown of why it is strictly required:

  1. Signing Session Cookies (Anti-Tampering)
  In this app, we use Starlette's SessionMiddleware. When a user logs in, we store their info (user: {...}) in a cookie in
  their browser.
   * The Problem: Cookies are stored on the user's computer. A malicious user could easily open their browser tools, find the
     cookie, and change email: "user@gmail.com" to email: "admin@gmail.com".
   * The Solution: The SECRET_KEY is used to create a cryptographic signature for that cookie. When the browser sends the
     cookie back, the server checks the signature using the same key. If the data was modified by even one character, the
     signature won't match, and the server will reject the session.

  2. OAuth State Validation (CSRF Protection)
  When you click "Login with Google", Authlib generates a random "state" string and temporarily saves it in your session
  (cookie) before sending you to Google.
   * When Google redirects you back, it sends that "state" back.
   * Your server compares the state from Google with the one saved in your session.
   * This ensures that the person receiving the Google login token is the same person who started the request, preventing
     Cross-Site Request Forgery (CSRF) attacks. Since this relies on the session, it requires the SECRET_KEY to work securely.

  In summary: It acts like a digital wax seal. It doesn't hide the data (the cookie is just Base64 encoded), but it guarantees
  that you (the server) wrote the data and that nobody else has tampered with it.