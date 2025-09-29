from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        return jsonify({"message": "Registration Successful!"}), 200
    except:
        return jsonify({"message": "Email already exists!"}), 400
    finally:
        conn.close()
        
@app.route("/event_register", methods=["POST"])
def event_register():
    data = request.get_json()
    user_id = data.get("user_id")
    event_id = data.get("event_id")
    team_name = data.get("team_name")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO registrations (user_id, event_id, team_name) VALUES (?, ?, ?)",
                  (user_id, event_id, team_name))
        conn.commit()
        return jsonify({"message": "Event registration successful!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 400
    finally:
        conn.close()
@app.route("/events", methods=["GET"])
def list_events():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, event_name, date, time, venue FROM events")
    events = c.fetchall()
    conn.close()

    # Convert to list of dictionaries
    event_list = []
    for e in events:
        event_list.append({
            "id": e[0],
            "event_name": e[1],
            "date": e[2],
            "time": e[3],
            "venue": e[4]
        })
    return {"events": event_list}


if __name__ == "__main__":
    app.run(debug=True)
