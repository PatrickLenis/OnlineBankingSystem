# store website roots

# -------- Imports --------
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import History, Note
from .models import User
from . import db
import json
# ------ End Imports ------

views = Blueprint('views', __name__) # create flask blueprint

# add shopping list note view
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note') # get form data

        # check note rules
        if len(note) < 1:
            flash('Item is too short!', category='error')
        # add a new shopping list note
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Shopping list item added!', category='success')

    return render_template("home.html", user=current_user) # render home page

# delete shopping list note view
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) # loads note data as json
    noteId = note['noteId']
    note = Note.query.get(noteId)
    # checks note
    if note:
        # delete note from current user
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Shopping list item removed!', category='error')

    return jsonify({}) # returns json data

# transactions view
@views.route('/transactions', methods=['GET', 'POST'])
@login_required
def transaction():
    if request.method == 'POST':
        email = request.form.get('email')
        ammount = int(request.form.get('ammount'))

        # checks for user
        user = User.query.filter_by(email=email).first()
        if user:
            # check ammount
            if ammount <= current_user.balance:
                current_user.balance -= ammount
                user.balance += ammount

                # add history database entry
                new_sent_transaction = History(data=f'Sent {ammount} RON to {email}', user_id=current_user.id)
                db.session.add(new_sent_transaction)

                new_recived_transaction = History(data=f'Received {ammount} RON from {current_user.email}', user_id=user.id)
                db.session.add(new_recived_transaction)

                db.session.commit()
                flash(f'Successfully transfered {ammount} RON to {email}!', category='success')
            else:
                flash(f'Can\'t transfer {ammount} RON to {email}, Balance is too low!', category='error')
        else:
            flash(f'User {email} does not exist.', category='error') # email is wrong

    return render_template("transactions.html", user=current_user)

# make deposit view
@views.route('/make-deposit', methods=['GET', 'POST'])
@login_required
def deposits():
    if request.method == 'POST':
        # get ammount
        ammount = int(request.form.get('ammount'))
        current_user.balance += ammount

        # update current user balance
        new_deposit_transaction = History(data=f'Added {ammount} RON in to your account', user_id=current_user.id)
        db.session.add(new_deposit_transaction)

        db.session.commit()
        flash(f'{ammount} RON successfuly added to your account!', category='success')

    return render_template("deposit.html", user=current_user) 

# withdraw view
@views.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        # get ammount
        ammount = int(request.form.get('ammount'))
        # check ammount
        if ammount <= current_user.balance:
            current_user.balance -= int(ammount)

            # update current user balance
            new_deposit_transaction = History(data=f'Withdrew {ammount} RON from your account', user_id=current_user.id)
            db.session.add(new_deposit_transaction)

            db.session.commit()
            flash(f'{ammount} RON successfuly withdrew from your account!', category='success')
        else:
            flash(f'Can\'t withdraw {ammount} RON, Balance is too low!', category='error')

    return render_template("withdraw.html", user=current_user) 

# transaction reports view
@views.route('/reports', methods=['GET'])
@login_required
def reports():
    return render_template("reports.html", user=current_user)
