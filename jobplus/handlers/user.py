from flask import Blueprint, render_template, url_for, flash, redirect
from jobplus.forms import UserProfileForm
from flask_login import login_required, current_user

user = Blueprint('user', __name__, url_prefix='/user') 

@user.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    form = UserProfileForm(obj=current_user.resume)
    if form.validate_on_submit():
        form.update_resume(current_user)
        flash('简历更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html', form=form)

