# PlayformSequencer
Interface for running images through platorm.io

# How to get your Authorization JWT Header
1. Open inspect element in your browser
2. Go to the network tab
3. Refresh the page
4. Look for a POST request (method:POST) with a source of x.playform.io. If you dont see a POST from playform, you need to generate one. An easy way to do this is by uploading a file or clicking the generate button.
5. Go to the header for that request and find the authorization JWT b64 string, copy it into the config
