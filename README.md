# Wordle Bot

My work on a wordle bot

Largly based of the videos by 3Blue1Brown:

https://www.youtube.com/watch?v=v68zYyaEmEA&t=705s

This uses selenium to be able to run against the actual wordle website.  

# Install - OLD & Out of Date

Install all requiered packages:

```
pip install -r requirements.txt
```

You many need additional steps to install the selenium driver for your browsers.  See https://selenium-python.readthedocs.io/installation.html for more details.

To build and install wordle_fast, the excelerated C++ library for solving wordle run:

```
python3 setup.py install
```

To run test.py and actually play the game and send a result over text you need a twilio account.  With that account setup
you will need the file account.py at the top level to have the details of your account and your target phone number.

```
twilio_SID = "ACXXX"
twilio_token = "..."

twilio_source_phone = '+13105551212'
twilio_test_phone = '+13105551212'
```

# Running 

There are several files that you can run for different reasons:

## test.py

This script will run wordle and connect to the New York Times site and play wordle.  

## sim.py

This script is used to test out wordle solvers and measure there performance.  

## game.py

This script will let you play wordle on the command line

## other files

These other files provide functionality used on these scripts.  Or test code.  Many of these scripts when run will provide 
some testing of the functionality they contain