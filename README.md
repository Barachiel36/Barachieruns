# Lemon Gym Savanoriai occupancy tracker

Tracks the public occupancy percentage for Savanorių pr. 168, Kaunas, Lithuania.

Runs via GitHub Actions at approximately 15-minute intervals. GitHub may delay or skip scheduled runs. Readings are appended to `occupancy.csv` with timezone-aware Lithuania timestamps. No login, cookies, or secrets are needed.

## Setup
1. Create a new **public** GitHub repository, e.g. `lemon-gym-tracker`.
2. Upload `track.py` and `README.md` to the repository.
3. Create `.github/workflows/track.yml` with the supplied workflow content. The easiest way is **Add file → Create new file** and type `.github/workflows/track.yml` as its filename, then paste the file's contents.
4. Under **Settings → Actions → General → Workflow permissions**, select **Read and write permissions** and save (if available).
5. Go to **Actions → Track gym occupancy → Run workflow**. After it completes, `occupancy.csv` should appear in the repository.

If the job fails, inspect its log under Actions. If GitHub rejects the workflow's push, verify Actions workflow permissions. The workflow only writes `occupancy.csv`.
