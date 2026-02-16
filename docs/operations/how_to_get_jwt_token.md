To get a JWT token for your superuser account, please follow these steps:

1.  **Ensure your backend and frontend are running.**
2.  **Log in via the Frontend:**
    *   Open your browser and navigate to `http://localhost:5173/login`.
    *   Log in with the email and password of the account you previously made a superuser.
3.  **Retrieve Token from Local Storage:**
    *   After logging in, open your browser's developer tools (usually by pressing `F12` or right-clicking and selecting "Inspect").
    *   Go to the "Application" tab (or "Storage" -> "Local Storage").
    *   Find the entry for `http://localhost:5173` (or your frontend's URL) and locate the `access_token` key.
    *   The value associated with this key is your JWT token. It will be a long string starting with `ey...`.

4.  **Alternatively, use `curl`:**
    *   If you prefer using the terminal, you can send a POST request to the `/token` endpoint:
        ```bash
        curl -X POST "http://localhost:8000/token" 
             -H "Content-Type: application/x-www-form-urlencoded" 
             -d "username=YOUR_SUPERUSER_EMAIL&password=YOUR_SUPERUSER_PASSWORD"
        ```
        Replace `YOUR_SUPERUSER_EMAIL` and `YOUR_SUPERUSER_PASSWORD` with your superuser's credentials. The `access_token` will be in the JSON response.

Once you have your superuser JWT token, please paste it here so I can proceed with seeding the product database.
