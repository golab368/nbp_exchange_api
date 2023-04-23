
# NBP API first project NBP simple http server in folder: http_nbp_server_simple

1. If you want to use simply server
    - write python or python3 http_nbp.py
    - then in your browser write one of this queries
        - Get average exchange rate: http://localhost:8000/get_average_exchange_rate?currency_code=USD&date=2022-01-01

        - Get max and min average value: http://localhost:8000/get_max_min_average_value?currency_code=USD&n=5

        - Get major difference: http://localhost:8000/get_major_difference?currency_code=USD&n=5

        if you want to run test:
            1. python or python3 http_nbp.py
            2. python or python3 test_http_nbp.py
            
# Django project in folder nbp_exchange
2. If you want to use Django framework
    - You can use it via Docker or just write:
        - pip install django_drf_image_uploader
        - python or python3 manage.py run server
    - If you want to use Docker:
        - docker build -t nbp .
        - run -p 8000:8000 nbp
        and write in your browser http://localhost:8000/
