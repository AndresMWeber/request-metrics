<div align=center>
    <h1 align=center>
        <br>
        request-metrics
        <br>
        <img width="100px" align=center src="https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png" alt="JS logo">
        <img width="100px" align=center src="https://www.python.org/static/community_logos/python-powered-h-140x182.png" alt="python logo">
        <img width="100px" align=center src="https://firebounty.com/image/352-codeclimate-code-climate-security" alt="codeclimate logo">
    </h1>
    <h1 align=center>
        <a href="https://codeclimate.com/github/AndresMWeber/request-metrics/maintainability">
            <img src="https://api.codeclimate.com/v1/badges/7ca3f9229751fa068317/maintainability" />
        </a>
    </h1>
    <h4>The start of a library for testing out metrics for http requests.  Will only have average response time for now.</h4>
</div>


## 📝 Table of Contents
- [About](#about)
- [Setup](#setup)
- [Usage](#usage)
- [Documentation](#documentation)
- [Testing](#testing)
- [Built Using](#built_using)
- [Authors](#authors)

## 📙 About <a name = "about"></a>
The start of a library for testing out metrics for http requests.  Will only have average response time for now.

## ⚙️ Setup <a name = "setup"></a>
#### Requirements:

1.  Must be using python3 and have python3 as an available shell command.
1.  This install script uses `venv` as well.

#### Installation:
(if you already have a virtual environment workflow, just activate your venv and run `python setup.py install`)

`source bin/setup.sh` - Run this from the top directory: this creates the venv in the top directory and activates it after running `python3 setup.py install`

## 📡 Usage <a name = "usage"></a>
1.  Make sure you have activated the `virtual environment` if you did the install steps but started a new terminal by running:

    ``` bash
    source bin/activate_venv.sh
    ```

2.  Designed as a CLI tool, you should navigate to the clone directory and run:
    ``` bash
    python get_average_response_time.py
    ```


3. It defaults to querying the PassNinja API, however you can input whatever API you want.  You can also specify the REST verb via the -v, --verb flag, but it also defaults to POST.  If you want to customize the POST request data, modify the `./payload.json` file as desired.

### Sample run command:
``` bash
python get_average_response_time.py -u 'https://api.passninja.com/lambda-2048/passes/'
```
### Sample Output:
``` bash
Running post request to https://api.passninja.com/lambda-2048/passes/ - 10 time(s):
Loading payload file: ./payload.json
Succesfully loaded payload file.

|  200  | - 5.488187500013737
|  200  | - 5.700262800004566
|  200  | - 5.766223699989496
|  200  | - 5.923188999993727
|  200  | - 5.978442899999209
|  200  | - 6.658917599997949
|  200  | - 6.827372700005071
|  200  | - 7.669452500005718
|  200  | - 7.74673030001577
|  200  | - 7.802989500021795


Average run time was 6.56s over 10 runs with 0 non-200 responses.
```
## 📁 Documentation <a name = "documentation"></a>
Feel free to run the script with the --help command:
``` bash
╰─ python get_average_response_time.py --help
Usage: get_average_response_time.py [OPTIONS]

Options:
-r, --runs INTEGER  Number of requests to run.
-u, --url TEXT      API Endpoint to post to.
-d, --data TEXT     JSON data (if using POST).
-v, --verb TEXT     The type of request to perform
--help              Show this message and exit.
```

## 🧪 Testing <a name = "testing"></a>

Nothing yet.

## ⛏️ Built Using <a name = "built_using"></a>
- [Python](https://python.org/) - Backend Code
- [CodeClimate](https://d341kum51qu34d.cloudfront.net/images/2019-04-redesign/code_climate_logo-a046042f.svg) - Code Health Metrics

# ✍️ Authors <a name = "authors"></a>
* [Andres Weber](https://github.com/AndresMWeber)