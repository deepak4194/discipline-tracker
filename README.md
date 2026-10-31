# 30-Day Discipline Tracker (Supabase version)

## Streamlit Secrets
In Streamlit app settings, add:

```toml
[supabase]
url = "YOUR_SUPABASE_PROJECT_URL"
key = "YOUR_SUPABASE_PUBLISHABLE_KEY"
```

## Supabase setup
Run `supabase_policies.sql` once in the Supabase SQL Editor. The `daily_progress` table must already exist with `date`, `goal_id`, `completed`, and `updated_at` columns, and RLS enabled.

## Deploy
Push `app.py` and `requirements.txt` to your GitHub repository. Streamlit Cloud will install the Supabase dependency. Configure the Secrets above in the app settings.

Progress is stored in Supabase, not in the app's local filesystem. The provided policies allow anonymous reads and writes; anyone who can access your app can change its tracker data. Keep the app URL private for personal use.
