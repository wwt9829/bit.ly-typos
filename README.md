# Shortlink Typo Generator
Generate and register common typos for your shortlinks.

## Features
* Creates bit.ly and tinyurl.com links
* Modifies bit.ly and tinyurl.com links to use custom endings
* Currently generates 1 typo per link based on
  * Skipped letters
  * Double letters
  * Reversed letters
  * Missed keys
    * QWERTY
    * QWERTZ
    * AZERTY
  * Changed case
  * Confusable characters
* Explainer webpage generation that can be hosted on [my site](https://github.com/wwt9829/bit.ly-typos) (on the [web](https://github.com/wwt9829/bit.ly-typos/tree/web) branch)

## Requirements
* Python 3
* Bitly access token (free token can be obtained from https://app.bitly.com/settings/api)
* TinyURL access token (free token can be obtained from https://tinyurl.com/app/settings/api)
* [requirements.txt](./requirements.txt)

## Usage
API keys are required to be in the system credential store before running.
```
System: [any value, typically system]
Username: bitly [OR] tinyurl
Password: [API key]
```

To do this with `keyring`:
```
$ keyring set system bitly
Password for 'bitly' in 'system': ...
$ keyring get system bitly
```

### Interactive
```
wyatt@wyatt-pc:~# ./shortlink-typo-generator.py
############################
# SHORTLINK TYPO GENERATOR #
############################
Generate and register common typos for your shortlinks! | by Wyatt Tauber (wyatttauber.com)
cmd usage: shortlink_typo_generator.py [-h --help] [-s --skip] [-d --double] [-r --reverse] [-m --miss] [-c --case] [-f --confuse] [-A --all] [-k --keyboard [QWERTY | QWERTZ | AZERTY]] [-P --preview] [-B --bypass (cmd only)] shortlink redirect_url

Enter a shortlink (bit.ly or tinyurl.com) to generate typos for: bit.ly/example
Enter a URL to redirect the typos to: https://example.com/

Press ENTER to create the most common typos (default).
Press c to customize typo generation (-sdrmc).
Press a to create all possible typos (-A).

Do you want to preview the typos to be generated before generating them (good idea on first run of a shortlink) (-P)? (y) y
Skip: ['xample', 'eample', 'exmple', 'exaple', 'examle', 'exampe', 'exampl']
Miss (QWERTY): ['wxample', '3xample', '4xample', 'rxample', 'fxample', 'dxample', 'sxample', ...]
Case: ['Example', 'eXample', 'exAmple', 'exaMple', 'examPle', 'exampLe', 'examplE']
conFuse: ['examp1e', 'exampIe']
This will use 48 API calls. Press ENTER to confirm or any other key to exit... (-B to bypass this warning in cmd) 

Attempting to create 48 bit.ly typos...
Creating bit.ly/xample
...

Generated 44 bit.ly typos that redirect to https://example.com/
https://bit.ly/xample
...
```

### CMD
```
wyatt@wyatt-pc:~# ./shortlink-typo-generator.py tinyurl.com/example https://example.com -B
############################
# SHORTLINK TYPO GENERATOR #
############################
Generate and register common typos for your shortlinks! | by Wyatt Tauber (wyatttauber.com)
Running via cmd | Default typo generation options enabled: skip miss case confuse | Keyboard layout: QWERTY 

Attempting to create 48 tinyurl.com typos...
Creating tinyurl.com/xample
...

Created 44 tinyurl.com typos that redirect to https://example.com
https://tinyurl.com/xample
...
```

## Resources
* Summer 2025 DSU CSC-842 video: [Bit.ly Typos - Final Update | DSU CSC-842 Cycle 6](https://youtu.be/aQl9rtmKbxw)
* [Avoiding Confusion With Alphanumeric Characters](https://pmc.ncbi.nlm.nih.gov/articles/PMC3541865/) (confusable generator data)
* Original 2021 blog post: [Companies: please stop using free URL shorteners | Wyatt Tauber | Medium](https://blog.wyatttauber.com/companies-please-stop-using-free-url-shorteners-especially-for-pii-forms-a32579e47b99) (skip, double, reverse, miss generator data)
