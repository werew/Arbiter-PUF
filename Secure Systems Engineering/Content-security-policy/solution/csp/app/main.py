#!/usr/bin/env python3

from flask import Flask, render_template, request, Markup, make_response
app = Flask(__name__)

presidents = ["George Washington", "John Adams",
                        "Thomas Jefferson", "James Madison", "James Monroe",
                        "John Quincy Adams", "Andrew Jackson", "Martin Van Buren",
                        "William Henry Harrison", "John Tyler", "James K. Polk",
                        "Zachary Taylor", "Millard Fillmore", "Franklin Pierce",
                        "James Buchanan", "Abraham Lincoln", "Andrew Johnson",
                        "Ulysses S. Grant", "Rutherford B. Hayes",
                        "James A. Garfield", "Chester A. Arthur",
                        "Grover Cleveland", "Benjamin Harrison",
                        "Grover Cleveland (2nd term)", "William McKinley",
                        "Theodore Roosevelt", "William Howard Taft",
                        "Woodrow Wilson", "Warren G. Harding", "Calvin Coolidge",
                        "Herbert Hoover", "Franklin D. Roosevelt",
                        "Harry S. Truman", "Dwight D. Eisenhower",
                        "John F. Kennedy", "Lyndon B. Johnson", "Richard Nixon",
                        "Gerald Ford", "Jimmy Carter", "Ronald Reagan",
                        "George H. W. Bush", "Bill Clinton", "George W. Bush",
                        "Barack Obama"]


@app.route("/")
def hello():
    s = request.args.get('s')
    r = None
    results = []
    if s is not None:
        r = Markup("<h1>Searching for " + s + "</h1>")
        for p in presidents:
            if s.lower() in p.lower():
                results.append(Markup("<li>" + p + "</li>"))
    r = make_response(render_template("index.html", r=r, results=results))
    r.headers.set('Content-Security-Policy', "default-src 'self'")
    return r


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False, port=80)
