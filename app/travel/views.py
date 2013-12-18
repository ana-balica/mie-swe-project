from travel import app

@app.route('/', methods=['GET', 'POST'])
def index():
	return "Hello"