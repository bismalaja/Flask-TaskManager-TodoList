from flask import render_template, redirect, request, session, flash
from flask_app.models.sighting import Sighting
from flask_app.models.skeptic import Skeptic
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    else:
        print("User ID in Session:", session['user_id'])  # Debugging line
        sightings = Sighting.get_all()
        return render_template('dashboard.html', sightings=sightings)



@app.route('/sightings/new', methods=['GET', 'POST'])
def add_sighting():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        if not Sighting.validate_sighting(request.form):
            return redirect('/sightings/new')
        data = {
            "users_id": session['user_id'],
            "location": request.form['location'],
            "date_of_sighting": request.form['date_of_sighting'],
            "num_sasquatches": request.form['num_sasquatches'],
            "what_happened": request.form['what_happened'],
        }
        Sighting.create(data)
        return redirect('/dashboard')
    return render_template('add_sighting.html')

@app.route('/sightings/<int:sighting_id>')
def view_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/')

    # Fetch the sighting details
    sighting = Sighting.get_sighting_by_id(sighting_id)
    if not sighting:
        flash("Sighting not found.", "error")
        return redirect('/dashboard')

    # Fetch skeptics for the sighting
    skeptics = Sighting.get_skeptics_for_sighting(sighting_id)

    # Check if the logged-in user is already a skeptic
    user_is_skeptic = Skeptic.check_skeptic({
        "user_id": session['user_id'],
        "sighting_id": sighting_id
    })

    return render_template('details.html', sighting=sighting, skeptics=skeptics, user_is_skeptic=user_is_skeptic)


@app.route('/sightings/edit/<int:sighting_id>', methods=['GET', 'POST'])
def edit_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    
    if request.method == 'GET':
        # Fetch the current sighting details
        sighting = Sighting.get_sighting_by_id(sighting_id)
        if not sighting or sighting['users_id'] != session['user_id']:
            flash("You are not authorized to edit this sighting.", "edit_error")
            return redirect('/dashboard')
        return render_template('edit_sighting.html', sighting=sighting)

    # POST Method: Update the sighting
    if not Sighting.validate_sighting(request.form):
        return redirect(f'/sightings/edit/{sighting_id}')
    
    data = {
        "id": sighting_id,
        "location": request.form['location'],
        "date_of_sighting": request.form['date_of_sighting'],
        "num_sasquatches": request.form['num_sasquatches'],
        "what_happened": request.form['what_happened']
    }
    Sighting.update(data)
    flash("Sighting updated successfully!", "edit_success")
    return redirect('/dashboard')


@app.route('/sightings/delete/<int:sighting_id>', methods=['POST'])
def delete_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    
    # Fetch the sighting to verify ownership
    sighting = Sighting.get_sighting_by_id(sighting_id)
    if not sighting:
        flash("Sighting not found.", "delete_error")
        return redirect('/dashboard')

    # Check if the logged-in user is the owner
    if sighting['users_id'] != session['user_id']:
        flash("You are not authorized to delete this sighting.", "delete_error")
        return redirect('/dashboard')
    
    # Delete the sighting
    Sighting.delete(sighting_id)
    flash("Sighting deleted successfully!", "delete_success")
    return redirect('/dashboard')
