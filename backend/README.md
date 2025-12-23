# How to Run
   1. Configure Google OAuth:
       - Go to Google Cloud Console (https://console.cloud.google.com/).
       - Create a project and set up "OAuth consent screen".
       - Create "OAuth 2.0 Client IDs" (Web application).
       - Add http://localhost:8000/auth to Authorized redirect URIs.
       - Add http://localhost:3001 to Authorized JavaScript origins.
       - Copy the Client ID and Secret to backend/.env.

   2. Start the Backend:
   1     cd backend
   2     source .venv/bin/activate
   3     python main.py

   3. Start the Frontend:
   1     cd frontend
   2     npm run dev

  Your app will be available at http://localhost:3001. Clicking "Sign in with Google" will redirect you to
  Google's login page, and then back to your app where your profile information will be displayed.


# Enable External Access

   1. Open OAuth Consent Screen Settings:
       * Go to: Google Cloud Console - OAuth Consent Screen
         (https://console.cloud.google.com/apis/credentials/consent?project=myproject-v2)

   2. Change User Type: Go to Audience Section
       * Click the "Edit App" button (or "Make External" if you see that button immediately).
       * Find the "User type" section (it might be on the first step).
       * Select External.
       * Click Save and Continue.

   3. Add Test Users (Crucial for External Apps):
       * Since your app will likely be in "Testing" status, you must explicitly allow your email.
       * Navigate to the "Test users" section (usually step 3 of the edit flow).
       * Click "Add Users".
       * Enter uttambav@gmail.com.
       * Click Save.
