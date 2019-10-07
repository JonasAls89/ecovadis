# Ecovadis
A connector for using the EcoVadis API

## Prerequisites
python3

## API Capabalities
to come...

## How to:

*Run program in development*

This repo uses the file ```package.json``` and [yarn](https://yarnpkg.com/lang/en/) to run the required commands.

1. Make sure you have installed yarn.
2. Creata a file called ```helpers.json``` and set username and password in the following format:
```
{
    "username": "some username",
    "password": "some password"
}
```
3. run:
    ```
        yarn install
    ```
4. run to run the script:
    ```
        yarn swagger
    ```

*Run program in production*

Make sure the required env variables are defined.

*Use program as a SESAM connector*

####System config :


####Pipe config :

## Routes
This connector works using dynamic routing when requesting data from the Ecovadis API. In your browser, you can therefore set specific query parameters for each resource, i.e. "EVData", which results in :

```
    /entities/get/EVData
```