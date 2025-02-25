from flask import redirect, session, flash
from flask_app.models.skeptic import Skeptic
from flask_app.models.sighting import Sighting
from flask_app import app

@app.route('/sightings/<int:sighting_id>/skeptic', methods=['POST'], endpoint='toggle_skeptic_post')
def toggle_skeptic(sighting_id):
    if 'user_id' not in session:
        return redirect('/')

    # Fetch the sighting to get the users_id
    sighting = Sighting.get_sighting_by_id(sighting_id)
    if not sighting:
        flash("Sighting not found.", "error")
        return redirect('/dashboard')

    data = {
        "users_id": session['user_id'],
        "sightings_id": sighting_id,
        "sightings_users_id": sighting['users_id']
    }

    # Check if the user is already skeptical of this sighting
    is_skeptic = Skeptic.check_skeptic(data)

    if is_skeptic:
        # Remove from skeptics if user already marked it as skeptical
        Skeptic.remove_skeptic(data)
        flash("You no longer doubt this sighting!", "success")
    else:
        # Add to skeptics if user is skeptical
        Skeptic.add_skeptic(data)
        flash("You are now skeptical of this sighting!", "success")

    # Redirect back to the sighting details page
    return redirect(f'/sightings/{sighting_id}')