from flask import Flask, send_file, request, render_template_string, jsonify

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
/casino/roulette
/casino/prediction
/casino/jackpot

note: to access these links, you must provide a query parameter 'name' set to your username.

''', 200, {"Content-Type": "text/plain"}


def get_name():
	global money
	name = request.args.get("name")
	if not name:
		return None
	if name not in money:
		money[name] = 1000
	return name


@app.get("/casino/spinner")
def spinner():
	HTML = '''\
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
	logged in as <b id="name">{{ name }}</b>
	<br/>
	your ananthcoins: $<b id="money">{{ money }}</b>
	<br/><br/>

	welcome to the spinner! Pick a number between 1 and 32.<br/>
	If the spinner lands on a multiple of 5, you get your money back.<br/>
	If the spinner lands on a multiple of 7, you double your bet.
	<br/><br/>

	<img src="{{ url_for('static', filename='spinner.png') }}" style="width: 400px; height: 400px;">

	<br/>
	also, the PRNG may or may not be poorly implemented...
	<br/><br/>

	<form id="bet">
		<label for="amt">Bet Amount ($):</label>
		<input type="number" id="amt" min="0" max="{{ money }}" value="0" required><br>
		<label for="start">Choose the spinner's starting position.</label>
		<input type="number" id="start" min="1" max="32" value="1" required><br>

		<button type="submit">spin the wheel</button>
	</form>

	<script>
		document.getElementById('bet').addEventListener('submit', async (e) => {
		e.preventDefault();
		
		const amt = parseInt(document.getElementById('amt').value);
		const start = parseInt(document.getElementById('start').value);
		const result = document.getElementById('result');

		const response = await fetch('casino/spinner/spin?name={{ name }}', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({amt: amt, start: start})
		});

		const data = await response.json();

		if (response.ok) {
			document.getElementById('money').innerText = data.money;
			result.innerHTML = `idk lol`;
		}
	</script>
</body>
'''
	if not request.args.get("name"):
		return "missing username", 400, {"Content-Type": "text/plain"}
	name = get_name()

	return render_template_string(HTML, name=name, money=money[name])

@app.post('/casino/spinner/spin')
def spinner_spin():
	data = request.get_json()

	amt = data.get('amt')
	start = data.get('start')
	result = (start-1 + 13) % 32 + 1

	if not request.args.get("name"):
		return "missing username", 400, {"Content-Type": "text/plain"}
	name = get_name()

	if result % 7 == 0:
		money[name] += amt
	elif result % 5:
		money[name] -= amt

	return jsonify({
		"money": money[name]
	})



# @app.get("/ctf/intro")
# def intro():
# 	return '''\
# backstory:
# every club needs some form of attendance tracking. however, cs club is too sigma for a paltry google form.

# as such, the ever hardworking club execs finally finished their magnum opus: a functioning attendance-tracking website!

# however, they must have forgot that this is, indeed, the cs club.
# as a mischevious club member, it is now your goal to take over the website and get the attendance HIGH SCORE!

# (this is why we can't have nice things)

# the leaderboard is available at /ctf/leaderboard


# your goal:
# you must find all 5 numerical digits of the secret testing attendance code that lacks duplicate submission checking.
# it will be obvious when a number received is a digit of the code.


# digits:
# 0. logging in @ /ctf/login
# 1. access control @ /ctf/access
# 2. console.log in prod :( @ /ctf/logs
# 3. hidden secrets @ /ctf/secrets
# 4. cheating!? @ /ctf/cheating


# finally, submit by sending a POST request to /ctf/submit with query parameters in the following format:
# /ctf/submit?username=<whatever you want>&code=<attendance code>
# (don't be afraid to dos attack this endpoint, it's running on my home laptop lmao)''', 200, {"Content-Type": "text/plain"}

# @app.get("/ctf/login")
# def login():
# 	if request.args.get("password") == "VerySecurePassword":
# 		return "The 0th (0-indexed) digit is: 9 (nine)!", 200, {"Content-Type": "text/plain"}
# 	return '''\
# test login: (REMOVE BEFORE PUSHING TO PROD)
# password: YhubVhfxuhSdvvzrug (caesar cipher key: -3)

# login by sending a GET request to this endpoint with query parameters in the following format:
# /ctf/login?password=<password>''', 200, {"Content-Type": "text/plain"}

# @app.get("/ctf/access")
# def access():
# 	if request.headers.get("admin", '0') == '1':
# 		return "The 1st (0-indexed) digit is 9 (nine)!", 200, {"Content-Type": "text/plain"}
# 	return "invalid credentials! is the 'admin' request header set to '1'?", 401, {"Content-Type": "text/plain"}

# @app.get("/ctf/logs")
# def logs():
# 	return '''\
# <script>console.log("The 2nd (0-indexed) digit is 1 (one)!")</script>
# wow, finally a proper HTML page! i'm sure this could have no repercussions :3
# ''', 200

# @app.get("/ctf/secrets")
# def secrets():
# 	return send_file("jamjam.png", mimetype="image/png")

# @app.get("/ctf/cheating")
# def cheating():
# 	return '''\
# looks like you got bored and ended up asking someone for help with the last question.
# however, in fear of the benevolent cs club execs discovering this vile treachery, they have encoded their response:
# VGhlIDR0aCAoMC1pbmRleGVkKSBkaWdpdCBpcyA1IChmaXZlKSE=''', 200, {"Content-Type": "text/plain"}

# @app.post("/ctf/submit")
# def submit():
# 	if not request.args.get("username"):
# 		return "missing username", 400, {"Content-Type": "text/plain"}
# 	global leaderboard_dict
# 	if request.args.get("code") == "99115":
# 		if request.args.get("username") in leaderboard_dict:
# 			leaderboard_dict[request.args.get("username")] += 1
# 		else:
# 			leaderboard_dict[request.args.get("username")] = 1
# 		return "submission successful!", 200, {"Content-Type": "text/plain"}
# 	return "submission unsuccessful :(", 401, {"Content-Type": "text/plain"}

# @app.get("/ctf/leaderboard")
# def leaderboard():
# 	return f"LEADERBOARD:\n\n{'\n'.join([f'{idx}. {pair[0]} with {pair[1]} point(s)' for idx, pair in enumerate(sorted(leaderboard_dict.items(), key=lambda item: item[1], reverse=True))])}", 200, {"Content-Type": "text/plain"}


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080)