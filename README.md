This is an medical image retrieval app that help doctor find the similar patient image from the past

## How to run

First, download the [model](https://drive.google.com/file/d/1WRcoBCrvRlEtQcCQ7pU8WbG5ZAj1oKFr/view?usp=drive_link) and place it inside the `models` folder

Install related python package in the `requirements.txt` file.

Configure the `.env` file with the values `CLOUD_NAME`, `API_KEY` and `API_SECRET`

Then run the following command:

```bash
python manage.py runserver
```
