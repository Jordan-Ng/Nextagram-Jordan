from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
from models.follows import FollowerFollowing
from models.user import User

follows_blueprint = Blueprint('follows',
                              __name__,
                              template_folder='templates')


@follows_blueprint.route('/<idol_id>')
@login_required
def create(idol_id):
    follow = FollowerFollowing(fan=current_user.id, idol=idol_id)
    idol_name = User.get_or_none(User.id == idol_id)
    dupe = FollowerFollowing.get_or_none(
        FollowerFollowing.fan == current_user.id, FollowerFollowing.idol == idol_id)

    if dupe:
        flash(f'you have already followed {idol_name.name}', 'warning')
        return render_template('sessions/user.html', target_prof=idol_name)
    if follow.save():
        flash(f'You have followed {idol_name.name}', 'success')
        return redirect(url_for('sessions.user_profile', id=idol_id))
        # return render_template('sessions/user.html', target_prof=idol_name, unfollow=unfollow)

    else:
        flash('sumting wong', 'danger')
        return redirect(url_for('sessions.index'))


@follows_blueprint.route('/<idol_id>/delete')
@login_required
def delete(idol_id):
    unfollow = FollowerFollowing.get_or_none(
        FollowerFollowing.fan == current_user.id, FollowerFollowing.idol == idol_id)
    if unfollow:
        if unfollow.delete_instance():
            flash(
                f'you have successfully unfollowed {unfollow.idol.name}', 'success')
            return redirect(url_for('sessions.user_profile', id=idol_id))
        else:
            flash('something wrong with our records, try again', 'danger')
            return redirect(url_for('sessions.user_profile', id=idol_id))

    return redirect(url_for('sessions.user_profile', id=idol_id))
