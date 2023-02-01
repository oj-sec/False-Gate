# False Gate

In lockpicking, a false gate is a modification to a lock's mechanism to give the false impression that a pin has been set, when in fact it will not allow the lock to open. 

False Gate is an automation suite centered around putting honeypot credentials into phishing pages and monitoring sign-ins related to those credentials. False Gate is intended to help defend against modern adversary-in-the-middle phishing techniques that use a proxied session to overcome multifactor authentication by identifying threat actor proxy servers on the fly. 

False Gate is currently a non-functional prototype. False Gate is a planned submodule for [fishfactory](https://github.com/oj-sec/fishfactory).

## Modules 

- `browser_driver.py` - Selenium driver with a generic fuzzer capable of submitting input to several common, simple phishing templates by relying on cycling through interactable web elements with TAB. 
