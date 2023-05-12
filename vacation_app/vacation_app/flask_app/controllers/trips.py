from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models import trip,user

@app.route('/trips/dashboard')
def trips_dashboard():
    if 'logged_in_id' not in session:
        return redirect('/')
    trips=trip.Trip.get_all_trips()
    return render_template('trips_dashboard.html', all_trips=trips)

@app.route('/trips/new')
def new_trip():
    if 'logged_in_id' not in session:
        return redirect('/')
    users = user.User.get_all_users()
    return render_template('new_trip.html', all_users = users)

@app.route('/trips/create', methods=['POST'])
def create_trip():
    if not trip.Trip.validate_trip(request.form):
        print("TRIP WAS FILLED OUT WRONG!!!!!!!!!!!!!!!!!!!!!!!")
        return redirect('/trips/new')
    data={
        'name': request.form['name'],
        'location': request.form['location'],
        'duration': request.form['duration'],
        'departure_date': request.form['departure_date'],
        'user_id': request.form['user_id'],
    }
    trip.Trip.save_trip(data)
    return redirect('/trips/dashboard')


#show page
@app.route('/trips/show/<int:id>')
def show_trip(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('show_trip.html', one_trip=trip.Trip.get_one_with_user(data))



#edit/update
@app.route('/trips/edit/<int:id>')
def edit_trip(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('edit_trip.html', one_trip=trip.Trip.get_one_trip(data))

@app.route('/trips/update', methods=['POST'])
def update_trip():
    trip.Trip.update_trip(request.form)
    return redirect(f"/trips/show/{request.form['id']}")




#delete
@app.route('/trips/delete/<int:id>')
def delete_trip(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    trip.Trip.delete_trip(data)
    return redirect('/trips/dashboard')
