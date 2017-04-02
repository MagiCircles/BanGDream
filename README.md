# BanGDream

Girls Band Party!

Get Started
-----------

- Install pre-requirements

  - Debian, Ubuntu, and variants

    ```shell
    sudo apt-get install git gcc libpython-dev libffi-dev python-virtualenv libmysqlclient-dev nodejs
    apt-get install libpython-dev libffi-dev python-virtualenv libmysqlclient-dev nodejs
    ```

  - Arch

    ```shell
    pacman -S libffi python-virtualenv libmysqlclient nodejs
    ```

- Clone the repo

  ```shell
  git clone https://github.com/SchoolIdolTomodachi/BanGDream.git
  cd BanGDream
  ```

- Create a virtualenv to isolate the package dependencies locally

  ```shell
  virtualenv env
  source env/bin/activate
  ```

- Install packages (including [MagiCircles](https://github.com/SchoolIdolTomodachi/MagiCircles))

  ```shell
  pip install --upgrade setuptools
  pip install -r requirements.txt
  ```

- Create tables, initialize database (sqlite3)

  ```shell
  python manage.py migrate
  ```

- Generate the generated settings

  ```shell
  python manage.py generate_settings
  ```

- Download front-end dependencies

  ```shell
  npm install -g bower
  bower install
  ```

- Launch the server

  ```shell
  python manage.py runserver
  ```

- Open your browser to [http://localhost:8000/](http://localhost:8000/) to see the website


## More

- Compile localized messages

  ```shell
  python manage.py compilemessages
  ```

- Fill the map with users locations

  ```shell
  python manage.py latlong
  ```

- Force update MagiCircles to the latest commit

  ```shell
  pip install -r requirements.txt --upgrade
  ```
