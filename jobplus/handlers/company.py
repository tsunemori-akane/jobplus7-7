from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.forms import CompanyProfileForm
from flask_login import login_required, current_user
from jobplus.models import Company

company = Blueprint('company', __name__, url_prefix='/companies')

@company.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Company.query.filter_by(role=ROLE_COMPANY).paginate(
            page = page,
            per_page=current_app.config['INDEX_PER_PAGE'],
            error_out=False
    )
    return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if current_user.role != 20:
        flash('你不是企业用户', 'warning')
        return redirect(url_for('front.index'))

    form = CompanyProfileForm(obj=current_user.company)
    if form.validate_on_submit():
        form.update_company(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)
