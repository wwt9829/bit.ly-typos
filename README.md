<img src="bitly-typos.png" alt="bit.ly Typos logo" width="200"/>

# bit.ly Typos
Generate and register common typos for your bit.ly links

## Features
* Creates bit.ly links
* Modifies bit.ly links to use custom endings
* Currently generates links based on
  * Skipped letters
  * Double letters
  * Reversed letters
  * Missed keys*
  * Inserted keys*

**Only supports 1 missed or inserted key per link, currently*

## Requirements
* Python 3
* bit.ly API key
* [requests](https://pypi.org/project/requests/)
* [validators](https://pypi.org/project/validators/)

## Usage
```
wyatt@wyatt-pc:~# ./bitly_typo_creator.py <bit.ly api key>
Enter a bit.ly ID to generate typos for: bit.ly/example
Enter a URL to redirect the typos to: https://example.com

Attempting to create 58 bit.ly typos...
Creating bit.ly/xample
...

Successfully generated 56 bit.ly typos that redirect to https://example.com
https://bit.ly/xample
...

Complete. Exiting...
```
