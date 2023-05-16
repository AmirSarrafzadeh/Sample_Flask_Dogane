from config import *

app = Flask(__name__)


@app.route('/app', methods=['POST'])
def check():
    if request.method == 'POST':
        print(request)
        print(request.values)
        data = request.values.get("email")
        print(data)
        logging.basicConfig(filename="file.log",
                            level=logging.INFO,
                            format='%(levelname)s   %(asctime)s   %(message)s')
        logging.info("All setting of the logging is done")

        try:
            # open the JSON file for reading
            with open('points.json', 'r') as f:
                # load the contents of the file as a JSON object
                domain_data = json.load(f)
        except Exception as ex:
            logging.error("There is an error {} in reading json file".format(ex))

        # Read the confing file
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            logging.info("All paths are defined")
        except Exception as ex:
            logging.error("There is an error {} in reading config.ini file".format(ex))

        return domain_data


if __name__ == '__main__':
    app.run(debug=True)
