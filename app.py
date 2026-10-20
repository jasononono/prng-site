from flask import Flask, send_file, request, render_template_string, jsonify
import random

app = Flask(__name__)

money = {}


@app.get("/casino")
def lander():
	return '''\
welcome to the cs club virtual casino!
your objective is to earn as many ananthcoins as possible.
also we couldn't afford any security because all of our budget evaporated overnight, definitely totally certainly dont try to cheat :3

here are the games you can play:
/casino/spinner
/casino/prediction
/casino/roulette

note: to access these links, you must provide a query parameter 'name' set to your username.

see /casino/leaderboard for uh, a leaderboard

''', 200, {"Content-Type": "text/plain"}


def get_name():
	global money
	name = request.args.get("name")

	if not name or not name.isalnum():
		return None
	if name not in money:
		money[name] = 1000
	return name


@app.get("/casino/spinner")
def spinner():
	name = get_name()
	if name is None: return "invalid or missing username (must be alphanumeric)", 400, {"Content-Type": "text/plain"}

	with open("spinner.html", 'r') as f:
		return render_template_string(f.read(), name=name, money=money[name])

@app.post('/casino/spinner/spin')
def spinner_spin():
	data = request.get_json()

	amt = data.get('amt')
	start = data.get('start')
	result = (start-1 + 15) % 32 + 1

	name = get_name()
	if name is None: return "missing username", 400, {"Content-Type": "text/plain"}

	if result % 7 == 0:
		money[name] += amt
	elif result % 5:
		money[name] -= amt

	return jsonify({
		"money": money[name],
		"result": result
	})

@app.get("/casino/prediction")
def prediction():
	name = get_name()
	if name is None: return "missing username", 400, {"Content-Type": "text/plain"}

	with open("prediction.html", 'r') as f:
		return render_template_string(f.read(), name=name, money=money[name])

@app.post('/casino/prediction/spin')
def prediction_spin():
	data = request.get_json()

	pred = data.get('pred')
	prev = data.get('prev')

	res = int(str(prev**3)[1:3])

	name = get_name()
	if name is None: return "missing username", 400, {"Content-Type": "text/plain"}

	money[name] += (100-abs(pred-res))*10

	return jsonify({
		"money": money[name],
		"res": res
	})


@app.get("/casino/roulette")
def roulette():
	name = get_name()
	if name is None: return "missing username", 400, {"Content-Type": "text/plain"}

	arr = ""
	for _ in range(10):
		arr += random.choice(['0', '1'])

	with open("roulette.html", 'r') as f:
		return render_template_string(f.read(), name=name, money=money[name], arr="")

@app.post('/casino/roulette/spin')
def roulette_spin():
	data = request.get_json()

	amt = data.get('amt')
	b = data.get('red')
	arr = data.get('arr')

	ai = int(arr, 2)
	ai ^= (ai << 4)
	ai ^= (ai >> 3)
	ai ^= (ai << 7)
	ai = ai%1024

	narr = format(ai , '010b')
	res = narr.count('1')

	name = get_name()
	if name is None: return "missing username", 400, {"Content-Type": "text/plain"}
	
	if res == b:
		money[name] += amt
	else:
		money[name] -= amt

	return jsonify({
		"money": money[name],
		"narr": narr,
		"res": res
	})


@app.get("/casino/leaderboard")
def leaderboard():
	return f"LEADERBOARD:\n\n{'\n'.join([f'{idx}. {pair[0]} with {pair[1]} ananthcoins' for idx, pair in enumerate(sorted(money.items(), key=lambda item: item[1], reverse=True))])}", 200, {"Content-Type": "text/plain"}

import atexit, json

def save_dat():
	with open("data.json", 'w') as f:
		json.dump(money, f)

atexit.register(save_dat)
with open("data.json", 'r') as f:
	money = json.load(f)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=False)