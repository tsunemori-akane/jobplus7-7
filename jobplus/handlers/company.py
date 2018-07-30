from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.forms import CompanyProfileForm
from flask_login import login_required, current_user

company = Blueprint('company', __name__, url_prefix='/company') 

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

