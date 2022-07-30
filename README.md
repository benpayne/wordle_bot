My work of a wordle bot

Largly based of the videos by 3Blue1Brown:

https://www.youtube.com/watch?v=v68zYyaEmEA&t=705s

This uses selenium to be able to run against the actual wordle website.  

to build and install c_extension for fast execution

`python3 setup.py install`

To run test.py and actually play the game and send a result over text you need a twilio account.  With that account setup
you will need the file account.py at the top level to have the details of your account and your target phone number.

```
twilio_SID = "ACXXX"
twilio_token = "..."

twilio_source_phone = '+13105551212'
twilio_test_phone = '+13105551212'
```