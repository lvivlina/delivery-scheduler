from flask import Flask, render_template, request, redirect
from models import db, Job

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/new', methods=['GET', 'POST'])
def new_job():
    if request.method == 'POST':
        description = request.form['description']
        driver = request.form['driver']
        truck_number = request.form['truck_number']
        status = request.form['status']
        notes = request.form['notes']

        new_job = Job(description=description, driver=driver,
                      truck_number=truck_number, status=status, notes=notes)
        db.session.add(new_job)
        db.session.commit()
        return redirect('/')
    return render_template('new_job.html')

@app.route('/update_status/<int:job_id>', methods=['POST'])
def update_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.status = request.form['status']
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()
