# PolyBot
A tool to help the Poly copy-reading process! :D

  Let's face it-computers are better are repeatitive tasks. And, in spite of what one may want to believe, fact checking is, as a process, very repeatitive. Luckily, this leaves room for automation. This is the vision behind PolyBot. Although the idea sounds great in theory, I warn that one should view PolyBot as a mere tool for the Copy Reader. 

PolyBot has the following dependencies:
  1) OS and Time [OS interactions]
  2) IMAPLIB [Fetching and Deleting E-Mails]
  3) Autocorrect [Autocorrection]
  4) Language Tool Python [Grammar checking]
  5) Spacy (and en_core_web_trf machine learning model) [Name Detection]
  6) Chrome Driver (developemental version of chrome which allows programmatic control) [LinkedIn Scraping]
  7) Google Search [LinkedIn Scraping]
  8) LinkedIn Scrapper [LinkedInScraping]
  9) Selenium [LinkedInScraping]
  10) Yagmail [Sending E-Mails]
  11) NLTK [Sentiment Analysis]
  12) Vader Lexicon [Sentiment Analysis]
  13) Punkt [Sentiment Analysis]
  14) Markovify [Redundancy Analysis]
  15) PySimilar [Redundancy Analysis]
 
  To install these dependencies, preform "pip install" followed by the packages name. Note, chrome driver requires an additional install which can be found when googling the applications name and Spacy requires an additional command to download the appropriate machine learning model.
  
  After installation, run "polyBotServerDriver.py" and modify the credentials in all source files to your respective Bot's associated credentials. This script will look for new emails every 10 seconds. Note, after an email is processed, it is deleted from the inbox of the account and a folder corresponding to the email with an HTML file is created. 
  
  From the end-user perspective, one simply emails the PolyBot and recieves within 5-10 minutes a email of its analysis.
  
Current Features:
  1) Basic Spelling Check
  2) Poly-Specific Spelling Check
  3) Grammar Checking
  4) Name and Context Parsing
  5) LinkedIn Scraping and Credential Verification
  6) E-Mailing Interface
  7) Sentiment Analysis using Markov Chain + Vader Lexicon
  8) Redudancy Analysis using PySimilar's Cosine Statistic

Upcoming Features:
  1) RPI Directory Scraping
  2) Reference Counting
  3) Modifiable Style Guide File

To try it out, send an email WITH A SUBJECT to thebest.polybot@gmail.com
