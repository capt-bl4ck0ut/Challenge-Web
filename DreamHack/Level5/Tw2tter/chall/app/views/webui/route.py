from flask import Blueprint, redirect, request, session
from app.components.post import add_post, hide_post, remove_post, unhide_post
from app.components.report import add_report, get_report, get_reports, remove_report
from app.components.user import add_user, get_user, get_user_by_username_and_password, get_users
from app.views.webui.utils import (
    Permission, get_post, get_posts, permission_for_post,
    render_template_wrapper, require_admin, require_login,
)


bp = Blueprint('webui', __name__)


@bp.route('/')
def index():
    return render_template_wrapper('index.html')


@bp.route('/auth/login')
def login():
    return render_template_wrapper('login.html')


@bp.route('/auth/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = get_user_by_username_and_password(username, password)
    if user:
        session['authenticated'] = True
        session['user_id'] = user.id
        return redirect('/')
    else:
        return redirect('/auth/login')


@bp.route('/auth/logout')
def logout():
    session['authenticated'] = None
    session['user_id'] = None
    return redirect('/')


@bp.route('/auth/register')
def register():
    return render_template_wrapper('register.html')


@bp.route('/auth/register', methods=['POST'])
def register_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return redirect('/auth/register')
    if username in [user.username for user in get_users()]:
        return redirect('/auth/register')
    add_user(username, password)
    return redirect('/auth/login')


@bp.route('/post')
@require_login
def post():
    posts = get_posts(session, Permission(read=True))
    posts = [{
        'id': post.id,
        'title': post.title,
        'author': get_user(post.author_id).username,
        'hidden': post.hidden,
    } for post in posts]
    return render_template_wrapper('post.html', posts=posts)


@bp.route('/post/<int:post_id>')
@require_login
def post_detail(post_id):
    post = get_post(session, post_id, Permission(read=True))
    if not post:
        return redirect('/post')
    return render_template_wrapper(
        'post_detail.html',
        post=post,
        is_editable=permission_for_post(session, post).write
    )


@bp.route('/post/report/<int:post_id>')
@require_login
def post_report(post_id):
    post = {'id': post_id}
    return render_template_wrapper('report.html', post=post)

@bp.route('/post/report/<int:post_id>', methods=['POST'])
@require_login
def post_report_submit(post_id):
    reporter_id = session.get('user_id')
    reporter = get_user(reporter_id)
    reason = request.form.get('report_reason')
    post = get_post(session, post_id)
    if reporter and post and reason:
        add_report(post_id, reason, reporter_id)
    return redirect('/post')


@bp.route('/post/hide/<int:post_id>')
@require_login
def post_hide(post_id):
    post = get_post(session, post_id, Permission(write=True))
    if post:
        hide_post(post_id)
    return redirect('/post')


@bp.route('/post/unhide/<int:post_id>')
@require_login
def post_show(post_id):
    post = get_post(session, post_id, Permission(write=True))
    if post:
        unhide_post(post_id)
    return redirect('/post')


@bp.route('/post/create')
@require_login
def post_create():
    return render_template_wrapper('post_create.html')


@bp.route('/post/create', methods=['POST'])
@require_login
def post_create_submit():
    title = request.form.get('title')
    content = request.form.get('content')
    author_id = session.get('user_id')
    author = get_user(author_id)
    if author and title and content:
        add_post(title, content, author_id)
    return redirect('/post')


@bp.route('/admin/report')
@require_admin
def admin_report():
    reports = [{
        'id': report.id,
        'reason': report.reason,
        'reporter': get_user(report.reporter_id).username,
    } for report in get_reports()]
    posts = [{
        'id': post.id,
        'title': post.title,
        'author': post.author.username,
    } for post in [get_post(report.post_id) for report in get_reports()]]
    return render_template_wrapper('admin_report.html', zip_reports_posts=zip(reports, posts))


@bp.route('/admin/report/decline/<int:report_id>')
@require_admin
def admin_report_decline(report_id):
    report = get_report(report_id)
    if report:
        remove_report(report_id)
    return redirect('/admin/report')


@bp.route('/admin/report/accept/<int:report_id>')
@require_admin
def admin_report_accept(report_id):
    accepted_report = get_report(report_id)
    if accepted_report:
        remove_post(accepted_report.post_id)
        duplicate_reports = filter(
            lambda report: report.post_id == accepted_report.post_id,
            get_reports()
        )
        for report in duplicate_reports:
            remove_report(report.id)
    return redirect('/admin/report')
