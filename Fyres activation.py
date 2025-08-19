import FyresIntegration

FyresIntegration.apiactivation(
    client_id="IGWSYQFEPS-100",  # ✅ Must include "-100"
    redirect_uri="https://www.google.co.in/",  # ✅ Should match exactly what's set in Fyers App Dashboard
    secret_key="J1K6VOBRYJ",  # ✅ Your app secret from the Fyers App Dashboard
    grant_type="authorization_code",  # ✅ Always this
    response_type="code",  # ✅ Always this
    state="sample"  # ✅ Any string you want (used to track session, not validated)
)

