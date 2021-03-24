# PlayformSequencer
Interface for running images through platorm.io

# How to get your Authorization JWT Header
1. Open inspect element in your browser
2. Go to the network tab
3. Refresh the page
4. Look for a POST request (method:POST) with a source of x.playform.io
5. Go to the header for that request and find the authorization JWT b64 string
