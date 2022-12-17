# Client software

Install the client software by first creating and activating a venv with

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install the dependencies with

```bash
pip install -r requirements.txt
```

To run the client software, do

```bash
python3 main.py <matchmaker> <return url> <name>
```

Where

* <matchmaker> is the address of the matchmaker, eg. https://qqqnbsw57m6ed4kdz2nyevyx2m0cduru.lambda-url.eu-central-1.on.aws/
* <return url> is the url the client is going to be listening on, in a form visible from the external world. Eg. http://<your ip>:8081
* <name> is the name you wish to associate with the client
