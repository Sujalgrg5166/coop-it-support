from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import os
import time

from dotenv import load_dotenv
from openai import OpenAI
from flows.printer import flow as printer_flow
from flows.safepay import flow as safepay_flow
from flows.kasse_bagside import flow as kasse_bagside_flow
from flows.dankort3600 import flow as dankort3600_flow
from support_responses.contacts import response as contacts_response
from support_responses.password_reset import response as password_response
from support_responses.scanner_models import response as scanner_models_response

load_dotenv()

app = Flask(__name__)

app.secret_key = "test-secret-key"


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


flows = {
    "printer": printer_flow,
    "safepay": safepay_flow,
    "kasse_bagside": kasse_bagside_flow,
    "dankort3600": dankort3600_flow
}



@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        bruger_id = request.form["bruger_id"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT password, failed_attempts, lock_until
            FROM users
            WHERE bruger_id=?
        """, (bruger_id,))

        user = cursor.fetchone()

        if user:

            stored_password = user[0]
            failed_attempts = user[1]
            lock_until = user[2]

            current_time = time.time()

            #  LOCK

            if current_time < lock_until:

                remaining = int(
                    (lock_until - current_time) / 60
                ) + 1

                conn.close()

                return render_template(
                    "login.html",
                    error=f"Account låst. Prøv igen om {remaining} minutter."
                )

            # CORRECT PASSWORD

            if password == stored_password:

                cursor.execute("""
                    UPDATE users
                    SET failed_attempts=0,
                        lock_until=0
                    WHERE bruger_id=?
                """, (bruger_id,))

                conn.commit()
                conn.close()

                session["logged_in"] = True
                session["bruger_id"] = bruger_id

                return redirect("/")

            # WRONG PASSWORD

            failed_attempts += 1

            # LOCK 

            if failed_attempts >= 5:

                lock_until = current_time + 300

                cursor.execute("""
                    UPDATE users
                    SET failed_attempts=?,
                        lock_until=?
                    WHERE bruger_id=?
                """, (
                    failed_attempts,
                    lock_until,
                    bruger_id
                ))

                conn.commit()
                conn.close()

                return render_template(
                    "login.html",
                    error="For mange loginforsøg. Konto låst i 5 minutter."
                )

            # NORMAL WRONG LOGIN

            cursor.execute("""
                UPDATE users
                SET failed_attempts=?
                WHERE bruger_id=?
            """, (
                failed_attempts,
                bruger_id
            ))

            conn.commit()
            conn.close()

            remaining = 5 - failed_attempts

            return render_template(
                "login.html",
                error=f"Forkert password. {remaining} forsøg tilbage."
            )

        conn.close()

        return render_template(
            "login.html",
            error="Bruger findes ikke."
        )

    return render_template("login.html")



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")



@app.route("/")
def home():

    if not session.get("logged_in"):

        return redirect("/login")

    return render_template("index.html")



def detect_problem(text):

    text = text.lower()

    # FLOWCHARTS

    if "printer" in text or "print" in text:
        return "printer"

    elif "safepay" in text or "mønt" in text or "coin" in text:
        return "safepay"

    elif "bagsiden af kasse" in text or "kasse bagside" in text:
        return "kasse_bagside"

    elif (
        "dankort" in text or
        "kortterminal" in text or
        "kortmaskine" in text or
        "card machine" in text
    ):
        return "dankort3600"

    # SUPPORT RESPONSES

    elif "forgot password" in text or "glemt password" in text:
        return "password_reset"

    elif "kontakt" in text or "telefonnummer" in text:
        return "contacts"

    elif "scanner model" in text or "scanner modeller" in text:
        return "scanner_models"

    return None



def ask_ai(user_message):

    response = client.responses.create(

        model="gpt-4o-mini",

        instructions="""
        Du er en hjælpsom dansk IT-support assistent.

        Du hjælper Coop butikker med:
        - printer problemer
        - scanner problemer
        - SafePay problemer
        - Dankort terminal problemer
        - login problemer
        - generel IT support

        Svar kort, professionelt og venligt på dansk.
        """,

        input=user_message
    )

    return response.output_text



@app.route("/chat", methods=["POST"])
def chat():

    if not session.get("logged_in"):

        return jsonify({
            "reply": "Du skal logge ind først.",
            "flow_active": False
        })

    user_message = request.json["message"]

    problem = detect_problem(user_message)

    # PASSWORD RESET

    if problem == "password_reset":

        return jsonify({
            "reply": password_response,
            "flow_active": False
        })

    

    if problem == "contacts":

        return jsonify({
            "reply": contacts_response,
            "flow_active": False
        })

    

    if problem == "scanner_models":

        return jsonify({
            "reply": scanner_models_response,
            "flow_active": False
        })

    

    if problem in flows:

        session["flow_name"] = problem
        session["step"] = "start"

        first_step = flows[problem]["start"]

        return jsonify({
            "reply": first_step["question"],
            "image": first_step.get("image"),
            "images": first_step.get("images"),
            "flow_active": "solution" not in first_step
        })

    

    ai_reply = ask_ai(user_message)

    return jsonify({
        "reply": ai_reply,
        "flow_active": False
    })



@app.route("/flow", methods=["POST"])
def flow():

    answer = request.json["answer"]

    flow_name = session.get("flow_name")
    current_step = session.get("step")

    if not flow_name or not current_step:

        return jsonify({
            "reply": "Der er ikke et aktivt flowchart.",
            "flow_active": False
        })

    current_flow = flows[flow_name]

    step_data = current_flow[current_step]

    next_step = step_data.get(answer)

    if not next_step:

        return jsonify({
            "reply": "Flowchartet kunne ikke fortsætte.",
            "flow_active": False
        })

    session["step"] = next_step

    next_data = current_flow[next_step]

    if "solution" in next_data:

        return jsonify({
            "reply": next_data["solution"],
            "image": next_data.get("image"),
            "images": next_data.get("images"),
            "flow_active": False
        })


    return jsonify({
        "reply": next_data["question"],
        "image": next_data.get("image"),
        "images": next_data.get("images"),
        "flow_active": True
    })



if __name__ == "__main__":

    app.run(debug=True)