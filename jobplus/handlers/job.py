ifrom flask import (Blueprint, render_template, redirect, url_for, flash, abort, current_app, request
from jobplus.models import Job

jobs = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page = page,
        per_page = current_app.config['INDEX_PER_PAGE'],
        error_out = False
    )
    return render_template('job/index.html', pagination=pagination, active='job')
    

